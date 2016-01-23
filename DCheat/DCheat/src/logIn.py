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

class logIn(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'/view/login.ui', self)
        self.ui.show()

        self.sock = object

    @pyqtSlot()
    def slot_login(self):
        userID =  self.ui.lineEdit.text()
        self.ui.close()
        self.sock = networkServer.networkServer(userID)
        loginResult = self.sock.send_login_message()

        if loginResult is 1:
            pass

        else:
            pass