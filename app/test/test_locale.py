import json

from app.test import get_random_string


class TestLanguage:
    NEW_LANGUAGE = get_random_string(5)

    def test_add_a_language(self, client: 'client'):
        response = client.post(f'/language/register/{TestLanguage.NEW_LANGUAGE}')
        assert response.status_code == 201 or response.status_code == 204

        response = client.get('/languages')
        data = json.loads(response.data.decode("utf-8"))
        assert TestLanguage.NEW_LANGUAGE in data['languages']

    def test_get_all_languages(self, client: 'client', default_locale: str):
        response = client.get('/languages')
        if response.status_code == 200:
            data = json.loads(response.data.decode("utf-8"))
            assert default_locale in data['languages']
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
        assert TestLanguage.NEW_LANGUAGE not in data

    def test_set_default_locale(self, client: 'client'):
        # Try to set an unregistered language, it will be failed.
        temp_locale = get_random_string(5)
        response = client.post(f'/locale/{temp_locale}')
        data = json.loads(response.data.decode("utf-8"))
        assert data['status'] == 'fail'
        client.post(f'/language/delete/{temp_locale}')

        response = client.post('/locale/en')
        assert response.status_code == 200

        response = client.post('/locale/ko')
        assert response.status_code == 200
