#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages

from novel import __version__

long_description = 'This project helps you to download novels from Internet, and easily write into files.'

if __name__ == '__main__':
    assert sys.version_info.major > 2, 'Only works with python3'
    setup(
        name='FetchNovels',
        version=__version__,
        description='Fetch novels from Internet',
        long_description=long_description,
        license='GPLv3',
        url='https://github.com/wangjiezhe/FetchNovels',

        author='wangjiezhe',
        author_email='wangjiezhe@gmail.com',

        packages=find_packages(exclude=['docs', 'tools', 'tests*']),
        entry_points={
            'console_scripts': ['fetchnovels=novel.main:main'],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ]
    )
