import conexion as con
from model.usuario import Usuario

class UsuarioData():
    
    def login(self, usuario:Usuario):
       self.db = con.Conexion().conectar()
       self.cursor = self.db.cursor()
       res = self.cursor.execute("SELECT * FROM usuarios WHERE usuario='{}' AND clave='{}'".format(usuario._usuario, usuario._clave))
       fila = res.fetchone()
       if fila:
           usuario = Usuario(usuario=fila[2], clave=fila[3])
           self.cursor.close()
           # NO cerrar la conexión singleton - se usa en toda la aplicación
           return usuario
       else:
           self.cursor.close()
           # NO cerrar la conexión singleton - se usa en toda la aplicación
           return None