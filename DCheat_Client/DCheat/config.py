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

    ALLOW_SITE = ['allowSite', 'http://cyber2010.kookmin.ac.kr/', 'https://algolab.kookmin.ac.kr']

    BAN_PROGRAM = ['banProgram', 'IExplorer', 'Chrome', 'FireFox', 'swing', 'edge', 'KakaoTalk', 'Line', 'NateOn', 'Skype', 'Tictoc', 'Between']
    BAN_PROGRAM_PNAME = ['banProgramPName', 'iexplore', 'chrome', 'firefox', 'swing', 'edge', 'KakaoTalk', 'LINE', 'NateOnMain', 'Skype', 'Tictoc', 'couple']
    BAN_PROGRAM_PATH = ['banProgramPath', ["Internet Explorer", ""], ["Goole", "Chrome"], ["Mozilla Firefox", ""], ["Swing", ""], ["Edge", ""],
                        ["Kakao", "KakaoTalk"], ["LINE", "LINE"], ["SK Communications", "NATEON"], ["Skype", "phone"], ["Tictoc", "bin"], ["Between", ""]]
    BAN_PROGRAM_RPORT = ['banProgramRPort', 0, 0, 0, 0, 0, 5223, 443, 5004, 12350, 23018, 0]
