# -*- coding: utf-8 -*-
"""
    networkServer.py

    Function for checking that client is using program.

    :copyright: Hwang Sek-jin
"""

import os
import platform
import wmi
import psutil
from DCheat import config
import time
import multiprocessing

class checkSystem(multiprocessing.Process):
    def __init__(self, banList, ppid, sock):
        multiprocessing.Process.__init__(self)

        self.banList = banList
        self.sock = sock
        self.ppid = ppid
        self.connecList = []

        self.clientOS = platform.system()
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
            if pid == self.ppid:
                continue

            process = psutil.Process(pid)

            for i in self.banList:
                if config.config.BAN_PROGRAM_PNAME[i]+self.ext == process.name():
                    process.kill()
                    break

    def check_in_windows(self):
        try:
            processes = wmi.WMI()
        except Exception as e:
            print(e)

        for process in processes.Win32_Process():
            if process.ProcessId == self.ppid:
                continue

            if process.ProcessId < 100:
                continue

            self.tempIndex = 0

            checkingPoint = 0
            processPath = process.ExecutablePath

            if processPath is None:
                continue

            processPath = processPath.split(config.config.WINDOWS_DIRECTORY_SEPARATOR)

            checkingPoint += self.check_name(process.Name)
            checkingPoint += self.check_path(processPath)
            checkingPoint += self.check_port(process.ProcessId)

            if checkingPoint > 0:
                self.sock.send_sensing_info(self.tempIndex, checkingPoint)
                self.banList.remove(self.tempIndex)

            else:
                self.makeConnecList(process.ProcessId)

    def check_in_linux(self):
        processes = psutil.pids()

        for pid in processes:
            if pid == self.ppid:
                continue

            if pid < 100:
                continue

            self.tempIndex  = 0

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

            if checkingPoint > 0:
                self.sock.send_sensing_info(self.tempIndex, checkingPoint)
                self.banList.remove(self.tempIndex)

            else:
                self.makeConnecList(pid)

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

    def makeConnecList(self, pid):
        pInfo = psutil.Process(pid)
        pName = pInfo.name()

        if len(pInfo.connections()) > 0 and (pName in self.connecList) is False:
            self.connecList.append(pName)

        fp = open('newdata.bin', 'wb')
        fp.write(str(self.connecList).strip('[]').replace(' ', '').replace(',', '*').encode('utf-8'))
        fp.close()

        os.rename('newdata.bin', 'data.bin')