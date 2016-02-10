# -*- coding: utf-8 -*-
"""
    DCheat.database
    ~~~~~~~~~~~~~~~~~
    DB 연결 및 쿼리 사용을 위한 공통 모듈.
    :copyright: (c)
    :license: MIT LICENSE 2.0, see license for more details.
"""

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import scoped_session, sessionmaker


class DBManager:
    """데이터베이스 처리를 담당하는 공통 클래스"""
    
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag = False, recycle_time = 3600):
        # 세션 생성 초기화
        DBManager.__engine = create_engine(db_url,
                                           pool_recycle = recycle_time,
                                           echo = db_log_flag)
        # DATABASE Not exist case
        if not database_exists(DBManager.__engine.url):
            # Creatre Database
            create_database(DBManager.__engine.url)
            
            DBManager.__engine = create_engine(db_url,
                                               pool_recycle = recycle_time,
                                               echo = db_log_flag)
            
        DBManager.__session = scoped_session(sessionmaker(autocommit = False, 
                                                          autoflush = False, 
                                                          bind = DBManager.__engine))

        # 전역 변수로 선언
        global dao
        dao = DBManager.__session
    
    @staticmethod
    def init_db():
#         from DCheat_Server.model import *
        from DCheat_Server.model import Base
        #metadata 연결
        Base.metadata.create_all(bind = DBManager.__engine)

        # Init Date Input
#         from datetime import datetime
#             from werkzeug.security import generate_password_hash
#             
#             from GradeServer.utils.utilUserQuery import insert_members,\
#                                                         insert_member_id,\
#                                                         insert_organization,\
#                                                         select_match_organization,\
#                                                         select_match_member_id
#             from GradeServer.utils.utilCourseQuery import insert_language
#             from GradeServer.resource.setResources import SETResources
#             
#             from GradeServer.utils.parameter.memberParameter import MemberParameter
            
#         from GradeServer.GradeServer_py3des import TripleDES
        
    dao = None