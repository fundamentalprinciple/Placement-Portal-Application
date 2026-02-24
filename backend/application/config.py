import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv, dotenv_values
load_dotenv()

class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")

    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
   
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_AUTHENTICATION_KEY = "auth_token"
    SECURITY_TOKEN_MAX_AGE = 3600
    SECURITY_PASSWORD_HASH = "bcrypt"     
    
    SECURITY_TOKEN_AUTHENTICATION = True
    SECURITY_API_ENABLED_METHODS = ["token"]
    SECURITY_JSON = True

    WTF_CSRF_ENABLED = False

    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/'

     
    
    
