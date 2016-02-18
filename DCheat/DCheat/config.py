"""
    config.py

    DCheat's config file.

    :copyright: Hwang Sek-jin
"""

import os

class config(object):
    ROOT_PATH = "%s/%s/" % (os.getcwd(), 'DCheat')
    HOST = '***.***.***.***'
    PORT = 9410

    OS_WINDOWS = 'Windows'
    OS_LINUX = 'Linux'

    WINDOWS_DIRECTORY_SEPARATOR = '\\'
    LINUX_DIRECTORY_SEPARATOR = '/'

    CONNECTION_STATUS_ESTABLISHED = 'ESTABLISHED'

    HEADER_LOGIN = 'LIN'
    HEADER_SELECT_COURSE = 'SCS'
    HEADER_CHEACK = 'PCH'
    HEADER_ADD_COURSE = 'ACS'
    HEADER_UPDATE_COURSE = 'UCS'