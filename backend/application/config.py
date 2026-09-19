import os

basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()


class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )
        elif DATABASE_URL.startswith("postgresql://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgresql://",
                "postgresql+psycopg://",
                1
            )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")
    )

    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    CELERY_BROKER_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    CELERY_RESULT_BACKEND = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.mailtrap.io"
    )

    MAIL_PORT = int(os.getenv('MAIL_PORT', 2525))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
