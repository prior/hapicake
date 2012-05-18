#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = '0.1.1'

setup(
    name='hapicake',
    version=VERSION,
    author='prior',
    author_email='mprior@hubspot.com',
    packages=find_packages(),
    url='https://github.com/HubSpot/hapicake',
    download_url='https://github.com/HubSpot/hapicake/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description='a next generation hapipy',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=0,<1',
        'cython>=0,<1',
        'gevent<2',
        'sanetime>=4,<5',
        'utilspy>=0,<1',
        'giftwrap>=1,<2',
    ],
    dependency_links=[
        'https://bitbucket.org/denis/gevent/get/82f623ff862a.tar.gz#egg=gevent'   # gevent 1.0b2
    ],
    platforms=['any'],
)

