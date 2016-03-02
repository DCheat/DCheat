# -*- coding: utf-8 -*-
"""
    adminSelectCourse.py

    Admin's function for register test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import *
from DCheat import config
import csv

class registerCourse(QtWidgets.QDialog):
    def __init__(self, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/registerCourse.ui', self)
        self.sock = socket
        self.banList = []
        self.allowList = []

        for i in range(1, len(config.config.BAN_PROGRAM)):
            checkBox = QtWidgets.QCheckBox()
            checkBox.clicked.connect(self.setBanList)
            label = QtWidgets.QLabel(config.config.BAN_PROGRAM[i])
            self.ui.formLayout.addRow(checkBox, label)

        for i in range(1, len(config.config.ALLOW_SITE)):
            checkBox = QtWidgets.QCheckBox()
            checkBox.clicked.connect(self.setAllowList)
            label = QtWidgets.QLabel(config.config.ALLOW_SITE[i])
            self.ui.formLayout_2.addRow(checkBox, label)

        self.ui.show()

    @pyqtSlot()
    def search_slot(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'open file', '', 'CSV파일 (*.csv)', '*.csv')

        print(filename, _filter)
        self.ui.textEdit_2.setText(filename)

        csvFile = open(filename, 'r')
        fp = csv.reader(csvFile)
        for i in fp:
            print(i)

    @pyqtSlot()
    def register_slot(self):
        print('zxcv')

    def setBanList(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 19) + 1

        if pos in self.banList:
            self.banList.remove(pos)

        else:
            self.banList.append(pos)

        print(self.banList)

    def setAllowList(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 19) + 1

        if pos in self.allowList:
            self.allowList.remove(pos)

        else:
            self.allowList.append(pos)

        print(self.allowList)