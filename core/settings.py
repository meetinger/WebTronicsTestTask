from core.logger_config import LOGGER_CONFIG as LOGGER_CFG

class Settings:
    #Root URL:
    ROOT_URL = 'http://localhost:8000/'

    # DB Setup
    DB_USER: str = 'userDB'
    DB_PASSWORD = 'passwordDB'
    DB_SERVER: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'wbTestTask'
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"

    # DB Test Setup
    DB_TEST_USER: str = 'userDB_Test'
    DB_TEST_PASSWORD = 'passwordDB_Test'
    DB_TEST_SERVER: str = 'localhost'
    DB_TEST_PORT: str = '5433'
    DB_TEST_NAME: str = 'wbTestTask_Test'
    DATABASE_TEST_URL = f"postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_SERVER}:{DB_TEST_PORT}/{DB_TEST_NAME}"


    # JWT Settings
    SECRET_KEY = 'ed546f271d436aeed02cb1b6e7ba496eba424e48d56bf6398e320c7100a280aa'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*30

    # Logger Configuration
    LOGGER_CONFIG = LOGGER_CFG

    # Attachments Storage
    POST_ATTACHMENTS_PATH = 'storage/attachments/'

    # Attachments Test Storage
    POST_TEST_ATTACHMENTS_DIR = 'attachments_test/'

settings = Settings()
