"""
Install with `pip install .`
"""
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
import codecs
import io
import re
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'test/']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='parserbot',
    version=find_version('parserbot', '__init__.py'),
    url='http://github.com/hyperstudio/parserbot/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Flask>=0.10.1'],
    cmdclass={'test': PyTest},
    license='GPL2',
    author='MIT HyperStudio',
    author_email='hyperstudio@mit.edu',
    test_suite='test',
    tests_require=['pytest', 'pytest-flask'],
    extras_require={
        'testing': ['pytest>=2.6.4', 'pytest-flask>=0.6.0'],
        'docs': ['Sphinx>=1.2.3'],
        'stanford_ner': ['nltk==3.0.1'],
        'deploy': ['gunicorn==19.3.0']
    },
    description='Natural Language services and APIs all in one place',
    long_description=long_description
)
