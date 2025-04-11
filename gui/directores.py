from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from data.directores import Director
import webbrowser


class DirectorsWindow(QDialog):
    def __init__(self, id_director, parent=None):
        super().__init__(parent)
        uic.loadUi("gui/directores.ui", self)
        self.id_director = id_director
        self.original_nombre = ""
        self.original_wiki = ""

        self.btnGrabar.clicked.connect(self.guardar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnCancelar.clicked.connect(self.reject)

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
            self.original_nombre = datos["nombre_director"]
            self.original_wiki = datos["wikipedia_director"]
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

        if self.id_director == 0:
            nuevo = Director(0)
            self.id_director = nuevo.crear_director(nombre, wiki)
        else:
            d = Director(self.id_director)
            d.actualizar_director(nombre, wiki)

        self.accept()

    def eliminar(self):
        confirmar = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Estás seguro de eliminar este director?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmar == QMessageBox.Yes:
            d = Director(self.id_director)
            eliminado = d.eliminar_director()
            if eliminado:
                self.id_director = 0
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el director.")

    def abrir_enlace_wiki(self):
        url = self.wikiDirector.text().strip()
        if url:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
