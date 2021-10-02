import os

from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPushButton, QLineEdit, QWidget, QComboBox, QDateEdit, QTextEdit, QTableWidget,\
    QTableWidgetItem, QMessageBox
from PySide6.QtCore import QFile, QDate, Slot

from db.connect import Connect
from db.query import SitesQuery
from ui.validator import valid_year

session = Connect().get_session()
sites = SitesQuery(session)


def show_warning_dialog(info: str) -> int:
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Information)
    warning.setWindowTitle("Предупреждение")
    warning.setText(info)
    warning.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
    return_value = warning.exec()
    if return_value == warning.Yes:
        return 1
    return 0


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
        self.btn_edit = self.window.findChild(QPushButton, 'btnEdit')
        self.btn_create = self.window.findChild(QPushButton, 'btnCreate')
        self.btn_delete = self.window.findChild(QPushButton, 'btnDelete')
        self.btn_ok = self.window.findChild(QPushButton, 'btnOK')
        self.btn_cancel = self.window.findChild(QPushButton, 'btnCancel')

        self.line_list = [self.line_forestry, self.line_kvartal, self.line_vydel, self.line_clearcut,
                          self.line_planting, self.line_thinning, self.line_quantity_plots, self.line_last_tax]

        # задаём специальные размеров колонок
        self.sites_table.setColumnWidth(0, 140)
        self.sites_table.setColumnWidth(1, 80)

        # параметры
        self.sites_list: list
        self.selected_site = None
        self.init_UI()

    def init_UI(self):
        self.sites_table.itemClicked.connect(self.set_site_info)
        self.btn_delete.clicked.connect(self.delete_site)
        self.btn_create.clicked.connect(self.activate_create_form)
        self.btn_ok.clicked.connect(self.create_new_site)
        self.btn_cancel.clicked.connect(self.close_create_form)

        self.set_visible_btn_of_create_site(visible=False)
        self.update_extra_fields()
        self.update_sites_table()
        self.window.show()

    def set_visible_btn_of_create_site(self, visible: bool):
        self.btn_ok.setVisible(visible)
        self.btn_cancel.setVisible(visible)

    def set_site_info(self):
        self.set_selected_row()
        site_info = self.get_site_info()[1:]  # без ID
        self.update_site_info(site_info)

    def get_site_info(self):
        site_info = self.sites_list[self.selected_site]
        return list(map(str, site_info))

    def set_selected_row(self):
        index = sorted(self.sites_table.selectedIndexes())
        self.selected_site = int(index[0].row())

    def update_site_info(self, site_info):
        for i in range(8):
            self.line_list[i].setText(site_info[i])

    def get_info_from_site_list(self):
        result = []
        for i in range(6):
            elem = self.line_list[i].text()
            if elem:
                result.append(elem)
            else:
                result.append(0)
        return result

    @staticmethod
    def update_extra_fields():
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

    def activate_create_form(self):
        self.update_site_info([None for i in range(8)])
        self.set_visible_btn_of_create_site(visible=True)
        self.set_status_widget(disabled=True)

    def close_create_form(self):
        self.update_site_info([None for i in range(8)])
        self.set_visible_btn_of_create_site(visible=False)
        self.set_status_widget(disabled=False)

    def create_new_site(self):
        confirm = self.validator_create_form()
        if confirm:
            info = self.get_info_from_site_list()
            sites.create(forestry=info[0], kvartal=info[1], vydel=info[2],
                         clearcut=info[3], planting=info[4], thinning=info[5])
            self.update_sites_table()
            self.close_create_form()

    def validator_create_form(self):
        if self.line_forestry.text():
            if self.line_kvartal.text():
                clearcut = self.line_clearcut.text()
                if clearcut:
                    if not valid_year(clearcut):
                        return 0
            else:
                return 0
        else:
            return 0

    def valid_year_line(self, line):
        value = line.text()
        if value:
            if valid_year(value):
                return 1
        return 0





    def set_status_widget(self, disabled: bool):
        if disabled:
            self.btn_edit.setDisabled(True)
            self.btn_create.setDisabled(True)
            self.btn_delete.setDisabled(True)
            self.sites_table.setDisabled(True)
            for elem in range(6):
                self.line_list[elem].setEnabled(True)
        else:
            self.set_placeholders()
            self.btn_edit.setEnabled(True)
            self.btn_create.setEnabled(True)
            self.btn_delete.setEnabled(True)
            self.sites_table.setEnabled(True)
            for elem in range(6):
                self.line_list[elem].setDisabled(True)

    def set_placeholders(self):
        pass

    def delete_site(self):
        if self.selected_site is not None:
            id_site = self.sites_list[self.selected_site][0]
            confirm = show_warning_dialog("Вы уверенны в том что хотите удалить?")
            if confirm:
                sites.delete(id_site)
                self.update_sites_table()
                self.update_site_info([None for i in range(8)])
            self.selected_site = None

