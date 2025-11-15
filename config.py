import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key") 
    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URI  =  "postgresql://ysf:123@localhost:5432/chat_app"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SECERT_KEY: str = os.getenv("SECRET_KEY")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "def_dbURI"


