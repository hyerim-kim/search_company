import json

from app.test import get_random_string


class TestCompanyInfo:
    RANDOM_STRING = get_random_string(200)
    NEW_COMPANY_ID = 'id_' + RANDOM_STRING
    NEW_COMPANY_NAME = 'name_' + RANDOM_STRING
    NEW_TAG = [RANDOM_STRING[2:10], RANDOM_STRING[55:59], RANDOM_STRING[100:109]]
    LANGUAGES = ['ko', 'en', 'ja']

    def test_add_company_info(self, client: 'client', delimiter: str, default_locale: str):
        data = {
            "name": TestCompanyInfo.NEW_COMPANY_NAME,
            "tag": delimiter.join(TestCompanyInfo.NEW_TAG),
            "language_id": default_locale
        }

        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        if response.status_code == 201:
            response = client.get(f'/company/name/{TestCompanyInfo.NEW_COMPANY_NAME}')
            assert response.status_code == 200

            company_info = json.loads(response.data.decode("utf-8"))[0]
            assert company_info['name'] == data['name']
            assert company_info['tag'] == data['tag']
            assert company_info['language_id'] == data['language_id']
        else:
            assert False

    def test_get_company_info_by_id(self, client: 'client'):
        response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
        assert response.status_code == 200

    def test_get_companies_info_by_name(self, client: 'client'):
        response = client.get(f'/company/name/{TestCompanyInfo.NEW_COMPANY_NAME}')
        assert response.status_code == 200

    def test_get_companies_info_by_tag(self, client: 'client'):
        response = client.get(f'/company/tag/{TestCompanyInfo.NEW_TAG[0]}')
        assert response.status_code == 200

    def test_get_companies_info_by_tags(self, client: 'client', delimiter: str):
        response = client.get(f'/company/tags/{delimiter.join(TestCompanyInfo.NEW_TAG)}')
        assert response.status_code == 200

    def test_add_a_tag(self, client: 'client', delimiter: str, default_locale: str):
        new_tag = TestCompanyInfo.NEW_TAG[0]
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tags/{default_locale}/{new_tag}')
        if response.status_code == 201:
            response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
            assert response.status_code == 200

            company_info = json.loads(response.data.decode("utf-8"))[0]
            assert new_tag in company_info['tag']
        else:
            assert False

    def test_add_tags(self, client: 'client', delimiter: str, default_locale: str):
        tags = delimiter.join(TestCompanyInfo.NEW_TAG)
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tags/{default_locale}/{tags}')
        if response.status_code == 201:
            response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
            assert response.status_code == 200
            company_info = json.loads(response.data.decode("utf-8"))[0]
            for tag in TestCompanyInfo.NEW_TAG:
                assert tag in company_info['tag']
        else:
            assert False

    def test_add_tags_to_all(self, client: 'client', delimiter: str):
        tags = delimiter.join(TestCompanyInfo.NEW_TAG)
        languages = delimiter.join(TestCompanyInfo.LANGUAGES)
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tags/{languages}/{tags}')
        if response.status_code == 201:
            response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
            assert response.status_code == 200
            company_info = json.loads(response.data.decode("utf-8"))[0]
            for tag in TestCompanyInfo.NEW_TAG:
                assert tag in company_info['tag']
        else:
            assert False

    def test_delete_a_tag(self, client: 'client', delimiter: str, default_locale: str):
        tag = TestCompanyInfo.NEW_TAG[0]
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tags/{default_locale}/{tag}')
        assert response.status_code == 200

    def test_delete_tags(self, client: 'client', delimiter: str, default_locale: str):
        tag = TestCompanyInfo.NEW_TAG
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tags/{default_locale}/{tag}')
        assert response.status_code == 200

    def test_delete_tags_from_all(self, client: 'client', delimiter: str):
        tag = TestCompanyInfo.NEW_TAG[0]
        languages = delimiter.join(TestCompanyInfo.LANGUAGES)
        response = client.post(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tags/{languages}/{tag}')
        assert response.status_code == 200
