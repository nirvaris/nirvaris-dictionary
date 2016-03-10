import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='nirvaris-dictionary',
    version='1.4',
    packages=['dictionary'],
    include_package_data=True,
    license='MIT License',  # example license
    description='A simple Django app for post and comments on the website with some meta-tags.',
    long_description=README,
    url='https://github.com/nirvaris/nirvaris-dictionary',
    author='Nirvaris',
    author_email='contact@nirvaris.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
