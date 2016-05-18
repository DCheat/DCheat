# -*- coding: utf-8 -*-
"""
    warningPopup.py

    warning message popup window.

    :copyright: Hwang Sek-jin
"""

import sys
import time
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from DCheat import config

class warningPopup(QtWidgets.QDialog):
    def __init__(self, message, parentUi = None, sock = None, closeMessgae = '', parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/warningPopup.ui', self)

        self.parentUi = parentUi
        self.sock = sock
        self.closeMessage = closeMessgae

        self.ui.label.setText(message)

        self.ui.show()

    @pyqtSlot()
    def ok_slot(self):
        time.sleep(1)
        try:
            if self.sock is not None:
                self.sock.closeSocket(self.closeMessage)

            self.ui.reject()

            if self.parentUi is not None:
                try:
                    self.parentUi.reject()
                except Exception as e:
                    sys.exit()
        except Exception as e:
            print(e)

    @pyqtSlot()
    def cancle_slot(self):
        self.ui.reject()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass