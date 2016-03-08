from DCheat_Server.model.testInfo import TestInfo

'''
update Course Start date
'''
def modify_course(courseIndex, startDate, endDate):
    dao.query(TestInfo).\
        filter(TestInfo.index == courseIndex).\
        update(dict(startDate = startDate,
                    endDate = endDate))
    