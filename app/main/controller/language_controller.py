# -- coding: utf-8 --

from flask import Blueprint

from app.main.service import language_service

language_api = Blueprint('language_api', __name__)


@language_api.route('/languages', methods=['GET'])
def get_all_languages():
    language_list = language_service.get_all_languages()
    return language_list if language_list else {}


@language_api.route('/language/register/<string:language_id>', methods=['POST'])
def add_a_language(language_id: str):
    return language_service.add_a_language(language_id)


@language_api.route('/language/delete/<string:language_id>', methods=['POST'])
def delete_a_language(language_id: str):
    return language_service.delete_a_language(language_id)


@language_api.route('/locale/<string:language_id>', methods=['POST'])
def set_locale(language_id: str):
    return language_service.set_default_locale(language_id)
