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
        self.btn_show = self.window.findChild(QPushButton, 'btnShow')
        self.btn_create = self.window.findChild(QPushButton, 'btnCreate')
        self.btn_delete = self.window.findChild(QPushButton, 'btnDelete')

        # задаём специальные размеров колонок
        self.sites_table.setColumnWidth(0, 140)
        self.sites_table.setColumnWidth(1, 80)

        # параметры
        self.sites_list: list
        self.selected_site: int
        self.initUT()

    def initUT(self):
        self.sites_table.itemClicked.connect(self.set_site_info)
        self.btn_delete.clicked.connect(self.delete_site)

        self.update_extra_fields()
        self.update_sites_table()
        self.window.show()

    def set_site_info(self):
        self.set_selected_row()
        site_info = self.get_site_info()
        self.update_site_info(site_info)

    def get_site_info(self):
        site_info = self.sites_list[self.selected_site]
        return list(map(str, site_info))

    def set_selected_row(self):
        index = sorted(self.sites_table.selectedIndexes())
        self.selected_site = int(index[0].row())

    def update_site_info(self, site_info):
        self.line_forestry.setText(site_info[1])
        self.line_kvartal.setText(site_info[2])
        self.line_vydel.setText(site_info[3])
        self.line_clearcut.setText(site_info[4])
        self.line_planting.setText(site_info[5])
        self.line_thinning.setText(site_info[6])
        self.line_quantity_plots.setText(site_info[7])
        self.line_last_tax.setText(site_info[8])

    def update_extra_fields(self):
        sites.set_last_tax()
        sites.set_quantity_plots()

    def set_sites_info(self):
        self.sites_list = sites.get_all_sites_list()

    def update_sites_table(self):
        self.set_sites_info()
        self.fill_table()

    def fill_table(self):
        self.sites_table.setRowCount(int(0))  # удаляем строки
        for item in self.sites_list:  # пересохраняем объект таблицы в строчку
            self.set_data_in_new_row(item[1:3])

    def set_data_in_new_row(self, data: list):
        rows = self.sites_table.rowCount()
        self.sites_table.setRowCount(int(rows + 1))  # добавляем новую строчку
        columns = self.sites_table.columnCount()
        for i in range(0, columns):
            item = QtWidgets.QTableWidgetItem(str(data[i]))
            self.sites_table.setItem(rows, i, item)

    def create_new_site(self):
        pass

    def delete_site(self):
        id_site = self.sites_list[self.selected_site][0]
        sites.delete(id_site)
        self.update_sites_table()
        self.update_site_info([None, None, None, None, None, None, None, None, None])
        self.selected_site = 0
