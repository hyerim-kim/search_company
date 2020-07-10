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

            company_info = json.loads(response.data.decode("utf-8"))[TestCompanyInfo.NEW_COMPANY_ID]
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

    def test_get_companies_info_by_tag(self, client: 'client', delimiter: str):
        tag = TestCompanyInfo.NEW_TAG[0]
        response = client.get(f'/company/tag/{tag}')
        assert response.status_code == 200

        company_info_list = json.loads(response.data.decode("utf-8"))
        for company_info in company_info_list.values():
            if tag in company_info['tag'].split(delimiter):
                return True
        assert False

    def test_get_companies_info_by_partial_tag(self, client: 'client', delimiter: str, default_locale: str):
        partial_tag = TestCompanyInfo.NEW_TAG[0][2:5]
        data = {'languages': [default_locale], 'tag': [TestCompanyInfo.NEW_TAG[0]]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]

        response = client.get(f'/company/tag/{partial_tag}')
        assert response.status_code == 204

    def test_get_companies_info_by_tags(self, client: 'client', delimiter: str, default_locale: str):
        tags = delimiter.join(TestCompanyInfo.NEW_TAG)
        data = {'languages': [default_locale], 'tag': TestCompanyInfo.NEW_TAG}
        # Try to add tags
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]

        response = client.get(f'/company/tag/{tags}', data=data)
        assert response.status_code == 200

        company_info_list = json.loads(response.data.decode("utf-8"))
        pass_count = 0
        for tag in TestCompanyInfo.NEW_TAG:
            for company_info in company_info_list.values():
                if tag in company_info['tag'].split(delimiter):
                    pass_count += 1
                    break

        assert pass_count == len(TestCompanyInfo.NEW_TAG)

    def test_add_a_tag(self, client: 'client', delimiter: str, default_locale: str):
        new_tag = TestCompanyInfo.NEW_TAG[0]
        data = {'languages': [default_locale], 'tag': [new_tag]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        if response.status_code == 201:
            response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
            assert response.status_code == 200

            company_info = json.loads(response.data.decode("utf-8"))[0]
            assert new_tag in company_info['tag']
        else:
            assert False

    def test_add_tags(self, client: 'client', delimiter: str, default_locale: str):
        tag = delimiter.join(TestCompanyInfo.NEW_TAG)
        data = {'languages': [default_locale], 'tag': [tag]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        if response.status_code == 201:
            response = client.get(f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/info')
            assert response.status_code == 200
            company_info = json.loads(response.data.decode("utf-8"))[0]
            for tag in TestCompanyInfo.NEW_TAG:
                assert tag in company_info['tag']
        else:
            assert False

    def test_add_tags_to_all(self, client: 'client', delimiter: str):
        tag = delimiter.join(TestCompanyInfo.NEW_TAG)
        data = {'languages': TestCompanyInfo.LANGUAGES, 'tag': [tag]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
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
        data = {'languages': default_locale, 'tag': [tag]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]

        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_delete_tags(self, client: 'client', delimiter: str, default_locale: str):
        tag = TestCompanyInfo.NEW_TAG
        data = {'languages': [default_locale], 'tag': tag}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]

        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_delete_tags_from_all(self, client: 'client', delimiter: str):
        tag = TestCompanyInfo.NEW_TAG[0]
        languages = delimiter.join(TestCompanyInfo.LANGUAGES)
        data = {'languages': languages, 'tag': [tag]}
        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/register/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code in [200, 201]

        response = client.post(
            f'/company/{TestCompanyInfo.NEW_COMPANY_ID}/delete/tag',
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200
