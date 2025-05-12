
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from data.peliculas import Peliculas
from utiles import recurso_relativo


class BuscarWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = recurso_relativo('gui/ventana_buscar.ui') # Cambié la ruta a la función recurso_relativo
        self.main = uic.loadUi(ui_path, self) # Cambié la ruta a la función recurso_relativo
        
         # Verificar si tblResultados está presente
        if hasattr(self.main, 'tblResultados'):
            self.tblResultados = self.main.tblResultados
        else:
            print("Error: El widget tblResultados no se encuentra en el archivo .ui")
            return       
        self.tblResultados.verticalHeader().setVisible(True)

        self.id_film = None
        self.id_director = None
        
        # Obtenemos las películas. Si no hay un director seleccionado, obtendremos todas las películas
        self.peliculas = Peliculas(id_director_seleccionado=None).getTodasPeliculas()

        # Conectamos los eventos
        self.txtBuscar.textChanged.connect(self.filtrar)
        self.checkVisto.stateChanged.connect(self.filtrar)

        self.tblResultados.itemDoubleClicked.connect(self.seleccionar)
        
        self.resultados_filtrados = []

        # Llamamos a cargarTabla pasando la lista completa de películas
        self.cargarTabla(self.peliculas)
        self.filtrar()  # Llamamos a filtrar para aplicar el filtro inicial

# buscar.py

    def cargarTabla(self, lista):
        # Establecer el número de columnas: id_film, id_director y nombre_film
        self.tblResultados.setColumnCount(5)
        self.tblResultados.setHorizontalHeaderLabels(["","","Nombre del Film", "Director", "Visto"]) # Cambié el encabezado a español
        self.tblResultados.setColumnWidth(0, 0)   # id_film
        self.tblResultados.setColumnWidth(1, 0)   # id_director
        self.tblResultados.setColumnWidth(2, 350)  # nombre_film
        self.tblResultados.setColumnWidth(3, 170)  # nombre_director
        self.tblResultados.setColumnWidth(4, 10) # film_visto

        # Establecer el número de filas según el tamaño de la lista
        self.tblResultados.setRowCount(len(lista))

        # Llenar la tabla con las filas correspondientes
        for i, fila in enumerate(lista):
            self.tblResultados.setItem(i, 0, QTableWidgetItem(str(fila[0])))  # id_film
            self.tblResultados.setItem(i, 1, QTableWidgetItem(str(fila[1])))  # id_director
            self.tblResultados.setItem(i, 2, QTableWidgetItem(str(fila[3])))  # nombre_film
            self.tblResultados.setItem(i, 3, QTableWidgetItem(str(fila[4]))) # nombre_director  
            self.tblResultados.setItem(i, 4, QTableWidgetItem(str(fila[5]))) # film_visto
            # Ocultar las columnas de id_film y id_director

    def filtrar(self):
        texto = self.txtBuscar.text().lower()
        solo_no_vistas = self.checkVisto.isChecked()

        # Filtra por nombre
        filtradas = [fila for fila in self.peliculas if texto in fila[3].lower()]

        # Si el checkbox está tildado, filtramos también por film_visto = False
        if solo_no_vistas:
            filtradas = [fila for fila in filtradas if not fila[5]]  # fila[5] es film_visto

        self.cargarTabla(filtradas)


    def seleccionar(self):
        fila = self.tblResultados.currentRow()
        if fila >= 0:
            self.id_film = int(self.tblResultados.item(fila, 0).text())
            self.id_director = int(self.tblResultados.item(fila, 1).text())
            self.accept()  # <-- ESTA LÍNEA ES CLAVE
