############################################################################
# JigsawGenerator                                                          #
# Copyright (C) 2021  Bruno Bollos Correa                                  #
#                                                                          #
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU General Public License as published by     #
# the Free Software Foundation, either version 3 of the License, or        #
# (at your option) any later version.                                      #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU General Public License for more details.                             #
#                                                                          #
# You should have received a copy of the GNU General Public License        #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

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
