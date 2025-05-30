# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Cine\gui\ventana_buscar.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ventana_busqueda(object):
    def setupUi(self, ventana_busqueda):
        ventana_busqueda.setObjectName("ventana_busqueda")
        ventana_busqueda.resize(669, 430)
        ventana_busqueda.setMaximumSize(QtCore.QSize(16777214, 16777215))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Book")
        font.setPointSize(10)
        font.setKerning(False)
        ventana_busqueda.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Cine\\gui\\../film.ico"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        ventana_busqueda.setWindowIcon(icon)
        ventana_busqueda.setAutoFillBackground(False)
        ventana_busqueda.setStyleSheet("border: 50px;\n"
"border-radius: 20 px;\n"
"border-color: rgb(48, 45, 44);\n"
"background-color: rgb(85, 255, 127);\n"
"background-color: rgb(0, 85, 0);")
        self.tblResultados = QtWidgets.QTableWidget(ventana_busqueda)
        self.tblResultados.setGeometry(QtCore.QRect(10, 50, 651, 371))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Book")
        font.setPointSize(10)
        self.tblResultados.setFont(font)
        self.tblResultados.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tblResultados.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tblResultados.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblResultados.setGridStyle(QtCore.Qt.NoPen)
        self.tblResultados.setObjectName("tblResultados")
        self.tblResultados.setColumnCount(0)
        self.tblResultados.setRowCount(0)
        self.layoutWidget = QtWidgets.QWidget(ventana_busqueda)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 631, 37))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(26)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtBuscar = QtWidgets.QLineEdit(self.layoutWidget)
        self.txtBuscar.setBaseSize(QtCore.QSize(1, 9))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Book")
        font.setPointSize(11)
        self.txtBuscar.setFont(font)
        self.txtBuscar.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.txtBuscar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtBuscar.setCursorPosition(0)
        self.txtBuscar.setAlignment(QtCore.Qt.AlignCenter)
        self.txtBuscar.setObjectName("txtBuscar")
        self.horizontalLayout.addWidget(self.txtBuscar)
        self.checkVisto = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkVisto.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        self.checkVisto.setFont(font)
        self.checkVisto.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkVisto.setStyleSheet("color: rgb(255, 255, 255);")
        self.checkVisto.setObjectName("checkVisto")
        self.horizontalLayout.addWidget(self.checkVisto)
        self.layoutWidget.raise_()
        self.tblResultados.raise_()

        self.retranslateUi(ventana_busqueda)
        QtCore.QMetaObject.connectSlotsByName(ventana_busqueda)

    def retranslateUi(self, ventana_busqueda):
        _translate = QtCore.QCoreApplication.translate
        ventana_busqueda.setWindowTitle(_translate("ventana_busqueda", "BÚSQUEDA DE FILMS"))
        self.txtBuscar.setPlaceholderText(_translate("ventana_busqueda", "Ingresar nombre del film"))
        self.checkVisto.setText(_translate("ventana_busqueda", "SIN VER"))
