from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='seatsio',
    version='1',
    description='The official Seats.io Python client library',
    long_description=readme,
    author='The seats.io dev team',
    author_email='hello@seats.io',
    url='https://github.com/seatsio/seatsio-python',
    download_url="https://github.com/seatsio/seatsio-python/archive/0.1.tar.gz",
    license="MIT",

    packages=[
        'seatsio'
    ],
    install_requires=[
        "requests",
        "munch",
        "jsonpickle",
        "future",
        "six"
    ],

    test_suite='tests',
    tests_require=['unittest2']
)
