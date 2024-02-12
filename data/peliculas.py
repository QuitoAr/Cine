from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtSql import QSqlDatabase


class Peliculas:
    def __init__(self,id_director_seleccionado):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("cine.db")
        self.db.open()
        self.model = QSqlQueryModel()
        self.load_data(id_director_seleccionado)
        self.db.close()

    def load_data(self,id_director_seleccionado):
        query = f"SELECT * FROM peliculas WHERE id_director = {id_director_seleccionado}"
        self.model.setQuery(query, self.db)
        if self.model.lastError().isValid():
            print(self.model.lastError().text())
        

    def getModel(self):
        return self.model

class EstaPeliculaData:
    def __init__(self, esta_pelicula):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("cine.db")
        self.db.open()
        self.model = QSqlQueryModel()
        self.insert_data(esta_pelicula)
        self.db.close()

    def insert_data(self,esta_pelicula):
        query = f"INSERT INTO peliculas (id_director, nombre_film, carpeta_contenedora, filmaffinity) VALUES ({esta_pelicula.id_director}, '{esta_pelicula.nombre_film}', '{esta_pelicula.carpeta_contenedora}', '{esta_pelicula.filmaffinity}')"
        self.model.setQuery(query, self.db)
        
        if self.model.lastError().isValid():
            print(self.model.lastError().text())
        
