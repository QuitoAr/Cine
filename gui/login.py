from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario
from PyQt5 import QtCore
import pyodbc

class Login():
    def __init__(self):
        self.login = uic.loadUi('gui/login.ui')
        self.initGUI()
        self.login.lblMensaje.setText('')
        self.login.show()
        
    def ingresar(self):
        if self.login.txtUsuario.text() == '':
            self.login.lblMensaje.setText('Debe ingresar un usuario válido.')
            self.login.txtUsuario.setFocus()
        elif self.login.txtClave.text() == '':
            self.login.lblMensaje.setText('Debe ingresar una clave válida.')
            self.login.txtClave.setFocus()
        else:
            self.login.lblMensaje.setText('')
            usu = Usuario(usuario=self.login.txtUsuario.text(), clave=self.login.txtClave.text())
            usuData = UsuarioData()
            usuData.login(usu)
            res = usuData.login(usu)
            if res:
                self.main = MainWindow()
                self.login.hide()
            else:
                self.login.lblMensaje.setText('Usuario o clave incorrectos.')
                self.login.txtUsuario.setFocus()
    
    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)