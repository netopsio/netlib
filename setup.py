#!/usr/bin/env python

from setuptools import setup
from netlib import __version__


setup(
    name='netlib',
    version=__version__,
    url='https://github.com/jtdub/netlib',
    author='James Williams',
    license='MIT',
    install_requires=[
        'paramiko',
        'pycrypto',
        'pysnmp',
        'keyring',
        'keyrings.alt'
    ],
    description='Simple access to network devices, such as routers and switches, via Telnet, SSH, and SNMP',
    packages=[
        'netlib',
    ],
)
