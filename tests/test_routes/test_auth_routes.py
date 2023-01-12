from unittest.mock import patch

import pytest

from faker import Faker
from tests.conftest import DATASET
from core.utils.misc import gen_random_str, is_dicts_equals
from core.utils.paths import get_api_path
from core.settings import settings

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
    def test_get_token_ok(self, client, user_admin):
        user_data = {
            'username': DATASET['users']['admin'].username,
            'password': DATASET['users']['admin'].password
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 200
        resp_json = resp.json()
        assert all(key in resp_json for key in ('access_token', 'refresh_token', 'token_type'))

    def test_get_token_invalid_credentials(self, client, user_admin):
        user_data = {
            'username': DATASET['users']['admin'].username + '_invalid',
            'password': DATASET['users']['admin'].password + '_invalid'
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 401

    @patch.object(settings, 'ALGORITHM')
    def test_get_token_error_500(self, mocked_algorithm, client, user_admin):
        mocked_algorithm.return_value = 'NOT_EXIST_ALGORITHM'
        user_data = {
            'username': DATASET['users']['admin'].username,
            'password': DATASET['users']['admin'].password
        }
        resp = client.post(get_api_path('get_token', append_root_url=False), data=user_data)
        assert resp.status_code == 500
