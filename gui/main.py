from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from data.directores import Directores
from data.peliculas import Peliculas ,EstaPeliculaData, EliminarPeliculaData
from model.peliculas import EstaPelicula
from PyQt5.QtCore import Qt
import sys
import socket


############# Clase MainWindow #############

class MainWindow():
    def __init__(self):
        self.main = uic.loadUi('gui/main.ui')
        self.main.setWindowFlag(Qt.FramelessWindowHint)
        self.ocultarColumnas()
        self.id_pelicula_seleccionada = 0
        self.id_director_seleccionado = 0
        self.llenarComboDirectores()
        self.botones()
        self.main.show()

############# Métodos de la clase MainWindow #############
# Estos métodos se ejecutarán cada vez que el usuario haga clic en un botón
###########################################################

    def botones(self):
        self.main.btnCarpeta.clicked.connect(self.on_btnCarpeta_clicked)
        # self.main.tblPeliculas.itemSelectionChanged.connect(self.on_row_clicked)
        self.main.tblPeliculas.clicked.connect(self.on_row_clicked)
        self.main.btnEditar.clicked.connect(self.on_btnEditar_clicked)
        self.main.btnNuevo.clicked.connect(self.on_btnNuevo_clicked)
        self.main.btnGuardar.clicked.connect(self.on_btnGuardar_clicked)
        self.main.btnCancelar.clicked.connect(self.on_btnCancelar_clicked)
        self.main.btnEliminar.clicked.connect(self.on_btnEliminar_clicked)
        self.main.btnInternet.clicked.connect(self.on_btnInternet_clicked)
        self.main.actionSalir.triggered.connect(self.on_actionSalir_triggered)
        self.main.cbcDirectores.currentIndexChanged.connect(self.on_combobox_changed)

    def on_btnCarpeta_clicked(self):
        ubicacion = self.main.txtCarpeta.text()
        if ubicacion:  # Si el campo input_ubicacion no está vacío
            nombre_host = socket.gethostname()
            servidor = "\\\\Titular\\"
            
            if not nombre_host == servidor:
                ubicacion = servidor +  ubicacion[0] + ubicacion[2:]
            
            if os.path.isdir(ubicacion):  # Si la ubicación es un directorio válido
                os.startfile(ubicacion)  # Abre el directorio
            else:
                message = "La ubicación especificada no es un directorio válido"
                QMessageBox.critical(None, "Error", message)
        
        else:  # Si el campo input_ubicacion está vacío
            directory = QFileDialog.getExistingDirectory(self.main, "Selecciona un directorio")
            print(directory)
            self.main.txtCarpeta_Contenedora.setText(directory)
        

    def on_btnNuevo_clicked(self):
        self.id_pelicula_seleccionada = 0
        self.vaciarCampos()
        self.habilitar_txts()
        self.insertando_editando()
        
    def on_btnEditar_clicked(self):
        if self.id_pelicula_seleccionada == 0: # Si no hay un film seleccionado
            QMessageBox.information(None, "Información", "Seleccione un film para editar.")
        else:
            self.insertando_editando()
            self.habilitar_txts()
            
    def on_btnGuardar_clicked(self):
        id_film = self.id_pelicula_seleccionada
        id_director = self.id_director_seleccionado
        anio = self.txtAnio.text()
        nombre_film = self.main.txtNombre.text()
        carpeta = self.main.txtCarpeta_Contenedora.text()
        internet = self.main.txtInternet.text()
        esta_pelicula = EstaPelicula(id_film, id_director,anio, nombre_film, carpeta, internet)
        esta_peliculaData = EstaPeliculaData(esta_pelicula)
        self.llenarTablaPeliculas()
        self.vaciarCampos()
        self.deshabilitar_txts()
        self.mirando()
            
    def on_btnCancelar_clicked(self):
        self.vaciarCampos()
        self.deshabilitar_txts()
        self.mirando()
        if self.id_pelicula_seleccionada == 0:
            self.on_row_clicked()

    def on_btnEliminar_clicked(self):
        eliminar = QMessageBox.question(self.main, "Eliminar", "¿Estás seguro de que quieres eliminar este film?", QMessageBox.Yes | QMessageBox.No)
        if eliminar == QMessageBox.Yes:
            # Crear una nueva instancia de EliminarPeliculaData pasando el id del film seleccionado
            eliminar_peliculaData = EliminarPeliculaData(self.id_pelicula_seleccionada)
            # Llamar al método delete_data de eliminar_peliculaData pasando el id del film seleccionado
            # eliminar_peliculaData.delete_data(self.id_pelicula_seleccionada)
            # Actualizar la tabla de películas
        self.llenarTablaPeliculas()
        self.vaciarCampos()
        self.deshabilitar_txts()
        self.mirando()
        self.on_row_clicked(self.main.tblPeliculas.currentIndex())
    
    def on_btnInternet_clicked(self):
        # QMessageBox.information(self.main, "Información", "Botón Internet clickeado!")
        url = self.main.txtFilmaffinity.text()
        if not url == "":  # Si el campo no está vacío
            # Abrir la URL en el navegador
            QDesktopServices.openUrl(QUrl(url))
        
    
    def on_actionSalir_triggered(self):
        self.main.close()
        
        

        
  ######### Comobo Directores #########
  # Este método se ejecutará cada vez que el usuario seleccione un director
  # en el combo box "cbcDirectores"
  # El método obtiene el registro completo del director seleccionado
  #####################################
          
    def on_combobox_changed(self):
        self.id_director_seleccionado = self.main.cbcDirectores.currentData()
        print(self.id_director_seleccionado)
        self.llenarTablaPeliculas()
       
        
    def llenarComboDirectores(self):
        directores = Directores()
        filas = directores.getFilas()
        self.main.cbcDirectores.insertItem(0, "-> Seleccionar una opción:")
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
            self.main.tblPeliculas.setRowCount(len(datos_peliculas))
            self.main.tblPeliculas.setColumnCount(len(datos_peliculas[0]))
            # Llena el QTableWidget con los datos
            for i, fila in enumerate(datos_peliculas):
                for j, dato in enumerate(fila):
                    item = QTableWidgetItem(str(dato))
                    self.main.tblPeliculas.setItem(i, j, item)
            self.main.tblPeliculas.selectRow(0)
            self.on_row_clicked()
            self.main.tblPeliculas.setEnabled(True) 
        else:
            self.main.tblPeliculas.setRowCount(0)
            self.vaciarCampos()
            self.main.tblPeliculas.setEnabled(False)
        
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
        
    def insertando_editando(self):
        self.main.btnGuardar.setEnabled(True)
        self.main.btnCancelar.setEnabled(True)
        self.main.btnNuevo.setEnabled(False)
        self.main.btnEditar.setEnabled(False)
        self.main.btnEliminar.setEnabled(False)
        self.main.tblPeliculas.setEnabled(False)
        self.main.btnInternet.setEnabled(False)
        self.main.btnCarpeta.setEnabled(False)
        self.main.txtAnio.setFocus()