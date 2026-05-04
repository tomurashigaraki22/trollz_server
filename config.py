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

    # Flutterwave Configuration
    FLUTTERWAVE_PUBLIC_KEY = os.getenv("FLUTTERWAVE_PUBLIC_KEY", "FLWPUBK-9dfb0a099633cdea36091144c4ab90a1-X")
    FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY", "")
    FLUTTERWAVE_ENCRYPTION_KEY = os.getenv("FLUTTERWAVE_ENCRYPTION_KEY", "")

    # Sendbox API Configuration (Legacy - keeping for backward compatibility)
    SENDBOX_STAGING_URL = "https://sandbox.staging.sendbox.co"
    SENDBOX_LIVE_URL = "https://live.sendbox.co"
    SENDBOX_API_KEY = os.getenv("SENDBOX_API_KEY", "")
    SENDBOX_ENVIRONMENT = os.getenv("SENDBOX_ENV", "live")  # staging or live

    @staticmethod
    def get_sendbox_base_url():
        """Get the appropriate Sendbox base URL based on environment."""
        if Config.SENDBOX_ENVIRONMENT == "live":
            return Config.SENDBOX_LIVE_URL
        return Config.SENDBOX_STAGING_URL
    
    # Terminal Africa API Configuration
    TERMINAL_TEST_PUBLIC_KEY = "pk_test_WeDJ1I1cKKkubg60rE6kXnwPJXlExlH1"
    TERMINAL_TEST_SECRET_KEY = "sk_test_metpCNX6TbGcuf8yy2h8DUvSwLTkAncn"
    TERMINAL_LIVE_PUBLIC_KEY = "pk_live_G8zfsoShEtgvDPUvHABwdF9Lw4a65HKg"
    TERMINAL_LIVE_SECRET_KEY = "sk_live_jiep2FyoHX3tImNV4eVkdVl1SXIHrFWM"
    TERMINAL_ENVIRONMENT = os.getenv("TERMINAL_ENV", "test")  # test or live (default: test)
    
    @staticmethod
    def get_terminal_base_url():
        """Get the appropriate Terminal base URL based on environment."""
        if Config.TERMINAL_ENVIRONMENT == "live":
            return "https://api.terminal.africa/v1"
        return "https://sandbox.terminal.africa/v1"
    
    @staticmethod
    def get_terminal_secret_key():
        """Get the appropriate Terminal secret key based on environment."""
        if Config.TERMINAL_ENVIRONMENT == "live":
            return Config.TERMINAL_LIVE_SECRET_KEY
        return Config.TERMINAL_TEST_SECRET_KEY
    
    @staticmethod
    def get_terminal_public_key():
        """Get the appropriate Terminal public key based on environment."""
        if Config.TERMINAL_ENVIRONMENT == "live":
            return Config.TERMINAL_LIVE_PUBLIC_KEY
        return Config.TERMINAL_TEST_PUBLIC_KEY

    # Warehouse/Origin Address Configuration
    WAREHOUSE_FIRST_NAME = os.getenv("WAREHOUSE_FIRST_NAME", "Trollz Store")
    WAREHOUSE_LAST_NAME = os.getenv("WAREHOUSE_LAST_NAME", "Warehouse")
    WAREHOUSE_STREET = os.getenv("WAREHOUSE_STREET", "LYPAS Plaza, Cluster Industrial Complex")
    WAREHOUSE_STREET_LINE_2 = os.getenv("WAREHOUSE_STREET_LINE_2", "")
    WAREHOUSE_CITY = os.getenv("WAREHOUSE_CITY", "Owerri")
    WAREHOUSE_STATE = os.getenv("WAREHOUSE_STATE", "Imo")
    WAREHOUSE_COUNTRY = os.getenv("WAREHOUSE_COUNTRY", "NG")
    WAREHOUSE_POST_CODE = os.getenv("WAREHOUSE_POST_CODE", "460001")
    WAREHOUSE_PHONE = os.getenv("WAREHOUSE_PHONE", "+234 800 000 0000")
    WAREHOUSE_EMAIL = os.getenv("WAREHOUSE_EMAIL", "warehouse@trollzstore.com")

    @staticmethod
    def get_warehouse_address():
        """Get warehouse address as a dictionary for Sendbox API."""
        return {
            "first_name": Config.WAREHOUSE_FIRST_NAME,
            "last_name": Config.WAREHOUSE_LAST_NAME,
            "street": Config.WAREHOUSE_STREET,
            "street_line_2": Config.WAREHOUSE_STREET_LINE_2,
            "city": Config.WAREHOUSE_CITY,
            "state": Config.WAREHOUSE_STATE,
            "country": Config.WAREHOUSE_COUNTRY,
            "post_code": Config.WAREHOUSE_POST_CODE,
            "phone": Config.WAREHOUSE_PHONE,
            "email": Config.WAREHOUSE_EMAIL,
            "name": None,
            "lng": None,
            "lat": None
        }
