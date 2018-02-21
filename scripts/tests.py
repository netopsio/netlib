#!/usr/bin/python

import unittest

class TestImports(unittest.TestCase):

    def test_import_keyring(self):
        try:
            from netlib.user_keyring import KeyRing
            user_keyring = True
        except:
            user_keyring = False
            raise
        self.assertTrue(user_keyring)

    def test_import_ssh(self):
        try:
            from netlib.conn_type import SSH
            ssh = True
        except:
            ssh = False
            raise
        self.assertTrue(ssh)

    def test_import_telnet(self):
        try:
            from netlib.conn_type import Telnet
            telnet = True
        except:
            telnet = False
            raise
        self.assertTrue(telnet)


if __name__ == '__main__':
    unittest.main()
