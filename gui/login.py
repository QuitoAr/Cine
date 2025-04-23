from PyQt5 import uic
from PyQt5.QtWidgets import QDialog  # Importar QDialog en lugar de QWidget
from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario
from utiles import recurso_relativo


class Login(QDialog):  # Cambié QWidget por QDialog
    def __init__(self):
        super().__init__()
        ui_path = recurso_relativo('gui/login.ui')
        self.login = uic.loadUi(ui_path, self)  # Carga el archivo .ui en la instancia de Login        
        self.initGUI()
        self.login.lblMensaje.setText('')
        self.show()

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
