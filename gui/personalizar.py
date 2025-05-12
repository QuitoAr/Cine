# personalizar.py
from PyQt5.QtWidgets import QLineEdit

class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selectAll()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.hasSelectedText():
            self.selectAll()

