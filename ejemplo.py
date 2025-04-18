from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QMenu, QAction
import sys

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo de QToolButton")
        self.setGeometry(100, 100, 400, 300)

        # Crear un QToolButton
        self.toolButton = QToolButton(self)
        self.toolButton.setText("Opciones")
        self.toolButton.setGeometry(150, 120, 100, 30)  # Posición y tamaño

        # Crear un menú para el QToolButton
        self.menu = QMenu(self)

        # Agregar acciones al menú
        accionUno = QAction("Acción 1", self)
        accionUno.triggered.connect(self.accion_uno)
        self.menu.addAction(accionUno)

        accionDos = QAction("Acción 2", self)
        accionDos.triggered.connect(self.accion_dos)
        self.menu.addAction(accionDos)

        accionTres = QAction("Acción 3", self)
        accionTres.triggered.connect(self.accion_tres)
        self.menu.addAction(accionTres)

        # Asignar el menú al QToolButton
        self.toolButton.setMenu(self.menu)
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)  # Menú emergente

    def accion_uno(self):
        print("¡Acción 1 ejecutada!")

    def accion_dos(self):
        print("¡Acción 2 ejecutada!")

    def accion_tres(self):
        print("¡Acción 3 ejecutada!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())