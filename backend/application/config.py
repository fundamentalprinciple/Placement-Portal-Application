import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv, dotenv_values
load_dotenv()

class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")

    WTF_CSRF_ENABLED = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
