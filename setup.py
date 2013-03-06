#!/usr/bin/env python

"""
 Copyright 2013 the original author or authors

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
"""

from codecs import open

from setuptools import find_packages, setup


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

try:
    import importlib
except ImportError:
    install_requires.append('importlib')

tests_requires = install_requires + [
    'nose',
]

setup(
    name='livetribe-plugins',
    version='1.0.0',
    url='http://github.com/livetribe/livetribe-plugins/',
    license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
    author='Alan D. Cabrera',
    author_email='dev@livetribe.codehaus.org',
    description='A simple python plugin framework.',
    # don't ever depend on refcounting to close files anywhere else
    long_description=open('README.rst', encoding='utf-8').read(),

    namespace_packages = ['livetribe'],
    package_dir = {'':'src'},
    packages=find_packages('src'),

    zip_safe=False,
    platforms='any',
    install_requires=install_requires,

    tests_require=tests_requires,
    test_suite='nose.collector',

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
