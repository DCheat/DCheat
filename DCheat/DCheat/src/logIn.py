#-*- coding: utf-8 -*-
"""
    logIn.py

    Function for user login to server.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat import config
from DCheat.src import networkServer
from DCheat.src import selectCourse
from DCheat.src import adminSelectCourse

class logIn(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/login.ui', self)
        self.ui.show()

        self.sock = object

    @pyqtSlot()
    def slot_login(self):
        userID =  self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        # 나중에 주석 해제
        # loginMessage = 'LUSER:{0}^{1}'.format(userID, password)
        # self.sock = networkServer.networkServer()
        # courses = self.sock.send_login_message(loginMessage)

        courses = '1,2,3,4,5'

        if courses is -1:
            pass

        elif courses:
            self.ui.reject()
            course = adminSelectCourse.adminSelectCourse(courseList=courses, socket=self.sock)

        else:
            self.ui.reject()
            course = selectCourse.selectCourse(courseList=courses, socket=self.sock)
            pass