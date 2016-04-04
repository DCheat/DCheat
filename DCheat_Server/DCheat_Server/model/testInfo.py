"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    test Info

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, ENUM

from DCheat_Server.model import Base
from DCheat_Server.model.master import Master
class TestInfo (Base) :
    
    __tablename__ = 'TestInfo'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    masterIndex = Column(INTEGER(unsigned = True),
                        ForeignKey(Master.index,
                                   onupdate = 'CASCADE',
                                   ondelete = 'CASCADE'),
                        autoincrement = True,
                        nullable =False)
    testName = Column(VARCHAR(255),
                 nullable = False,
                 unique = True)
    startDate = Column(DATETIME,
                         nullable = False)
    endDate = Column(DATETIME,
                         nullable = False)
    makeChart = Column(ENUM ('TRUE',
                             'FALSE'),
                       default = 'FALSE',
                       nullable = False)
    