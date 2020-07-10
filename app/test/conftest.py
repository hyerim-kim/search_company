import pytest

from manage import app


@pytest.fixture
def client():
    yield app.test_client()


@pytest.fixture
def default_locale():
    return app.config['DEFAULT_LOCALE']\


@pytest.fixture
def delimiter():
    return app.config['DELIMITER']

