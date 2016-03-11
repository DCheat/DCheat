import os
import socketserver

class ForkingRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        from DCheat_Server.utils.selectQuery import select_unfinished_test_course_for_user,\
                                            select_user_index,\
                                            select_master_index,\
                                            select_course_index,\
                                            select_course,\
                                            select_allow_list_index,\
                                            select_ban_list_index
        from DCheat_Server.utils.insertQuery import insert_allow_list_in_course,\
                                                    insert_ban_list_in_course,\
                                                    insert_course,\
                                                    insert_user_in_course,\
                                                    insert_user
        from DCheat_Server.utils.updateQuery import modify_course,\
                                                    delete_ban_list_in_course,\
                                                    modify_ban_list_in_course,\
                                                    delete_allow_list_in_course,\
                                                    modify_allow_list_in_course
                                                    
        # Echo the back to the client
        data = self.request.recv(4096)
        data = data.decode()
        
        print("AAAAA")
        if data.find("SIN") != -1:
            self.login_handler(data)
        elif data.find("SCS") != -1:
            self.select_course(data)
        elif data.find("ACS") != -1:
            self.master_add_course_handler(data)
        elif data.find("UCS") != -1:
            self.master_modify_course_handler(data)
        #if data.find("SCS") != -1:
        #    testIndex = int(data.split()[0])
        #    programIndexList = select_ban_list_in_test(testIndex)
        #    siteIndexList = select_allow_site_index()
        #    return [programIndexList+"^"+siteIndexList]
    
    def login_handler(self, data):
        id = data.split(";")[2].split(",")[0]
        password = data.split(";")[2].split(",")[1]
        sendData = ''
        try:
            if password.len != 0:
                idIndex = select_master_index(id)
                courseList = select_unfinished_test_course_for_master(idIndex)
            else:
                idIndex = select_user_index(id)
                courseList = select_unfinished_test_course_for_user(idIndex)
        except:
            return 0
        courseList = str(courseList).strip('[]').replace(' ', '')
        sendData = idIndex+"^"+courseList
        self.request.send(sendData.encode('utf-8'))
    
    def select_course(self, data):
        courseName = data.split(";")[2]
        sendData = ''
        courseIndex = select_course_index(courseName)
        siteIndexList = select_allow_list_index(courseIndex)
        siteIndexList = str(siteIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','')
        programIndexList = select_ban_list_index(courseIndex)
        programIndexList = str(programIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','')
        sendData = programIndexList+"^"+siteIndexList
        self.request.send(sendData.encode('utf-8'))
    
    def master_add_course_handler(self, data):
        masterIndex = int(data.split(";")[0])
        addList = data.split(";")[2].split("^")
        courseName = addList[0]
        startDate = addList[1].split(",")[0]
        endDate = addList[1].split(",")[1]
        banList = addList[2].replace(",", '')
        allowList = addList[3].replace(",", '')
        userList = addList[4].split("$")
        try:
            dao.add(insert_course(masterIndex, courseName, startDate, endDate))
            dao.commit()
        except:
            dao.rollback()
            return 
        testIndex = select_course_index(courseName)
        for userInfo in userList:
            try:
                userIndex = select_user_index(userInfo[0])
            except:
                try:
                    dao.add(insert_user(userInfo[0], userInfo[2]))
                except:
                    dao.rollback()
                    return
                dao.commit()
                userIndex = select_user_index(userInfo[0])
                dao.add(insert_user_in_course(testIndex, userIndex))
        for banProgram in banList:
            dao.add(insert_ban_list_in_course(testIndex, int(banProgram)))
        for allowSite in allowList:
            dao.add(inset_allow_list_in_course(testIndex, int(allowSite)))
        dao.commit()
        return
    def master_modify_course_handler(self, data):
        masterIndex = int(data.split(";")[0])
        updateList = data.split(";")[2].split("^")
        startDate = updateList[0].split(",")[0]
        endDate = updateList[0].split(",")[1]
        banList = updateList[1].replace(",", '')
        allowList = updateList[2].replace(",", '')
        userList = updateList[3].split("$")
        courseIndex = select_course(masterIndex)
        modify_course(startDate = startDate,
                      endDate = endDate)
        try:
            dao.commit()
        except:
            dao.rollback()
        try:
            delete_ban_list_in_course(courseIndex)
            delete_allow_list_in_course(courseIndex)
            dao.commit()
        except:
            dao.rollback()
        for banIndex in banList:
            try:
                modify_ban_list_in_course(courseIndex, int(banIndex))
            except:
                insert_ban_list_in_course(courseIndex, int(banIndex))
        for webIndex in AllowList:
            try:
                modify_allow_list_in_course(courseIndex, int(webIndex))
            except:
                modify_allow_list_in_course(courseIndex, int(webIndex))
        for userInfo in userList:
            try:
                userIndex = select_user_index(userInfo[0])
            except:
                dao.add(insert_user(userInfo[0], userInfo[2]))
                dao.commit()
                userIndex = select_user_index(userInfo[0])
                dao.add(insert_user_in_course(testIndex, userIndex))
                
        return 
    def sign_up_handler():
        return
    def user_allow_ban_list_handler():
        return
    def send_email_handler():
        return
        
    