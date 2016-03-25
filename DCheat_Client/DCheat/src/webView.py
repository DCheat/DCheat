# -*- coding: utf-8 -*-
"""
    webView.py

    Function for webview.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, pyqtSlot
from DCheat import config
from DCheat.src import checkSystem
import os

class webView(QtWidgets.QMainWindow):
    def __init__(self, program, web, courseName, sock, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH + 'view/webView.ui', self)

        self.banProgram = program
        self.allowWeb = web
        self.sock = sock
        self.courseName = courseName

        for i in self.allowWeb:
            view = QWebView()
            view.load(QUrl(config.config.ALLOW_SITE[i]))
            self.ui.tabWidget.addTab(view, config.config.ALLOW_SITE[i].lstrip('https://www.'))

        self.ui.webView.load(QUrl('http://www.kookmin.ac.kr'))

        try:
            self.mp = checkSystem.checkSystem(self.banProgram, os.getpid(), self.sock)
            self.mp.daemon = True
            self.mp.start()
        except Exception as e:
            print(e)

        self.ui.show()

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

    def closeEvent(self, event):
        from DCheat.src import warningPopup
        event.ignore()

        datasize = 0
        newdatasize = 0

        try:
            newdatasize = os.path.getsize('newdata.bin')
        except:
            pass

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
            connecMessage = '%s,%s'%(self.courseName, data)
        except Exception as e:
            print(e)

        try:
            result = warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock, self.mp, connecMessage)
        except Exception as e:
            print(e)


    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            pass