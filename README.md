# NetLib

Netlib is my attempt at re-writing my
['pyRouterLib'](https://github.com/jtdub/pyRouterLib). The goal is to create a
library that is much more efficient and easier to use to establish SSH, Telnet,
and SNMP connection to network devices, such as routers and switches.

## Install

    git clone https://github.com/jtdub/netlib.git
    cd netlib
    sudo python setup.py install

## Access via Telnet and SSH

Currently, the SSH and Telnet modules have been created. Both modules have a
very similar API structure, with the biggest difference between the two are how
connections are established to network devices.

To use either the SSH or Telnet module, you need to import the library into your script:

    from netlib.conn_type import SSH
    from netlib.conn_type import Telnet 

From there, you define your connection parameters:

    telnet = Telnet('somerouter', 'username', 'password')
    ssh = SSH('somerouter', 'username', 'password')

Once the basic parameters have been set, you establish a connection to the
device.

    telnet.connect()
    ssh.connect()

Once you are connected, you are free to send commands to you network device. If
you intend to iterate through output that is long, then you can disable paging
on the output.

    telnet.disable_paging()
    ssh.disable_paging()

    telnet.command('show version')
    ssh.command('show version')

If you need to enter a privileged mode, you can use the set_enable api.

    telnet.set_enable('supersecretpassword')
    ssh.set_enable('supersecretpassword')

When you've completed your task on the device, you can close your connections.

    telnet.close()
    ssh.close()

At this point, those are the features that both libraries share. As the telnet
library and ssh library vary on how they parse data, there is a need for extra
functionality on the ssh library. Here is the API functionality that is
specific to the ssh library:

    ssh.clear_buffer()

The SSH library stores output into a buffer. Sometimes this buffer can present
results that aren't expected. Clearing the buffer should mitigate the
unexpected results.

## SNMP

SNMP functionality is still very experimental. It currently only supports SNMP
version 2. Version 3 support will hopefully come soon.

To use the SNMP functionality, you will need to import the module into your
python script.

    from netlib.conn_type import SNMPv2

From there, enter your polling parameters.

    r = SNMPv2('somerouter', 'superl33tr34d0ly_community', mib_name='SNMPv2-MIB',
             symbol_name='sysDescr', mib_index='0')

Then you poll the device.

    r.get()

Doing this returns the raw data. To display the information pulled in a human
readable format, you will need to call the extract method.

    r.extract()

Again, the functionality of the SNMP module is still very limited. I hope to
work on it soon and create a more robust functionality for SNMP.

## User Credentials

When working with a large number of devices, it's inconvenient to have to type
your credentials in a large number of times and storing your credentials
directly into a script can be insecure. Therefore, I created a library that
allows you to store them, in a file (still in-securely, but at least it's not
directly in a script that could be shared).

There are two methods. The first is a 'simple' method, which simple creates a
file and stores the credentials in the format of:

    username
    password
    enablepassword

The second method stores the credentials as a yaml file:

    username: some_user
    password: some_pass
    enable: some_l33t_pass

To call these methods you import the library:

    from netlib.user_creds import simple
    from netlib.user_creds import simple_yaml

Note, that you only need to use one method. Next, you call the method and
define your parameters:

    simple = simple(creds_file='.tacacs')
    yaml = simple_yaml(creds_file='.tacacs.yml')

The default file name for simple is '.tacacslogin' and for simple_yaml it's
'.tacacs.yml', respectively. These files are stored in your home directory
(~/).

If the files don't exist, then you are prompted for your credentials, so that
you can create them.

    >>> from netlib.user_creds import simple_yaml
    >>> y = simple_yaml(creds_file='.tacacs.yml')
    Username: jtdub
    User Password: 
    Confirm Password: 
    Error: Your user passwords do not match.
    
    User Password: 
    Confirm Password: 
    Enable Password: 
    Confirm Password: 
    Creating the credentials file, as it does not exist.
    File Location: /Users/jtdub/.tacacs.yml

As you can see, if your passwords do not match, then it prompts you to re-enter
your passwords. From here, your credentials are passed to your script in the
form of a dictionary:

    >>> y
    {'username': 'jtdub', 'enable': 'tew', 'password': 'asdf'}
    >>>

This is true for both simple and yaml formats.

## SNMP Credentials

Storage and usage of SNMP credentials will be created when I flesh out SNMP
functionality of the library.
