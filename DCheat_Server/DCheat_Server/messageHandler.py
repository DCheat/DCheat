import os
import socketserver

class ForkingRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        from DCheat_Server.utils.selectQuery import select_unfinished_test_course_for_user,\
                                            select_user_index,\
                                            select_ban_list_in_test,\
                                            select_allow_site_index
        # Echo the back to the client
        data = self.request.recv(4096)
        cur_pid = os.getpid()
        response = bytes('%d: %s' % (cur_pid, data), 'utf-8')
        self.request.send(response)
        print("AAAAA")
        if data.find("SIN") != -1:
            userId = data.split()[4]
            courseList = select_unfinished_test_course_for_user()
            userIndex = select_user_index(userId)
            return [userIndex+"^"+courseList]
        if data.find("SCS") != -1:
            testIndex = int(data.split()[0])
            programIndexList = select_ban_list_in_test(testIndex)
            siteIndexList = select_allow_site_index()
            return [programIndexList+"^"+siteIndexList]
    
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
        
    