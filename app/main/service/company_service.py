# -- coding: utf-8 --

from flask import make_response, jsonify

from app.main.model.company import Company
from app.main.model.company_info import CompanyInfo
from app.main.service import save_change, delete_all


def add_company(company_id: str):
    company = Company.query.filter_by(company_id=company_id).first()
    if not company:
        new_company = Company(company_id=company_id)
        save_change(new_company)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(response_object, 201)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Company already exists.',
        }
        return make_response(response_object, 200)


def get_company_by_id(company_id: str = None):
    company = Company.query.get(company_id)
    if company:
        return make_response(jsonify(company_id=company.company_id), 200)
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no any company by id({company_id}).',
        }
        return make_response(response_object, 200)


def get_all_companies():
    company_list = Company.query.all()
    companies = jsonify(
        companies=[company.company_id for company in company_list]
        if company_list else dict()
    )

    return make_response(companies, 200 if companies else 204)


def delete_company(company_id: str):
    data_list_for_delete = CompanyInfo.query.filter_by(company_id=company_id).all()
    company = Company.query.filter_by(company_id=company_id).first()
    if company:
        data_list_for_delete.append(company)
    delete_all(data_list_for_delete)

    response_object = {
        'status': 'success',
        'message': 'Successfully deleted.'
    }
    return make_response(response_object, 200)
