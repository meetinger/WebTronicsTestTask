import random
import string


def gen_random_str(str_len: int, symbols: str = string.ascii_letters + string.digits):
    """Возвращает строку из случайных символов"""
    return ''.join(random.choices(symbols, k=str_len))


def is_dicts_equals(d1: dict, d2: dict, ignore_keys: tuple = ()):
    """Проверяет два словаря на равенство, игнорируя ключи ignore_keys"""
    keys1 = set(d1).difference(ignore_keys)
    keys2 = set(d2).difference(ignore_keys)
    return keys1 == keys2 and all(d1[key] == d2[key] for key in keys1)