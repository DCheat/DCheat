from DCheat_Server.database import DBManager

try:
    DBManager.init("mysql+pymysql://root:dkfrhflwma@localhost/DCheat")
    DBManager.init_db()

except Exception as e:
    print(e)