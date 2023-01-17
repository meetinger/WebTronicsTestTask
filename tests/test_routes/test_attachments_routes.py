from core.utils.attachments import get_view_url, delete_file
from tests.conftest import DATASET

class TestViewAttachment:

    def test_view_attachment_ok(self, client, user, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        post_db = post(user=user_admin, post_data=DATASET['posts']['with_attachments'])
        attachments_filenames = [get_view_url(a.filename) for a in post_db.attachments]
        assert all(client.get(url=a_fn).status_code == 200 for a_fn in attachments_filenames)

    def test_view_attachment_not_found_db(self, client):
        assert client.get(url=get_view_url('NOT_EXIST_FILENAME.png')).status_code == 404

    def test_view_attachment_not_found_file(self, client, user, post):
        user_admin = user(user_in=DATASET['users']['admin'])
        post_db = post(user=user_admin, post_data=DATASET['posts']['with_attachments'])
        attachments_db = post_db.attachments
        delete_file(attachments_db[0].filename)
        assert client.get(url=get_view_url(attachments_db[0].filename)).status_code == 404
