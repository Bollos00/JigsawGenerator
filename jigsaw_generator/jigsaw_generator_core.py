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
Module jigsaw_generator_core.

Contains the class JigsawGeneratorCore.
"""
from enum import Enum
import numpy
import random


class JigsawGeneratorCore:
    """
    This class contains a lot of the "engine" of the `JigsawGenerator`.

    While the `JigsawGenerator` class is responsible to manage the GUI and to draw
     the jigsaw, this class deal with all the "logic" of the jigsaw, setting the design
     of each piece.

    Attributes
    ----------
    matrix: numpy.ndarray
        Two-dimensional array that contains elements of type `JigsawGeneratorCore.Cell`
         that must indicate the type of each border of each cell of the jigsaw.
    """

    class BorderType(Enum):
        """
        Enumeration that indicates the possible borders of one cell.

        `INVALID` must be an impossible state;
        `FEMININE` borders are cutted inside the piece, it creates a hold inside
         the piece, requiring its corresponding border (the same border from a
         neighbor piece) to be `MASCULINE`;
        `NEUTRAL` are entirely straight borders;
        `MASCULINE` are the exaclty opposite of the `FEMININE`, they are cutted
         outside its piece, "invading" the area of its neighbor cell. It requires
         that its corresponding border is of type `FEMININE`.
        """

        INVALID = -2
        FEMININE = -1
        NEUTRAL = 0
        MASCULINE = 1

    @staticmethod
    def inverse_border_type(border_type):
        """
        Return the inverse `JigsawGeneratorCore.BorderType`.

        Attributes
        ----------
        border_type: JigsawGeneratorCore.BorderType
            Type of the border
        """
        if border_type == JigsawGeneratorCore.BorderType.FEMININE:
            return JigsawGeneratorCore.BorderType.MASCULINE
        if border_type == JigsawGeneratorCore.BorderType.MASCULINE:
            return JigsawGeneratorCore.BorderType.FEMININE
        return border_type

    class WhichBorder(Enum):
        """
        This enumeration indicates the location of a border in a piece.
        """

        DOWN = 0
        UP = 1
        LEFT = 2
        RIGHT = 3

    class Piece:
        """
        Class that describe the design of a jigsaw piece.

        More details...

        Attributes
        ----------
        up: JigsawGeneratorCore.BorderType
        down: JigsawGeneratorCore.BorderType
        left: JigsawGeneratorCore.BorderType
        right: JigsawGeneratorCore.BorderType
        """

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
                    self.matrix[i, j] = JigsawGeneratorCore.Piece()

    def set_shape(self, shape):
        """
        Recriate the matrix with the given shape.

        Parameters
        ----------
        self: JigsawGeneratorCore
            Instance of this class.
        shape: Tuple[int, int]
            Tuple that indicates the new shaoe of the matrix.
        """
        self.matrix = numpy.ndarray(shape, dtype=numpy.object)
        self.matrix.fill(JigsawGeneratorCore.Piece())
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                self.matrix[i, j] = JigsawGeneratorCore.Piece()

    def make_borders(self):
        """
        Set all the borders of the jigsaw to `JigsawGeneratorCore.BorderType.NEUTRAL`.

        Parameters
        ----------
        self: JigsawGeneratorCore
            Instance of this class.
        """
        for i in range(self.matrix.shape[0]):
            self.matrix[i, 0].up = JigsawGeneratorCore.BorderType.NEUTRAL
            self.matrix[i, -1].down = JigsawGeneratorCore.BorderType.NEUTRAL

        for j in range(self.matrix.shape[1]):
            self.matrix[0, j].left = JigsawGeneratorCore.BorderType.NEUTRAL
            self.matrix[-1, j].right = JigsawGeneratorCore.BorderType.NEUTRAL

    def generate_random(self):
        """
        Generate the jigsaw with random state.

        Initially ot call `make_borders()`, then it attributtes a random type for all
         border of all pieces on the jigsaw.

        Parameters
        ----------
        self: JigsawGeneratorCore
            Instance of this class.
        """
        self.make_borders()

        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.matrix[i, j].up == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].up = random.choice(
                        [JigsawGeneratorCore.BorderType.MASCULINE, JigsawGeneratorCore.BorderType.FEMININE]
                    )
                    # Feminine or Masculine
                    self.matrix[i, j - 1].down = self.inverse_border_type(self.matrix[i, j].up)

                if self.matrix[i, j].down == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].down = random.choice(
                        [JigsawGeneratorCore.BorderType.MASCULINE, JigsawGeneratorCore.BorderType.FEMININE]
                    )
                    self.matrix[i, j + 1].up = self.inverse_border_type(self.matrix[i, j].down)

                if self.matrix[i, j].left == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].left = random.choice(
                        [JigsawGeneratorCore.BorderType.MASCULINE, JigsawGeneratorCore.BorderType.FEMININE]
                    )
                    self.matrix[i - 1, j].right = self.inverse_border_type(self.matrix[i, j].left)

                if self.matrix[i, j].right == JigsawGeneratorCore.BorderType.INVALID:
                    self.matrix[i, j].right = random.choice(
                        [JigsawGeneratorCore.BorderType.MASCULINE, JigsawGeneratorCore.BorderType.FEMININE]
                    )
                    self.matrix[i + 1, j].left = self.inverse_border_type(self.matrix[i, j].right)

    def get_cell(self, cell_coordinates):
        """
        Return the matrix element from the given coordinates.

        Parameters
        ----------
        self: JigsawGeneratorCore
            Instance of this class.
        shape: Tuple[int, int]
            Tuple that indicates the coordinates.
        """
        return self.matrix[cell_coordinates[0], cell_coordinates[1]]
