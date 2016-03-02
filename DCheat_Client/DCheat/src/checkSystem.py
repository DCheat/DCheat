# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for checking that client is using program.

    :copyright: Hwang Sek-jin
"""

import platform
import wmi
import psutil
from DCheat import config
import time

class checkSystem(object):
    def __init__(self, banList):
        self.clientOS = platform.system()
        self.banList = banList

        self.ext = ''

        if self.clientOS == config.config.OS_WINDOWS:
            self.ext = '.exe'

    def startChecking(self):
        self.preCheck()
        while True:
            if self.clientOS == config.config.OS_WINDOWS:
                self.checkInWindows()

            else:
                self.checkInLinux()

            time.sleep(58)

    def preCheck(self):
        processes = psutil.pids()

        for pid in processes:
            process = psutil.Process(pid)

            for pro in self.banList:
                if pro[0]+self.ext == process.name():
                    process.kill()
                    break

    def checkInWindows(self):
        processes = wmi.WMI()

        for process in processes.Win32_Process():
            if process.ProcessId < 100:
                continue

            else:
                checkingPoint = 0
                processPath = process.ExecutablePath.split(config.config.WINDOWS_DIRECTORY_SEPARATOR)

                checkingPoint += self.checkName(process.Name)
                checkingPoint += self.checkPath(processPath)
                checkingPoint += self.checkPort(process.ProcessId)

                if checkingPoint > 10:
                    print('사용')

                elif checkingPoint > 0:
                    print('{}확률 사용'.format(checkingPoint/20))

                else:
                    pass

    def checkInLinux(self):
        processes = psutil.pids()

        for pid in processes:
            if pid < 100:
                continue

            else:
                try:
                    process = psutil.Process(pid)
                except Exception as e:
                    continue

                checkingPoint = 0
                processPath = process.exe().split(config.config.LINUX_DIRECTORY_SEPARATOR)

                checkingPoint += self.checkName(process.name())
                checkingPoint += self.checkPath(processPath)
                checkingPoint += self.checkPort(pid)

                if checkingPoint > 10:
                    print('사용')

                elif checkingPoint > 0:
                    print('{}확률 사용'.format(checkingPoint/20))

                else:
                    pass

    def checkName(self, name):
        for pro in self.banList:
            if pro[0] + self.ext == name:
                return 10

        return 0

    def checkPath(self, processPath):
        pathCheck = 0

        for pro in self.banList:
            if pro[1] in processPath:
                pathCheck += 1

            if pro[2] in processPath:
                pathCheck += 1

            if pathCheck > 0:
                return pathCheck * 3

        return 0

    def checkPort(self, pid):
        try:
            processInfo = psutil.Process(pid)
        except Exception as e:
            return 0

        connecList = processInfo.connections()

        for connec in connecList:
            if connec[5] == config.config.CONNECTION_STATUS_ESTABLISHED:
                for pro in self.banList:
                    if connec[4][1] == pro[3]:
                        return 4

        return 0





