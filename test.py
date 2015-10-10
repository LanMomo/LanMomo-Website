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

        self.assertEqual(binary_exp_hash, actual_hash)

    def test_get_hash_empty_password(self):
        password = ''
        salt = 'salt'
        expected_hash = ("2e3fce77cf8c4c7478a96d20"
                         "7c1c39715892cac84a18cbec"
                         "9b634f4bc22b390b48cd30a4"
                         "df2e7ebbaee65c346a662c5be"
                         "2d12441322f7a4bac821a382c4af091")
        binary_exp_hash = binascii.unhexlify(expected_hash)
        actual_hash = app.get_hash(password, salt)

        self.assertEqual(binary_exp_hash, actual_hash)

    def test_get_hash_empty_salt(self):
        password = 'pass'
        salt = ''
        expected_hash = ("5b722b307fce6c944905d132"
                         "691d5e4a2214b7fe92b73892"
                         "0eb3fce3a90420a19511c301"
                         "0a0e7712b054daef5b57bad5"
                         "9ecbd93b3280f210578f547f4aed4d25")
        binary_exp_hash = binascii.unhexlify(expected_hash)
        actual_hash = app.get_hash(password, salt)

        self.assertEqual(binary_exp_hash, actual_hash)


if __name__ == '__main__':
    unittest.main()
