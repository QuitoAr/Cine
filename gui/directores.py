from PyQt5 import QtWidgets, uic
import sys
import os
print(os.path.exists('gui/directores.ui'))  # debería dar True



class DirectorsWindow(QtWidgets.QMainWindow):  # ← cambio aquí
    def __init__(self, id_director):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), 'directores.ui')
        print(f"Intentando cargar UI desde: {ui_path}")
        uic.loadUi(ui_path, self)

        self.id_director = id_director
        self.labelId_Director.setText(str(self.id_director))
    
    def open_directors_window(self):
        self.directors_window = DirectorsWindow()
        self.directors_window.show()

    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = DirectorsWindow()
    main_window.show()
    sys.exit(app.exec_())