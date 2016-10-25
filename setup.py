import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()

setup(
    name="pytest-test-groups",
    description=('A Pytest plugin for running a subset of your tests by '
                 'splitting them in to equally sized groups.'),
    url='https://github.com/mark-adams/pytest-test-groups',
    author='Mark Adams',
    author_email='mark@markadams.me',
    packages=['pytest_test_groups'],
    version='1.0.3',
    long_description=read('README.rst'),
    install_requires=['pytest>=2.5'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Testing',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5'
                 ],
    entry_points={
        'pytest11': [
            'test-groups = pytest_test_groups',
        ]
    },
)
