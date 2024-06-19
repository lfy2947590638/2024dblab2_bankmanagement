import os
SECRET_KEY = os.urandom(24)
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1651511154'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'lfyzy@20230724'
    MYSQL_DB = 'BankManagementSystem'
    MYSQL_CURSORCLASS = 'DictCursor'  # 使得查询返回字典形式