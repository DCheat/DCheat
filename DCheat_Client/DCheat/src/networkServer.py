# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for connecting server and sending data.

    :copyright: Hwang Sek-jin
"""

import socket
from DCheat import config

BUFFER_SIZE = 4096

class networkServer(object):
    def __init__(self):
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientsock.connect((config.config.HOST, config.config.PORT))
        except Exception as e:
            print(e)
        print('asdf')
        self.userNumber = 0

    def send_login_message(self, userID = '', password = ''):
        message = '0;{};{},{}'.format(config.config.HEADER_SIGNIN, userID, password)

        self.clientsock.sendall(message)
        recvMessage = self.clientsock.recv(BUFFER_SIZE)
        recvMessage = recvMessage.split('^')

        self.userNumber = recvMessage[0]

        if self.userNumber is 0:
            self.clientsock.close()
            return self.userNumber

        return recvMessage[1].split(',')

    def send_select_course(self, courseName):
        message = '0;{};{}'.format(config.config.HEADER_SELECT_COURSE, courseName)

        self.clientsock.sendall(courseName)
        totalMessage = self.clientsock.recv(BUFFER_SIZE)

        message = totalMessage.split('^')
        banProgram = message[0].split(',')
        allowWeb = message[1].split(',')

        return banProgram, allowWeb

    def send_process_info(self):
        # 작성중.....
        pass
