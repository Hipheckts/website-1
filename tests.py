#!flask/bin/python
import unittest
import bcrypt

from app import app, db
from app.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/website-testdb'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        user = User(name="harambe", email="harambe@cincinnatizoo.org",
                    password=bcrypt.hashpw("IAmHarambe".encode("utf-8"), bcrypt.gensalt2()))
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
