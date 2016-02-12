"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할  사용자 정보

"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from DCheat_Server.model import Base

class User (Base) :
    
    __tablename__ ='User'
    
    index = Column(INTEGER(unsigned = True),
            primary_key =True,
            autoincrement = True,
            nullable =False)
    id =  Column(VARCHAR(255),
                 nullable = False,
                 unique = True)
    name = Column(VARCHAR(255),
                      nullable =False)
    