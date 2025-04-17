from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QTableWidgetItem
import socket
import os
import webbrowser
import requests

from data.directores import Directores
from data.peliculas import Peliculas, EstaPeliculaData, EliminarPeliculaData, UltimoIdFilm
from model.peliculas import EstaPelicula
from gui.directores import DirectorsWindow  # Importá la clase, no uic


############# Clase MainWindow #############

class MainWindow():
    def __init__(self):
        self.main = uic.loadUi('gui/main.ui')
        self.main.setWindowFlag(Qt.FramelessWindowHint)
        self.ocultarColumnas()
        self.id_pelicula_seleccionada = 0
        self.id_pelicula_old = 0
        self.id_director_seleccionado = 0
        self.actualizando_campos = True
        self.llenarComboDirectores()
        self.botones()
        self.main.show()
        
        self.main.txtAnio.textChanged.connect(self.hay_cambios)
        self.main.txtNombre.textChanged.connect(self.hay_cambios)
        self.main.txtCarpeta.textChanged.connect(self.hay_cambios)
        self.main.txtInternet.textChanged.connect(self.hay_cambios)
        self.main.txtInternet.returnPressed.connect(self.abrir_wikipedia)

#######################################################################
############# Métodos de la clase MainWindow ###########################
#######################################################################

    def botones(self):
        #self.main.btnInternet.clicked.connect(self.abrir_wikipedia)
        #self.main.btnEditar.clicked.connect(self.hay_cambios)
        self.main.txtCarpeta.returnPressed.connect(self.on_txtCarpeta_enter)
        self.main.btnDirector.clicked.connect(self.on_btnDirectores_clicked)  
        self.main.btnNuevo.clicked.connect(self.on_btnNuevo_clicked)
        self.main.btnGrabar.clicked.connect(self.on_btnGrabar_clicked)
        self.main.btnCancelar.clicked.connect(self.on_btnCancelar_clicked)
        self.main.btnEliminar.clicked.connect(self.on_btnEliminar_clicked)
        self.main.cbcDirectores.currentIndexChanged.connect(self.on_combobox_changed)
        self.main.tblPeliculas.itemSelectionChanged.connect(self.on_row_clicked)
        

    def on_btnDirectores_clicked(self):
        id_director = self.id_director_seleccionado or 0
        dialogo = DirectorsWindow(id_director, parent=self.main, main_window=self)

        resultado = dialogo.exec_()

        if resultado == QDialog.Accepted and dialogo.cambios:
            nuevo_id = dialogo.id_director

            self.actualizarComboDirectores()  # Siempre refrescamos el combo

            if nuevo_id != 0:
                # Se creó uno nuevo o se modificó el mismo
                self.seleccionarDirectorEnCombo(nuevo_id)
            else:
                # Se eliminó el director actual: seleccionamos uno anterior o primero disponible
                self.id_director_seleccionado = self.obtenerIdDirectorActual()  # este método puede retornar el primer ID válido
                self.seleccionarDirectorEnCombo(self.id_director_seleccionado)

            # Al cambiar el director, la tabla se debe actualizar automáticamente
            # Esto ocurre porque on_combobox_changed se encarga de actualizar la tabla


    def on_combobox_changed(self):
        self.id_director_seleccionado = self.main.cbcDirectores.currentData()
        
        if self.id_director_seleccionado is None:
            self.main.tblPeliculas.setRowCount(0)
            return

        self.llenarTablaPeliculas()

        if self.main.tblPeliculas.rowCount() > 0:
            self.main.tblPeliculas.selectRow(0)
            self.on_row_clicked()


    def estoy_en_titular(self):
        return socket.gethostname().lower() == 'titular'

    def ruta_para_abrir(self, ubicacion_local):
        """Devuelve la ruta adecuada para abrir según si estás en \\Titular o en otra máquina."""
        if self.estoy_en_titular():
            return ubicacion_local
        else:
            unidad = ubicacion_local[0].lower()
            subruta = ubicacion_local[3:]  # salta 'D:\' -> empieza desde posición 3
            return fr"\\Titular\{unidad}\{subruta}"

    def on_txtCarpeta_enter(self):
        ubicacion = self.main.txtCarpeta.text().strip()

        if ubicacion:
            ruta_final = self.ruta_para_abrir(ubicacion)

            if os.path.isdir(ruta_final):
                QDesktopServices.openUrl(QUrl.fromLocalFile(ruta_final))
            else:
                QMessageBox.critical(self.main, "Error", "La ubicación especificada no es un directorio válido.")
        else:
            self.insertando_editando()
            carpeta_seleccionada = QFileDialog.getExistingDirectory(self.main, "Selecciona un directorio")

        if carpeta_seleccionada:
            carpeta_local = carpeta_seleccionada

            # 🔁 Si viene como ruta de red tipo '//titular/f/Films/...' la convertimos
            if carpeta_local.startswith('//') or carpeta_local.startswith('/'):
                partes = carpeta_local.replace('/', '\\').split('\\')
                # Esperamos algo como ['', '', 'titular', 'f', 'Films', 'Carpeta']
                if len(partes) >= 5 and partes[2].lower() == 'titular':
                    unidad = partes[3].upper()
                    subruta = '\\'.join(partes[4:])
                    carpeta_local = f"{unidad}:\\{subruta}"

            self.main.txtCarpeta.setText(carpeta_local)



    def on_btnNuevo_clicked(self):
        if self.id_director_seleccionado == 0:
            QMessageBox.information(None, "Agregar un film", "Seleccione un director.")
            return
        self.actualizando_campos = True
        self.id_pelicula_old = self.id_pelicula_seleccionada
        self.id_pelicula_seleccionada = 0
        self.vaciarCampos()
        self.insertando_editando()
        
    def hay_cambios(self):
        if self.actualizando_campos:
            return
        ' Averigua si los campos cambiaron por presion de una tecla'
        if self.id_pelicula_seleccionada == 0: # Si no hay un film seleccionado
            QMessageBox.information(None, "Información", "No hay un film seleccionado para editar.")
        else:
            self.insertando_editando()
            
    def on_btnGrabar_clicked(self):
        self.actualizando_campos = True
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
            self.mirando()
        except Exception as ex:
            print("Error:", ex)
        self.actualizando_campos = False
        
    def on_btnCancelar_clicked(self):
        self.actualizando_campos = True
        self.on_row_clicked()
        self.mirando()
        self.actualizando_campos = False

    def on_btnEliminar_clicked(self): # Elimina un film y selecciona el primero de la lista
        eliminar = QMessageBox.question(self.main, "Eliminar", "¿Estás seguro de que quieres eliminar este film?", QMessageBox.Yes | QMessageBox.No)
        if eliminar == QMessageBox.Yes:
            eliminar_peliculaData = EliminarPeliculaData()
            eliminar_peliculaData.delete_data(self.id_pelicula_seleccionada)    
        self.llenarTablaPeliculas()
        registros = self.main.tblPeliculas.rowCount()
        if registros > 0:
            self.main.tblPeliculas.selectRow(0)
            self.mirando()
    
    def abrir_wikipedia(self):
        url = self.main.txtInternet.text().strip()
        
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
        else:
            nombre = self.main.txtNombre.text().strip()
            if not nombre:
                return

            # Usamos la API de Wikipedia para buscar
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": nombre,
                "format": "json"
            }

            try:
                response = requests.get(search_url, params=params)
                data = response.json()
                resultados = data.get("query", {}).get("search", [])
                if resultados:
                    # Tomamos la primera página encontrada
                    titulo = resultados[0]["title"]
                    wiki_url = f"https://en.wikipedia.org/wiki/{titulo.replace(' ', '_')}"
                    self.main.txtInternet.setText(wiki_url)
                    webbrowser.open(wiki_url)
            except Exception as e:
                print("Error al buscar en Wikipedia:", e)
         

        
  ######### Comobo Directores #########
  # Este método se ejecutará cada vez que el usuario seleccione un director
  # en el combo box "cbcDirectores"
  # El método obtiene el registro completo del director seleccionado
  #####################################
          
    # Removed redundant definition of on_combobox_changed
       
        
    def llenarComboDirectores(self):
        self.main.cbcDirectores.clear()
        directores = Directores()
        filas = directores.getFilas()
        
        for id_director, nombre_director in filas:
            self.main.cbcDirectores.addItem(nombre_director, id_director)

        if self.main.cbcDirectores.count() > 0:
            self.main.cbcDirectores.setCurrentIndex(0)  # Esto dispara on_combobox_changed automáticamente
        else:
            self.id_director_seleccionado = 0
            self.main.tblPeliculas.setRowCount(0)


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
        self.actualizando_campos = True
        try:
            fila = self.main.tblPeliculas.currentRow()
        except Exception:
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
        self.actualizando_campos = False

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
            
    def mirando(self):
        self.main.btnGrabar.setEnabled(False)
        self.main.btnCancelar.setEnabled(False)
        self.main.btnNuevo.setEnabled(True)
        self.main.tblPeliculas.setEnabled(True)
        self.main.btnEliminar.setEnabled(True)
        self.main.btnCarpeta.setEnabled(True)
        self.main.cbcDirectores.setEnabled(True)
        
    def insertando_editando(self):
        self.main.btnGrabar.setEnabled(True)
        self.main.btnCancelar.setEnabled(True)
        self.main.btnNuevo.setEnabled(False)
        self.main.btnEliminar.setEnabled(False)
        self.main.tblPeliculas.setEnabled(False)
        self.main.btnCarpeta.setEnabled(False)
        self.main.cbcDirectores.setEnabled(False)

    def actualizarComboDirectores(self):
        """Rellena el ComboBox de directores desde la base de datos."""
        self.main.cbcDirectores.clear()
        directores = Directores()
        filas = directores.getFilas()
        for id_dir, nombre_dir in filas:
            self.main.cbcDirectores.addItem(nombre_dir, id_dir)


    def seleccionarDirectorEnCombo(self, id_director):
        """Selecciona en el combo el director por ID."""
        index = self.main.cbcDirectores.findData(id_director)
        if index != -1:
            self.main.cbcDirectores.setCurrentIndex(index)
        else:
            self.main.cbcDirectores.setCurrentIndex(-1)

    def setearDirectorActivo(self, id_director):
        """Selecciona un director por ID y actualiza la vista de películas."""
        index = self.main.cbcDirectores.findData(id_director)
        if index != -1:
            self.main.cbcDirectores.setCurrentIndex(index)
        else:
            self.main.cbcDirectores.setCurrentIndex(-1)

        self.id_director_seleccionado = id_director
        self.llenarTablaPeliculas()
        if self.main.tblPeliculas.rowCount() > 0:
            self.main.tblPeliculas.selectRow(0)
            self.on_row_clicked()

    def obtenerIdDirectorActual(self):
        if self.main.cbcDirectores.count() == 0:
            return 0
        return self.main.cbcDirectores.itemData(0)  # Selecciona el primer item si queda alguno
