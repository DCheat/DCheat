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
import multiprocessing

class checkSystem(multiprocessing.Process):
    def __init__(self, banList):
        multiprocessing.Process.__init__(self)
        self.clientOS = platform.system()
        self.banList = banList
        self.tempIndex = 0

        self.ext = ''

        if self.clientOS == config.config.OS_WINDOWS:
            self.ext = '.exe'

    def run(self):
        self.pre_check()

        while True:
            if self.clientOS == config.config.OS_WINDOWS:
                self.check_in_windows()

            else:
                self.check_in_linux()

            time.sleep(59)

    def pre_check(self):
        processes = psutil.pids()

        for pid in processes:
            process = psutil.Process(pid)

            for i in self.banList:
                if config.config.BAN_PROGRAM_PNAME[i]+self.ext == process.name():
                    process.kill()
                    break

    def check_in_windows(self):
        processes = wmi.WMI()

        for process in processes.Win32_Process():
            self.tempIndex = 0

            if process.ProcessId < 100:
                continue

            else:
                checkingPoint = 0
                processPath = process.ExecutablePath

                if processPath is None:
                    continue

                processPath = processPath.split(config.config.WINDOWS_DIRECTORY_SEPARATOR)

                checkingPoint += self.check_name(process.Name)
                print('a',checkingPoint)
                checkingPoint += self.check_path(processPath)
                print('b',checkingPoint)
                checkingPoint += self.check_port(process.ProcessId)
                print('c',checkingPoint)

                if checkingPoint > 10:
                    print('사용', config.config.BAN_PROGRAM[self.tempIndex])

                elif checkingPoint > 2:
                    print('{}확률 사용'.format(checkingPoint/20), config.config.BAN_PROGRAM[self.tempIndex])

                else:
                    pass

    def check_in_linux(self):
        processes = psutil.pids()

        for pid in processes:
            self.tempIndex  = 0

            if pid < 100:
                continue

            else:
                try:
                    process = psutil.Process(pid)
                except Exception as e:
                    continue

                checkingPoint = 0
                processPath = process.exe()

                if processPath is None:
                    continue

                processPath = processPath.split(config.config.LINUX_DIRECTORY_SEPARATOR)

                checkingPoint += self.check_name(process.name())
                checkingPoint += self.check_path(processPath)
                checkingPoint += self.check_port(pid)

                if checkingPoint > 10:
                    print('사용', config.config.BAN_PROGRAM[self.tempIndex])

                elif checkingPoint > 2:
                    print('{}확률 사용'.format(checkingPoint/20), config.config.BAN_PROGRAM[self.tempIndex])

                else:
                    pass

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

                if config.config.BAN_PROGRAM_PATH[i][1] in processPath\
                    or config.config.BAN_PROGRAM_PATH[i][1] == "":
                    pathCheck += 1

        pathCheck = pathCheck * 2

        return pathCheck

    def check_port(self, pid):
        try:
            processInfo = psutil.Process(pid)
        except Exception as e:
            return 0

        connecList = processInfo.connections()

        if self.tempIndex > 0:
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





