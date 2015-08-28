def get_creds(creds_file):
    from os.path import expanduser
    from os.path import isfile
    import getpass

    if not isfile(expanduser('~/' + creds_file)):
        blank_user = True
        while blank_user is True:
            username = raw_input("Username: ")
            if len(username) <= 0:
                print("Error: Your username can't be blank.")
            else:
                blank_user = False

        password_match = False
        while password_match is False:
            password = getpass.getpass("User Password: ").strip()
            confirm_password = getpass.getpass("Confirm Password: ").strip()
            if password == confirm_password:
                password_match = True
            else:
                print("Error: Your user passwords do not match.\n")

        enable_match = False
        while enable_match is False:
            enable = getpass.getpass("Enable Password: ").strip()
            confirm_enable = getpass.getpass("Confirm Password: ").strip()
            if enable == confirm_enable:
                enable_match = True
            else:
                print("Error: Your enable passwords do not match.\n")

        return {'username': username, 'password': password, 'enable': enable}


def simple(creds_file=".tacacslogin"):
    from os.path import expanduser
    from os.path import isfile

    creds = get_creds(creds_file)

    if not isfile(expanduser('~/' + creds_file)):
        print("Creating the credentials file, as it does not exist.")
        print("File Location: " + expanduser('~/' + creds_file))
        with open(expanduser('~/' + creds_file), 'w') as f:
            f.write(creds['username'] + "\n")
            f.write(creds['password'] + "\n")
            f.write(creds['enable'] + "\n")
        f.close()
        return creds
    else:
        with open(expanduser('~/' + creds_file), 'r') as f:
            simple_creds = {}
            simple_creds['username'] = f.readline().strip()
            simple_creds['password'] = f.readline().strip()
            simple_creds['enable'] = f.readline().strip()
        f.close()
        return simple_creds


def simple_yaml(creds_file=".tacacs.yml"):
    from os.path import expanduser
    from os.path import isfile
    import yaml

    creds = get_creds(creds_file)

    if not isfile(expanduser('~/' + creds_file)):
        print("Creating the credentials file, as it does not exist.")
        print("File Location: " + expanduser('~/' + creds_file))
        with open(expanduser('~/' + creds_file), 'w') as f:
            f.write(yaml.dump(creds, default_flow_style=False))
        f.close()
        return creds
    else:
        with open(expanduser('~/' + creds_file), 'r') as f:
            yaml_creds = yaml.load(f)
        f.close()
        return yaml_creds
