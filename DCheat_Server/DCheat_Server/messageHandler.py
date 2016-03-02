import os
import socketserver

class ForkingRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(4096)
        cur_pid = os.getpid()
        response = bytes('%d: %s' % (cur_pid, data), 'utf-8')
        self.request.send(response)
        print("AAAAA")
        return
    
    def login_handler():
        return
    def sign_up_handler():
        return
    def user_allow_ban_list_handler():
        return
    def send_email_handler():
        return
    def master_insert_course_handler():
        return
    def master_modify_course_handler():
        return
        
    