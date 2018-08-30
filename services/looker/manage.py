import unittest
import click
from datetime import datetime

from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import DXLooker, InvoicingByLibrary
from project.api.looker_api_handler import get_look

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def seed_db():
    """Seeds the database"""
    db.session.add(DXLooker(datetime(2018, 8, 1).isoformat()))
    db.session.commit()


@cli.command()
@click.option("-l")
def pull_look(l):
    json_object = get_look(l)
    for j in json_object:
        i = InvoicingByLibrary(**j)
        db.session.add(i)
    db.session.commit()
    print(InvoicingByLibrary.query.all())


if __name__ == "__main__":
    cli()
