from PyQt5.QtWidgets import QMessageBox
import pyodbc

class Conexion():
    def __init__(self):
        try:
            server = 'QUITO\\SQLEXPRESS'  # Nombre del servidor
            database = 'Cine'  # Nombre de la base de datos
            
            # Conexión con autenticación de Windows
            self.con = pyodbc.connect(
                f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'Trusted_Connection=yes;'
            )
            
            # self.crearTablas()  # Si necesitas crear tablas, descomenta esta línea
            
        except Exception as ex:
            QMessageBox.information(None, "Error", f"Falló la conexión con el Servidor: {ex}")
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
            
