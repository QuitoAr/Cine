# conexion_base.py
import conexion as con

class ConexionBase:
    def __init__(self):
        self.db = con.Conexion().conectar()
        if self.db:
            self.cursor = self.db.cursor()
        else:
            self.cursor = None

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
