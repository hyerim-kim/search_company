# -- coding: utf-8 --

from flask import Blueprint, request

from app.main.service import company_service, company_info_service

company_api = Blueprint('company_api', __name__)


@company_api.route('/company/register/<string:company_id>', methods=['POST'])
def add_new_company(company_id: str):
    return company_service.add_company(company_id)


@company_api.route('/company/<string:company_id>', methods=['GET'])
def get_company_by_id(company_id: str):
    return company_service.get_company_by_id(company_id=company_id)


@company_api.route('/companies', methods=['GET'])
def get_all_companies():
    return company_service.get_all_companies()


@company_api.route('/company/delete/<string:company_id>', methods=['POST'])
def delete_a_company(company_id: str):
    return company_service.delete_company(company_id)


@company_api.route('/company/<string:company_id>/register', methods=['POST'])
def add_a_company_info(company_id: str):
    return company_info_service.add_company_info(company_id, request.data)


@company_api.route('/company/<string:company_id>/info', methods=['GET'])
def get_company_info_by_id(company_id: str):
    return company_info_service.get_company_info_by_id(company_id=company_id)


@company_api.route('/company/name/<string:name>', methods=['GET'])
def get_company_info_by_name(name: str):
    return company_info_service.get_companies_info_by_name(name=name)


@company_api.route('/company/tag/<string:tag>', methods=['GET'])
def get_company_by_tag(tag: str):
    return company_info_service.get_companies_info_by_tag(tag=tag)


@company_api.route('/company/tags/<string:tags>', methods=['GET'])
def get_company_by_tags(tags: str):
    return company_info_service.get_companies_info_by_tags(tags=tags)


@company_api.route('/company/<string:company_id>/register/tags/<string:language_id>/<string:tags>', methods=['POST'])
def add_tags(company_id: str, language_id: str, tags: str):
    return company_info_service.add_tags(company_id, language_id, tags)


@company_api.route('/company/<string:company_id>/delete/tags/<string:language_id>/<string:tags>', methods=['POST'])
def delete_tags(company_id: str, language_id: str, tags: str):
    return company_info_service.delete_tags(company_id, language_id, tags)
