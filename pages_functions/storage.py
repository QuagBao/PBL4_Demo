from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QDialog
from PyQt5 import QtWidgets
from ui.pages.storage_UI import Ui_Form
from PyQt5.uic import loadUi
from information_string import information_string
import sys
import re
import ast

class Storage(QWidget):
    def __init__(self):
        super(Storage, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        information_string._instance = information_string()
        result = information_string._instance.get_storage()
        self.handle_receive_data()
        print("Đã qua storage")

    def handle_receive_data(self):
        information_string._instance = information_string()
        result = information_string._instance.get_storage()
        result_1 = ast.literal_eval(result)
        row=0
        self.ui.tableWidget_2.setRowCount(len(result_1))
        for person in result_1:
            self.ui.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(" " + (person["device"])))
            self.ui.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(" " + "{:.2f}".format(person["total"]) + " MB"))
            self.ui.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(" " + "{:.2f}".format(person["used"])+ " MB"))
            self.ui.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(" " + "{:.2f}".format(person["free"])+ " MB"))
            self.ui.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(" " + "{:.2f}".format(person["percent"])+ " %"))
            row=row+1

            
