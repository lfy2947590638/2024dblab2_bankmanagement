from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)
app.secret_key = '1651511154'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lfyzy@20230724'
app.config['MYSQL_DB'] = 'BankManagementSystem'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['UPLOAD_FOLDER'] = 'lab2/app/static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SECRET_KEY'] = '1651511154'

mysql = MySQL(app)

from app import routes
