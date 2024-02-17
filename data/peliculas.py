from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtSql import QSqlDatabase

import conexion as con

class Peliculas:
    def __init__(self, id_director_seleccionado):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(f"SELECT * FROM peliculas WHERE id_director = {id_director_seleccionado} ORDER BY anio, nombre_film")
        except Exception as ex:
            print(ex)
    def getFilas_Peliculas(self):
        try:
            filas_peliculas = self.cursor.fetchall()
        finally:
            self.cursor.close()
            self.db.close()
        return filas_peliculas

class EstaPeliculaData:
    pass
    # def __init__(self, esta_pelicula):
    #     self.db = QSqlDatabase.addDatabase("QSQLITE")
    #     self.db.setDatabaseName("cine.db")
    #     self.db.open()
    #     self.model = QSqlQueryModel()
    #     self.insert_data(esta_pelicula)
    #     self.db.close()

    # def insert_data(self,esta_pelicula):
    #     if esta_pelicula.id_film == 0:
    #         query = f"INSERT INTO peliculas (id_director, nombre_film, carpeta_contenedora, filmaffinity) VALUES ({esta_pelicula.id_director}, '{esta_pelicula.nombre_film}', '{esta_pelicula.carpeta_contenedora}', '{esta_pelicula.filmaffinity}')"
    #     else:
    #         query = f"UPDATE peliculas SET nombre_film = '{esta_pelicula.nombre_film}', carpeta_contenedora = '{esta_pelicula.carpeta_contenedora}', filmaffinity = '{esta_pelicula.filmaffinity}' WHERE id_film = {esta_pelicula.id_film}"
    #     self.model.setQuery(query, self.db)
        
    #     if self.model.lastError().isValid():
    #         print(self.model.lastError().text())
        

class EliminarPeliculaData:
    def __init__(self, id_pelicula_seleccionada):
        pass
    #     self.db = QSqlDatabase.addDatabase("QSQLITE")
    #     self.db.setDatabaseName("cine.db")
    #     self.db.open()
    #     self.model = QSqlQueryModel()
    #     self.delete_data(id_pelicula_seleccionada)
    #     self.db.close()

    # def delete_data(self,id_pelicula_seleccionada):
    #     query = f"DELETE FROM peliculas WHERE id_film = {id_pelicula_seleccionada}"
    #     self.model.setQuery(query, self.db)
        
    #     if self.model.lastError().isValid():
    #         print(self.model.lastError().text())