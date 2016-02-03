# -*- coding: utf-8 -*-
"""
    adminSelectCourse.py

    Admin's function for select test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat import config

class adminSelectCourse(QtWidgets.QDialog):
    def __init__(self, courseList, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/adminSelectCourse.ui', self)

        self.sock = socket
        self.courseList = courseList
        self.courseList = courseList.split(',')

        i = 0
        for course in self.courseList:
            courseLabel = QtWidgets.QLabel(course)
            startLabel = QtWidgets.QLabel('0000-00-00 00:00:00')
            endLabel = QtWidgets.QLabel('0000-00-00 00:00:00')
            countLabel = QtWidgets.QLabel(str(250))

            courseLabel.setAlignment(Qt.AlignHCenter)
            startLabel.setAlignment(Qt.AlignHCenter)
            endLabel.setAlignment(Qt.AlignHCenter)
            countLabel.setAlignment(Qt.AlignHCenter)

            button = QtWidgets.QPushButton("수정")
            button.clicked.connect(lambda: self.modify_test())

            self.ui.gridLayout.addWidget(courseLabel, i, 0)
            self.ui.gridLayout.addWidget(startLabel, i, 1)
            self.ui.gridLayout.addWidget(endLabel, i, 2)
            self.ui.gridLayout.addWidget(countLabel, i, 3)
            self.ui.gridLayout.addWidget(button, i, 4)
            i+=1

        self.ui.show()

    @pyqtSlot()
    def insert_test(self):
        print('asdfasdf')

    def modify_test(self):
        print('sadf')