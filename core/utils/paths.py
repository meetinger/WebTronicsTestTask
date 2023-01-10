from urllib.parse import urljoin

from core.settings import settings

# словарь с путями
API_PATHS_DICT = {
    'view_attachment': '/attachments/view/',
    'view_post': '/posts/view'
}
def get_api_path(path_name: str) -> str:
    """Получить ссылку на API метод"""
    return urljoin(settings.ROOT_URL, API_PATHS_DICT[path_name])