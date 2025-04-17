from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from data.peliculas import Peliculas


class BuscarWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        import os
        ruta_ui = os.path.join(os.path.dirname(__file__), "ventana_buscar.ui")
        uic.loadUi(ruta_ui, self)

        self.id_film = None
        self.id_director = None
        
        # Obtenemos las películas. Si no hay un director seleccionado, obtendremos todas las películas
        self.peliculas = Peliculas(id_director_seleccionado=None).getTodasPeliculas()

        # Conectamos los eventos
        self.txtBuscar.textChanged.connect(self.filtrar)
        self.btnAceptar.clicked.connect(self.seleccionar)
        self.btnCancelar.clicked.connect(self.reject)
        
        self.resultados_filtrados = []

        # Llamamos a cargarTabla pasando la lista completa de películas
        self.cargarTabla(self.peliculas)


    def cargarTabla(self, lista):
        # Establecer el número de columnas: id_film, id_director y nombre_film
        self.tblResultados.setColumnCount(3)
        self.tblResultados.setHorizontalHeaderLabels(["ID", "Director", "Nombre de la Película"])
        self.tblResultados.setColumnWidth(0, 50)   # id_film
        self.tblResultados.setColumnWidth(1, 80)   # id_director
        self.tblResultados.setColumnWidth(2, 300)  # nombre_film

        # Establecer el número de filas según el tamaño de la lista
        self.tblResultados.setRowCount(len(lista))

        # Llenar la tabla con las filas correspondientes
        for i, fila in enumerate(lista):
            self.tblResultados.setItem(i, 0, QTableWidgetItem(str(fila[0])))  # id_film
            self.tblResultados.setItem(i, 1, QTableWidgetItem(str(fila[1])))  # id_director
            self.tblResultados.setItem(i, 2, QTableWidgetItem(str(fila[3])))  # nombre_film

    def filtrar(self):
        texto = self.txtBuscar.text().lower()
        filtradas = [fila for fila in self.peliculas if texto in fila[3].lower()]
        self.cargarTabla(filtradas)

    def seleccionar(self):
        fila = self.tblResultados.currentRow()
        if fila >= 0:
            self.id_film = int(self.tblResultados.item(fila, 0).text())
            self.id_director = int(self.tblResultados.item(fila, 1).text())
            self.accept()  # <-- ESTA LÍNEA ES CLAVE
