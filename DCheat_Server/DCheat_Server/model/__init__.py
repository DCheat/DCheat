"""
    DCheat_server.model
    ~~~~~~~~~~~~~~

    DCheat_server에 적용될 model에 대한 패키지 초기화 모듈.

    :copyright: (c) 2016 Lee Jong Seok
"""


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['master', 'user', 'banList', 'banProgram', 'testInfo', 'testingUser', 'allowList', 'allowSite']