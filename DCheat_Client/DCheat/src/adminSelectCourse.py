# -*- coding: utf-8 -*-
"""
    adminSelectCourse.py

    Admin's function for select test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from DCheat import config
from DCheat.src import registerCourse
from DCheat.src import updateCourse

class adminSelectCourse(QtWidgets.QDialog):
    def __init__(self, courseList, socket, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/adminSelectCourse.ui', self)

        self.sock = socket
        self.courseList = []
        self.courseList = self.courseList + courseList
        self.register = object
        self.dataPos = -1
        pListWidget = QtWidgets.QWidget()
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setWidget(pListWidget)
        self.pListLayout = QtWidgets.QGridLayout()
        self.pListLayout.setAlignment(Qt.AlignTop)
        pListWidget.setLayout(self.pListLayout)

        self.makeCourseLayout()

    @pyqtSlot()
    def insert_test(self):
        self.register = registerCourse.registerCourse(self.sock, self.ui, self.courseList)
        self.register.rejectSignal.connect(self.registerHandler)

    def modify_test(self):
        sender = self.sender()
        self.dataPos = int((sender.pos().y() - 9) / 29)

        courseInfo = self.courseList[self.dataPos].split(',')

        name = courseInfo[0]
        testDate = courseInfo[1].split(' ')[0]
        startTime = courseInfo[1].split(' ')[1]
        endTime = courseInfo[2].split(' ')[1]
        bantemp = courseInfo[3].split('*')
        allowtemp = courseInfo[4].split('*')
        stdCount = int(courseInfo[5])

        banProgram = []
        allowSite = []

        try:
            for i in bantemp:
                banProgram.append(int(i))
        except Exception as e:
            pass

        try:
            for i in allowtemp:
                allowSite.append(int(i))
        except Exception as e:
            pass

        self.register = updateCourse.updateCourse(self.sock, name, testDate, startTime, endTime,
                                                  banProgram, allowSite)
        self.register.rejectSignal.connect(self.registerHandler)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass

    def registerHandler(self, message):
        if message == '0':
            pass

        elif self.dataPos is -1:
            self.courseList.append(message)

        else:
            del self.courseList[self.dataPos]
            self.courseList.insert(self.dataPos, message)
            self.dataPos = -1

        self.makeCourseLayout()

    def makeCourseLayout(self):
        try:
            if self.pListLayout.count() is not 0:
                while self.pListLayout.count():
                    item = self.pListLayout.takeAt(0)
                    wid = item.widget()
                    wid.deleteLater()
        except Exception as e:
            print(e)

        listPos = 0

        for course in self.courseList:
            if len(course) is 0:
                break

            courseInfo = course.split(',')

            courseLabel = QtWidgets.QLabel(courseInfo[0])
            startLabel = QtWidgets.QLabel(courseInfo[1])
            endLabel = QtWidgets.QLabel(courseInfo[2])
            countLabel = QtWidgets.QLabel(courseInfo[5])

            courseLabel.setAlignment(Qt.AlignHCenter)
            startLabel.setAlignment(Qt.AlignHCenter)
            endLabel.setAlignment(Qt.AlignHCenter)
            countLabel.setAlignment(Qt.AlignHCenter)

            button = QtWidgets.QPushButton("수정")
            button.clicked.connect(self.modify_test)

            self.pListLayout.addWidget(courseLabel, listPos, 0)
            self.pListLayout.addWidget(startLabel, listPos, 1)
            self.pListLayout.addWidget(endLabel, listPos, 2)
            self.pListLayout.addWidget(countLabel, listPos, 3)
            self.pListLayout.addWidget(button, listPos, 4)
            listPos += 1

        self.ui.show()