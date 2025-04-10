from PyQt5.QtWidgets import QApplication
from gui.login import Login
import sys
import os
from gui import login
sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))


class Cine():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login = Login()
        
        self.app.exec_()

    if __name__ == "__main__":

        app = QApplication(sys.argv)
        login = Login()
        login.show()
        sys.exit(app.exec_())
