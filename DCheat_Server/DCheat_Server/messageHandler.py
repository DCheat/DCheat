import socketserver

from werkzeug.security import check_password_hash

from DCheat_Server.DCheat_py3des import TripleDES
from DCheat_Server.database import dao
from DCheat_Server.tasks import send_mail
from DCheat_Server.utils.insertQuery import insert_allow_list_in_course,\
                                            insert_ban_list_in_course,\
                                            insert_course,\
                                            insert_user_in_course,\
                                            insert_user
from DCheat_Server.utils.selectQuery import select_unfinished_test_course_for_user,\
                                            select_unfinished_test_course_for_master,\
                                            select_user_index,\
                                            select_user_process_info, \
                                            select_master_check,\
                                            select_course_index, \
                                            select_allow_list_index,\
                                            select_ban_list_index,\
                                            select_user_count,\
                                            select_user_info,\
                                            select_master_email,\
                                            select_ban_program_name,\
                                            select_user_in_course
from DCheat_Server.utils.updateQuery import modify_course,\
                                            delete_ban_list_in_course,\
                                            modify_ban_list_in_course,\
                                            delete_allow_list_in_course,\
                                            modify_allow_list_in_course,\
                                            update_user_process_info


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
            elif data.find("PCH") != -1:
                self.send_email_handler(data)
            elif data.find("SCL") != -1:
                self.user_logout_handler(data)
                break
          
        return
    
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
                    userCount = select_user_count(courseInfo.index)
                    banList = select_ban_list_index(courseInfo.index)
                    allowList = select_allow_list_index(courseInfo.index)
                    
                    banList = str(banList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',','*')
                    allowList = str(allowList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',','*')
                    
                    courseData = courseInfo.testName + "," + str(courseInfo.startDate) + "," + str(courseInfo.endDate) + "," + banList  + "," + allowList + "," + str(userCount)
                                 
                    courses = courses + '^' + courseData
            except:
                courses = ''                    
            
                
            courses = courses.lstrip('^')
        
        else:
            try:
                idIndex = select_user_index(id)
            except:
                self.request.send('0'.encode('utf-8'))
                return
            
            try:
                courseList = select_unfinished_test_course_for_user(idIndex)
                if len(courseList) is 0:
                  self.request.send('-1'.encode('utf-8'))
                  return
                courses = str(courseList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace("'", '')
            except:
                self.request.send('-1'.encode('utf-8'))
                return
            
        sendData = str(idIndex)+"^"+courses
        self.request.send(sendData.encode('utf-8'))
        
    def user_logout_handler(self, data):
        userIndex = int(data.split(";")[0])
        courseName = data.split(";")[2]
        processList = data.split(":")[3].split(",")[1]
        courseIndex = select_course_index(courseName)
        processInfo = ''
            
        if len(processList) is not 0:
            try:
                processInfo = select_user_process_info(courseIndex, userIndex)
                processList = processList.split("*")
                for process in processList:
                    if processInfo.find(process) == -1:
                        processInfo = processInfo + "*" + process
                update_user_process_info(courseIndex, userIndex, processInfo)
                                        
            except:
                update_user_process_info(courseIndex, userIndex, processList)
        
        self.request.send('1'.encode('utf-8'))
        self.request.close()
        return
    
    def select_course(self, data):
        courseName = data.split(";")[2]
        sendData = ''
        courseIndex = select_course_index(courseName)
        siteIndexList = select_allow_list_index(courseIndex)
        siteIndexList = str(siteIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',', '*')
        programIndexList = select_ban_list_index(courseIndex)
        programIndexList = str(programIndexList).strip('[]').replace(' ','').replace('(','').replace(',)','').replace(',', '*')
        sendData = programIndexList+","+siteIndexList
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
            try:
                dao.add(insert_course(masterIndex, courseName, startDate, endDate))
                dao.commit()
            except Exception as e:
                dao.rollback()
                print(e)
                self.request.send("0".encode('utf-8'))
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
                            dao.commit()
                        except Exception as e:
                            dao.rollback()
                            print(e)
                            self.request.send("-1".encode('utf-8'))
                            return
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
        except Exception as e:
            print(e)
            dao.rollback()
            self.request.send("0".encode('utf-8'))

    def master_modify_course_handler(self, data):
        updateList = data.split(";")[2].split(",")
        courseName = updateList[0]
        startDate = updateList[1]
        endDate = updateList[2]
        banList = updateList[3].split("*")
        allowList = updateList[4].split("*")
        userList = updateList[5].split("*")
        courseIndex = select_course_index(courseName)

        try:
            if len(userList) is not 0:
                for userInfo in userList:
                    userInfo = userInfo.split('$')

                    try:
                        userIndex = select_user_index(userInfo[0])
                    except:
                        dao.add(insert_user(userInfo[0], userInfo[1]))
                        dao.commit()
                        userIndex = select_user_index(userInfo[0])
                    try:
                        tempIndex = select_user_in_course(courseIndex, userIndex)
                    except Exception as e:
                        dao.add(insert_user_in_course(courseIndex, userIndex))
                        dao.commit()

                delete_ban_list_in_course(courseIndex)
                delete_allow_list_in_course(courseIndex)

                dao.commit()
        except Exception as e:
            dao.rollback()
            self.request.send("-1".encode('utf-8'))
            return

        try:
            modify_course(courseName = courseName,
                          startDate = startDate,
                          endDate = endDate)

            if len(banList[0]) is not 0:
                for banIndex in banList:
                    try:
                        modify_ban_list_in_course(courseIndex, int(banIndex))
                    except:
                        insert_ban_list_in_course(courseIndex, int(banIndex))

            if len(allowList[0]) is not 0:
                for webIndex in allowList:
                    try:
                        modify_allow_list_in_course(courseIndex, int(webIndex))
                    except:
                        insert_allow_list_in_course(courseIndex, int(webIndex))

            dao.commit()
        except:
            dao.rollback()
            self.request.send("-1".encode('utf-8'))
            return
        try:
            userCount = select_user_count(courseIndex)
        except Exception as e:
            self.request.send("-1".encode('utf-8'))

        self.request.send(str(userCount).encode('utf-8'))
        
    def sign_up_handler(self, data):
        return
    def send_email_handler(self, data):
        try:
            info = data.split(";")
            userIndex = int(info[0])
            programInfo = info[2].split(',')
            userInfo = select_user_info(userIndex)
            mailAddress = select_master_email(programInfo[2])[0]
            programName = select_ban_program_name(programInfo[0])[0]
            send_mail.delay(userInfo[0], userInfo[1], programName, programInfo[1], mailAddress)
        except Exception as e:
            print(e)
        return
