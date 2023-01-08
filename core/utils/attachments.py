import logging
import os
import random
import string
import mimetypes
from urllib.parse import urljoin

from core.settings import settings

logger = logging.getLogger(__name__)

mimetypes.init()


def gen_filename(content_type: str) -> str:
    """Сгенерировать имя файла"""
    mimetypes_ins = mimetypes.MimeTypes()
    mime_ext_dict = mimetypes_ins.types_map_inv[0] | mimetypes_ins.types_map_inv[1]
    file_extension = mime_ext_dict[content_type][0]
    try:
        random_str = ''.join(random.choices(string.ascii_letters+string.digits, k=10))
        return random_str + file_extension
    except KeyError:
        logger.error(msg=f'Unsupported file mimetype: {content_type}')
        raise TypeError('Unsupported file mimetype')


def save_file(filename: str, file_bytes: bytes) -> bool:
    """Сохранить файл"""
    file_path = os.path.join(settings.POST_ATTACHMENTS_PATH, filename)
    with open(file_path, 'wb') as file:
        file.write(file_bytes)
    return True

def get_view_url(filename: str):
    """Создание ссылки для просмотра картинки"""
    url = urljoin(settings.ROOT_URL, '/attachments/view/'+filename)
    return url
