import os
import socketserver
from socketserver import ThreadingTCPServer
from DCheat_Server.messageHandler import ForkingRequestHandler

class ForkingServer(ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == '__main__':

        # 데이터베이스 처리 
    from DCheat_Server.database import DBManager
    try:
        DBManager.init("mysql+pymysql://root:dkfrhflwma@localhost/DCheat")
        DBManager.init_db()

    except Exception as e:
        print(e)
    
    from DCheat_Server.utils.selectQuery import select_allow_site_list,\
                                                select_master_email,\
                                                select_allow_site_in_test,\
                                                select_ban_program_in_test,\
                                                select_unfinished_test_course_for_user,\
                                                select_unfinished_test_course_for_master,\
                                                select_course_index,\
                                                select_allow_list_index,\
                                                select_ban_list_index
    allowSiteList = select_allow_site_list()
    emailAddress = select_master_email()
    allowSiteListInTest = select_allow_site_in_test()
    banProgramInTest = select_ban_program_in_test()
    unfinishedTestCourseForUser = select_unfinished_test_course_for_user(1)
    unfinishedTestCourseForMaster = select_unfinished_test_course_for_master()
    print(str(unfinishedTestCourseForMaster).strip('[]').replace(' ', ''))
    temp = ''
    for i in unfinishedTestCourseForMaster:
        temp = i.testName+","+str(i.startDate)+","+str(i.endDate)
    print(temp)
    print(select_unfinished_test_course_for_user(1))
    testIndex = select_course_index('test1')
    siteListIndexInTest = select_allow_list_index(testIndex)
    banListIndexInTest = select_ban_list_index(testIndex)
    print(str(siteListIndexInTest).strip('[]').replace(' ','').replace('(','').replace(',)',''))
    print(str(banListIndexInTest).strip('[]').replace(' ','').replace('(','').replace(',)',''))
    
    address = ('', 9410)  # let the kernel assign a portf
    server = ForkingServer(address,
                               ForkingRequestHandler)
    ip, port = server.server_address  # what port was assigned?

    print('Server loop running in process:', os.getpid())
    server.serve_forever()

    # Clean up
    #server.shutdown()
    #server.socket.close()