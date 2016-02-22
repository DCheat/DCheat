import os
import socketserver


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(4096)
        cur_pid = os.getpid()
        response = bytes('%d: %s' % (cur_pid, data), 'utf-8')
        self.request.send(response)
        print("AAAAA")
        return


class ForkingEchoServer(socketserver.ForkingMixIn,
                        socketserver.TCPServer,
                        ):
    pass


if __name__ == '__main__':
    import socket
    import threading

        # 데이터베이스 처리 
    from DCheat_Server.database import DBManager
    try:
        DBManager.init("mysql+pymysql://root:dkfrhflwma@localhost/DCheat")
        DBManager.init_db()

    except Exception as e:
        print(e)
    
    from DCheat_Server.utils.selectQuery import select_allow_site_list
    allowSiteList = select_allow_site_list()

    address = ('10.0.2.15', 9410)  # let the kernel assign a portf
    server = ForkingEchoServer(address,
                               ForkingEchoRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()
    print('Server loop running in process:', os.getpid())

    # Clean up
    #server.shutdown()
    #server.socket.close()