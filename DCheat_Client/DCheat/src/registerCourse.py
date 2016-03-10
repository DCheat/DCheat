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
import datetime
import csv

class registerCourse(QtWidgets.QDialog):
    def __init__(self, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/registerCourse.ui', self)
        self.sock = socket
        self.banList = []
        self.allowList = []
        self.students = []

        pListWidget = QtWidgets.QWidget()
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setWidget(pListWidget)
        pListLayout = QtWidgets.QVBoxLayout()
        pListLayout.setAlignment(Qt.AlignTop)
        pListWidget.setLayout(pListLayout)

        for i in range(1, len(config.config.BAN_PROGRAM)):
            checkBox = QtWidgets.QCheckBox(config.config.BAN_PROGRAM[i])
            checkBox.clicked.connect(self.set_ban_list)
            pListLayout.addWidget(checkBox)

        sListWidget = QtWidgets.QWidget()
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setWidget(sListWidget)
        sListLayout = QtWidgets.QVBoxLayout()
        sListLayout.setAlignment(Qt.AlignTop)
        sListWidget.setLayout(sListLayout)

        for i in range(1, len(config.config.ALLOW_SITE)):
            checkBox = QtWidgets.QCheckBox(config.config.ALLOW_SITE[i])
            checkBox.clicked.connect(self.set_allow_list)
            sListLayout.addWidget(checkBox)

        self.ui.show()

    @pyqtSlot()
    def search_slot(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'open file', '/', 'CSV파일 (*.csv)', '*.csv')

        print(filename, _filter)
        self.ui.textEdit_2.setText(filename)

        csvFile = open(filename, 'r')
        self.students = csv.reader(csvFile)

    @pyqtSlot()
    def register_slot(self):
        self.banList.sort()
        self.allowList.sort()

        date = str(datetime.date(self.ui.dateEdit.date().year(), self.ui.dateEdit.date().month(), self.ui.dateEdit.date().day()))
        startTime = str(datetime.time(self.timeEdit.time().hour(), self.timeEdit.time().minute()))
        endTime = str(datetime.time(self.timeEdit_2.time().hour(), self.timeEdit_2.time().minute()))

        courseDate = '{} {},{} {}'.format(date, startTime, date, endTime)

        print(courseDate)

        self.sock.make_course(self.ui.lineEdit.text(), courseDate, self.banList, self.allowList, self.students)

    def set_ban_list(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 19) + 1

        if pos in self.banList:
            self.banList.remove(pos)

        else:
            self.banList.append(pos)

        print(self.banList)

    def set_allow_list(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 19) + 1

        if pos in self.allowList:
            self.allowList.remove(pos)

        else:
            self.allowList.append(pos)

        print(self.allowList, self.ui.lineEdit.text())