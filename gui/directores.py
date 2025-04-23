import webbrowser
import requests

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from data.directores import Director
from utiles import recurso_relativo
class DirectorsWindow(QDialog):
    def __init__(self, id_director=0, parent=None, main_window=None):
        super().__init__(parent)
        #uic.loadUi("gui/directores.ui", self)
        ui_path = recurso_relativo('gui/directores.ui') # Cargar la ruta del archivo .ui
        self.main = uic.loadUi(ui_path, self)
        self.id_director = id_director
        self.main_window = main_window
        self.cambios = False
        self.original_nombre = ""
        self.original_wiki = ""

        self.btnGrabar.clicked.connect(self.guardar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnCancelar.clicked.connect(self.reject)
        self.btnNuevo.clicked.connect(self.nuevo_director)

        self.nombreCineasta.textChanged.connect(self.detectar_cambios)
        self.wikiDirector.textChanged.connect(self.detectar_cambios)
        
        self.wikiDirector.returnPressed.connect(self.abrir_enlace_wiki)


        if self.id_director != 0:
            self.cargar_director()
        else:
            self.btnEliminar.setEnabled(False)
            self.btnGrabar.setEnabled(False)  # Deshabilitar hasta que se empiece a escribir

    def cargar_director(self):
        director = Director(self.id_director)
        datos = director.getDirector()
        if datos:
            self.id_cargado = datos["id_director"]
            self.original_nombre = datos["nombre_director"]
            self.original_wiki = datos["wikipedia_director"]
            self.labelId_Director.setText(str(self.id_cargado))
            self.nombreCineasta.setText(self.original_nombre)
            self.wikiDirector.setText(self.original_wiki)
        self.btnGrabar.setEnabled(False)

    def detectar_cambios(self):
        nombre_actual = self.nombreCineasta.text().strip()
        wiki_actual = self.wikiDirector.text().strip()

        if self.id_director == 0:
            # Nuevo director: habilitar guardar si hay nombre
            self.btnGrabar.setEnabled(nombre_actual != "")
        else:
            cambios = (
                nombre_actual != self.original_nombre or
                wiki_actual != self.original_wiki
            )
            self.btnGrabar.setEnabled(cambios)

    def guardar(self):
        nombre = self.nombreCineasta.text().strip()
        wiki = self.wikiDirector.text().strip()

        if nombre == "":
            QMessageBox.warning(self, "Advertencia", "El nombre del director no puede estar vacío.")
            return

        if self.id_director == 0:  # Es nuevo
            nuevo = Director(0)
            nuevo_id = nuevo.crear_director(nombre, wiki)
            if nuevo_id:
                self.id_director = nuevo_id
                self.cambios = True
        else:  # Modificación
            d = Director(self.id_director)
            if d.actualizar_director(nombre, wiki):
                self.cambios = True

        self.accept()  # Cierra la ventana



    def eliminar(self):
        confirmacion = QMessageBox.question(
            self, "Confirmar", "¿Estás seguro de que deseas eliminar este director?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            try:
                d = Director(self.id_director)
                d.eliminar_director()
                self.cambios = True
                self.id_director = 0
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el director.\n{str(e)}")



    def abrir_enlace_wiki(self):
        url = self.wikiDirector.text().strip()
        
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
        else:
            nombre = self.nombreCineasta.text().strip()
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
                    self.wikiDirector.setText(wiki_url)
                    webbrowser.open(wiki_url)
            except Exception as e:
                print("Error al buscar en Wikipedia:", e)

            
    def nuevo_director(self):
        self.id_director = 0
        self.nombreCineasta.clear()
        self.wikiDirector.clear()
        self.labelId_Director.clear()

        self.original_nombre = ""
        self.original_wiki = ""

        self.btnGrabar.setEnabled(False)
        self.btnCancelar.setEnabled(True)
        self.btnNuevo.setEnabled(False)
        self.btnEliminar.setEnabled(False)

        self.nombreCineasta.setFocus()

    def cancelar_operacion(self):
        QMessageBox.information(self, "Cancelado", "Se canceló la operación.")

        if self.id_director == 0:
            # Operación cancelada al crear uno nuevo: limpiar todo
            self.nombreCineasta.clear()
            self.wikiDirector.clear()
            self.btnGrabar.setEnabled(False)
            self.btnEliminar.setEnabled(False)
            self.btnNuevo.setEnabled(True)
        else:
            # Restaurar valores originales del director en edición
            self.nombreCineasta.setText(self.original_nombre)
            self.wikiDirector.setText(self.original_wiki)
            self.btnGrabar.setEnabled(False)

        self.btnCancelar.setEnabled(False)
        self.btnNuevo.setEnabled(True)
        self.btnEliminar.setEnabled(True)   

