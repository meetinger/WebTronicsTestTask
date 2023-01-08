from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    """Класс для работы с паролями"""
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        """Проверка пароля"""
        return crypt_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str):
        """Хеширование пароля"""
        return crypt_context.hash(password)
