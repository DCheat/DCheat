"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    allow List

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from DCheat_Server.model import Base
from DCheat_Server.model.testInfo import TestInfo
from DCheat_Server.model.allowSite import AllowSite

class AllowList (Base) :
    
    __tablename__ ='AllowList'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    testIndex =  Column(INTEGER(unsigned = True),
                        ForeignKey(TestInfo.index,
                                   onupdate = 'CASCADE',
                                   ondelete = 'CASCADE'),
                 nullable = False)
    webIndex = Column(INTEGER(unsigned = True),
                      ForeignKey(AllowSite.index,
                                 onupdate = 'CASCADE',
                                 ondelete = 'CASCADE'),
                      nullable =False)
    isDeleted = Column(ENUM ('TRUE',
                             'FALSE'),
                       default = 'FALSE',
                       nullable = False)