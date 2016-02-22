'''
Insert Query
:copyright: (c) 2016 Lee Jong Seok
'''
from DCheat_Server.database import dao
from DCheat_Server.model.allowSite import AllowSite
from DCheat_Server.model.banProgram import BanProgram
from DCheat_Server.model.master import Master
'''
Insert Allow Site List
'''
def insert_allow_site(siteURL, siteName):
    return AllowSite(siteURL = siteURL,
                     siteName = siteName)

'''
Insert Ban Program List
'''
def insert_ban_program(programName, processName, processPath1, processPath2, processPort):
    return BanProgram(programName = programName,
                      processName = processName,
                      processPath1 = processPath1,
                      processPath2 = processPath2,
                      processPort = processPort)
    
'''
Insert Master
'''
def insert_master(id, password, emailAddress):
    return Master(id = id,
                  password = password,
                  emailAddress = emailAddress)