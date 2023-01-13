import enum
from typing import Literal
from urllib.parse import urljoin

from core.settings import settings

class ApiPaths(enum.Enum):
    """Пути API"""
    user_register = '/auth/register'
    get_token = '/auth/get_token'
    create_post = '/posts/create'
    view_attachment = '/attachments/view/'
    view_post = '/posts/view/'
    edit_post = '/posts/edit/'
    info_current_user = '/users/info'
    info_user = '/users/{user_id}/info'
    user_posts = '/users/{user_id}/posts'


def get_api_path(path_name: str, append_root_url=True) -> str:
    """Получить ссылку на API метод"""
    if append_root_url:
        return urljoin(settings.ROOT_URL, ApiPaths[path_name].value)
    return ApiPaths[path_name].value
