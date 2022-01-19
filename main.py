# Katarzyna Zaleska
# WCY19IJ1S1

import sys

from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
