from PyQt5.QtWidgets import QMessageBox
import pyodbc

# Nombre del servidor conectado (o None)
servidor_conectado = None

# Instancia global singleton de conexión
_conexion_instance = None

class Conexion():
    _instance = None
    
    def __new__(cls):
        # Singleton: siempre devolver la misma instancia
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializar la conexión una sola vez"""
        if hasattr(self, '_initialized'):
            return  # Ya inicializado
        self._initialized = True
        
        # Cambiar orden de servidores: intentar primero TITULAR (remoto), luego QUITO (local)
        servers_to_try = [
            {'name': 'titular', 'trusted': False, 'uid': 'sa', 'pwd': '123'},
            {'name': 'QUITO\\SQLEXPRESS', 'trusted': True, 'uid': 'sa', 'pwd': '123'},
            {'name': 'QUITO\\SQLEXPRESS', 'trusted': False, 'uid': 'sa', 'pwd': '123'},
        ]
        
        last_error = None
        for srv_config in servers_to_try:
            server = srv_config['name']
            database = 'Cine'
            username = srv_config['uid']
            password = srv_config['pwd']
            try:
                if srv_config['trusted']:
                    print(f"[Conexion] Intentando {server} (Trusted)")
                    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;Connection Timeout=10;'
                    self.con = pyodbc.connect(conn_str)
                else:
                    print(f"[Conexion] Intentando {server} (UID/PWD)")
                    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no;Trusted_Connection=no;Connection Timeout=10;'
                    self.con = pyodbc.connect(conn_str)
                print(f"[Conexion] ✓ Conectado a {server}")
                globals()['servidor_conectado'] = server
                self.server_used = server
                return
            except Exception as e:
                print(f"[Conexion] ✗ Falló {server}: {e}")
                last_error = e
                continue
        
        # Si llegamos aquí, ningún servidor funcionó
        print("[Conexion] ✗ No se conectó a ningún servidor")
        QMessageBox.information(None, "Error", f"Falló la conexión con todos los servidores.\nÚltimo error: {last_error}")
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
            
