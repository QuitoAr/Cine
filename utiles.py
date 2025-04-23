# utiles.py
import sys
import os

# Detectar si se está ejecutando desde PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def recurso_relativo(ruta_relativa):
    """
    Retorna la ruta absoluta al recurso, ya sea desde el entorno normal
    o desde el entorno empaquetado con PyInstaller.
    """
    return os.path.join(BASE_DIR, ruta_relativa)
