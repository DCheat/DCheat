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
from werkzeug.security import generate_password_hash


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
        from DCheat_Server.model.allowList import AllowList
        from DCheat_Server.model.allowSite import AllowSite
        from DCheat_Server.model.banList import BanList
        from DCheat_Server.model.banProgram import BanProgram
        from DCheat_Server.model.master import Master
        from DCheat_Server.model.testInfo import TestInfo
        from DCheat_Server.model.testingUser import TestingUser
        from DCheat_Server.model.user import User
        from DCheat_Server.model import Base
        #metadata 연결
        Base.metadata.create_all(bind = DBManager.__engine)

        # Init Date Input
        try:
            from datetime import datetime
            from werkzeug.security import generate_password_hash
            from DCheat_Server.DCheat_py3des import TripleDES
            TripleDES.init()
            from DCheat_Server.utils.insertQuery import insert_allow_site,\
                                                        insert_ban_program,\
                                                        insert_master
            dao.add(insert_allow_site("http://cyber2010.kookmin.ac.kr", "KMU CYBER CAMPUS"))
            dao.add(insert_allow_site("https://algolab.kookmin.ac.kr", "KMU GRADE SERVER"))
            dao.add(insert_ban_program("KakaoTalk", "KakaoTalk", "Kakao", "KakaoTalk", 5223))
            dao.add(insert_ban_program("LINE", "LINE", "LINE", "LINE", 443))
            dao.add(insert_ban_program("NATEON", "NateOnMain", "SK Communications", "NATEON", 5004))
            dao.add(insert_ban_program("Skype", "Skype", "Skype", "phone", 12350))
            dao.add(insert_ban_program("Tictoc", "Tictoc", "Tictoc", "bin", 23018))
            dao.add(insert_ban_program("Between", "couple", "Between", "0", 0))
            dao.add(insert_ban_program("Internet Explorer", "iexplorer", "Internet Explorer", "0", 0))
            dao.add(insert_ban_program("Chrome", "chrome", "Google", "Chrome", 0))
            dao.add(insert_ban_program("Firefox", "firefox", "Mozilla Firefox", "0", 0))
            dao.add(insert_master("algolab", generate_password_hash(TripleDES.encrypt(str('rhflwma5106!'))), 'hikoukigumo@naver.com'))
            dao.commit()
        except Exception as e:
            print(e)
            dao.rollback()

dao = None