# -- coding: utf-8 --
import json
from typing import List

from flask import make_response, current_app, jsonify

from app.main.model.company_info import CompanyInfo
from app.main.service import *


def add_company_info(company_id: str, data: bytes):
    data = json.loads(data)
    if CompanyInfo.query.filter_by(company_id=company_id, language_id=data['language_id']).first():
        response_object = {
            'status': 'fail',
            'message': f'Already exist company by parameters(company_id({company_id}), '
                       f'language_id({data["language_id"]})).'
        }
        return make_response(response_object, 201)

    company_info = CompanyInfo(
        company_id=company_id,
        language_id=data['language_id'],
        name=data['name'],
        tag=data['tag']
    )
    save_change(company_info)

    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return make_response(response_object, 201)


def update_company_info(company_id: str, data: bytes):
    data = json.loads(data)
    company_info = CompanyInfo.query.filter_by(company_id=company_id, language_id=data['language_id']).first()

    if company_info:
        if data.get('name') is not None:
            company_info.name = data['name']
        if data.get('tag') is not None:
            delimiter = current_app.config['DELIMITER']
            company_info.tag = delimiter.join(set(company_info.tag.split(delimiter)) | set(data.get('tag')))
        # TODO
    else:
        company_info = CompanyInfo(
            company_id=company_id,
            language_id=data['language_id'],
            name=data['name'],
            tag=data['tag']
        )
    save_change(company_info)

    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return make_response(response_object, 201)


def add_tags(company_id: str, language_id: list, tags: str):
    delimiter = current_app.config['DELIMITER']
    company_info_list: List[CompanyInfo] = []
    for language in language_id.split(delimiter):
        company_info: CompanyInfo = CompanyInfo.query.filter_by(company_id=company_id, language_id=language).first()
        if company_info:
            company_info.tag = delimiter.join(set(company_info.tag.split(delimiter)) | set(tags.split(delimiter)))
        else:
            company_info = CompanyInfo(company_id=company_id, language_id=language, name=None, tag=tags)
        company_info_list.append(company_info)

    save_all(company_info_list)

    response_object = {
        'status': 'success',
        'message': 'Successfully registered.'
    }
    return make_response(response_object, 201)


# def delete_tags(company_id: str, language_id: str, tags: str):
#     company_info: CompanyInfo = CompanyInfo.query.filter_by(company_id=company_id, language_id=language_id).first()
#     delimiter: str = current_app.config['DELIMITER']
#
#     if company_info:
#         company_info.tag = delimiter.join(list(set(company_info.tag.split(delimiter)) - set(tags.split(delimiter))))
#         save_change(company_info)
#         response_object = {
#             'status': 'success',
#             'message': 'Successfully deleted.'
#         }
#     else:
#         response_object = {
#             'status': 'fail',
#             'message': f'There is no data by parameters(company_id:{company_id}, language_id:{language_id}).'
#         }
#     return make_response(response_object, 200)


def delete_tags(company_id: str, language_id: list, tags: str):
    delimiter: str = current_app.config['DELIMITER']
    company_info_list: List[CompanyInfo] = []
    for language in language_id.split(delimiter):
        company_info: CompanyInfo = CompanyInfo.query.filter_by(company_id=company_id, language_id=language).first()
        if company_info:
            company_info.tag = set(company_info.tag.split(delimiter)) - set(tags.split(delimiter))
            company_info_list.append(company_info)

    save_all(company_info_list)

    response_object = {
        'status': 'success',
        'message': 'Successfully deleted.'
    }

    return make_response(response_object, 200)


def get_company_info_by_id(company_id: str):
    company_info_list = CompanyInfo.query.filter_by(company_id=company_id).all()
    if company_info_list:
        result = get_company_info_result(company_info_list)
        return make_response(jsonify(result), 200)
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no any company info by id({company_id}).',
        }
        return make_response(response_object, 200)


def get_companies_info_by_name(name: str):
    company_info_list = (
        CompanyInfo.query.filter(
            CompanyInfo.name.like(f"%{name}%")
        ).filter_by(
            language_id=current_app.config['DEFAULT_LOCALE']
        ).all()
    )
    result = get_company_info_result(company_info_list)
    return make_response(jsonify(result), 200 if result else 204)


def get_companies_info_by_tag(tag: str):
    query = CompanyInfo.query.filter(CompanyInfo.tag.like(f"%{tag}%"))
    return get_companies_info_has_tags(query)


def get_companies_info_by_tags(tags: str):
    tags = set(tags.split(current_app.config['DELIMITER']))

    queries = []
    for tag in tags:
        like = CompanyInfo.tag.like(f"%{tag}%")
        queries.append(CompanyInfo.query.filter(like))

    return get_companies_info_has_tags(queries[0].union(*queries[1:]))


def get_companies_info_has_tags(query):
    language_id = current_app.config['DEFAULT_LOCALE']

    company_info_list = query.filter_by(language_id=language_id).all()
    result = get_company_info_result(company_info_list)

    if not result:
        company_info = query.first()
        if company_info:
            result = [{
                'company_id': company_info.company_id,
                'language_id': company_info.language_id,
                'name': company_info.name,
                'tag': company_info.tag
            }]
    return make_response(jsonify(result), 200 if result else 204)


def get_company_info_result(company_info_list: list) -> list:
    return [{
        'company_id': info.company_id,
        'language_id': info.language_id,
        'name': info.name,
        'tag': info.tag
    } for info in company_info_list]
