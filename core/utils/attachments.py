import logging
import mimetypes
import os
import random
import string
from typing import IO, Generator
from urllib.parse import urljoin

from fastapi import Depends

from core.settings import settings
from core.utils.misc import gen_random_str
from core.utils.paths import get_api_path

logger = logging.getLogger(__name__)

def get_attachments_path() -> str:
    """Путь хранения вложений"""
    return settings.POST_ATTACHMENTS_PATH

def gen_filename(content_type: str) -> str:
    """Сгенерировать имя файла"""
    mimetypes_ins = mimetypes.MimeTypes()
    mime_ext_dict = mimetypes_ins.types_map_inv[0] | mimetypes_ins.types_map_inv[1]
    try:
        file_extension = mime_ext_dict[content_type][0]
        random_str = gen_random_str(str_len=30)
        return random_str + file_extension
    except KeyError:
        logger.error(msg=f'Unsupported file mimetype: {content_type}')
        raise TypeError(f'Unsupported file mimetype: {content_type}')


def get_file_path(filename: str) -> str:
    """Получить путь файла"""
    return os.path.join(get_attachments_path(), filename)

def save_file(filename: str, file_bytes: bytes) -> bool:
    """Сохранить файл"""
    file_path = get_file_path(filename)
    with open(file_path, 'wb') as file:
        file.write(file_bytes)
    return True

def delete_file(filename: str) -> bool:
    """Удалить файл"""
    file_path = get_file_path(filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def get_view_url(filename: str) -> str:
    """Создание ссылки для просмотра картинки"""
    url = urljoin(get_api_path('view_attachment'), filename)
    return url

def get_attachment_file(filename: str) -> IO:
    """Получение файла по имени файла"""
    return open(get_file_path(filename), 'r')
