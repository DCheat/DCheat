# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for connecting server and sending data.

    :copyright: Hwang Sek-jin
"""

from socket import *
from DCheat import config

class networkServer(object):
    def __init__(self, userID):
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.connect((config.HOST, config.PORT))
        self.userID = userID

    def send_login_message(self):
        self.clientsock.sendall(self.userID)
        loginResult = self.clientsock.recv(1024)
        if loginResult is -1:
            self.clientsock.close()
        return loginResult

    def send_process_info(self):
        # 작성중.....
        pass
