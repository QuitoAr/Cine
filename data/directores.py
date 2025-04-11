import conexion as con

class BaseDirectoresDB:
    def __init__(self):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()

    def cerrar(self):
        self.cursor.close()
        self.db.close()


class Directores(BaseDirectoresDB):
    def __init__(self):
        super().__init__()

    def getFilas(self):
        try:
            self.cursor.execute("SELECT id_director, nombre_director FROM directores ORDER BY nombre_director")
            filas = self.cursor.fetchall()
            return filas
        finally:
            self.cerrar()


class Director(BaseDirectoresDB):
    def __init__(self, id_director=0):
        super().__init__()
        self.id_director = id_director

    def getDirector(self):
        try:
            self.cursor.execute(
                "SELECT * FROM directores WHERE id_director = ?",
                (self.id_director,)
            )
            fila = self.cursor.fetchone()
            if fila:
                return {
                    "id_director": fila[0],
                    "nombre_director": fila[1],
                    "wikipedia_director": fila[2]
                }
            else:
                return None
        finally:
            self.cerrar()
            
    def actualizar_director(self, nuevo_nombre, nueva_wiki):
        try:
            self.cursor.execute(
                "UPDATE directores SET nombre_director = ?, wikipedia_director = ? WHERE id_director = ?",
                (nuevo_nombre, nueva_wiki, self.id_director)
            )
            self.db.commit()
            return True
        except Exception as e:
            print("❌ Error al actualizar:", e)
            return False
        finally:
            self.cerrar()
            
    def crear_director(self, nombre, wiki):
        try:
            self.cursor.execute(
                "INSERT INTO directores (nombre_director, wikipedia_director) VALUES (?, ?)",
                (nombre, wiki)
            )
            self.db.commit()
            nuevo_id = self.cursor.lastrowid
            return nuevo_id
        except Exception as e:
            print("❌ Error al crear:", e)
            return None
        finally:
            self.cerrar()

    def eliminar_director(self):
        try:
            self.cursor.execute(
                "DELETE FROM directores WHERE id_director = ?",
                (self.id_director,)
            )
            self.db.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("❌ Error al eliminar:", e)
            return False
        finally:
            self.cerrar()
