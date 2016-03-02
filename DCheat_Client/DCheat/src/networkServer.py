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
        loginInfo = '{},{}'.format(userID, password)
        message = bytes(config.config.MESSAGE_FORM.format(0, config.config.HEADER_SIGNIN, loginInfo))

        try:
            self.clientsock.sendall(message)
            recvMessage = (self.clientsock.recv(BUFFER_SIZE)).encode('utf-8')

        except Exception as e:
            return -1

        if recvMessage == '0':
            self.clientsock.close()
            return 0

        recvMessage = recvMessage.split('^')

        self.userNumber = recvMessage[0]

        return recvMessage[1].split(',')

    def send_select_course(self, courseName):
        message = bytes(config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_SELECT_COURSE, courseName))

        try:
            self.clientsock.sendall(courseName)
            recvMessage = (self.clientsock.recv(BUFFER_SIZE)).encode('utf-8')

        except Exception as e:
            return -1

        message = recvMessage.split('^')
        banProgram = message[0].split(',')
        allowWeb = message[1].split(',')

        return banProgram, allowWeb

    def send_sensing_info(self, programIndex, point):
        sensingMessage = '{},{}'.format(programIndex, point)
        message = bytes(config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_SELECT_COURSE, sensingMessage))

        while True:
            try:
                self.clientsock.sendall(message)
                recvMessage = self.clientsock.recv(BUFFER_SIZE)

            except Exception as e:
                return -1

            if recvMessage.encode('utf-8') == '1':
                break
