#!/usr/bin/env python

from setuptools import setup
from netlib import __version__


setup(
    name='netlib',
    version=__version__,
    url='https://github.com/netopsio/netlib',
    author='James Williams',
    license='MIT',
    install_requires=[
        'paramiko',
        'pycrypto',
        'keyring',
        'keyrings.alt'
    ],
    description='Simple access to network devices, such as routers and switches, via Telnet and SSH.',
    packages=[
        'netlib',
    ],
)
