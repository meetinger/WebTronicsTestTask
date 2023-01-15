from core.utils.misc import is_dicts_equals
from core.utils.paths import get_api_path
from tests.conftest import DATASET


class TestSetReaction:
    def test_create_reaction_ok(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'like'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 200
        assert resp.json() == (data_json | {'user_id': user_common.id, 'is_deleted': False})

    def test_unset_reaction_ok(self, client, user, user_token, post, reaction):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        reaction_db = reaction(user=user_common, entity=post_db, reaction_type='like')

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'unset'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == (data_json | {'user_id': user_common.id, 'is_deleted': True})

    def test_update_reaction_ok(self, client, user, user_token, post, reaction):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        reaction_db = reaction(user=user_common, entity=post_db, reaction_type='like')

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'dislike'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 200
        assert resp.json() == (data_json | {'user_id': user_common.id, 'is_deleted': False})


    def test_set_reaction_invalid_params(self, client, user, user_token):
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)
        data_json = {
            'entity_type': 'NOT_EXIST_ENTITY_TYPE',
            'entity_id': 1,
            'reaction_type': 'NOT_REACTION_ENTITY_TYPE'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})
        assert resp.status_code == 400

    def test_set_reaction_entity_not_found(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id + 1,
            'reaction_type': 'like'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 404

    def test_set_reaction_own_entity(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])

        user_admin_token = user_token(user=user_admin)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'like'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_admin_token["access_token"]}'})

        assert resp.status_code == 409

    def test_unset_reaction_not_found(self, client, user, user_token, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'unset'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 404

    def test_update_reaction_already_set(self, client, user, user_token, post, reaction):
        user_admin = user(user_in=DATASET['users']['admin'])
        user_common = user(user_in=DATASET['users']['user'])

        user_common_token = user_token(user=user_common)

        post_db = post(user=user_admin, post_data=DATASET['posts']['without_attachments'])

        reaction_db = reaction(user=user_common, entity=post_db, reaction_type='like')

        data_json = {
            'entity_type': 'post',
            'entity_id': post_db.id,
            'reaction_type': 'like'
        }

        resp = client.post(url=get_api_path('set_reaction'), json=data_json,
                           headers={'Authorization': f'Bearer {user_common_token["access_token"]}'})

        assert resp.status_code == 409
