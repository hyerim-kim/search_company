import os

import pytest
from flask import current_app

from app.main.config import basedir
from manage import app


class TestDevelopmentConfig:
    @pytest.fixture
    def create_app(self):
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self, create_app):
        assert app.config['SECRET_KEY'] is not 'kkk'
        assert app.config['DEBUG'] is True
        assert current_app is not None
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'search_company.db')


class TestTestingConfig:
    @pytest.fixture
    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self, create_app):
        assert app.config['SECRET_KEY'] is not 'kkk'
        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///' + os.path.join(basedir, 'search_company_test.db')
