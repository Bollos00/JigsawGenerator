# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtCore import Qt, QPointF

from ui_jigsaw_generator_main_window import Ui_JigsawGenerator
from jigsaw_generator_core import JigsawGeneratorCore


class JigsawGenerator(QMainWindow):

    def draw_borders(self, width, height, painter, pixmap):
        painter.drawLine(0, 0, 0, height - 1)
        painter.drawLine(0, 0, width - 1, 0)
        painter.drawLine(0, height - 1, width - 1, height - 1)
        painter.drawLine(width - 1, 0, width - 1, height - 1)
        return painter, pixmap

    def paint_neutral(self, cell_coordinates, where, painter, pixmap):
        begin, end = None, None

        if where == JigsawGeneratorCore.WhichBorder.DOWN:
            y = int((cell_coordinates[1] + 1)*self.cell_height)
            x_begin = int(cell_coordinates[0]*self.cell_width)
            x_end = int((cell_coordinates[0] + 1)*self.cell_width)
            begin, end = [x_begin, y], [x_end, y]

        elif where == JigsawGeneratorCore.WhichBorder.UP:
            y = int(cell_coordinates[1]*self.cell_height)
            x_begin = int(cell_coordinates[0]*self.cell_width)
            x_end = int((cell_coordinates[0] + 1)*self.cell_width)
            begin, end = [x_begin, y], [x_end, y]

        elif where == JigsawGeneratorCore.WhichBorder.LEFT:
            x = int(cell_coordinates[0]*self.cell_width)
            y_begin = int(cell_coordinates[1]*self.cell_height)
            y_end = int((cell_coordinates[1] + 1)*self.cell_height)
            begin, end = [x, y_begin], [x, y_end]

        elif where == JigsawGeneratorCore.WhichBorder.RIGHT:
            x = int((cell_coordinates[0] + 1)*self.cell_width)
            y_begin = int(cell_coordinates[1]*self.cell_height)
            y_end = int((cell_coordinates[1] + 1)*self.cell_height)
            begin, end = [x, y_begin], [x, y_end]

        painter.drawLine(begin[0], begin[1], end[0], end[1])

        return painter, pixmap

    def paint_masculine(self, cell_coordinates, where, painter, pixmap):
        A, B, C, D, E = None, None, None, None, None

        if where == JigsawGeneratorCore.WhichBorder.DOWN:
            y = (cell_coordinates[1] + 1)*self.cell_height
            x_begin = cell_coordinates[0]*self.cell_width
            A = QPointF(x_begin, y)
            B = QPointF(x_begin + self.cell_width*.4, y)
            C = QPointF(x_begin + self.cell_width*.5, y + self.cell_height*.2)
            D = QPointF(x_begin + self.cell_width*.6, y)
            E = QPointF(x_begin + self.cell_width, y)

        elif where == JigsawGeneratorCore.WhichBorder.UP:
            y = cell_coordinates[1]*self.cell_height
            x_begin = cell_coordinates[0]*self.cell_width
            A = QPointF(x_begin, y)
            B = QPointF(x_begin + self.cell_width*.4, y)
            C = QPointF(x_begin + self.cell_width*.5, y - self.cell_height*.2)
            D = QPointF(x_begin + self.cell_width*.6, y)
            E = QPointF(x_begin + self.cell_width, y)

        elif where == JigsawGeneratorCore.WhichBorder.LEFT:
            x = cell_coordinates[0]*self.cell_width
            y_begin = cell_coordinates[1]*self.cell_height
            A = QPointF(x, y_begin)
            B = QPointF(x, y_begin + self.cell_height*.4)
            C = QPointF(x - self.cell_width*.2, y_begin + self.cell_height*.5)
            D = QPointF(x, y_begin + self.cell_height*.6)
            E = QPointF(x, y_begin + self.cell_height)

        elif where == JigsawGeneratorCore.WhichBorder.RIGHT:
            x = (cell_coordinates[0] + 1)*self.cell_width
            y_begin = cell_coordinates[1]*self.cell_height
            A = QPointF(x, y_begin)
            B = QPointF(x, y_begin + self.cell_height*.4)
            C = QPointF(x + self.cell_width*.2, y_begin + self.cell_height*.5)
            D = QPointF(x, y_begin + self.cell_height*.6)
            E = QPointF(x, y_begin + self.cell_height)

        painter.drawLine(A, B)
        painter.drawLine(B, C)
        painter.drawLine(C, D)
        painter.drawLine(D, E)

        return painter, pixmap

    def draw_on_pixmap(self):
        self.load_image(self.image_path)
        pixmap = self.ui.labelImage.pixmap()
        painter = QPainter(pixmap)
        painter.setPen(Qt.white)

        self.draw_borders(pixmap.width(), pixmap.height(), painter, pixmap)

        for i in range(self.x):
            for j in range(self.y):
                cell = self.core.get_cell([i, j])

                # print('{0}, {1} : [{2}, {3}, {4}, {5}]'.format(i, j, cell.up, cell.down, cell.left, cell.right))

                if cell.up == JigsawGeneratorCore.BorderType.MASCULINE:
                    self.paint_masculine([i, j], JigsawGeneratorCore.WhichBorder.UP, painter, pixmap)
                if cell.down == JigsawGeneratorCore.BorderType.MASCULINE:
                    self.paint_masculine([i, j], JigsawGeneratorCore.WhichBorder.DOWN, painter, pixmap)
                if cell.left == JigsawGeneratorCore.BorderType.MASCULINE:
                    self.paint_masculine([i, j], JigsawGeneratorCore.WhichBorder.LEFT, painter, pixmap)
                if cell.right == JigsawGeneratorCore.BorderType.MASCULINE:
                    self.paint_masculine([i, j], JigsawGeneratorCore.WhichBorder.RIGHT, painter, pixmap)

        self.ui.labelImage.setPixmap(pixmap)

    def SLOT_generate(self):
        # print("Generate called")

        self.x = self.ui.spinBoxX.value()
        self.y = self.ui.spinBoxY.value()
        self.core.set_shape([self.x, self.y])
        self.core.generate_random()
        self.draw_on_pixmap()

    def load_image(self, image_path):
        self.image_path = image_path
        pixmap = QPixmap(self.image_path)
        self.ui.labelImage.resize(pixmap.size())
        self.ui.labelImage.setPixmap(pixmap)
        self.cell_width = float(pixmap.width())/self.x
        self.cell_height = float(pixmap.height())/self.y

    def __init__(self):
        super(JigsawGenerator, self).__init__()

        self.ui = Ui_JigsawGenerator()
        self.ui.setupUi(self)
        self.ui.pushButtonGenerate.released.connect(self.SLOT_generate)
        self.ui.spinBoxX.valueChanged.connect(self.SLOT_generate)
        self.ui.spinBoxY.valueChanged.connect(self.SLOT_generate)

        self.x = self.ui.spinBoxX.value()
        self.y = self.ui.spinBoxY.value()
        self.core = JigsawGeneratorCore([self.x, self.y])

        self.load_image(os.path.dirname(os.path.realpath(__file__)) + "/image_template.jpg")

        self.SLOT_generate()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = JigsawGenerator()

    widget.show()
    sys.exit(app.exec_())
