import os

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QComboBox, QDateEdit, QTextEdit, QTableWidget
from PySide6.QtCore import QFile, QDate

from db.connect import Connect
from db.query import SitesQuery

session = Connect().get_session()
sites = SitesQuery(session)


class Start(QWidget):
    def __init__(self, uifile, parent=None):
        super(Start, self).__init__(parent)
        self.ui_file = QFile(uifile)
        self.ui_file.open(QFile.ReadOnly)
        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()

        # определим элементы управления
        self.table_bill = self.window.findChild(QTableWidget, 'tableWidget')

        # # замена имени колонки в форме
        # self.table_bill.horizontalHeaderItem(3).setText('Действие')
        #
        # # задаём специальные размеров колонок
        # self.table_bill.setColumnWidth(0, 100)  # дата
        # self.table_bill.setColumnWidth(1, 100)  # сумма
        # self.table_bill.setColumnWidth(2, 100)  # действие
        # self.table_bill.setColumnWidth(3, 240)  # комментарий
        self.id = []

        self.filling_table()
        self.window.show()

    def set_data_in_new_row(self, data: list):
        rows = self.table_bill.rowCount()
        self.table_bill.setRowCount(int(rows + 1))
        columns = self.table_bill.columnCount()
        for i in range(0, columns):
            item = QtWidgets.QTableWidgetItem(str(data[i]))
            self.table_bill.setItem(rows, i, item)

    # метод заполнения таблицы
    def filling_table(self):
        self.table_bill.setRowCount(int(0)) # удаляем строки
        items = sites.get_all()
        self.id = []
        for item in items:
            # пересохраняем объект таблицы в строчку
            row = []
            self.id.append(item.id)
            row.append(item.forestry)
            row.append(item.kvartal)
            row.append(item.vydel)
            # вставляем строчку в таблицу
            self.set_data_in_new_row(row)
