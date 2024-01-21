from os import path
from sys import argv, exit
from PySide6.QtWidgets import QApplication

from ui.main import MainWin


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWin(path.join('ui', 'main.ui'))
    exit(app.exec())

