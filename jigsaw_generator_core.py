from enum import Enum
import numpy
import random


class JigsawGeneratorCore:

    class BorderType(Enum):
        INVALID = -2
        FEMININE = -1
        NEUTRAL = 0
        MASCULINE = 1

    @staticmethod
    def inverse_border_type(border_type):
        if border_type == JigsawGeneratorCore.BorderType.FEMININE:
            return JigsawGeneratorCore.BorderType.MASCULINE
        if border_type == JigsawGeneratorCore.BorderType.MASCULINE:
            return JigsawGeneratorCore.BorderType.FEMININE
        return border_type

    class WhichBorder(Enum):
        DOWN = 0
        UP = 1
        LEFT = 2
        RIGHT = 3

    class Cell:

        def __init__(self):
            self.up = JigsawGeneratorCore.BorderType.INVALID
            self.down = JigsawGeneratorCore.BorderType.INVALID
            self.left = JigsawGeneratorCore.BorderType.INVALID
            self.right = JigsawGeneratorCore.BorderType.INVALID


    def __init__(self, shape=None):
        if shape is not None:
            self.matrix = numpy.ndarray(shape, dtype=numpy.object)
            for i in range(self.matrix.shape[0]):
                for j in range(self.matrix.shape[1]):
                    self.matrix[i, j] = JigsawGeneratorCore.Cell()

    def set_shape(self, shape):
        self.matrix = numpy.ndarray(shape, dtype=numpy.object)
        self.matrix.fill(JigsawGeneratorCore.Cell())
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                self.matrix[i, j] = JigsawGeneratorCore.Cell()

    def make_borders(self):
        for i in range(self.matrix.shape[0]):
            self.matrix[i, 0].up = JigsawGeneratorCore.BorderType.NEUTRAL
            self.matrix[i, -1].down = JigsawGeneratorCore.BorderType.NEUTRAL

        for j in range(self.matrix.shape[1]):
            self.matrix[0, j].left = JigsawGeneratorCore.BorderType.NEUTRAL
            self.matrix[-1, j].right = JigsawGeneratorCore.BorderType.NEUTRAL

    def generate_random(self):
        self.make_borders()

        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.matrix[i, j].up == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].up = random.choice([JigsawGeneratorCore.BorderType.MASCULINE,
                                                          JigsawGeneratorCore.BorderType.FEMININE])  # Feminine or Masculine
                    self.matrix[i, j - 1].down = self.inverse_border_type(self.matrix[i, j].up)

                if self.matrix[i, j].down == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].down = random.choice([JigsawGeneratorCore.BorderType.MASCULINE,
                                                            JigsawGeneratorCore.BorderType.FEMININE])
                    self.matrix[i, j + 1].up = self.inverse_border_type(self.matrix[i, j].down)

                if self.matrix[i, j].left == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].left = random.choice([JigsawGeneratorCore.BorderType.MASCULINE,
                                                            JigsawGeneratorCore.BorderType.FEMININE])
                    self.matrix[i - 1, j].right = self.inverse_border_type(self.matrix[i, j].left)

                if self.matrix[i, j].right == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].right = random.choice([JigsawGeneratorCore.BorderType.MASCULINE,
                                                             JigsawGeneratorCore.BorderType.FEMININE])
                    self.matrix[i + 1, j].left = self.inverse_border_type(self.matrix[i, j].right)

    def get_cell(self, cell_coordinates):
        return self.matrix[cell_coordinates[0], cell_coordinates[1]]
