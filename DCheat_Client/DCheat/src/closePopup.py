# -*- coding: utf-8 -*-
"""
    warningPopup.py

    warning message popup window.

    :copyright: Hwang Sek-jin
"""

import sys
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from DCheat import config

class closePopup(QtWidgets.QDialog):
    def __init__(self, parentUi, sock, multiprocess, messgae, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/closePopup.ui', self)

        self.parentUi = parentUi
        self.sock = sock
        self.mp = multiprocess
        self.closeMessage = "시험이 종료되었습니다.\n %d초 후 종료됩니다."
        self.message = messgae
        self.count = 10

        self.ui.label.setText(self.closeMessage % (self.count))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.message_display)
        self.timer.start(1100)

        self.ui.show()

    @pyqtSlot()
    def ok_slot(self):
        try:
            self.sock.closeSocket(self.message)

            self.mp.terminate()

            self.ui.reject()

            if self.parentUi is not None:
                try:
                    self.parentUi.reject()
                except Exception as e:
                    sys.exit()
        except Exception as e:
            print(e)

    def message_display(self):
        if self.count is 0:
            self.ok_solt()

        self.ui.label.setText(self.closeMessage % (self.count))
        self.count -= 1

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass