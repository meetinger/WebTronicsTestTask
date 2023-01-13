from core.utils.paths import get_api_path
from core.utils.serialization import sqlalchemy_to_pydantic_or_dict
from schemas.users_schemas import UserOut, UserLimited
from tests.conftest import DATASET


def test_info_current_user(client, user, user_token):
    user_admin = user(user_in=DATASET['users']['admin'])
    user_admin_token = user_token(user_admin)

    resp = client.get(url=get_api_path('info_current_user', append_root_url=False),
                      headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
    assert resp.status_code == 200
    assert resp.json() == sqlalchemy_to_pydantic_or_dict(UserOut, user_admin, to_dict=True)


class TestUserInfo:
    def test_user_by_id_ok_same_user(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_admin_token = user_token(user_admin)
        resp = client.get(url=get_api_path('info_user').format(user_id=user_admin.id),
                          headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
        assert resp.status_code == 200
        assert resp.json() == sqlalchemy_to_pydantic_or_dict(UserOut, user_admin, to_dict=True)

    def test_user_by_id_not_found(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_admin_token = user_token(user_admin)
        resp = client.get(url=get_api_path('info_user').format(user_id=user_admin.id + 1),
                          headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})
        assert resp.status_code == 404

    def test_user_by_id_another_user(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])
        user_common_token = user_token(user_common)

        resp = client.get(url=get_api_path('info_user').format(user_id=user_admin.id),
                          headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})
        assert resp.status_code == 200
        assert resp.json() == sqlalchemy_to_pydantic_or_dict(UserLimited, user_admin, to_dict=True)


def test_user_posts(client, user, user_token, post):
    user_admin = user(user_in=DATASET['users']['admin'])
    user_admin_token = user_token(user_admin)

    post_with_attachments = post(user=user_admin, post_data=DATASET['posts']['with_attachments'])
    post_without_attachments = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

    resp = client.get(url=get_api_path('user_posts').format(user_id=user_admin.id),
                      headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})

    assert resp.status_code == 200
    assert len(resp.json()) == 2
