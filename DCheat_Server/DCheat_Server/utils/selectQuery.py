'''
Select Query
:copyright: (c) 2016 Lee Jong Seok
'''
from DCheat_Server.database import dao
from DCheat_Server.model.banProgram import BanProgram
from DCheat_Server.model.banList import BanList
from DCheat_Server.model.allowSite import AllowSite
from DCheat_Server.model.allowList import AllowList
from DCheat_Server.model.testInfo import TestInfo
from DCheat_Server.model.user import User
from DCheat_Server.model.testingUser import TestingUser
from DCheat_Server.model.master import Master
from datetime import datetime
from sqlalchemy import func, and_
                     
def select_user_info(userIndex):
    return dao.query(User.id,
                     User.name).\
              filter(User.index == userIndex).first()

def select_user_index(userId):
    return dao.query(User.index).\
              filter(User.id == userId).first().userIndex      
              
def select_master_info(masterIndex):
    return dao.query(Master.id,
                     Master.email).\
              filter(Master.index == masterIndex).first()
              
def select_course_index(courseName):
    return dao.query(TestInfo.index).\
              filter(TestInfo.testName == courseName).first().index
              
def select_course(masterIndex):
    return dao.query(TestInfo.index).\
              filter(TestInfo.masterIndex == masterIndex).first().index   
        
def select_allow_site_list():
    return dao.query(AllowSite.siteURL,
                     AllowSite.siteName).all()

def select_allow_list_index(testIndex):
    return dao.query(AllowList.webIndex).\
              filter(AllowList.testIndex == testIndex).all()

def select_allow_site_in_test():
    return dao.query(AllowSite.siteURL,
                     AllowSite.siteName).\
                join(AllowList,
                     AllowList.webIndex == AllowSite.index).\
                join(TestInfo,
                     TestInfo.index == AllowList.testIndex).all()
                     
def select_ban_list_index(testIndex):
    return dao.query(BanList.banIndex).\
              filter(BanList.testIndex == testIndex).all()
                    
def select_ban_program_in_test():
    return dao.query(BanProgram.processName,
                     BanProgram.processPath1,
                     BanProgram.processPath2,
                     BanProgram.processPort).\
                join(BanList,
                     BanList.banIndex == BanProgram.index).\
                join(TestInfo,
                     TestInfo.index == BanList.testIndex).all()
            
def select_ban_list_in_test(testIndex):
    return dao.query(BanList.banIndex).all()

def select_unfinished_test_course_for_user(userIndex):
    return dao.query(TestInfo.testName).\
                join(TestingUser,
                     TestingUser.testIndex == TestInfo.index).\
                join(User,
                     User.index == userIndex).\
                filter(and_(TestInfo.endDate > datetime.now(),
                            TestInfo.startDate <= datetime.now())).all()
        
def select_unfinished_test_course_for_master():
    return dao.query(TestInfo.testName,
                     TestInfo.startDate,
                     TestInfo.endDate,
                     func.count(TestingUser.userIndex)).\
                join(TestingUser,
                     TestingUser.testIndex == TestInfo.index).\
                join(Master,
                     Master.index == TestInfo.masterIndex).\
                filter(TestInfo.endDate > datetime.now()).all()
                
def select_master_email():
    return dao.query(Master.emailAddress).\
                join(TestInfo,
                     TestInfo.masterIndex == Master.index).first()


    