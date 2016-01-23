import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat.src import logIn

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('./DCheat/view/login.ui', self)
        self.ui.show()

    @pyqtSlot()
    def slot_login(self):
        a = self.ui.lineEdit.text()
        print(os.getcwd()+'/view')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    userLogIn = logIn.logIn()
    sys.exit(app.exec())