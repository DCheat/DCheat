from DCheat_Server.model.testInfo import TestInfo
from DCheat_Server.model.banList import BanList
from DCheat_Server.model.allowList import AllowList

'''
update Course Start date
'''
def modify_course(courseIndex, startDate, endDate):
    dao.query(TestInfo).\
        filter(TestInfo.index == courseIndex).\
        update(dict(startDate = startDate,
                    endDate = endDate))
        
def delete_ban_list_in_course(courseIndex):
    dao.query(BanList).\
        filter(BanList.testIndex == courseIndex).\
        update(dict(isDeleted = "TRUE"))
        
def modify_ban_list_in_course(courseIndex, banIndex):
    dao.query(BanList).\
        filter(BanList.testIndex == courseIndex,
               BanList.banIndex == banIndex).\
        update(dict(isDeleted = "FALSE"))
        
def delete_allow_list_in_course(courseIndex):
    dao.query(AllowList).\
        filter(AllowList.testIndex == courseIndex).\
        update(dict(isDeleted = "TRUE"))
        
def modify_allow_list_in_course(courseIndex, webIndex):
    dao.query(AllowList).\
        filter(AllowList.testIndex == courseIndex,
               AllowList.banIndex == webIndex).\
        update(dict(isDeleted = "FALSE"))