"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할  관리자 정보

"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from DCheat_Server.model import Base

class Master (Base) :
    
    __tablename__ ='Master'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    id =  Column(VARCHAR(255),
                 nullable = False,
                 unique = True)
    password = Column(VARCHAR(255),
                      nullable =False)
    emailAddress = Column(VARCHAR(255),
                          nullable =True)
    