from flask_script import Manager

from bee_api import app
import fixtures as _fixtures
import models

manager = Manager(app)


@manager.command
def tables():
    "Create database tables."
    models.create_tables(app)


@manager.command
def fixtures():
    "Install test data fixtures into the configured database."
    _fixtures.install(app, *_fixtures.all_data)


if __name__ == "__main__":
    manager.run()