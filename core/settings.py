from core.logger_config import LOGGER_CONFIG as LOGGER_CFG

class Settings:
    # DB Setup
    DB_USER: str = 'userDB'
    DB_PASSWORD = 'passwordDB'
    DB_SERVER: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'wbTestTask'
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

    # JWT Settings
    SECRET_KEY = 'ed546f271d436aeed02cb1b6e7ba496eba424e48d56bf6398e320c7100a280aa'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*30

    # Logger Configuration
    LOGGER_CONFIG = LOGGER_CFG


settings = Settings()
