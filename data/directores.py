import conexion as con

class Directores:
    def __init__(self):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT * FROM directores")
        
    def getFilas(self):
        try:
            filas = self.cursor.fetchall()
        finally:
            self.cursor.close()
            self.db.close()
        return filas