import os
import DCheat_Server
from socketserver import ThreadingTCPServer
from DCheat_Server.messageHandler import ForkingRequestHandler
from DCheat_Server.chart import chart

class ForkingServer(ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    try:
        address = ('', 9410)  # let the kernel assign a portf
        server = ForkingServer(address,
                                   ForkingRequestHandler)
        ip, port = server.server_address  # what port was assigned?

        chartThread = chart()
        chartThread.start()


        print('Server loop running in process:', os.getpid())
        server.serve_forever()

    except (KeyboardInterrupt, SystemExit):
        server.socket.close()
        try:
            server.shutdown(1)
        except:
            pass