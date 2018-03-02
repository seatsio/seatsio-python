from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='seatsio',
    version='1',
    description='The official Seats.io Python client library',
    long_description=readme,
    author_email='hello@seats.io',
    url='https://github.com/seatsio/seatsio-python',
    packages=find_packages(exclude=('tests')),
    test_suite='tests',
    tests_require=['unittest2']
)
