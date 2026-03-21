import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "57.131.33.181")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Pityboy@22")
    DB_NAME = os.getenv("DB_NAME", "trollzstorecom_tr0llz_db")

    # JWT
    JWT_SECRET = os.getenv("JWT_SECRET", "trollz_store_jwt_secret_key_2026")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 72))

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 4500))
