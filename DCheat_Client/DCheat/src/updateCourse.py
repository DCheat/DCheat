# -*- coding: utf-8 -*-
"""
    adminSelectCourse.py

    Admin's function for register test course.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot, QDate, QTime, pyqtSignal
from DCheat.src import warningPopup
from DCheat import config
import datetime
import csv

class updateCourse(QtWidgets.QDialog):
    rejectSignal = pyqtSignal(str)

    def __init__(self, socket, name, testDate, startTime, endTime, banList, allowList, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH +'view/updateCourse.ui', self)
        self.sock = socket

        self.name = name
        self.date = testDate.split('-')
        self.startTime = startTime.split(':')
        self.endTime = endTime.split(':')
        self.banList = banList
        self.allowList = allowList

        self.students = []
        self.ui.label_5.setText(self.name)


        self.ui.dateEdit.setDate(QDate(int(self.date[0]), int(self.date[1]), int(self.date[2])))
        self.ui.timeEdit.setTime(QTime(int(self.startTime[0]), int(self.startTime[1])))
        self.ui.timeEdit_2.setTime(QTime(int(self.endTime[0]), int(self.endTime[1])))

        pListWidget = QtWidgets.QWidget()
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.setWidget(pListWidget)
        pListLayout = QtWidgets.QVBoxLayout()
        pListLayout.setAlignment(Qt.AlignTop)
        pListWidget.setLayout(pListLayout)

        for i in range(1, len(config.config.BAN_PROGRAM)):
            checkBox = QtWidgets.QCheckBox(config.config.BAN_PROGRAM[i])
            checkBox.clicked.connect(self.set_ban_list)

            if i in self.banList:
                checkBox.setChecked(True)

            pListLayout.addWidget(checkBox)


        sListWidget = QtWidgets.QWidget()
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.setWidget(sListWidget)
        sListLayout = QtWidgets.QVBoxLayout()
        sListLayout.setAlignment(Qt.AlignTop)
        sListWidget.setLayout(sListLayout)

        for i in range(1, len(config.config.ALLOW_SITE)):
            checkBox = QtWidgets.QCheckBox(config.config.ALLOW_SITE[i])
            checkBox.clicked.connect(self.set_allow_list)

            if i in self.allowList:
                checkBox.setChecked(True)

            sListLayout.addWidget(checkBox)

        self.ui.show()

    @pyqtSlot()
    def search_slot(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'open file', '/',
                                                                  'CSV파일 (*.csv)', '*.csv')

        if len(filename) is 0:
            return

        self.ui.textEdit_2.setText(filename)

        csvFile = open(filename, 'r')
        data = csv.reader(csvFile)

        for i in data:
            self.students.append(i)

    @pyqtSlot()
    def update_slot(self):
        if self.ui.timeEdit.time() >= self.ui.timeEdit_2.time():
            warningPopup.warningPopup('시험 시간을 다시 확인하세요.')
            return

        self.banList.sort()
        self.allowList.sort()

        date = str(datetime.date(self.ui.dateEdit.date().year(), self.ui.dateEdit.date().month(),
                                 self.ui.dateEdit.date().day()))
        startTime = str(datetime.time(self.timeEdit.time().hour(), self.timeEdit.time().minute()))
        endTime = str(datetime.time(self.timeEdit_2.time().hour(), self.timeEdit_2.time().minute()))

        courseDate = '{} {},{} {}'.format(date, startTime, date, endTime)

        result = self.sock.update_course(self.name, courseDate, self.banList, self.allowList, self.students)

        if result == -1:
            result = warningPopup.warningPopup('수정에 실패했습니다. csv파일 등을 확인해보세요.')

        else:
            self.rejectSignal.emit(self.makeMessage(courseDate, result))
            self.ui.reject()

    def set_ban_list(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 22) + 1

        if pos in self.banList:
            self.banList.remove(pos)

        else:
            self.banList.append(pos)

    def set_allow_list(self):
        sender = self.sender()

        pos = int((sender.pos().y() - 9) / 22) + 1

        if pos in self.allowList:
            self.allowList.remove(pos)

        else:
            self.allowList.append(pos)

    def closeEvent(self, event):
        from DCheat.src import warningPopup

        event.ignore()
        result = warningPopup.warningPopup('종료하시겠습니까?\n 종료하시면 현재 입력한 데이터는 모두 사라집니다.',
                                           self.ui)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass

    def makeMessage(self, courseDate, stdCount):
        try:
            endTime = datetime.datetime(self.ui.dateEdit.date().year(), self.ui.dateEdit.date().month(),
                                        self.ui.dateEdit.date().day(), self.timeEdit_2.time().hour(),
                                        self.timeEdit_2.time().minute())

            if datetime.datetime.now() > endTime:
                return '0'

            programList = str(self.banList).strip('[]').replace(' ', '').replace(',', '*')
            siteList = str(self.allowList).strip('[]').replace(' ', '').replace(',', '*')
            return '{},{},{},{},{}'.format(self.name, courseDate, programList,
                                           siteList, stdCount)
        except Exception as e:
            print(e)