# utiles.py
import sys
import os

def recurso_relativo(ruta_relativa):
    """Devuelve la ruta absoluta al recurso, considerando si está empaquetado."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

