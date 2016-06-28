class KeyRing(object):

    def __init__(self, username):
        import keyring
        import getpass
        self.username = username

    def get_creds(self):

        if keyring.get_password('nl_user_pass',
                                username=self.username) is None:
            print('No credentials keyring exist. Creating new credentials.')
            self.set_creds()
        else:
            user_pass = keyring.get_password('nl_user_pass',
                                             username=self.username)

            enable_pass = keyring.get_password('nl_enable_pass',
                                               username=self.username)

            return {'username': self.username,
                    'password': user_pass,
                    'enable': enable_pass}

    def set_creds(self):
        match = False
        while match is False:
            password1 = getpass.getpass('Enter your user password: ')
            password2 = getpass.getpass('Confirm your user password: ')

            if password1 == password2:
                user_password = password1
                match = True

        match = False
        while match is False:
            password1 = getpass.getpass('Enter your enable password: ')
            password2 = getpass.getpass('Confirm your enable password: ')

            if password1 == password2:
                enable_password = password1
                match = True

        user_pass = keyring.set_password('nl_user_pass',
                                         username=self.username,
                                         password=user_password)

        enable_pass = keyring.set_password('nl_enable_pass',
                                           username=self.username,
                                           password=enable_password)


        self.get_creds()

    def del_creds(self):
        tries = 0
        max_tries = 5

        while tries <= max_tries:
            user_pass = keyring.get_password('nl_user_pass',
                                             username=self.username)
            ask_pass = getpass.getpass('Enter your user password: ')

            if user_pass == ask_pass:
                print('Deleting keyring credentials for {}'.format(
                    self.username))
                keyring.delete_password('nl_user_pass',
                                        username=self.username)
                keyring.delete_password('nl_enable_pass',
                                        username=self.username)
                tries = max_tries + 1
            else:
                tries += 1
                print('Error: Incorrect password.')
