import os

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QComboBox, QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QFile, QDate, Slot

from db.connect import Connect
from db.query import SitesQuery

session = Connect().get_session()
sites = SitesQuery(session)


class MainWin(QWidget):
    def __init__(self, uifile, parent=None):
        super(MainWin, self).__init__(parent)
        self.ui_file = QFile(uifile)
        self.ui_file.open(QFile.ReadOnly)
        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui_file)
        self.ui_file.close()

        # определим элементы управления
        self.sites_table = self.window.findChild(QTableWidget, 'sitesTable')
        self.line_forestry = self.window.findChild(QLineEdit, 'lineForestry')
        self.line_kvartal = self.window.findChild(QLineEdit, 'lineKvartal')
        self.line_vydel = self.window.findChild(QLineEdit, 'lineVydel')
        self.line_clearcut = self.window.findChild(QLineEdit, 'lineClearcut')
        self.line_planting = self.window.findChild(QLineEdit, 'linePlanting')
        self.line_thinning = self.window.findChild(QLineEdit, 'lineThinning')
        self.line_quantity_plots = self.window.findChild(QLineEdit, 'lineQuantityPlots')
        self.line_last_tax = self.window.findChild(QLineEdit, 'lineLastTax')

        # задаём специальные размеров колонок
        self.sites_table.setColumnWidth(0, 140)
        self.sites_table.setColumnWidth(1, 80)

        # параметры
        self.sites_list = []
        self.initUT()

    def initUT(self):
        self.sites_table.itemClicked.connect(self.set_site_info)
        self.update_extra_fields()
        self.get_sites_info()
        self.fill_table()
        self.window.show()

    def set_site_info(self):
        result = self.get_selected_row()
        self.update_site_info(result)

    def get_selected_row(self):
        index = sorted(self.sites_table.selectedIndexes())
        result = int(index[0].row())
        site_info = self.sites_list[result]
        return site_info

    def update_site_info(self, site_info):
        site_info = list(map(str, site_info))
        self.line_forestry.setText(site_info[0])
        self.line_kvartal.setText(site_info[1])
        self.line_vydel.setText(site_info[2])
        self.line_clearcut.setText(site_info[3])
        self.line_planting.setText(site_info[4])
        self.line_thinning.setText(site_info[5])
        self.line_quantity_plots.setText(site_info[6])
        self.line_last_tax.setText(site_info[7])

    def update_extra_fields(self):
        sites.set_last_tax()
        sites.set_quantity_plots()

    def get_sites_info(self):
        self.sites_list = sites.get_all_sites_list()

    def fill_table(self):
        self.sites_table.setRowCount(int(0))  # удаляем строки
        for item in self.sites_list:  # пересохраняем объект таблицы в строчку
            self.set_data_in_new_row(item[:2])

    def set_data_in_new_row(self, data: list):
        rows = self.sites_table.rowCount()
        self.sites_table.setRowCount(int(rows + 1))  # добавляем новую строчку
        columns = self.sites_table.columnCount()
        for i in range(0, columns):
            item = QtWidgets.QTableWidgetItem(str(data[i]))
            self.sites_table.setItem(rows, i, item)
