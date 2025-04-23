from PyQt5.QtWidgets import QApplication
import sys

# Asegúrate de que el import de Login sea correcto
from gui.login import Login  # Verifica que esta clase exista en gui/login.py

class Cine:
    def __init__(self):
        self.app = QApplication(sys.argv)  # Inicializa la aplicación Qt
        self.login = Login()  # Crea una instancia de Login
        self.login.show()  # Muestra la ventana de Login
        self.app.exec_()  # Inicia el bucle de eventos de la aplicación

if __name__ == "__main__":
    cine = Cine()  # Crea una instancia de Cine y ejecuta la aplicación
