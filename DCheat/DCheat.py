import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat.src import logIn

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    userLogIn = logIn.logIn()

    sys.exit(app.exec())