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

class logIn(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/login.ui', self)
        self.ui.show()

        self.sock = object

    @pyqtSlot()
    def slot_login(self):
        userID =  self.ui.lineEdit.text()
        # 나중에 주석 해제
        # self.sock = networkServer.networkServer(userID)
        # self.sock.send_login_message()

        loginResult = '1,2,3,4,5'

        if loginResult is -1:
            pass

        else:
            self.ui.reject()
            course = selectCourse.selectCourse(courseList=loginResult, socket=self.sock)
            pass