#!/usr/bin/env python
from setuptools import setup, find_packages

version = '1.0.6'


def readme():
    with open('README.md') as fp:
        return fp.read()


setup(
    name='api.mock',
    version=version,
    description='A utility of APIMock. (https://github.com/brucezz/APIMock)',
    long_description=readme(),
    url='https://github.com/brucezz/APIMockHelper',
    author='Bruce Zheng',
    author_email='im.brucezz@gmail.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='adb python',
    packages=find_packages(),
    install_requires=[
        'docopt',
        'prettytable',
    ],
    entry_points={
        'console_scripts': [
            'api.mock = apimock.helper:main'
        ]
    },
)
