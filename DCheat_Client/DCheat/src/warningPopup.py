# -*- coding: utf-8 -*-
"""
    warningPopup.py

    warning message popup window.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import *
from DCheat import config

class warningPopup(QtWidgets.QDialog):
    def __init__(self, message, parentUi, sock = None, multiprocess = None, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/warningPopup.ui', self)

        self.parentUi = parentUi
        self.sock = sock
        self.mp = multiprocess

        self.ui.label.setText(message)

        self.ui.show()

    @pyqtSlot()
    def ok_slot(self):
        print('asdf')

        if self.sock is not None:
            self.sock.close()
        if self.mp is not None:
            self.mp.terminate()

        self.ui.reject()
        self.parentUi.reject()

    @pyqtSlot()
    def cancle_slot(self):
        self.ui.reject()