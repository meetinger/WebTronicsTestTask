from fastapi import UploadFile

from db.models import User
from schemas.users_schemas import UserIn
from tests.dataset.gen_images import IMG_COLORS, IMG_EXT

DATASET = {
    'users': {'admin': UserIn(username='Admin',name='Одмен',email='admin@mail.ru',password='admin_password'),
              'user': UserIn(username='User',name='Юзверь',email='user@mail.ru',password='user_password')},
    'posts': {
        'with_attachments': {'text': 'Post with attachments', 'attachments': [UploadFile(filename=f'dataset/attachments_files/{color}{IMG_EXT}') for color in IMG_COLORS]},
        'post_without_attachments': {'text': 'Post without attachments', 'attachments': []}
    }
}