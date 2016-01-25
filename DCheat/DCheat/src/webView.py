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
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from DCheat import config

class webView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(config.config.ROOT_PATH + 'view/webView.ui', self)

        self.ui.webView.load(QUrl('http://www.kookmin.ac.kr'))

        self.ui.show()
