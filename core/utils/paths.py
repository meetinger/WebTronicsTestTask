from urllib.parse import urljoin

from core.settings import settings

# словарь с путями
API_PATHS_DICT = {
    'user_register': '/auth/register',
    'get_token': '/auth/get_token',
    'create_post': '/posts/create',
    'view_attachment': '/attachments/view/',
    'view_post': '/posts/view'
}
def get_api_path(path_name: str, append_root_url=True) -> str:
    """Получить ссылку на API метод"""
    if append_root_url:
        return urljoin(settings.ROOT_URL, API_PATHS_DICT[path_name])
    return API_PATHS_DICT[path_name]
