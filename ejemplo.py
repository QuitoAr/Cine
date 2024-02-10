from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.combobox = QComboBox(self)
        self.setCentralWidget(self.combobox)

        # Asumiendo que tienes una base de datos SQLite llamada 'mydatabase.db'
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('cine.db')
        db.open()

        self.model = QSqlTableModel(db=db)
        self.model.setTable('directores')
        self.model.select()

        self.combobox.setModel(self.model)
        self.combobox.setModelColumn(1)  # Mostrar solo la segunda columna

        self.combobox.currentIndexChanged.connect(self.on_combobox_changed)

    def on_combobox_changed(self, index):
        # Obtener el valor de la primera columna de la línea seleccionada
        first_column_value = self.model.record(index).value(0)
        print(first_column_value)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()