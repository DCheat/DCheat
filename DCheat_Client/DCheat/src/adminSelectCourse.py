# -*- coding: utf-8 -*-
"""
    adminSelectCourse.py

    Admin's function for select test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from DCheat import config
from DCheat.src import registerCourse
from DCheat.src import updateCourse

class adminSelectCourse(QtWidgets.QDialog):
    def __init__(self, courseList, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/adminSelectCourse.ui', self)

        self.sock = socket
        self.courseList = courseList

        i = 0
        self.courseList = self.courseList.split(',')
        for course in self.courseList:
            # courseInfo = course.split('$')
            #
            # courseLabel = QtWidgets.QLabel(courseInfo[0])
            # startLabel = QtWidgets.QLabel(courseInfo[1])
            # endLabel = QtWidgets.QLabel(courseInfo[2])
            # countLabel = QtWidgets.QLabel(courseInfo[3])
            # banProrgam = courseInfo[4].split(',')
            # allowSite = courseInfo[5].split(',')

            courseLabel = QtWidgets.QLabel(course)
            startLabel = QtWidgets.QLabel('0000-00-00 00:00:00')
            endLabel = QtWidgets.QLabel('0000-00-00 00:00:00')
            countLabel = QtWidgets.QLabel(str(250))

            courseLabel.setAlignment(Qt.AlignHCenter)
            startLabel.setAlignment(Qt.AlignHCenter)
            endLabel.setAlignment(Qt.AlignHCenter)
            countLabel.setAlignment(Qt.AlignHCenter)

            button = QtWidgets.QPushButton("수정")
            button.clicked.connect(self.modify_test)

            self.ui.gridLayout.addWidget(courseLabel, i, 0)
            self.ui.gridLayout.addWidget(startLabel, i, 1)
            self.ui.gridLayout.addWidget(endLabel, i, 2)
            self.ui.gridLayout.addWidget(countLabel, i, 3)
            self.ui.gridLayout.addWidget(button, i, 4)
            i+=1

        self.ui.show()

    @pyqtSlot()
    def insert_test(self):
        print('asdfasdf')
        try:
            register = registerCourse.registerCourse(self.sock)
        except Exception as e:
            print(e)

    def modify_test(self):
        sender = self.sender()
        dataPos = int((sender.pos().y() - 21) / 41)

        # courseInfo = course[dataPos].split('$')
        #
        # name = courseInfo[0]
        # testDate = courseInfo[1].split(' ')[0]
        # startTime = courseInfo[1].split(' ')[1]
        # endTime = courseInfo[2].split(' ')[1]
        # bantemp = courseInfo[4].split(',')
        # allowtemp = courseInfo[5].split(',')
        #
        # banProgram = []
        # allowSite = []
        #
        # for i in bantemp:
        #     banProgram.append(int(i))
        #
        # for i in allotemp:
        #     allowSite.append(int(i))

        name = 'asdf'
        testDate = '2012-01-01'
        startTime = '11:00:00'
        endTime = '12:00:00'
        banProgram = [1,2,3,4,5]
        allowSite = [1]

        register = updateCourse.updateCourse(self.sock, name, testDate, startTime, endTime, banProgram, allowSite)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)