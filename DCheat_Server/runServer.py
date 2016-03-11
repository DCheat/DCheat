import os
import socketserver
from socketserver import ThreadingTCPServer
from DCheat_Server.messageHandler import ForkingRequestHandler

class ForkingServer(ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == '__main__':

        # 데이터베이스 처리 
    from DCheat_Server.database import DBManager
    try:
        DBManager.init("mysql+pymysql://root:dkfrhflwma@localhost/DCheat")
        DBManager.init_db()

    except Exception as e:
        print(e)
    
    address = ('', 9410)  # let the kernel assign a portf
    server = ForkingServer(address,
                               ForkingRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    print('Server loop running in process:', os.getpid())
    server.serve_forever()

    # Clean up
    #server.shutdown()
    #server.socket.close()