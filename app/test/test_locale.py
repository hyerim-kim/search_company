import json

from app.test import get_random_string


class TestLanguage:
    NEW_LANGUAGE = get_random_string(5)
    NEW_PREFIX = NEW_LANGUAGE + '_'

    def test_add_a_language(self, client: 'client'):
        response = client.post(f'/language/add/{TestLanguage.NEW_LANGUAGE}|{TestLanguage.NEW_PREFIX}')
        assert response.status_code == 201 or response.status_code == 204

        response = client.get('/languages')
        data = json.loads(response.data.decode("utf-8"))
        assert TestLanguage.NEW_LANGUAGE in data.keys()
        assert TestLanguage.NEW_PREFIX == data[TestLanguage.NEW_LANGUAGE]

    def test_get_all_languages(self, client: 'client'):
        response = client.get('/languages')
        if response.status_code == 200:
            data = json.loads(response.data.decode("utf-8"))
            assert TestLanguage.NEW_LANGUAGE in data.keys()
        else:
            assert False

    def test_delete_a_language(self, client: 'client', default_locale: str):
        # Try to delete the default locale, it will be failed.
        response = client.post(f'/language/delete/{default_locale}')
        assert response.status_code == 423

        response = client.post(f'/language/delete/{TestLanguage.NEW_LANGUAGE}')
        assert response.status_code == 200

        response = client.get('/languages')
        data = json.loads(response.data.decode("utf-8"))
        assert TestLanguage.NEW_LANGUAGE not in data.keys()

    def test_set_default_locale(self, client: 'client'):
        # Try to set an unregistered language, it will be failed.
        response = client.post('/locale/ch')
        data = json.loads(response.data.decode("utf-8"))
        assert data['status'] == 'fail'

        response = client.post('/locale/en')
        assert response.status_code == 200

        response = client.post('/locale/ko')
        assert response.status_code == 200
