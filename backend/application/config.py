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

