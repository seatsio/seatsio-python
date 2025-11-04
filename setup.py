from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='seatsio',
    version='v81.12.0',
    description='The official Seats.io Python client library',
    author='The seats.io dev team',
    author_email='hello@seats.io',
    url='https://github.com/seatsio/seatsio-python',
    license="MIT",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages()
)
