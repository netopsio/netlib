# NetLib

Netlib is my attempt at re-writing my
['pyRouterLib'](https://github.com/jtdub/pyRouterLib). The goal is to create a
library that is much more efficient and easier to use to establish SSH, Telnet,
and SNMP connection to network devices, such as routers and switches.

## Install

    git clone https://github.com/jtdub/netlib.git
    cd netlib
    sudo pip install -r requirements.txt
    sudo python setup.py install

## Access via Telnet and SSH

Currently, the SSH and Telnet modules have been created. Both modules have a
very similar API structure, with the biggest difference between the two are how
connections are established to network devices.

To use either the SSH or Telnet module, you need to import the library into your script:

    from netlib.remote import SSH
    from netlib.remote import Telnet

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
version <= 2. Version 3 support will hopefully come soon.

To use the SNMP functionality, you will need to import the module into your
python script.

    from netlib.remote import SNMP

From there, enter your polling parameters.

    r = SNMP('somerouter', 'superl33tr34d0ly_community', 'someMIBname')

Then you poll the device.

    r.snmp_get()

Again, the functionality of the SNMP module is still very limited. I hope to
work on it soon and create a more robust functionality for SNMP.
