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

"""
Module jigsaw_generator.

Contains the class JigsawGenerator.
"""
import os
import random

from PySide2.QtWidgets import QMainWindow, QFileDialog, QInputDialog
from PySide2.QtWidgets import QColorDialog, QApplication, QStyleFactory
from PySide2.QtWidgets import QShortcut
from PySide2.QtGui import QPixmap, QPainter, QPainterPath,  QColor, QPalette
from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Qt, QPointF, QSize, QRect
from PySide2.QtSvg import QSvgGenerator

from ui_jigsaw_generator_main_window import Ui_JigsawGenerator
from jigsaw_generator_core import JigsawGeneratorCore
from smoothed_path import smoothed_path

class JigsawGenerator(QMainWindow):
    """
    Summary.

    More details

    Attributes
    ----------
    ui: Ui_JigsawGenerator
        Instance of the class Ui_JigsawGenerator.

    x: int
        Number of rows of the Jigsaw.
        Input from ui.spinBoxX.value()

    y: int
        Number of rows of the Jigsaw.
        Input from ui.spinBoxY.value()

    core: JigsawGeneratorCore
        Instance of the JigsawGeneratorCore class.

    pen_color: QColor
        Color of the pen used to draw the image and the SVG

    image_path: str
        Absolute path to the image where the jigsaw will be built upon.

    cell_width: float
        Float variable that indicates the width of each cell of the jigsaw on the image.

    cell_height: float
        Float variable that indicates the height of each cell of the jigsaw on the image.
    """

    @staticmethod
    def draw_borders(width: int, height: int, painter: QPainter):
        """
        Draw a rectangular using the given painter with the dimensions passed as arguments.

        When drawing on a QPixmap, pass the dimensions with one decreasing
         one unit, for example:
        ```
        JigsawGenerator.draw_borders(w-1, h-1, painter)
        ```

        Parameters
        ----------
        width: int
            The width of the draw.

        height: int
            The height of the draw

        painter: QPainter
            Element of the QPainter class used to paint the borders.
        """
        painter.drawLine(0, 0, 0, height)
        painter.drawLine(0, 0, width, 0)
        painter.drawLine(0, height, width, height)
        painter.drawLine(width, 0, width, height)
        return painter

    @staticmethod
    def paint_masculine_border(
        cell_coordinates, where, cell_width, cell_height, patterns, painter, smooth_factor
    ):
        """
        Draw the masculine border of one cell.

        Parameters
        ----------
        cell_coordinates: List[int]
            Coordinates [x, y] of the cell.

        where: JigsawGeneratorCore.WhichBorder
            Indicates which border will be painted.

        cell_width: float
            Indicates the width of each cell.

        cell_height: float
            Indicates the height of each cell.

        patterns: List[str]
            The patterns considered to paint the border.
            Supported "Triangle" and "Square"

        painter: QPainter
            The QPainter element used to paint the borders

        smooth_factor: float
        """

        pattern = random.choice(patterns)

        if "Triangle" in pattern:
            #          C  ---*
            #               / \
            #              /   \
            #             /     \
            # ___________/       \___________
            # |          |       |          |
            # A          B       D          E

            A, B, C, D, E = None, None, None, None, None

            # parameters necessary to make the borders different between
            #  each other
            b0, b1 = .3, .45
            c0, c1 = .4, .6
            c2, c3 = .15, .25
            d0, d1 = .55, .7
            x0, x1 = -.05, .05

            if where == JigsawGeneratorCore.WhichBorder.DOWN:
                y = (cell_coordinates[1] + 1)*cell_height
                x_begin = cell_coordinates[0]*cell_width
                A = QPointF(x_begin, y)
                B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y + cell_height*random.uniform(x0, x1))
                C = QPointF(x_begin + cell_width*random.uniform(c0, c1),
                            y + cell_height*random.uniform(c2, c3))
                D = QPointF(x_begin + cell_width*random.uniform(d0, d1),
                            y + cell_height*random.uniform(x0, x1))
                E = QPointF(x_begin + cell_width, y)

            elif where == JigsawGeneratorCore.WhichBorder.UP:
                y = cell_coordinates[1]*cell_height
                x_begin = cell_coordinates[0]*cell_width
                A = QPointF(x_begin, y)
                B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y + cell_height*random.uniform(x0, x1))
                C = QPointF(x_begin + cell_width*random.uniform(c0, c1),
                            y - cell_height*random.uniform(c2, c3))
                D = QPointF(x_begin + cell_width*random.uniform(d0, d1),
                            y + cell_height*random.uniform(x0, x1))
                E = QPointF(x_begin + cell_width, y)

            elif where == JigsawGeneratorCore.WhichBorder.LEFT:
                x = cell_coordinates[0]*cell_width
                y_begin = cell_coordinates[1]*cell_height
                A = QPointF(x, y_begin)
                B = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(b0, b1))
                C = QPointF(x - cell_width*random.uniform(c2, c3),
                            y_begin + cell_height*random.uniform(c0, c1))
                D = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(d0, d1))
                E = QPointF(x, y_begin + cell_height)

            elif where == JigsawGeneratorCore.WhichBorder.RIGHT:
                x = (cell_coordinates[0] + 1)*cell_width
                y_begin = cell_coordinates[1]*cell_height
                A = QPointF(x, y_begin)
                B = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(b0, b1))
                C = QPointF(x + cell_width*random.uniform(c2, c3),
                            y_begin + cell_height*random.uniform(c0, c1))
                D = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(d0, d1))
                E = QPointF(x, y_begin + cell_height)

            path = QPainterPath(A)

            if "Rounded" in pattern:
                smoothed_path(smooth_factor, [A, B, C, D, E], path)
            else:
                path.lineTo(B)
                path.lineTo(C)
                path.lineTo(D)
                path.lineTo(E)

            painter.drawPath(path)

        elif "Square" in pattern:
            #         C * ________ * D
            #            |       |
            #            |       |
            #            |       |
            # ___________|       |___________
            # |          |       |          |
            # A          B       E          F

            A, B, C, D, E, F = None, None, None, None, None, None

            # parameters necessary to make the borders different between
            #  each other
            b0, b1 = .3, .45
            c0, c1 = .15, .25
            e0, e1 = .55, .7
            x0, x1 = -.05, .05

            if where == JigsawGeneratorCore.WhichBorder.DOWN:
                y = (cell_coordinates[1] + 1)*cell_height
                x_begin = cell_coordinates[0]*cell_width
                A = QPointF(x_begin, y)
                B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y + cell_height*random.uniform(x0, x1))
                C = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y + cell_height*random.uniform(c0, c1))
                D = QPointF(x_begin + cell_width*random.uniform(e0, e1),
                            y + cell_height*random.uniform(c0, c1))
                E = QPointF(x_begin + cell_width*random.uniform(e0, e1),
                            y + cell_height*random.uniform(x0, x1))
                F = QPointF(x_begin + cell_width, y)

            elif where == JigsawGeneratorCore.WhichBorder.UP:
                y = cell_coordinates[1]*cell_height
                x_begin = cell_coordinates[0]*cell_width
                A = QPointF(x_begin, y)
                B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y + cell_height*random.uniform(x0, x1))
                C = QPointF(x_begin + cell_width*random.uniform(b0, b1),
                            y - cell_height*random.uniform(c0, c1))
                D = QPointF(x_begin + cell_width*random.uniform(e0, e1),
                            y - cell_height*random.uniform(c0, c1))
                E = QPointF(x_begin + cell_width*random.uniform(e0, e1),
                            y + cell_height*random.uniform(x0, x1))
                F = QPointF(x_begin + cell_width, y)

            elif where == JigsawGeneratorCore.WhichBorder.LEFT:
                x = cell_coordinates[0]*cell_width
                y_begin = cell_coordinates[1]*cell_height
                A = QPointF(x, y_begin)
                B = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(b0, b1))
                C = QPointF(x - cell_width*random.uniform(c0, c1),
                            y_begin + cell_height*random.uniform(b0, b1))
                D = QPointF(x - cell_width*random.uniform(c0, c1),
                            y_begin + cell_height*random.uniform(e0, e1))
                E = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(e0, e1))
                F = QPointF(x, y_begin + cell_height)

            elif where == JigsawGeneratorCore.WhichBorder.RIGHT:
                x = (cell_coordinates[0] + 1)*cell_width
                y_begin = cell_coordinates[1]*cell_height
                A = QPointF(x, y_begin)
                B = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(b0, b1))
                C = QPointF(x + cell_width*random.uniform(c0, c1),
                            y_begin + cell_height*random.uniform(b0, b1))
                D = QPointF(x + cell_width*random.uniform(c0, c1),
                            y_begin + cell_height*random.uniform(e0, e1))
                E = QPointF(x + cell_width*random.uniform(x0, x1),
                            y_begin + cell_height*random.uniform(e0, e1))
                F = QPointF(x, y_begin + cell_height)

            path = QPainterPath(A)

            if "Rounded" in pattern:
                smoothed_path(smooth_factor, [A, B, C, D, E, F], path)
            else:
                path.lineTo(B)
                path.lineTo(C)
                path.lineTo(D)
                path.lineTo(E)
                path.lineTo(F)

            painter.drawPath(path)

        # elif "Circle" in pattern:
        #     A, B, C, D, E, F = None, None, None, None, None, None
        #
        #     # parameters necessary to make the borders different between
        #     #  each other
        #     b0, b1 = .3, .45
        #     c0, c1 = .15, .25
        #     e0, e1 = .55, .7
        #     x0, x1 = -.05, .05
        #     r0, r1 = (e1 - b0)/2, .5/2
        #
        #     if where == JigsawGeneratorCore.WhichBorder.DOWN:
        #         y = (cell_coordinates[1] + 1)*cell_height
        #         x_begin = cell_coordinates[0]*cell_width
        #         A = QPointF(x_begin, y)
        #         B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
        #                     y + cell_height*random.uniform(x0, x1))
        #         C = QPointF(x_begin + cell_width*random.uniform(b0, b1),
        #                     y + cell_height*random.uniform(c0, c1))
        #         D = QPointF(x_begin + cell_width*random.uniform(e0, e1),
        #                     y + cell_height*random.uniform(c0, c1))
        #         E = QPointF(x_begin + cell_width*random.uniform(e0, e1),
        #                     y + cell_height*random.uniform(x0, x1))
        #         F = QPointF(x_begin + cell_width, y)
        #
        #     elif where == JigsawGeneratorCore.WhichBorder.UP:
        #         y = cell_coordinates[1]*cell_height
        #         x_begin = cell_coordinates[0]*cell_width
        #         A = QPointF(x_begin, y)
        #         B = QPointF(x_begin + cell_width*random.uniform(b0, b1),
        #                     y + cell_height*random.uniform(x0, x1))
        #         C = QPointF(x_begin + cell_width*random.uniform(b0, b1),
        #                     y - cell_height*random.uniform(c0, c1))
        #         D = QPointF(x_begin + cell_width*random.uniform(e0, e1),
        #                     y - cell_height*random.uniform(c0, c1))
        #         E = QPointF(x_begin + cell_width*random.uniform(e0, e1),
        #                     y + cell_height*random.uniform(x0, x1))
        #         F = QPointF(x_begin + cell_width, y)
        #
        #     elif where == JigsawGeneratorCore.WhichBorder.LEFT:
        #         x = cell_coordinates[0]*cell_width
        #         y_begin = cell_coordinates[1]*cell_height
        #         A = QPointF(x, y_begin)
        #         B = QPointF(x + cell_width*random.uniform(x0, x1),
        #                     y_begin + cell_height*random.uniform(b0, b1))
        #         C = QPointF(x - cell_width*random.uniform(c0, c1),
        #                     y_begin + cell_height*random.uniform(b0, b1))
        #         D = QPointF(x - cell_width*random.uniform(c0, c1),
        #                     y_begin + cell_height*random.uniform(e0, e1))
        #         E = QPointF(x + cell_width*random.uniform(x0, x1),
        #                     y_begin + cell_height*random.uniform(e0, e1))
        #         F = QPointF(x, y_begin + cell_height)
        #
        #     elif where == JigsawGeneratorCore.WhichBorder.RIGHT:
        #         x = (cell_coordinates[0] + 1)*cell_width
        #         y_begin = cell_coordinates[1]*cell_height
        #         A = QPointF(x, y_begin)
        #         B = QPointF(x + cell_width*random.uniform(x0, x1),
        #                     y_begin + cell_height*random.uniform(b0, b1))
        #         C = QPointF(x + cell_width*random.uniform(c0, c1),
        #                     y_begin + cell_height*random.uniform(b0, b1))
        #         D = QPointF(x + cell_width*random.uniform(c0, c1),
        #                     y_begin + cell_height*random.uniform(e0, e1))
        #         E = QPointF(x + cell_width*random.uniform(x0, x1),
        #                     y_begin + cell_height*random.uniform(e0, e1))
        #         F = QPointF(x, y_begin + cell_height)
        #
        #     path = QPainterPath(A)
        #     path.lineTo(B)
        #     path.lineTo(C)
        #     # Connect point `C` with point `D` with an arc that has radius between
        #     #  `r0` and `r1`
        #     center = QPointF((C + D)/2)
        #     radiusX = random.uniform(r0, r1)*cell_width
        #     radiusY = random.uniform(r0, r1)*cell_height
        #     rec = QRectF(center.x() - radiusX, center.y() - radiusY, 2*radiusX, 2*radiusY)
        #
        #     path.arcTo(rec, 60, 240)
        #
        #     path.lineTo(E)
        #     path.lineTo(F)
        #     painter.drawPath(path)

        return painter

    def draw_on_pixmap(self):
        """
        Draw the jigsaw on the pixmap located on `image_path`.

        The pixmap which the jigsaw will be drawn upon uses a QPen of the color
         `pen_color`, with number of rows `x` and number of lines `y`. The output
          is saved on the label `ui.labelImage` when the process is finished.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the own class.
        """
        self.load_image(self.image_path)
        pixmap = self.ui.labelImage.pixmap()
        painter = QPainter(pixmap)
        painter.setPen(self.pen_color)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        JigsawGenerator.draw_borders(pixmap.width() - 1, pixmap.height() - 1, painter)

        patterns = list()

        if self.ui.checkBoxTriangleBorders.isChecked():
            patterns.append("Triangle")
        if self.ui.checkBoxTriangleRounded.isChecked():
            patterns.append("Triangle Rounded")
        if self.ui.checkBoxSquaredBorders.isChecked():
            patterns.append("Square")
        if self.ui.checkBoxSquaredRounded.isChecked():
            patterns.append("Square Rounded")

        if not list:
            print("Select at least one border pattern")
            painter.end()
            self.ui.labelImage.setPixmap(pixmap)
            return

        rounded_factor = self.ui.doubleSpinBoxSmoothFactor.value()

        for i in range(self.x):
            for j in range(self.y):
                cell = self.core.get_cell([i, j])

                if cell.up == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.UP,
                        self.cell_width, self.cell_height, patterns, painter, rounded_factor
                    )
                if cell.down == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.DOWN,
                        self.cell_width, self.cell_height, patterns, painter, rounded_factor
                    )
                if cell.left == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.LEFT,
                        self.cell_width, self.cell_height, patterns, painter, rounded_factor
                    )
                if cell.right == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.RIGHT,
                        self.cell_width, self.cell_height, patterns, painter, rounded_factor
                    )

        painter.end()
        self.ui.labelImage.setPixmap(pixmap)

    def draw_on_svg(self, width, height):
        """
        Generate a SVG jigsaw of the given width and height.

        The SVG which the jigsaw will be drawn upon uses a QPen of the color
         `pen_color`, with number of rows `x` and number of lines `y`.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the own class.

        width: int
            Width of the SVG.

        height: int
            Hieght of the SVG.
        """
        filename, filters = QFileDialog.getSaveFileName(
            parent=self, caption="Save Image", filter="SVG (*.svg)",
            selected_filter="output.svg"
        )

        generator = QSvgGenerator()
        generator.setFileName(filename)
        generator.setSize(QSize(width, height))
        generator.setViewBox(QRect(0, 0, width, height))

        painter = QPainter(generator)
        painter.setPen(self.pen_color)
        painter.setRenderHint(QPainter.Antialiasing, True)

        JigsawGenerator.draw_borders(width, height, painter)

        patterns = list()

        if self.ui.checkBoxTriangleBorders.isChecked():
            patterns.append("Triangle")
        if self.ui.checkBoxTriangleRounded.isChecked():
            patterns.append("Triangle Rounded")
        if self.ui.checkBoxSquaredBorders.isChecked():
            patterns.append("Square")
        if self.ui.checkBoxSquaredRounded.isChecked():
            patterns.append("Square Rounded")

        if not list:
            print("Select at least one border pattern")
            return

        rounded_factor = self.ui.doubleSpinBoxSmoothFactor.value()

        cell_width = float(width)/self.x
        cell_height = float(height)/self.y

        for i in range(self.x):
            for j in range(self.y):
                cell = self.core.get_cell([i, j])

                if cell.up == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.UP,
                        cell_width, cell_height, patterns, painter, rounded_factor
                    )
                if cell.down == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.DOWN,
                        cell_width, cell_height, patterns, painter, rounded_factor
                    )
                if cell.left == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.LEFT,
                        cell_width, cell_height, patterns, painter, rounded_factor
                    )
                if cell.right == JigsawGeneratorCore.BorderType.MASCULINE:
                    JigsawGenerator.paint_masculine_border(
                        [i, j], JigsawGeneratorCore.WhichBorder.RIGHT,
                        cell_width, cell_height, patterns, painter, rounded_factor
                    )

        painter.end()

    def SLOT_generate_image(self):
        """
        Function called when `ui.pushButtonGenerateImage` is released.

        It generates the jigsaw and update the pixmap of `ui.labelImage`

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class
        """
        self.x = self.ui.spinBoxX.value()
        self.y = self.ui.spinBoxY.value()
        self.core.set_shape([self.x, self.y])
        self.core.generate_random()
        self.draw_on_pixmap()

    def SLOT_generate_svg(self):
        """
        Function called when `ui.pushButtonGenerateSvg` is released.

        It generates the jigsaw on a SVG file and export it to the
         desired path.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class
        """
        width, ok = QInputDialog.getInt(
            self, "Width", "Set width:",
            self.ui.labelImage.pixmap().width()
        )
        height, ok = QInputDialog.getInt(
            self, "Hieght", "Set height:",
            self.ui.labelImage.pixmap().height()
        )

        self.draw_on_svg(width, height)

    def SLOT_load_image_dialog(self):
        """
        Function called when `ui.pushButtonLoadImage` is released.

        Create a `QFileDialog` and try to load a new file.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class
        """
        file_path, filter = QFileDialog.getOpenFileName(
            parent=self,
            caption="Load Image",
            filter="Images (*.png *.jpg *.jpeg *..gif *.bpm)"
        )

        if file_path:
            self.load_image(file_path)

    def SLOT_save_image_dialog(self):
        """
        Function called when `ui.pushButtonSaveImage` is released.

        Create a QFileDialog and try to save the generated pixmap
         on the selected file.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class
        """

        file_path, filter = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Image",
            filter="Images (*.png *.jpg *.jpeg *..gif *.bpm)"
        )

        if file_path:
            self.save_image(file_path)

    def SLOT_select_pen_color_dialog(self):
        """
        Function called when ui.pushButtonPenColor is released.

        Create a QColorDialog to select the color of the pen and update
         the background of `ui.pushButtonPenColor` when finished.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class
        """

        self.pen_color = QColorDialog.getColor(
            self.pen_color, self, "Select pen color"
        )
        self.ui.pushButtonPenColor.setStyleSheet(
            "QPushButton {{ background-color: {} }}".format(str(self.pen_color.name()))
        )

    def load_image(self, image_path):
        """
        Try to load the image on the given path.

        Returns `True` if succeeded.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class

        image_path: str
            Path to the file
        """

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print("It was not possible to load the file {}".format(image_path))
            return False

        self.image_path = image_path
        self.ui.labelImage.resize(pixmap.size())
        self.ui.labelImage.setPixmap(pixmap)
        self.cell_width = float(pixmap.width())/self.x
        self.cell_height = float(pixmap.height())/self.y
        return True

    def save_image(self, image_path):
        """
        Try to save the image on the given path.

        Returns `True` if succeeded.

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class

        image_path: str
            Path to the file
        """
        pixmap = self.ui.labelImage.pixmap()

        return pixmap.save(image_path)

    def set_application_theme(self, theme_name):
        """
        Set the GUI theme with the theme passed

        Parameters
        ----------
        self: JigsawGenerator
            Instance of the class

        theme_name: str
            Which theme (can be "Fusion Dark" and "Fusion Light")
        """
        if theme_name == "Fusion Dark":
            QApplication.instance().setStyle(QStyleFactory.create("Fusion"))
            darkPalette = QPalette()
            darkPalette.setColor(QPalette.BrightText,      Qt.red)
            darkPalette.setColor(QPalette.WindowText,      Qt.white)
            darkPalette.setColor(QPalette.ToolTipBase,     Qt.white)
            darkPalette.setColor(QPalette.ToolTipText,     Qt.white)
            darkPalette.setColor(QPalette.Text,            Qt.white)
            darkPalette.setColor(QPalette.ButtonText,      Qt.white)
            darkPalette.setColor(QPalette.HighlightedText, Qt.black)
            darkPalette.setColor(QPalette.Window,          QColor(53, 53, 53))
            darkPalette.setColor(QPalette.Base,            QColor(25, 25, 25))
            darkPalette.setColor(QPalette.AlternateBase,   QColor(53, 53, 53))
            darkPalette.setColor(QPalette.Button,          QColor(53, 53, 53))
            darkPalette.setColor(QPalette.Link,            QColor(42, 130, 218))
            darkPalette.setColor(QPalette.Highlight,       QColor(42, 130, 218))
            QApplication.instance().setPalette(darkPalette)

        elif theme_name == "Fusion Light":
            QApplication.instance().setStyle(QStyleFactory.create("Fusion"))
            lightPalette = QPalette()
            lightPalette.setColor(QPalette.BrightText,      Qt.cyan)
            lightPalette.setColor(QPalette.WindowText,      Qt.black)
            lightPalette.setColor(QPalette.ToolTipBase,     Qt.black)
            lightPalette.setColor(QPalette.ToolTipText,     Qt.black)
            lightPalette.setColor(QPalette.Text,            Qt.black)
            lightPalette.setColor(QPalette.ButtonText,      Qt.black)
            lightPalette.setColor(QPalette.HighlightedText, Qt.white)
            lightPalette.setColor(QPalette.Window,          QColor(202, 202, 202))
            lightPalette.setColor(QPalette.Base,            QColor(228, 228, 228))
            lightPalette.setColor(QPalette.AlternateBase,   QColor(202, 202, 202))
            lightPalette.setColor(QPalette.Button,          QColor(202, 202, 202))
            lightPalette.setColor(QPalette.Link,            QColor(213, 125, 37))
            lightPalette.setColor(QPalette.Highlight,       QColor(42, 130, 218))

            QApplication.instance().setPalette(lightPalette)

    def __init__(self):
        super(JigsawGenerator, self).__init__()

        self.ui = Ui_JigsawGenerator()
        self.ui.setupUi(self)

        self.ui.pushButtonGenerateImage.released.connect(self.SLOT_generate_image)
        self.ui.pushButtonLoadImage.released.connect(self.SLOT_load_image_dialog)
        self.ui.pushButtonSaveImage.released.connect(self.SLOT_save_image_dialog)
        self.ui.pushButtonGenerateSvg.released.connect(self.SLOT_generate_svg)
        self.ui.pushButtonPenColor.released.connect(self.SLOT_select_pen_color_dialog)

        shortcut_close = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        shortcut_close.activated.connect(self.close)

        self.x = self.ui.spinBoxX.value()
        self.y = self.ui.spinBoxY.value()
        self.core = JigsawGeneratorCore([self.x, self.y])

        self.pen_color = QColor(Qt.white)

        self.load_image(os.path.dirname(os.path.realpath(__file__)) + "/image_template.png")

        self.SLOT_generate_image()

        self.set_application_theme("Fusion Dark")
