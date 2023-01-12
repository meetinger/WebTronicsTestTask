import pytest
from faker.providers import profile

from core.utils.misc import gen_random_str
from core.utils.paths import get_api_path
from faker import Faker

class TestRegister:
    fake = Faker()

    @pytest.fixture()
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
        assert resp.json() == {
            'id': 1,
            'username': profile['username'],
            'name': profile['name'],
            'email': profile['email']
        }

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
