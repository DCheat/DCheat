# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for checking that client is using program.

    :copyright: Hwang Sek-jin
"""

import os
import platform
import psutil
from DCheat import config
from PyQt5.QtCore import QThread
import time

class checkSystem(QThread):
    def __init__(self, courseName, banList, sock):
        QThread.__init__(self)

        self.courseName = courseName
        self.banList = banList
        self.sock = sock
        self.pid = os.getpid()
        self.connecList = []

        self.clientOS = platform.system()
        self.tempIndex = 0

        self.ext = ''
        self.thispid = os.getpid()

        if self.clientOS == config.config.OS_WINDOWS:
            self.dirSeperator = config.config.WINDOWS_DIRECTORY_SEPARATOR
            self.ext = '.exe'

        else:
            self.dirSeperator = config.config.LINUX_DIRECTORY_SEPARATOR

        try:
            self.pre_check()
            time.sleep(1)

        except Exception as e:
            print(e)

    def run(self):
        try:
            self.check_process()

        except Exception as e:
            print(e)

    def pre_check(self):
        processes = psutil.process_iter()
        for process in processes:
            try:
                for i in self.banList:
                    if config.config.BAN_PROGRAM_PNAME[i] + self.ext == process.name():
                        process.kill()
                        break

            except:
                continue

    def check_process(self):
        try:
            processes = psutil.process_iter()

        except Exception as e:
            print(e)

        for process in processes:
            try:
                if process.pid == self.pid or process.pid < 100:
                    continue

                processPath = process.exe()
                processName = process.name()
                processId = process.pid

            except Exception as e:
                continue

            self.tempIndex = 0

            checkingPoint = 0

            if processPath is None:
                continue

            processPath = processPath.split(self.dirSeperator)

            checkingPoint += self.check_name(processName)
            checkingPoint += self.check_path(processPath)
            checkingPoint += self.check_port(processId)

            if checkingPoint > 2:
                self.sock.send_sensing_info(self.tempIndex, checkingPoint, self.courseName)
                self.banList.remove(self.tempIndex)

            else:
                self.makeConnecList(processId)

    def check_name(self, name):
        for i in self.banList:
            if config.config.BAN_PROGRAM_PNAME[i] + self.ext == name:
                self.tempIndex = i
                return 10

        return 0

    def check_path(self, processPath):
        pathCheck = 0

        if self.tempIndex > 0:
            pathCheck += 1

            if config.config.BAN_PROGRAM_PATH[self.tempIndex][0] in processPath:
                pathCheck += 1

            if config.config.BAN_PROGRAM_PATH[self.tempIndex][1] in processPath\
                or config.config.BAN_PROGRAM_PATH[self.tempIndex][1] == "":
                pathCheck += 1

        else:
            for i in self.banList:
                if config.config.BAN_PROGRAM_PATH[i][0] in processPath:
                    self.tempIndex = i
                    pathCheck += 1

                if config.config.BAN_PROGRAM_PATH[i][1] in processPath:
                    self.tempIndex = i
                    pathCheck += 1

        pathCheck = pathCheck * 2

        return pathCheck

    def check_port(self, pid):
        try:
            processInfo = psutil.Process(pid)
        except Exception as e:
            return 0

        connecList = processInfo.connections()

        if self.tempIndex > 0 and config.config.BAN_PROGRAM_RPORT[self.tempIndex] is not 0:
            for connec in connecList:
                if connec[5] == config.config.CONNECTION_STATUS_ESTABLISHED:
                    if connec[4][1] == config.config.BAN_PROGRAM_RPORT[self.tempIndex]:
                        return 5

        for connec in connecList:
            if connec[5] == config.config.CONNECTION_STATUS_ESTABLISHED:
                for i in self.banList:
                    if connec[4][1] == config.config.BAN_PROGRAM_RPORT[i]:
                        self.tempIndex = i
                        return 3

        return 0

    def makeConnecList(self, pid):
        try:
            pInfo = psutil.Process(pid)
            pName = pInfo.name()

            if len(pInfo.connections()) > 0 and (pName in self.connecList) is False\
                and pid != self.pid:
                self.connecList.append(pName)

            fp = open('newdata.bin', 'wb')
            fp.write(str(self.connecList).strip('[]').replace(' ', '').replace("'", '').replace(',', '*').encode('utf-8'))
            fp.close()

            os.remove('data.bin')
        except Exception as e:
            print(e)

        try:
            os.rename('newdata.bin', 'data.bin')
        except Exception as e:
            print(e)
