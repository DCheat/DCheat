"""
    config.py

    DCheat's config file.

    :copyright: Hwang Sek-jin
"""

import os

class config(object):
    ROOT_PATH = "%s/%s/" % (os.getcwd(), 'DCheat')
    HOST = '203.246.112.179'
    PORT = 9410

    OS_WINDOWS = 'Windows'
    OS_LINUX = 'Linux'

    WINDOWS_DIRECTORY_SEPARATOR = '\\'
    LINUX_DIRECTORY_SEPARATOR = '/'

    CONNECTION_STATUS_ESTABLISHED = 'ESTABLISHED'

    HEADER_SIGNIN = 'SIN'
    HEADER_SIGNUP = 'SUP'
    HEADER_SELECT_COURSE = 'SCS'
    HEADER_CHEACK = 'PCH'
    HEADER_ADD_COURSE = 'ACS'
    HEADER_UPDATE_COURSE = 'UCS'
    HEADER_CLOSE_SOCKET = 'SCL'

    MESSAGE_FORM = '{};{};{}'

    BAN_PROGRAM = ['banProgram', 'KakaoTalk', 'Line', 'NateOn', 'Skype', 'Tictoc', 'Between', 'IExplorer', 'Chrome', 'FireFox']
    ALLOW_SITE = ['allowSite', 'http://cyber2010.kookmin.ac.kr/', 'https://algolab.kookmin.ac.kr']
