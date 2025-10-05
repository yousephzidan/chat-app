import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECERT_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key") 
    DEBUG: bool = False
    TESTING: bool = False
    DB_URI = os.getenv("DB_URI", "postgresql://postgres:root@localhost:5432/chat_app")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DB_URI = os.getenv("DB_URI")
    SECERT_KEY: str = os.getenv("SECRET_KEY")

class TestingConfig(Config):
    TESTING = True
    DB_URI = "def_dbURI"