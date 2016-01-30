# -*- coding: utf-8 -*-
"""
    webView.py

    Function for webview.

    :copyright: Hwang Sek-jin
"""

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from DCheat import config

class webView(QtWidgets.QMainWindow):
    def __init__(self, program, web, sock, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH + 'view/webView.ui', self)

        self.banProgram = program
        self.allowWeb = web
        self.sock = sock

        for i in range(len(self.allowWeb)):
            view = QWebView()
            view.load(QUrl(self.allowWeb[i]))
            self.ui.tabWidget.addTab(view, self.allowWeb[i].lstrip('https://www.'))

        self.ui.webView.load(QUrl('http://www.kookmin.ac.kr'))

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