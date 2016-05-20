# -*- coding: utf-8 -*-
"""
    webView.py

    Function for webview.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import Qt, pyqtSlot, QUrl, QTimer, QThread
from DCheat import config
from DCheat.src import checkSystem
import datetime
import os
import wmi

class webView(QtWidgets.QMainWindow):
    def __init__(self, program, web, courseName, endTime, sock, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH + 'view/webView.ui', self)

        self.banProgram = program
        self.allowWeb = web
        self.sock = sock
        self.courseName = courseName
        self.endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        self.checkPopup = False

        for i in self.allowWeb:
            view = QWebView()
            view.load(QUrl(config.config.ALLOW_SITE[i]))
            self.ui.tabWidget.addTab(view, config.config.ALLOW_SITE[i].lstrip('https://www.'))

        self.ui.webView.load(QUrl('http://www.kookmin.ac.kr'))

        try:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.rest_time_display)
            self.timer.start(900)

        except Exception as e:
            print(e)

        self.ui.show()

        try:
            self.threadTimer = QTimer(self)
            self.threadTimer.timeout.connect(self.check_thread_run)

            self.mp = checkSystem.checkSystem(self.courseName, self.banProgram, self.sock)
            self.mp.start()

            self.threadTimer.start(41000)

        except Exception as e:
            print(e)

    @pyqtSlot()
    def slot_back(self):
        self.ui.webView.back()

    @pyqtSlot()
    def slot_forward(self):
        self.ui.webView.forward()

    @pyqtSlot()
    def slot_stop(self):
        self.ui.webView.stop()

    @pyqtSlot()
    def slot_reload(self):
        self.ui.webView.reload()

    def closeEvent(self, event = None):
        from DCheat.src import warningPopup

        if event is not None:
            event.ignore()

        connecMessage = self.check_other_process()

        try:
            result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock, connecMessage)

        except Exception as e:
            print(e)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass

    def rest_time_display(self):
        try:
            currentTime = datetime.datetime.now()
            restTime = self.endTime - currentTime
            restTime = int(restTime.total_seconds())

            if restTime <= 0:
                restTime = abs(restTime)
                printFormat = "-%d:%02d:%02d"

                if self.checkPopup is False:
                    from DCheat.src import closePopup
                    self.checkPopup = True
                    connecMessage = self.check_other_process()

                    try:
                        result = closePopup.closePopup(self.ui, self.sock, self.mp, connecMessage)

                    except Exception as e:
                        print(e)

            else:
                printFormat = "%d:%02d:%02d"

            h, m = divmod(restTime, 3600)
            m, s = divmod(m, 60)

            self.ui.lcdNumber.display(printFormat % (h, m, s))

        except Exception as e:
            print(e)

    def check_thread_run(self):
        try:
            self.mp.start()

        except Exception as e:
            print(e)

    def check_other_process(self):
        datasize = 0
        newdatasize = 0

        try:
            newdatasize = os.path.getsize('newdata.bin')

        except:
            try:
                datasize = os.path.getsize('data.bin')

            except:
                pass

        if newdatasize > datasize:
            try:
                fp = open('newdata.bin')

            except Exception as e:
                print(e)

        else:
            try:
                fp = open('data.bin')

            except Exception as e:
                print(e)
        try:
            data = fp.read()
            fp.close()
            connecMessage = '%s,%s' % (self.courseName, data)

        except Exception as e:
            print(e)

        return connecMessage