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

        self.userNumber = 0

    def close(self):
        self.clientsock.close()

    def send_login_message(self, userID = '', password = ''):
        loginInfo = '{},{}'.format(userID, password)
        message = (config.config.MESSAGE_FORM.format(0, config.config.HEADER_SIGNIN, loginInfo)).encode('utf-8')

        try:
            self.clientsock.sendall(message)
            recvMessage = (self.clientsock.recv(BUFFER_SIZE)).decode()

        except Exception as e:
            print(e)
            return -1

        if recvMessage == '0':
            self.clientsock.close()
            return 0

        if password == '':
            recvMessage = recvMessage.split('^')

            self.userNumber = recvMessage[0]

            return recvMessage[1].split(',')

        else:
            recvMessage = recvMessage.split('^')

            self.userNumber = recvMessage[0]

            courseInfo = []
            for info in range(1, len(recvMessage)):
                course = info.split('$')
                courseInfo.append(course)

            return courseInfo

    def send_select_course(self, courseName):
        message = bytes(config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_SELECT_COURSE, courseName))

        try:
            self.clientsock.sendall(message)
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

    def make_course(self, courseName, courseDate, programList, siteList, students):
        programList = str(programList).strip('[]').replace(' ', '')
        siteList = str(siteList).strip('[]').replace(' ', '')

        stdList = ''

        for std in students:
            stdList = stdList + (str(std).strip('[]').replace(' ', '')) + '$'

        stdList.rstrip('$')

        makeMessage = '{}^{}^{}^{}^{}'.format(courseName, courseDate, programList, siteList, stdList)
        message = config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_ADD_COURSE, makeMessage)

        try:
            self.clientsock.sendall(message)
            recvMessage = self.clientsock.recv(BUFFER_SIZE)

        except Exception as e:
            return -1

        if recvMessage.encode('utf-8') == '1':
            pass

        else:
            print('asdf')



    def update_course(self, courseName, courseDate, programList, siteList, students):
        programList = str(programList).strip('[]').replace(' ', '')
        siteList = str(siteList).strip('[]').replace(' ', '')

        stdList = ''

        for std in students:
            stdList = stdList + (str(std).strip('[]').replace(' ', '')) + '$'

        stdList.rstrip('$')

        makeMessage = '{}^{}^{}^{}^{}'.format(courseName, courseDate, programList, siteList, stdList)
        message = config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_ADD_COURSE, makeMessage)

        try:
            self.clientsock.sendall(message)
            recvMessage = self.clientsock.recv(BUFFER_SIZE)

        except Exception as e:
            return -1

        if recvMessage.encode('utf-8') == '1':
            pass

        else:
            print('asdf')