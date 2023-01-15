from pprint import pprint

from core.utils.attachments import delete_file
from core.utils.paths import get_api_path
from tests.conftest import DATASET


def test_post_create(client, user, user_token, db_session):
    user_admin = user(user_in=DATASET['users']['admin'])
    user_admin_token = user_token(user=user_admin)
    data = DATASET['posts']['with_attachments']
    resp = client.post(get_api_path('create_post', append_root_url=False), data={'text': data['text']},
                       files=data['attachments'],
                       headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
    resp_json = resp.json()
    pprint(resp.content)
    pprint(resp.json())
    assert resp.status_code == 200
    assert resp_json['text'] == data['text']
    assert 'reactions_count' in resp_json
    assert len(resp_json['attachments_urls']) == len(data['attachments'])

def test_view_post(client, user, user_token, post):
    user_admin = user(user_in=DATASET['users']['admin'])
    user_admin_token = user_token(user=user_admin)
    post_data = DATASET['posts']['with_attachments']
    post_db = post(user=user_admin, post_data=post_data)
    resp = client.get(url=f'{get_api_path("view_post", append_root_url=False)}{post_db.id}',
                      headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json['text'] == post_data['text']
    assert 'reactions_count' in resp_json
    assert len(resp_json['attachments_urls']) == len(post_data['attachments'])


class TestEditPost:
    def test_edit_post_ok(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_admin_token = user_token(user=user_admin)
        post_data = DATASET['posts']['with_attachments']
        post_db = post(user=user_admin, post_data=post_data)
        post_edit_data = DATASET['posts']['without_attachments']
        resp = client.put(url=f'{get_api_path("edit_post", append_root_url=False)}{post_db.id}',
                          data={'text': post_edit_data['text']}, files=post_edit_data['attachments'],
                          headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json['text'] == post_edit_data['text']
        assert 'reactions_count' in resp_json
        assert len(resp_json['attachments_urls']) == len(post_edit_data['attachments'])

    def test_edit_post_another_user(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])
        user_common_token = user_token(user=user_common)
        post_data = DATASET['posts']['with_attachments']
        post_db = post(user=user_admin, post_data=post_data)
        post_edit_data = DATASET['posts']['without_attachments']

        resp = client.put(url=f'{get_api_path("edit_post", append_root_url=False)}{post_db.id}',
                          data={'text': post_edit_data['text']}, files=post_edit_data['attachments'],
                          headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 403
