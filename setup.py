from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='seatsio',
    version='v48',
    description='The official Seats.io Python client library',
    author='The seats.io dev team',
    author_email='hello@seats.io',
    url='https://github.com/seatsio/seatsio-python',
    license="MIT",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    packages=find_packages(),
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
