# -- coding: utf-8 --
import os
import pytest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import init_app, db
from app.main.model import company, company_info, language
from app.main.controller.company_controller import company_api
from app.main.controller.language_controller import language_api


if not os.getenv('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'development'

app = init_app('dev')
app.register_blueprint(company_api)
app.register_blueprint(language_api)
app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(host='0.0.0.0')


@manager.command
def test():
    """Runs the unit tests."""
    pytest.main(['-x', './app/test', '-rsxX', '--fixtures', './app/test'])


if __name__ == '__main__':
    manager.run()

