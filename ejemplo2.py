from PyQt5.QtWidgets import QCommandLinkButton, QApplication, QVBoxLayout, QWidget

def on_button_clicked():
    print("Botón clickeado!")

app = QApplication([])

# Crear un QCommandLinkButton
button = QCommandLinkButton("Mi botón")
button.clicked.connect(on_button_clicked)

# Crear un QWidget y un layout para mostrar el botón
widget = QWidget()
layout = QVBoxLayout(widget)
layout.addWidget(button)

widget.show()

app.exec_()