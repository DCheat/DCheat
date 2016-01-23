import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat.src import logIn

# class Form(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         QtWidgets.QDialog.__init__(self, parent)
#         self.ui = uic.loadUi('./DCheat/view/selectCourse.ui', self)
#         self.ui.listWidget.addItem('asdf')
#         self.ui.listWidget.addItem('asdf2')
#         self.ui.listWidget.addItem('asdf3')
#         self.ui.show()
#
#     @pyqtSlot()
#     def slot_select(self):
#         a = self.ui.listWidget.currentItem()
#         print()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #w = Form()
    userLogIn = logIn.logIn()
    sys.exit(app.exec())