
from importlib import import_module

APP_NAME = 'jigsaw_generator'

APP_VERSION = '0.0.0'

PYSIDE_VERSION = '2'

PySide = import_module('PySide' + PYSIDE_VERSION)

# For some reason, the only way to import QtSvg is to do it
#  this way, PySide.QtSvg returns error
Widgets = import_module('PySide' + PYSIDE_VERSION + '.QtWidgets')
Core = import_module('PySide' + PYSIDE_VERSION + '.QtCore')
Gui = import_module('PySide' + PYSIDE_VERSION + '.QtGui')

Svg = import_module('PySide' + PYSIDE_VERSION + '.QtSvg')
