
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-key-change-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/travel_db?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
