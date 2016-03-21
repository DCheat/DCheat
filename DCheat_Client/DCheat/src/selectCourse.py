# -*- coding: utf-8 -*-
"""
    selectCourse.py

    Function for select test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from DCheat import config
from DCheat.src import webView

class selectCourse(QtWidgets.QDialog):
    def __init__(self, courseList, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/selectCourse.ui', self)

        self.sock = socket

        self.courseList = courseList
        self.courseList = courseList.split(',')

        for course in self.courseList:
            self.ui.listWidget.addItem(course)

        self.ui.show()

    @pyqtSlot()
    def slot_select(self):
        index = self.ui.listWidget.currentRow()
        print(index)

        # 나중에 주석 해제
        # banProgram, allowWeb = self.sock.send_selectCourse(self.courseList[index])
        # if banProgram is -1:
        #     asdf

        banProgram = [6, 9]
        allowWeb = [1, 2]

        self.ui.reject()

        webView.webView(program=banProgram, web=allowWeb, sock=self.sock)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass
