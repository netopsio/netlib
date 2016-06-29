#!/usr/bin/python

import unittest
import keyring

from netlib.user_keyring import KeyRing

creds = {'username': 'testuser', 'password': 'testpass', 'enable': 'enabletest'}

class TestKeyRing(unittest.TestCase):
    user = KeyRing(username=creds['username'])
    keyring.set_password('nl_user_pass', username=creds['username'], password=creds['password'])
    keyring.set_password('nl_user_enable', username=creds['username'], password=creds['enable'])

class TestSetCreds(TestKeyRing):
    def test_1(self):
        self.assertEquals(self.user.get_creds(), creds)

if __name__ == '__main__':
    unittest.main()
