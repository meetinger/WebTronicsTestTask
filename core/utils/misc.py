import random
import string


def gen_random_str(str_len: int, symbols: str = string.ascii_letters + string.digits):
    """Возвращает строку из случайных символов"""
    return ''.join(random.choices(symbols, k=str_len))
