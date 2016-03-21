import sys
import socket
from DCheat import config
from DCheat.src import warningPopup

global clientsock

try:
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((config.config.HOST, config.config.PORT))
except Exception as e:
    print(e)
    warningPopup.warningPopup('네트워크 장애가 발생했습니다. 다시 실행하세요.')
    sys.exit(0)