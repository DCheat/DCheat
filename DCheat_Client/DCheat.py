import sys
from PyQt5 import QtWidgets

from DCheat.src import logIn

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    userLogIn = logIn.logIn()

    sys.exit(app.exec())