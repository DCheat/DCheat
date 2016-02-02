"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ban program

"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from DCheat_Server.model import Base

class BanProgram (Base) :
    
    __tablename__ = 'BanProgram'
    
    index = Column(INTEGER(unsigned = True),
            primary_key = True,
            autoincrement = True,
            nullable = False)
    programName = Column(VARCHAR(1024),
                 nullable = False,
                 unique = True)
    processName = Column(VARCHAR(1024),
                 nullable = False)
    processPath = Column(VARCHAR(1024),
                 nullable = False)
    processPort = Column(INTEGER(unsigned = True),
                 nullable = False)