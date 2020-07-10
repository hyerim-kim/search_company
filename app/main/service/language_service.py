# -- coding: utf-8 --
from typing import List

from flask import abort, make_response, current_app, jsonify

from app.main.model.language import Language
from app.main.service import save_change, delete


def add_a_language(language_id: str):
    language = Language.query.filter_by(language_id=language_id).first()
    if not language:
        new_language = Language(language_id=language_id)
        save_change(new_language)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(response_object, 201)
    else:
        response_object = {
            'status': 'fail',
            'message': f'The language({language_id}) already exists.',
        }
        return make_response(response_object, 200)


def delete_a_language(language_id: str):
    if language_id == current_app.config['DEFAULT_LOCALE']:
        response_object = {
            'status': 'fail',
            'message': f'The language_id({language_id}) is default locale.'
        }
        return make_response(response_object, 423)

    language = Language.query.filter_by(language_id=language_id).first()
    if language:
        delete(language)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no language by id({language_id})'
        }

    return make_response(response_object, 200)


def get_all_languages():
    languages = {'languages': []}
    for language in Language.query.all():
        languages['languages'].append(language.language_id)

    return make_response(languages, 200 if languages else 204)


def set_default_locale(language_id: str):
    if Language.query.filter_by(language_id=language_id).first():
        current_app.config['DEFAULT_LOCALE'] = language_id
        response_object = {
            'status': 'success',
            'message': f'Successfully changed `DEFAULT_LOCALE` to {language_id}.'
        }
    else:
        response_object = {
            'status': 'fail',
            'message': f'There is no language by id({language_id})'
        }

    return make_response(response_object, 200)
