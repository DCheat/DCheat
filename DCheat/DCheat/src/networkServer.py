# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for connecting server and sending data.

    :copyright: Hwang Sek-jin
"""

from socket import *
from DCheat import config

BUFFER_SIZE = 10240

class networkServer(object):
    def __init__(self, userID):
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.clientsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clientsock.connect((config.config.HOST, config.config.PORT))
        self.userID = userID

    def send_login_message(self, loginMsg):
        self.clientsock.sendall(self.userID)
        loginResult = self.clientsock.recv(BUFFER_SIZE)
        if loginResult is -1:
            self.clientsock.close()
        return loginResult

    def send_select_course(self, courseName):
        self.clientsock.sendall(courseName)
        totalMessage = self.clientsock.recv(BUFFER_SIZE)

        message = totalMessage.split('^')
        banProgram = message[0].split(',')
        allowWeb = message[1].split(',')

        return banProgram, allowWeb

    def send_process_info(self):
        # 작성중.....
        pass
