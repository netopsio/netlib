from distutils.core import setup

import netlib

setup(
    name='netlib',
    version=netlib.__version__,
    url='https://github.com/jtdub/netlib',
    author='James Williams',
    install_requires=['paramiko>=1.14.0'],
    description='Simple access to network devices, such as routers and switches, via Telnet, SSH, and SNMP',
    packages=['netlib',],
    )
