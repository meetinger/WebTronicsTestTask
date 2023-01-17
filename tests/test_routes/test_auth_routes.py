from unittest.mock import patch

import pytest
from faker import Faker

from core.settings import settings
from core.utils.misc import gen_random_str, is_dicts_equals
from core.utils.paths import get_api_path
from tests.conftest import DATASET


class TestRegister:
    fake = Faker()

    @pytest.fixture(scope="function")
    def profile(self):
        user_data = {
            'username': self.fake.unique.user_name(),
            'name': self.fake.unique.name(),
            'email': self.fake.unique.free_email(),
            'password': gen_random_str(str_len=10)
        }
        return user_data

    def test_register_ok(self, client, profile):
        resp = client.post(get_api_path('user_register', append_root_url=False), json=profile)
        assert resp.status_code == 200
        resp_correct = {
            'id': 1,
            'username': profile['username'],
            'name': profile['name'],
            'email': profile['email']
        }
        assert is_dicts_equals(resp.json(), resp_correct, ignore_keys=('id',))

    def test_register_repeat_email(self, client, profile):
        resp1 = client.post(get_api_path('user_register', append_root_url=False), json=profile)
        assert resp1.status_code == 200
        profile['username'] = self.fake.unique.user_name()
        resp2 = client.post(get_api_path('user_register', append_root_url=False), json=profile)
        assert resp2.status_code == 409

    def test_register_repeat_username(self, client, profile):
        resp1 = client.post(get_api_path('user_register', append_root_url=False), json=profile)
        assert resp1.status_code == 200
        profile['email'] = self.fake.unique.free_email()
        resp2 = client.post(get_api_path('user_register', append_root_url=False), json=profile)
        assert resp2.status_code == 409


class TestGetToken:
    def test_get_token_ok(self, client, user):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_data = {
            'username': DATASET['users']['admin'].username,
            'password': DATASET['users']['admin'].password
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 200
        resp_json = resp.json()
        assert all(key in resp_json for key in ('access_token', 'refresh_token', 'token_type'))

    def test_get_token_invalid_credentials(self, client, user):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_data = {
            'username': DATASET['users']['admin'].username + '_invalid',
            'password': DATASET['users']['admin'].password + '_invalid'
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 401

    @patch.object(settings, 'ALGORITHM', 'NOT_EXIST_ALGORITHM')
    def test_get_token_error_500(self, client, user):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_data = {
            'username': DATASET['users']['admin'].username,
            'password': DATASET['users']['admin'].password
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 500

class TestRefreshTokens:
    def test_refresh_tokens_ok(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        admin_token = user_token(user=user_admin)
        resp = client.post(get_api_path('refresh_tokens', append_root_url=False), json={'refresh_token': admin_token['refresh_token']})
        assert resp.status_code == 200
        resp_json = resp.json()
        assert all(key in resp_json for key in ('access_token', 'refresh_token', 'token_type'))

    def test_refresh_tokens_wrong_token_type(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        admin_token = user_token(user=user_admin)
        resp = client.post(get_api_path('refresh_tokens', append_root_url=False), json={'refresh_token': admin_token['access_token']})
        assert resp.status_code == 403

    @patch.object(settings, 'REFRESH_TOKEN_EXPIRE_MINUTES', -1)
    def test_refresh_tokens_wrong_token_type(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        admin_token = user_token(user=user_admin)
        resp = client.post(get_api_path('refresh_tokens', append_root_url=False), json={'refresh_token': admin_token['refresh_token']})
        assert resp.status_code == 403

    def test_refresh_tokens_invalid_credentials(self, client, user, user_token):
        user_admin = user(user_in=DATASET['users']['admin'])
        admin_token = user_token(user=user_admin)
        resp = client.post(get_api_path('refresh_tokens', append_root_url=False),
                           json={'refresh_token': admin_token['refresh_token']+'_invalid'})
        assert resp.status_code == 401
