import logging
import mimetypes
import os
import random
import string
from typing import IO
from urllib.parse import urljoin

from core.settings import settings
from core.utils.paths import get_api_path

logger = logging.getLogger(__name__)

def gen_filename(content_type: str) -> str:
    """Сгенерировать имя файла"""
    mimetypes_ins = mimetypes.MimeTypes()
    mime_ext_dict = mimetypes_ins.types_map_inv[0] | mimetypes_ins.types_map_inv[1]
    file_extension = mime_ext_dict[content_type][0]
    try:
        random_str = ''.join(random.choices(string.ascii_letters+string.digits, k=30))
        return random_str + file_extension
    except KeyError:
        logger.error(msg=f'Unsupported file mimetype: {content_type}')
        raise TypeError('Unsupported file mimetype')


def get_file_path(filename: str) -> str:
    """Создание пути файла"""
    return os.path.join(settings.POST_ATTACHMENTS_PATH, filename)

def save_file(filename: str, file_bytes: bytes) -> bool:
    """Сохранить файл"""
    file_path = get_file_path(filename)
    with open(file_path, 'wb') as file:
        file.write(file_bytes)
    return True

def delete_file(filename: str) -> bool:
    """Удалить файл"""
    file_path = get_file_path(filename)
    os.remove(file_path)
    return True

def get_view_url(filename: str) -> str:
    """Создание ссылки для просмотра картинки"""
    url = urljoin(get_api_path('view_attachment'), filename)
    return url

def get_attachment_file(filename: str) -> IO:
    """Получение файла по имени файла"""
    return open(get_file_path(filename), 'r')
