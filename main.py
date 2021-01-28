import sys

from PySide2.QtWidgets import QApplication
from jigsaw_generator import JigsawGenerator

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = JigsawGenerator()

    widget.show()

    sys.exit(app.exec_())
