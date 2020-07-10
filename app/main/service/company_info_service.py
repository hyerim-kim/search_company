# -- coding: utf-8 --
import json
from typing import List

from flask import make_response, current_app, jsonify

from app.main.model.company import Company
from app.main.model.company_info import CompanyInfo
from app.main.service import *


def add_a_company_info(company_id: str, data: bytes):
    data = json.loads(data)
    if CompanyInfo.query.filter_by(company_id=company_id, language_id=data['language_id']).first():
        response_object = {
            'status': 'fail',
            'message': f'Already exist company information by parameters(company_id({company_id}), '
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


def add_tags(company_id: str, data: bytes):
    data = json.loads(data)
    languages = data.get('languages')
    tag = set(data.get('tag'))
    delimiter = current_app.config['DELIMITER']

    company_info_list: List[CompanyInfo] = []
    for language in languages:
        company_info: CompanyInfo = CompanyInfo.query.filter_by(company_id=company_id, language_id=language).first()
        if company_info:
            company_info.tag = delimiter.join(set(company_info.tag.split(delimiter)) | tag)
        else:
            if not Company.query.filter_by(company_id=company_id).first():
                continue
            company_info = CompanyInfo(company_id=company_id, language_id=language, name=None, tag=delimiter.join(tag))
        company_info_list.append(company_info)

    if company_info_list:
        save_all(company_info_list)

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(response_object, 201)
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no company by company_id({company_id})'
        }
        return make_response(response_object, 200)


def delete_tags(company_id: str, data: bytes):
    data = json.loads(data)
    languages = data.get('languages')
    tag = set(data.get('tag'))
    delimiter: str = current_app.config['DELIMITER']

    company_info_list: List[CompanyInfo] = []
    for language in languages:
        company_info: CompanyInfo = CompanyInfo.query.filter_by(company_id=company_id, language_id=language).first()
        if company_info:
            company_info.tag = delimiter.join(set(company_info.tag.split(delimiter)) - tag)
            company_info_list.append(company_info)

    if company_info_list:
        save_all(company_info_list)

        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no company by company_id({company_id})'
        }

    return make_response(response_object, 200)


def get_company_info_by_id(company_id: str):
    company_info_list = CompanyInfo.query.filter_by(company_id=company_id).all()
    if company_info_list:
        result = get_company_info_result(company_info_list)
        if result:
            return make_response(jsonify(result), 200)
    return make_response({}, 204)


def get_companies_info_by_name(name: str):
    company_info_list = CompanyInfo.query.filter(
        CompanyInfo.name.like(f"%{name}%")
    ).all()

    result = {}
    default_locale = current_app.config['DEFAULT_LOCALE']
    for info in company_info_list:
        if info.company_id not in result:
            if info.language_id != default_locale:
                default_locale_info = CompanyInfo.query.filter_by(
                    company_id=info.company_id,
                    language_id=default_locale
                ).first()
                if default_locale_info:
                    info = default_locale_info
            result[info.company_id] = {
                'company_id': info.company_id,
                'language_id': info.language_id,
                'name': info.name,
                'tag': info.tag
            }

    return make_response(jsonify(result), 200 if result else 204)


def get_companies_info_by_tags(tags: str):
    delimiter = current_app.config['DELIMITER']
    default_locale = current_app.config['DEFAULT_LOCALE']
    tags = set(tags.split(delimiter))

    result = {}
    for tag in tags:
        like = CompanyInfo.tag.like(f"%{tag}%")
        company_info_list = CompanyInfo.query.filter(like).all()
        for info in company_info_list:
            if info.company_id not in result and tag in info.tag.split(delimiter):
                display_name = info.name
                if info.language_id != default_locale:
                    default_locale_info = CompanyInfo.query.filter_by(
                        company_id=info.company_id, language_id=default_locale
                    ).first()
                    if default_locale_info:
                        display_name = default_locale_info.name

                result[info.company_id] = {
                    'display_name': display_name,
                    'company_id': info.company_id,
                    'language_id': info.language_id,
                    'name': info.name,
                    'tag': info.tag
                }

    return make_response(result, 200 if result else 204)


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
