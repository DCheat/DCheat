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
    programName = Column(VARCHAR(255),
                 nullable = False,
                 unique = True)
    processName = Column(VARCHAR(255),
                 nullable = False)
    processPath1 = Column(VARCHAR(255),
                 default = "0",
                 nullable = False)
    processPath2 = Column(VARCHAR(255),
                 default = "0",
                 nullable = False)
    processPort = Column(INTEGER(unsigned = True),
                 default = 0,
                 nullable = False)