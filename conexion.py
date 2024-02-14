import pyodbc
from PyQt5.QtWidgets import QMessageBox

class Conexion():
    def __init__(self):
        try:
            # msgBox = QMessageBox()
            # msgBox.setText("Conectando con el servidor...")
            # msgBox.setStandardButtons(QMessageBox.NoButton)
            # msgBox.exec_()            
            server = 'titular' 
            database = 'Cine' 
            username = 'python' 
            password = 'cala9405' 
            self.con = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+';Encrypt=no;Trusted_Connection=no;')
            # self.crearTablas()
            # msgBox.close()
        except Exception as ex:
            QMessageBox.critical(None, "Falló la conexión con el Servidor")
            self.quit()
    
    def conectar(self):
        return self.con

            
    def crearTablas(self):
        sql_create_table1 = "CREATE TABLE usuarios (id INT IDENTITY(1,1) PRIMARY KEY, nombre VARCHAR(50), usuario VARCHAR(50) UNIQUE,clave VARCHAR(50))"
        cur = self.con.cursor()
        try:
            cur.execute(sql_create_table1)
        except:
            pass    
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
            
       