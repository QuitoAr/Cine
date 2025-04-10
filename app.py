import sys
import os

# Add the ui directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))

from cine import Cine

app = Cine()