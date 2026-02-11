from PyQt5.QtWidgets import QMessageBox
import pyodbc

# Nombre del servidor conectado (o None)
servidor_conectado = None

# Caché global para reutilizar la conexión
_conexion_cache = None
_servidor_cache = None

class Conexion():
    def __init__(self):
        # Si ya tenemos una conexión en caché, usarla directamente
        global _conexion_cache, _servidor_cache
        if _conexion_cache is not None and _servidor_cache is not None:
            self.con = _conexion_cache
            self.server_used = _servidor_cache
            globals()['servidor_conectado'] = _servidor_cache
            return
        try:
            server = 'titular'
            database = 'Cine'
            username = 'sa'
            password = '123'
            # Añadir Connection Timeout para evitar bloqueos largos
            self.con = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+';Encrypt=no;Trusted_Connection=no;Connection Timeout=5;')
            # Registrar servidor usado y guardarlo en caché
            try:
                globals()['servidor_conectado'] = server
                self.server_used = server
                # Guardar en caché global
                _conexion_cache = self.con
                _servidor_cache = server
            except Exception:
                self.server_used = server
            # self.crearTablas()
        except Exception as ex:
            # Intentar servidor alternativo con varios modos
            server2 = 'QUITO\\SQLEXPRESS'
            database2 = 'Cine'
            username = 'sa'
            password = '123'
            ex2 = None
            ex3 = None
            # 1) Intento con Trusted_Connection (autenticación Windows)
            try:
                # Trusted with trust server certificate and short timeout
                self.con = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                    f'SERVER={server2};'
                    f'DATABASE={database2};'
                    f'Trusted_Connection=yes;'
                    f'UID={username};'
                    f'PWD={password};'
                )
                globals()['servidor_conectado'] = server2
                self.server_used = server2
                # Guardar en caché global
                _conexion_cache = self.con
                _servidor_cache = server2
            except Exception as e2:
                ex2 = e2
                # 2) Intento con UID/PWD (mismos credenciales que titular)
                try:
                    # Intento con UID/PWD y timeout corto
                    self.con = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server2+';DATABASE='+database2+';UID='+username+';PWD='+password+';Encrypt=no;Trusted_Connection=no;Connection Timeout=5;')
                    globals()['servidor_conectado'] = server2
                    self.server_used = server2
                    # Guardar en caché global
                    _conexion_cache = self.con
                    _servidor_cache = server2
                except Exception as e3:
                    ex3 = e3
                    # Ninguno funcionó: informar con los errores recogidos
                    msg = f"Falló la conexión con los servidores:\n1) titular: {ex}\n2) Quito (Trusted): {ex2}\n3) Quito (UID/PWD): {ex3}"
                    QMessageBox.information(None, "Error", msg)
                    self.con = None
    
    def conectar(self):
        return self.con

            
    def crearTablas(self):
        sql_create_table1 = "CREATE TABLE usuarios (id INT IDENTITY(1,1) PRIMARY KEY, nombre VARCHAR(50), usuario VARCHAR(50) UNIQUE,clave VARCHAR(50))"
        cur = self.con.cursor()
        try:
            cur.execute(sql_create_table1)
        except Exception as e:
            print(f"Error creating table: {e}")    
        self.con.commit()
        cur.close()
        print("Tablas creadas")
        self.crearAdmin()
        

    def crearAdmin(self):
        try:
            sql_insert = """INSERT INTO usuarios (nombre, usuario, Clave) VALUES ('{}','{}','{}')""".format('Administrador', 'admin', 'citizen')
            cur = self.con.cursor()
            cur.execute(sql_insert)
            self.con.commit()
        except Exception as ex:
            print("Admin:",ex)
            
