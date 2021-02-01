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
Auxiliar module that implements a simple algorithm that assists on the creation of smoothed paths.
"""
import numpy

from PySide2.QtCore import QPointF
from PySide2.QtGui import QPainterPath

# Source:
# https://stackoverflow.com/questions/40764011/how-to-draw-a-smooth-curved-line-that-goes-through-several-points-in-qt


def distance(pt1, pt2):
    """
    Return the distance between the two points.

    Parameters
    ----------
    pt1: QPointF
    pt2: QPointF
    """
    hd = (pt1.x() - pt2.x()) * (pt1.x() - pt2.x())
    vd = (pt1.y() - pt2.y()) * (pt1.y() - pt2.y())
    return numpy.sqrt(hd + vd)


def get_line_start(pt1, pt2):
    """
    Return the begin of the line.

    Parameters
    ----------
    pt1: QPointF
    pt2: QPointF
    """
    pt = QPointF()
    d = distance(pt1, pt2)

    rat = .5 if (d == 0) else 10.0 / d

    if rat > 0.5:
        rat = 0.5

    pt.setX((1.0 - rat) * pt1.x() + rat * pt2.x())
    pt.setY((1.0 - rat) * pt1.y() + rat * pt2.y())
    return pt


def get_line_end(pt1, pt2):
    """
    Return the end of the line.

    Parameters
    ----------
    pt1: QPointF
    pt2: QPointF
    """
    pt = QPointF()
    d = distance(pt1, pt2)

    rat = .5 if (d == 0) else 10.0 / d

    if rat > .5:
        rat = .5

    pt.setX(rat * pt1.x() + (1.0 - rat)*pt2.x())
    pt.setY(rat * pt1.y() + (1.0 - rat)*pt2.y())
    return pt


def smoothed_path(factor, points_input, path):
    """
    Return the smoothed `QPainterPath` `path` of the points of `ponts_input`.

    Example:
    ```
    from smoothed_path import smoothed_path
    from PySide2.QtCore import QPointF
    from PySide2.QtGui import QPainterPath

    A0 = QPointF(x0, y0)
    A1 = QPointF(x1, y1)
    A2 = QPointF(x2, y2)
    ...
    An = QPointF(xn, yn)

    # Create the path with its initial point
    path = QPainterPath(A0)

    path = smoothed_path(.1, [A0, A1, A2, ...], path)
    ```

    Parameters
    ----------
    factor: float
        Smooth factor.

    points_input: List[QPointF]
        Points of the path.

    path: QPainterPath
        Path on its initial point
    """
    points = list()
    count = len(points_input)

    for i, p in enumerate(points_input):
        # Except for first and last points, check what the distance between two
        # points is and if its less then min, don't add them to the list.
        if len(points) > 1 and i < count - 2 and distance(points[-1], p) < factor:
            continue

        points.append(p)

    # Don't proceed if we only have 3 or less points.
    if len(points) < 3:
        return path

    for i, p in enumerate(points):

        p1 = p if i == len(points) - 1 else points[i + 1]

        pt1 = get_line_start(p, p1)

        if i == 0:
            path.lineTo(pt1)
        else:
            path.quadTo(points[i], pt1)

        pt2 = get_line_end(points[i], p1)
        path.lineTo(pt2)

    return path
