#!/usr/bin/python

import unittest
import keyring

class TestKeyRing(unittest.TestCase):
    creds = {'username': 'testuser', 'password': 'testpass', 'enable': 'enabletest'}

class TestSetCreds(TestKeyRing):
    def test_1(self):
        self.assertEquals(creds)

if __name__ == '__main__':
    unittest.main()
