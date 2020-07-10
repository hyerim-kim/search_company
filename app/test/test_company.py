import json

from app.test import get_random_string


class TestCompany:
    NEW_COMPANY = 'id_' + get_random_string(252)

    def test_add_new_company(self, client: 'client'):
        response = client.post(f'/company/register/{TestCompany.NEW_COMPANY}')
        assert response.status_code == 201 or response.status_code == 204

        response = client.get(f'/company/{TestCompany.NEW_COMPANY}')
        data = json.loads(response.data.decode("utf-8"))
        assert TestCompany.NEW_COMPANY == data['company_id']

    def test_get_company_by_id(self, client: 'client'):
        response = client.get(f'/company/{TestCompany.NEW_COMPANY}')
        if response.status_code == 200:
            data = json.loads(response.data.decode("utf-8"))
            assert TestCompany.NEW_COMPANY == data['company_id']
        else:
            assert False

    def test_get_all_companies(self, client: 'client'):
        response = client.get('/companies')
        if response.status_code == 200:
            data = json.loads(response.data.decode("utf-8"))
            assert TestCompany.NEW_COMPANY in data['companies']
        else:
            assert False

    def test_delete_a_company(self, client: 'client'):
        response = client.post(f'/company/delete/{TestCompany.NEW_COMPANY}')
        assert response.status_code == 200

        response = client.get(f'/company/{TestCompany.NEW_COMPANY}')
        data = json.loads(response.data.decode("utf-8"))
        assert data['status'] == 'fail'

        response = client.get(f'/company/{TestCompany.NEW_COMPANY}/info')
        data = json.loads(response.data.decode("utf-8"))
        assert data['status'] == 'fail'
