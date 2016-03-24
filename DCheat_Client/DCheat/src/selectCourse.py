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

        for course in self.courseList:
            self.ui.listWidget.addItem(course)

        self.ui.show()

    @pyqtSlot()
    def slot_select(self):
        index = self.ui.listWidget.currentRow()

        # 나중에 주석 해제
        banProgram, allowWeb = self.sock.send_select_course(self.courseList[index])
        if banProgram is 0:
            return

        self.ui.reject()

        webView.webView(banProgram, allowWeb, self.courseList[index], self.sock)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass
