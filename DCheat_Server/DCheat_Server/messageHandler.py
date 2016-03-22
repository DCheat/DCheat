import os
import socketserver
from DCheat_Server.database import dao
from werkzeug.security import check_password_hash
from DCheat_Server.DCheat_py3des import TripleDES
from DCheat_Server.utils.selectQuery import select_unfinished_test_course_for_user,\
                                            select_unfinished_test_course_for_master,\
                                            select_user_index,\
                                            select_master_index,\
                                            select_master_check,\
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


class ForkingRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
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
            elif data.find("SCL") != -1:
                self.request.close()
            #if data.find("SCS") != -1:
            #    testIndex = int(data.split()[0])
            #    programIndexList = select_ban_list_in_test(testIndex)
            #    siteIndexList = select_allow_site_index()
            #    return [programIndexList+"^"+siteIndexList]
    
    def login_handler(self, data):
        id = data.split(";")[2].split(",")[0]
        password = data.split(";")[2].split(",")[1]
        courses = ''
        
        if len(password) != 0:
            try:
                masterInfo = select_master_check(id)
                idIndex = masterInfo.index
                if check_password_hash(masterInfo.password, TripleDES.encrypt(str(password))) is False:
                    self.request.send('0'.encode('utf-8'))
                    return
            except:
                self.request.send('0'.encode('utf-8'))
                return
            try:
                courseList = select_unfinished_test_course_for_master(idIndex)
                for courseInfo in courseList:
                    banList = select_ban_list_index(courseInfo.index)
                    allowList = select_allow_list_index(courseInfo.index)
                    str(banList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',','*')
                    str(allowList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',','*')
                    courseData = courseInfo.testName + "," + courseInfo.startDate + "," + courseInfo.endDate + "," + banList  + allowList + str(courseInfo[4])
                                 
                    courses = courses + '^' + courseData
                    
            except:
                courseList = ''
                
            courses.lstrip('^')
        
        else:
            try:
                idIndex = select_user_index(id)
            except:
                self.request.send('0'.encode('utf-8'))
                return
            
            try:
                courseList = select_unfinished_test_course_for_user(idIndex)
                courses = str(courseList).strip('[]').replace(' ', '')
            except:
                self.request.send('-1'.encode('utf-8'))
                return
            
        sendData = str(idIndex)+"^"+courses
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
        addList = data.split(";")[2].split(",")
        courseName = addList[0]
        startDate = addList[1]
        endDate = addList[2]
        banList = addList[3].split("*")
        allowList = addList[4].split("*")
        userList = addList[5].split("*")
        print(masterIndex,courseName,startDate, endDate, banList, allowList, userList)
        try:
            dao.add(insert_course(masterIndex, courseName, startDate, endDate))
            dao.commit()
        except Exception as e:
            dao.rollback()
            print(e)
            self.request.send("2".encode('utf-8'))
            return 
        testIndex = select_course_index(courseName)

        if len(userList[0]) is not 0:
            for userInfo in userList:
                userInfo = userInfo.split('$')
                try:
                    userIndex = select_user_index(userInfo[0])
                except:
                    try:
                        dao.add(insert_user(userInfo[0], userInfo[1]))
                    except Exception as e:
                        dao.rollback()
                        print(e)
                        self.request.send("0".encode('utf-8'))
                        return
                    dao.commit()
                    userIndex = select_user_index(userInfo[0])
                dao.add(insert_user_in_course(testIndex, userIndex))

        if len(banList[0]) is not 0:
            for banProgram in banList:
                dao.add(insert_ban_list_in_course(testIndex, int(banProgram)))

        if len(allowList[0]) is not 0:
            for allowSite in allowList:
                dao.add(insert_allow_list_in_course(testIndex, int(allowSite)))
        dao.commit()
        self.request.send("1".encode('utf-8'))

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
        for webIndex in allowList:
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
    def send_email_handler():
        return
        
    
