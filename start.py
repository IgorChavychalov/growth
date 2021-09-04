import os

import PySide6

import db.connect
# from db.model import Site

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

conn = db.connect.Connect().get_session()

from ui.main import Start

if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication(sys.argv)
    mainwindow = Start(os.path.join('ui', 'form.ui'))
    sys.exit(app.exec_())
