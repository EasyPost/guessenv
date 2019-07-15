#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils import setup, find_packages


setup(
    name='guessenv',
    version='0.2',
    author='EasyPost OSS',
    author_email='oss@easypost.com',
    url='https://github.com/easypost/guessenv',
    license='ISC',
    packages=find_packages(exclude=['test']),
    description='Parse Python files and look for required environment variables',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'guessenv = guessenv.__main__:main',
        ]
    },
    project_urls={
        'Issue Tracker': 'https://github.com/easypost/guessenv/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: ISC License (ISCL)',
    ]
)
