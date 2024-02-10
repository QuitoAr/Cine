from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel


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
    