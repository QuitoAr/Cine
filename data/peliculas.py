import conexion as con
from PyQt5.QtWidgets import QMessageBox

class Peliculas:
    def __init__(self, id_director_seleccionado):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(f"SELECT * FROM peliculas WHERE id_director = {id_director_seleccionado} ORDER BY anio, nombre_film")
        except Exception as ex:
            QMessageBox.critical(None, f"Error al leer la base de datos. Error: {ex}")
            self.db.close()
            self.cursor.close()
    
    def getFilas_Peliculas(self):
        try:
            filas_peliculas = self.cursor.fetchall()
        finally:
            self.cursor.close()
            self.db.close()
        return filas_peliculas

class EstaPeliculaData:
    def __init__(self):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        # self.insert_data(esta_pelicula)

    def insert_data(self, esta_pelicula):
        if esta_pelicula.id_film == 0:
            accion = "insertar"
            query = f"INSERT INTO peliculas (id_director, anio, nombre_film, carpeta, internet) VALUES ({esta_pelicula.id_director}, '{esta_pelicula.anio}' ,'{esta_pelicula.nombre_film}', '{esta_pelicula.carpeta}', '{esta_pelicula.internet}')"
        else:
            accion = "actualizar"
            query = f"UPDATE peliculas SET anio = '{esta_pelicula.anio}' ,nombre_film = '{esta_pelicula.nombre_film.replace("'", "''")}', carpeta = '{esta_pelicula.carpeta}', internet = '{esta_pelicula.internet}' WHERE id_film = {esta_pelicula.id_film}"
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as ex:
            QMessageBox.critical(None, f"Error al {accion} en la base de datos. Error: {ex}")        
        
        self.cursor.close()
        self.db.close()

class UltimoIdFilm:
    def __init__(self):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()

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

class EliminarPeliculaData:
    def __init__(self):
        pass
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()    #     self.delete_data(id_pelicula_seleccionada)

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
