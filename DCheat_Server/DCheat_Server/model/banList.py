"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ban List

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from DCheat_Server.model import Base
from DCheat_Server.model.testInfo import TestInfo
from DCheat_Server.model.banProgram import BanProgram

class BanList (Base) :
    
    __tablename__ = 'BanList'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    testIndex =  Column(INTEGER(unsigned = True),
                        ForeignKey(TestInfo.index,
                                   onupdate = 'CASCADE',
                                   ondelete = 'CASCADE'),
                 nullable = False)
    banIndex = Column(INTEGER(unsigned = True),
                      ForeignKey(BanProgram.index,
                                 onupdate = 'CASCADE',
                                 ondelete = 'CASCADE'),
                      nullable =False)
    isDeleted = Column(ENUM ('TRUE',
                             'FALSE'),
                       default = 'FALSE',
                       nullable = False)