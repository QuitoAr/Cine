from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
import os

from data.directores import Directores
from data.peliculas import Peliculas, EstaPeliculaData, EliminarPeliculaData, UltimoIdFilm
from model.peliculas import EstaPelicula


############# Clase MainWindow #############

class MainWindow():
    def __init__(self):
        self.main = uic.loadUi('gui/main.ui')
        self.main.setWindowFlag(Qt.FramelessWindowHint)
        self.ocultarColumnas()
        self.id_pelicula_seleccionada = 0
        self.id_pelicula_old = 0
        self.id_director_seleccionado = 0
        self.llenarComboDirectores()
        self.botones()
        self.main.show()

#######################################################################
############# Métodos de la clase MainWindow ###########################
#######################################################################

    def botones(self):
        self.main.btnCarpeta.clicked.connect(self.on_btnCarpeta_clicked)
        self.main.btnDirector.clicked.connect(self.on_btnDirectores_clicked)  
        self.main.btnEditar.clicked.connect(self.on_btnEditar_clicked)
        self.main.btnNuevo.clicked.connect(self.on_btnNuevo_clicked)
        self.main.btnGuardar.clicked.connect(self.on_btnGuardar_clicked)
        self.main.btnCancelar.clicked.connect(self.on_btnCancelar_clicked)
        self.main.btnEliminar.clicked.connect(self.on_btnEliminar_clicked)
        self.main.btnInternet.clicked.connect(self.on_btnInternet_clicked)
        self.main.cbcDirectores.currentIndexChanged.connect(self.on_combobox_changed)
        self.main.tblPeliculas.itemSelectionChanged.connect(self.on_row_clicked)

    def on_btnDirectores_clicked(self):
        self.win_directores = uic.loadUi('gui/directores.ui')
        self.win_directores.show()


    def on_btnCarpeta_clicked(self):
        ubicacion = self.main.txtCarpeta.text()
        servidor = "\\\\Titular\\"
        nombre_host = socket.gethostname()
        
        if nombre_host == servidor:
            es_servidor = True
        else:
            es_servidor = False
        
        if ubicacion:  # Si el campo input_ubicacion no está vacío
            if not es_servidor:
                ubicacion = servidor +  ubicacion[0] + ubicacion[2:]
            
            if os.path.isdir(ubicacion):  # Si la ubicación es un directorio válido
                os.startfile(ubicacion)  # Abre el directorio
            else:
                message = "La ubicación especificada no es un directorio válido"
                QMessageBox.critical(None, "Error", message)
        
        else:  # Si el campo input_ubicacion está vacío
            self.insertando_editando()
            directory = QFileDialog.getExistingDirectory(self.main, "Selecciona un directorio")
            if not es_servidor:
                directory = directory[10:]
                directory = directory.replace("/", chr(92))
                directory = directory[0].upper() + ":" + directory[1:]
            
            self.main.txtCarpeta.setText(directory)
        

    def on_btnNuevo_clicked(self):
        if self.id_director_seleccionado == 0:
            QMessageBox.information(None, "Agregar un film", "Seleccione un director.")
            return
        self.id_pelicula_old = self.id_pelicula_seleccionada
        self.id_pelicula_seleccionada = 0
        self.vaciarCampos()
        self.habilitar_txts()
        self.insertando_editando()
        
    def on_btnEditar_clicked(self):
        if self.id_pelicula_seleccionada == 0: # Si no hay un film seleccionado
            QMessageBox.information(None, "Información", "No hay un film seleccionado para editar.")
        else:
            self.insertando_editando()
            self.habilitar_txts()
            
    def on_btnGuardar_clicked(self):
        id_film = self.id_pelicula_seleccionada
        id_director = self.id_director_seleccionado
        anio = self.main.txtAnio.text()
        nombre_film = self.main.txtNombre.text()
        carpeta = self.main.txtCarpeta.text()
        internet = self.main.txtInternet.text()
        esta_pelicula = EstaPelicula(id_film, id_director,anio, nombre_film, carpeta, internet)
        esta_peliculadata = EstaPeliculaData()
        esta_peliculadata.insert_data(esta_pelicula)            
        self.llenarTablaPeliculas()
        
        if self.id_pelicula_seleccionada == 0:
            ultimo_id_film = UltimoIdFilm()
            self.id_pelicula_seleccionada = ultimo_id_film.get_ultimo_id_film()
        try:
            fila = self.encontrar_fila_por_id(self.id_pelicula_seleccionada)
            self.main.tblPeliculas.selectRow(fila)
            self.deshabilitar_txts()
            self.mirando()
        except Exception as ex:
            print("Error:", ex)
            
    def on_btnCancelar_clicked(self):
        self.on_row_clicked()
        self.deshabilitar_txts()
        self.mirando()

    def on_btnEliminar_clicked(self): # Elimina un film y selecciona el primero de la lista
        eliminar = QMessageBox.question(self.main, "Eliminar", "¿Estás seguro de que quieres eliminar este film?", QMessageBox.Yes | QMessageBox.No)
        if eliminar == QMessageBox.Yes:
            eliminar_peliculaData = EliminarPeliculaData()
            eliminar_peliculaData.delete_data(self.id_pelicula_seleccionada)    
        self.llenarTablaPeliculas()
        registros = self.main.tblPeliculas.rowCount()
        if registros > 0:
            self.main.tblPeliculas.selectRow(0)
            self.deshabilitar_txts()
            self.mirando()
    
    def on_btnInternet_clicked(self):
        url = self.main.txtInternet.text()
        if not url == "":  # Si el campo no está vacío
            # Abrir la URL en el navegador
            QDesktopServices.openUrl(QUrl(url))
        else:  # Si el campo está vacío
            QMessageBox.information(self.main, "Información", "No hay link para abrir.")            

        
  ######### Comobo Directores #########
  # Este método se ejecutará cada vez que el usuario seleccione un director
  # en el combo box "cbcDirectores"
  # El método obtiene el registro completo del director seleccionado
  #####################################
          
    def on_combobox_changed(self):
        self.id_director_seleccionado = self.main.cbcDirectores.currentData()
        self.llenarTablaPeliculas()
        if self.main.tblPeliculas.rowCount() > 0:
            self.main.tblPeliculas.selectRow(0)
            self.on_row_clicked()
       
        
    def llenarComboDirectores(self):
        directores = Directores()
        filas = directores.getFilas()
        for fila in filas:
        # Asumiendo que cada fila es una tupla donde el primer elemento es el id y el segundo es el nombre
            id_director, nombre_director = fila
            self.main.cbcDirectores.addItem(nombre_director, id_director)

    #####################################################
    ################### TABLAS DE PELICULAS
    #####################################################
    
    def llenarTablaPeliculas(self):
        peliculas = Peliculas(self.id_director_seleccionado)    #self.id_director_seleccionado)
        datos_peliculas = peliculas.getFilas_Peliculas()
        if datos_peliculas:
            self.main.tblPeliculas.horizontalHeaderVisible = True
            self.main.tblPeliculas.setRowCount(len(datos_peliculas))
            self.main.tblPeliculas.setColumnCount(len(datos_peliculas[0]))
            # Llena el QTableWidget con los datos
            for i, fila in enumerate(datos_peliculas):
                for j, dato in enumerate(fila):
                    item = QTableWidgetItem(str(dato))
                    self.main.tblPeliculas.setItem(i, j, item)
            self.main.tblPeliculas.setEnabled(True)
        else:
            self.main.tblPeliculas.horizontalHeaderVisible = False
            self.main.tblPeliculas.setRowCount(0)
            self.vaciarCampos()
            self.main.tblPeliculas.setEnabled(False)
            self.id_pelicula_seleccionada = 0
        
    def ocultarColumnas(self):
        self.main.tblPeliculas.hideColumn(1)  # Oculta la columna 1
        self.main.tblPeliculas.hideColumn(4)  # Oculta la columna 2
        self.main.tblPeliculas.hideColumn(5)  # Oculta la columna 2
                
    def on_row_clicked(self):
        try:
            fila = self.main.tblPeliculas.currentRow()
        except:
            fila = -1
        if fila == -1:
            fila = 0
            self.vaciarCampos()
        else:
            self.id_pelicula_seleccionada = self.main.tblPeliculas.item(fila, 0).text()
            self.main.txtAnio.setText(self.main.tblPeliculas.item(fila, 2).text())
            self.main.txtNombre.setText(self.main.tblPeliculas.item(fila, 3).text())
            self.main.txtCarpeta.setText(self.main.tblPeliculas.item(fila, 4).text())
            self.main.txtInternet.setText(self.main.tblPeliculas.item(fila, 5).text())

    def encontrar_fila_por_id(self, id_pelicula_seleccionada):
        for i in range(self.main.tblPeliculas.rowCount()):
            if self.main.tblPeliculas.item(i, 0).text() == id_pelicula_seleccionada:
                return i
        return -1  # Retorna -1 si no se encuentra el id

