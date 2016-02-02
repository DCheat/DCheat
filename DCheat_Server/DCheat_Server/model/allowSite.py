"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    allow site

"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from DCheat_Server.model import Base

class AllowSite (Base) :
    
    __tablename__ = 'AllowSite'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    siteURL =  Column(VARCHAR(1024),
                 nullable = False)
    siteName = Column(VARCHAR(1024),
                      nullable =False,
                      unique = True)
    