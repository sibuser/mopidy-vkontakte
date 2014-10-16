from __future__ import unicode_literals

import re
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return [l.rstrip() for l in f.readlines()]


def get_test_requirements():
    with open('test-requirements.txt', 'r') as f:
        return [l.rstrip() for l in f.readlines()]

setup(
    name='Mopidy-VKontakte',
    version=get_version('mopidy/vkontakte/__init__.py'),
    url='https://github.com/sibuser/mopidy-vkontakte',
    license='Apache License, Version 2.0',
    author='Alexey Ulyanov',
    author_email='sibuser.nsk@gmail.com',
    description='Mopidy extension for VKontakte allows \
        to listen to music from VKontakte social network.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=get_requirements(),
    test_suite='nose.collector',
    tests_require=get_test_requirements(),
    entry_points={
        'mopidy.ext': [
            'vkontakte = mopidy.vkontakte:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
