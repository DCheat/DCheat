# -*- coding: utf-8 -*-
"""
    selectCourse.py

    Function for select test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat import config
from DCheat.src import networkServer

class selectCourse(QtWidgets.QDialog):
    def __init__(self, courseList, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'/view/selectCourse.ui', self)

        self.courseList = courseList
        self.courseList = courseList.split(',')

        for course in self.courseList:
            self.ui.listWidget.addItem(course)

        self.ui.show()

    @pyqtSlot()
    def slot_select(self):
        a = self.ui.listWidget.currentRow()
        print(a, self.courseList[a])