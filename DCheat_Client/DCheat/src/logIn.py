#-*- coding: utf-8 -*-
"""
    logIn.py

    Function for user login to server.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from DCheat import config
from DCheat.src import networkServer
from DCheat.src import selectCourse
from DCheat.src import adminSelectCourse

class logIn(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/login.ui', self)

        self.ui.lineEdit_2.setEchoMode(2)
        QtWidgets.QWidget.setTabOrder(self.ui.lineEdit, self.ui.lineEdit_2)

        self.sock = networkServer.networkServer()

        self.ui.show()

    @pyqtSlot()
    def slot_login(self):
        userID =  self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        try:
            courses = self.sock.send_login_message(userID, password)
        except Exception as e:
            print(e)

        if courses is 0:
            pass

        elif len(password) is 0:
            self.ui.reject()
            course = selectCourse.selectCourse(courses, self.sock)

        else:
            self.ui.reject()
            course = adminSelectCourse.adminSelectCourse(courses, self.sock)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass

        if QKeyEvent.key() == Qt.Key_Enter or QKeyEvent.key() == Qt.Key_Return:
            self.slot_login()