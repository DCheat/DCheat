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
                     
def select_user_info(userIndex):
    return dao.query(User.id,
                     User.name).\
              filter(User.index == userIndex).first()
def select_master_info(masterIndex):
    return dao.query(Master.id,
                     Master.email).\
              filter(Master.index == masterIndex).first()    
                     
def select_allow_site_list():
    return dao.query(AllowSite.siteURL,
                     AllowSite.siteName).all()

def select_allow_site_in_test():
    return dao.query(AllowSite.siteURL,
                     AllowSite.siteName).\
                join(TestInfo,
                     TestInfo.index == AllowList.testIndex).\
                join(AllowList,
                     AllowList.webIndex == AllowSite.index).all()
                    
def select_ban_program_in_test():
    return dao.query(BanProgram.processName,
                     BanProgram.processPath1,
                     BanProgram.processPath2,
                     BanProgram.processPort).\
                join(TestInfo,
                     TestInfo.index == BanList.testIndex).\
                join(BanList,
                     BanList.banIndex == BanProgram.index).all()

def select_unfinished_test_course_for_user():
    return dao.query(TestInfo.testName).\
                join(TestingUser,
                     TestingUser.testIndex == TestInfo.testIndex),\
                join(User,
                     User.index == TestingUser.userIndex).\
                filter(TestInfo.endDate > datetime(now)).all()
        
def select_unfinished_test_course_for_master():
    return dao.query(TestInfo.testName,
                     TestInfo.startDate,
                     TestInfo.endDate,
                     count(TestingUser.userIndex)).\
                join(Master,
                     Master.index == TestInfo.masterIndex).\
                join(TestingUser,
                     TestingUser.testIndex == TestInfo.index).\
                filter(TestInfo.endDate > datetime(now)).all()
                
def select_master_email():
    return dao.query(Master.emailAddress).\
                join(TestInfo,
                     TestInfo.masterIndex == Master.index).first()


    