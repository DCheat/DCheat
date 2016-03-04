import os
import socketserver

class ForkingRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        from DCheat_Server.utils.selectQuery import select_unfinished_test_course_for_user,\
                                            select_user_index,\
                                            select_course_index,\
                                            select_allow_list_index,\
                                            select_ban_list_index
        # Echo the back to the client
        data = self.request.recv(4096)
        data = data.decode()
        cur_pid = os.getpid()
        response = bytes('%d: %s' % (cur_pid, data), 'utf-8')
        self.request.send(response)
        print("AAAAA")
        if data.find("SIN") != -1:
            login_handler(data)
        elif data.find("SCS") != -1:
            select_course(data)
        #if data.find("SCS") != -1:
        #    testIndex = int(data.split()[0])
        #    programIndexList = select_ban_list_in_test(testIndex)
        #    siteIndexList = select_allow_site_index()
        #    return [programIndexList+"^"+siteIndexList]
    
    def login_handler(self, data):
        userId = data.split(";")[2]
        sendData = ''
        try:
            userIndex = select_user_index(userId)
        except:
            return 0
        courseList = select_unfinished_test_course_for_user(userIndex)
        courseList = str(courseList).strip('[]').replace(' ', '')
        sendData = userIndex+"^"+courseList
        return sendData
    
    def select_course(self, data):
        courseName = data.split(":")[2]
        sendData = ''
        courseIndex = select_course_index(courseName)
        siteIndexList = select_allow_list_index(courseIndex)
        siteIndexList = str(siteIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','')
        programIndexList = select_ban_list_index(courseIndex)
        programIndexList = str(programIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','')
        sendData = programIndexList+"^"+siteIndexList
        return sendData
    
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
        
    