######### Campos y botones de main #########
# Estos métodos se ejecutarán cada vez que el usuario haga clic en un botón
#################################

    def vaciarCampos(self):
        # self.id_pelicula_seleccionada = 0
        self.main.txtNombre.setText("")
        self.main.txtAnio.setText("")
        self.main.txtCarpeta.setText("")
        self.main.txtInternet.setText("")
            
    def habilitar_txts(self):
        self.main.txtNombre.setEnabled(True)
        self.main.txtAnio.setEnabled(True)
        self.main.txtCarpeta.setEnabled(True)
        self.main.txtInternet.setEnabled(True)
            
    def deshabilitar_txts(self):
        self.main.txtAnio.setEnabled(False)
        self.main.txtNombre.setEnabled(False)
        self.main.txtCarpeta.setEnabled(False)
        self.main.txtInternet.setEnabled(False)

    def mirando(self):
        self.main.btnGuardar.setEnabled(False)
        self.main.btnCancelar.setEnabled(False)
        self.main.btnNuevo.setEnabled(True)
        self.main.tblPeliculas.setEnabled(True)
        self.main.btnEditar.setEnabled(True)
        self.main.btnEliminar.setEnabled(True)
        self.main.btnCarpeta.setEnabled(True)
        self.main.btnInternet.setEnabled(True)
        self.main.cboDirectores.setEnabled(True)
        
    def insertando_editando(self):
        self.main.btnGuardar.setEnabled(True)
        self.main.btnCancelar.setEnabled(True)
        self.main.btnNuevo.setEnabled(False)
        self.main.btnEditar.setEnabled(False)
        self.main.btnEliminar.setEnabled(False)
        self.main.tblPeliculas.setEnabled(False)
        self.main.btnInternet.setEnabled(False)
        self.main.btnCarpeta.setEnabled(False)
        self.main.cboDirectores.setEnabled(False)
        self.main.txtAnio.setFocus()
        