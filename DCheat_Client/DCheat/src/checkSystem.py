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

            for pro in self.banList:
                if pro[0]+self.ext == process.name():
                    process.kill()
                    break

    def check_in_windows(self):
        processes = wmi.WMI()

        for process in processes.Win32_Process():
            if process.ProcessId < 100:
                continue

            else:
                checkingPoint = 0
                processPath = process.ExecutablePath

                if processPath is not None:
                    processPath = processPath.split(config.config.WINDOWS_DIRECTORY_SEPARATOR)
                    checkingPoint += self.check_path(processPath)

                print(processPath)
                checkingPoint += self.check_name(process.Name)
                checkingPoint += self.check_port(process.ProcessId)

                if checkingPoint > 10:
                    print('사용')

                elif checkingPoint > 0:
                    print('{}확률 사용'.format(checkingPoint/20))

                else:
                    pass

    def check_in_linux(self):
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
                processPath = process.exe()

                if processPath is not None:
                    processPath = processPath.split(config.config.LINUX_DIRECTORY_SEPARATOR)
                    checkingPoint += self.check_path(processPath)

                checkingPoint += self.check_name(process.name())
                checkingPoint += self.check_port(pid)

                if checkingPoint > 10:
                    print('사용')

                elif checkingPoint > 0:
                    print('{}확률 사용'.format(checkingPoint/20))

                else:
                    pass

    def check_name(self, name):
        for pro in self.banList:
            if pro[0] + self.ext == name:
                return 10

        return 0

    def check_path(self, processPath):
        pathCheck = 0

        for pro in self.banList:
            if pro[1] in processPath:
                pathCheck += 1

            if pro[2] in processPath or pro[2] == '':
                pathCheck += 1

            if pathCheck > 0:
                return pathCheck * 3

        return 0

    def check_port(self, pid):
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





