# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for connecting server and sending data.

    :copyright: Hwang Sek-jin
"""

from DCheat import clientsock
from DCheat import config
from DCheat.src import warningPopup

BUFFER_SIZE = 4096

class networkServer(object):
    def __init__(self):
        self.userNumber = 0

    def close(self, closeMessage):
        message = (config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_CLOSE_SOCKET,
                                                     closeMessage)).encode('utf-8')
        try:
            clientsock.send(message)
        except Exception as e:
            pass

        clientsock.close()

    def send_login_message(self, userID = '', password = ''):
        loginInfo = '{},{}'.format(userID, password)
        message = (config.config.MESSAGE_FORM.format(0, config.config.HEADER_SIGNIN, loginInfo)).encode('utf-8')
        q = message.decode().split(',')
        try:
            clientsock.send(message)
            recvMessage = (clientsock.recv(BUFFER_SIZE)).decode()
        except Exception as e:
            warningPopup.warningPopup('접속 문제입니다. 다시 시도하세요.')
            return 0

        if recvMessage == '0':
            warningPopup.warningPopup('잘못된 아이디 또는 비밀번호를 입력하셨습니다.')
            return 0

        elif recvMessage == '-1':
            warningPopup.warningPopup('볼수 있는 시험이 없습니다.')
            return 0

        recvMessage = recvMessage.split('^')

        self.userNumber = recvMessage[0]

        if len(password) is 0:
            courseList = recvMessage[1].split(',')

            return courseList

        else:
            courseInfo = recvMessage[1:]

            return courseInfo

    def send_select_course(self, courseName):
        message = (config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_SELECT_COURSE,
                                                     courseName)).encode('utf-8')

        try:
            clientsock.sendall(message)
            recvMessage = (clientsock.recv(BUFFER_SIZE)).decode()

        except Exception as e:
            warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)
            return 0

        if recvMessage == '0':
            warningPopup.warningPopup('종료하시겠습니까?', self.ui, self.sock)

        banProgram = []
        allowWeb = []

        message = recvMessage.split(',')

        if len(message[0]) is not 0:
            tempbanProgram = message[0].split('*')

            for i in tempbanProgram:
                banProgram.append(int(i))

        if len(message[1]) is not 0:
            tempallowWeb = message[1].split('*')

            for i in tempallowWeb:
                allowWeb.append(int(i))

        return banProgram, allowWeb

    def send_sensing_info(self, programIndex, point):
        sensingMessage = '{},{}'.format(programIndex, point)
        message = (config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_CHEACK,
                                                     sensingMessage)).encode('utf-8')

        while True:
            try:
                clientsock.sendall(message)
                recvMessage = (clientsock.recv(BUFFER_SIZE)).decode()

            except Exception as e:
                pass

    def make_course(self, courseName, courseDate, programList, siteList, students):
        programList = str(programList).strip('[]').replace(' ', '').replace(',', '*')
        siteList = str(siteList).strip('[]').replace(' ', '').replace(',', '*')

        stdList = ''

        for std in students:
            stdList = stdList + (str(std).strip('[]').replace(' ', '')).replace(',', '$') + '*'

        stdList = stdList.rstrip('*')

        makeMessage = '{},{},{},{},{}'.format(courseName, courseDate, programList, siteList, stdList)
        makeMessage = makeMessage.replace("'", '')
        message = (config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_ADD_COURSE,
                                                     makeMessage)).encode('utf-8')

        try:
            clientsock.send(message)
            recvMessage = (clientsock.recv(BUFFER_SIZE)).decode()

        except Exception as e:
            return 0

        if recvMessage == '1':
            return 1

        elif recvMessage == '-1':
            return -1

        else:
            return 0



    def update_course(self, courseName, courseDate, programList, siteList, students):
        programList = str(programList).strip('[]').replace(' ', '').replace(',', '*')
        siteList = str(siteList).strip('[]').replace(' ', '').replace(',', '*')

        stdList = ''

        for std in students:
            stdList = stdList + (str(std).strip('[]').replace(' ', '')).replace(',', '$') + '*'

        stdList = stdList.rstrip('*')

        makeMessage = '{},{},{},{},{}'.format(courseName, courseDate, programList, siteList, stdList)
        message = config.config.MESSAGE_FORM.format(self.userNumber, config.config.HEADER_UPDATE_COURSE,
                                                    makeMessage).encode('utf-8')

        try:
            clientsock.sendall(message)
            recvMessage = clientsock.recv(BUFFER_SIZE).decode()

        except Exception as e:
            return 0

        if recvMessage.encode('utf-8') == '1':
            return 1

        else:
            return 0