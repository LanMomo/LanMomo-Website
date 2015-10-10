import app
import unittest
from models import User
from database import db_session, clear_db
import hashlib
import binascii


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.setup('config/test_config.py')

    def tearDown(self):
        clear_db()


class EmailExistsTestCase(BaseTestCase):

    def insert_email_fixture(self):
        username = 'test'
        firstname = 'test'
        lastname = 'test'
        email = 'test@test.com'
        phone = '123-123-1234'
        salt = 'salt'
        password = app.get_hash('test', salt)

        user = User(username, firstname, lastname, email,
                    phone, password, salt)

        db_session.add(user)
        db_session.commit()

    def test_email_does_not_exists(self):
        actual = app.email_exists("test@test.com")
        self.assertFalse(actual)

    def test_email_exists(self):
        self.insert_email_fixture()
        actual = app.email_exists("test@test.com")
        self.assertTrue(actual)


class GetHashTestCase(BaseTestCase):

    def test_get_hash(self):
        password = 'pass'
        salt = 'salt'
        expected_hash = ("4ab3490b9dd9fbcd6eb9ec6e"
                         "2078a99c8de5d4d0ae1371fa"
                         "ad97fdc83774dbeeec52c971"
                         "c41971f71b131587c1becb17"
                         "07435b24771d392631298647ba04e37d")
        binary_exp_hash = binascii.unhexlify(expected_hash)
        actual_hash = app.get_hash(password, salt)
        print(binascii.hexlify(actual_hash))

        self.assertEqual(binary_exp_hash, actual_hash)

    def get_hash_empty_password(self):
        password = ''
        salt = 'salt'
        expected_hash = self.get_hash(password, salt)
        actual_hash = app.get_hash(password, salt)

        self.assertEqual(expected_hash, actual_hash)

    def get_hash_empty_salt(self):
        password = 'pass'
        salt = ''
        expected_hash = self.get_hash(password, salt)
        actual_hash = app.get_hash(password, salt)

        self.assertEqual(expected_hash, actual_hash)


if __name__ == '__main__':
    unittest.main()
