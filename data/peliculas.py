from PyQt5.QtWidgets import QMessageBox
from conexion_base import ConexionBase

class Peliculas(ConexionBase):
    def __init__(self, id_director_seleccionado):
        super().__init__()
        if not self.cursor:
            return
        try:
            self.cursor.execute(
                "SELECT * FROM peliculas WHERE id_director = ? ORDER BY anio, nombre_film",
                (id_director_seleccionado,)
            )
        except Exception as ex:
            QMessageBox.critical(None, "Error", f"Error al leer la base de datos: {ex}")
            self.cerrar()

    def getFilas_Peliculas(self):
        try:
            return self.cursor.fetchall()
        finally:
            self.cerrar()
    
    def getTodasPeliculas(self):
        try:
            self.cursor.execute("""
                SELECT f.id_film, f.id_director, f.anio, f.nombre_film, d.nombre_director,f.film_visto
                FROM peliculas f
                JOIN directores d ON f.id_director = d.id_director
                ORDER BY f.nombre_film, f.anio
            """)
            return self.cursor.fetchall()
        except Exception as ex:
            QMessageBox.critical(None, "Error", f"Error al obtener todas las películas: {ex}")
            return []
        finally:
            self.cerrar()


class EstaPeliculaData(ConexionBase):
    def __init__(self):
        super().__init__()

    def insert_data(self, esta_pelicula):
        if not self.cursor:
            return

        if esta_pelicula.id_film == 0:
            accion = "insertar"
            query = """
                INSERT INTO peliculas (id_director, anio, nombre_film, carpeta, internet, film_visto)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (
                esta_pelicula.id_director,
                esta_pelicula.anio,
                esta_pelicula.nombre_film,
                esta_pelicula.carpeta,
                esta_pelicula.internet,
                esta_pelicula.film_visto
            )
        else:
            accion = "actualizar"
            query = """
                UPDATE peliculas
                SET anio = ?, nombre_film = ?, carpeta = ?, internet = ?,film_visto = ?
                WHERE id_film = ?
            """
            params = (
                esta_pelicula.anio,
                esta_pelicula.nombre_film,
                esta_pelicula.carpeta,
                esta_pelicula.internet,
                esta_pelicula.film_visto,
                esta_pelicula.id_film
            )

        try:
            self.cursor.execute(query, params)
            self.db.commit()
        except Exception as ex:
            QMessageBox.critical(
                None,
                "Error en la base de datos",  # Título del mensaje
                f"Error al {accion} en la base de datos. Error: {ex}"  # Texto del mensaje
)
        finally:
            self.cerrar()

    def get_ultimo_id_film(self):
        try:
            self.cursor.execute("SELECT MAX(id_film) FROM peliculas")
            self.ultimo_id_film = self.cursor.fetchone()[0]
        except Exception as ex:
            QMessageBox.critical(None, f"Error al leer la base de datos. Error: {ex}")
        finally:
            self.cursor.close()
            self.db.close()
        return self.ultimo_id_film


class EliminarPeliculaData(ConexionBase):
    def __init__(self):
        super().__init__()
        #self.db = self.conectar()
        #self.cursor = self.db.cursor()    #     self.delete_data(id_pelicula_seleccionada)

    def delete_data(self,id_pelicula_seleccionada):
        query = f"DELETE FROM peliculas WHERE id_film = {id_pelicula_seleccionada}"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as ex:
            QMessageBox.critical(None, f"Error al eliminar registro. Error: {ex}")
        finally:
            self.cursor.close()
            self.db.close()

class UltimoIdFilm(ConexionBase):
    def __init__(self):
        super().__init__()

    def get_ultimo_id_film(self):
        try:
            self.cursor.execute("SELECT MAX(id_film) FROM peliculas")
            self.ultimo_id_film = self.cursor.fetchone()[0]
        except Exception as ex:
            QMessageBox.critical(None, f"Error al leer la base de datos. Error: {ex}")
        finally:
            self.cerrar()
        return self.ultimo_id_film

