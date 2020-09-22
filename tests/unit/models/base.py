from tests import base
from src import utils
from src import db


class Base(base.Base):
    """Base test class for Model unit tests."""
    def setUp(self):
        super(Base, self).setUp()
        # Rollback any transaction in process and recreate the database from scratch.
        #
        # Per http://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy,
        # the hangs I was sometimes seeing in my test runs may have had to do
        # with outstanding transactions.  Automatically rolling back any
        # pending transaction seems to have fixed the hangs. -- ODS 13 Apr 2016
        db.session.rollback()
        utils.resetDB(db)
