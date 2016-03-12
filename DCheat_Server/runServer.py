import os
import DCheat_Server
import socketserver
from socketserver import ThreadingTCPServer
from DCheat_Server.messageHandler import ForkingRequestHandler

class ForkingServer(ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    address = ('', 9410)  # let the kernel assign a portf
    server = ForkingServer(address,
                               ForkingRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    print('Server loop running in process:', os.getpid())
    server.serve_forever()

    # Clean up
    #server.shutdown()
    #server.socket.close()