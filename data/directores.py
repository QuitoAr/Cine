from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class Directores:
    def __init__(self):
        # Asumiendo que tienes una base de datos SQLite llamada 'mydatabase.db'
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('cine.db')
        self.db.open()

        self.model = QSqlTableModel(db=self.db)
        self.model.setTable('directores')
        self.model.select()
        self.db.close()

    def getModel(self):
        return self.model