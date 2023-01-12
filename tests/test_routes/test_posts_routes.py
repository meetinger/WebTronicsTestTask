from pprint import pprint

from core.utils.paths import get_api_path
from tests.conftest import DATASET


def test_post_create(client, user_admin_token):
    data = DATASET['posts']['with_attachments']
    resp = client.post(get_api_path('create_post', append_root_url=False), data={'text': data['text']},
                       files=data['attachments'],
                       headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
    resp_json = resp.json()
    pprint(resp.content)
    pprint(resp.json())
    assert resp.status_code == 200
    assert resp_json['text'] == data['text']
    assert len(resp_json['attachments']) == len(data['attachments'])
