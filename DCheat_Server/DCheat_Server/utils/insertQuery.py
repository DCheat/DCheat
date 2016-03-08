'''
Insert Query
:copyright: (c) 2016 Lee Jong Seok
'''
from DCheat_Server.database import dao
from DCheat_Server.model.allowSite import AllowSite
from DCheat_Server.model.allowList import AllowList
from DCheat_Server.model.banProgram import BanProgram
from DCheat_Server.model.banList import BanList
from DCheat_Server.model.user import User
from DCheat_Server.model.testingUser import TestingUser
from DCheat_Server.model.testInfo import TestInfo 
from DCheat_Server.model.master import Master
'''
Insert Allow Site
'''
def insert_allow_site(siteURL, siteName):
    return AllowSite(siteURL = siteURL,
                     siteName = siteName)

'''
Insert Allow Site List in Course

'''
def insert_allow_list_in_course(testIndex, webIndex):
    return AllowList(testIndex = testIndex,
                     webIndex = webIndex)
    
'''   
Insert Ban Program
'''
def insert_ban_program(programName, processName, processPath1, processPath2, processPort):
    return BanProgram(programName = programName,
                      processName = processName,
                      processPath1 = processPath1,
                      processPath2 = processPath2,
                      processPort = processPort)

'''
Insert Ban Program List in Course
'''
def insert_ban_list_in_course(testIndex, banIndex):
    return BanList(testIndex = testIndex,
                   banIndex = banIndex)

'''
Insert Course
'''
def insert_course(masterIndex, testName, startDate, endDate):
    return TestInfo(masterIndex = masterIndex,
                    testName = testName,
                    startDate = startDate,
                    endDate = endDate)

'''
Insert User In Course
'''
def insert_user_in_course(testIndex, userIndex):
    return TestingUser(testIndex = testIndex,
                       userIndex = userIndex)
    
'''
Insert Master
'''
def insert_master(id, password, emailAddress):
    return Master(id = id,
                  password = password,
                  emailAddress = emailAddress)
    
'''
Insert User
'''
def insert_user(id, name):
    return User(id = id,
                name = name)