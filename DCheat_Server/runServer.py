import os
import socketserver


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        cur_pid = os.getpid()
        response = bytes('%d: %s' % (cur_pid, data), 'utf-8')
        self.request.send(response)
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

    address = ('localhost', 0)  # let the kernel assign a port
    server = ForkingEchoServer(address,
                               ForkingEchoRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()
    print('Server loop running in process:', os.getpid())

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    message = 'Hello, world'.encode()
    print('Sending : {!r}'.format(message))
    len_sent = s.send(message)

    # Receive a response
    response = s.recv(1024)
    print('Received: {!r}'.format(response))

    # Clean up
    server.shutdown()
    s.close()
    server.socket.close()