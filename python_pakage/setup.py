# path : ./setup.py

from setuptools import setup, find_packages


setup(
    name='mypackage',
    version= '1.0.0', 
    description='Python Package Example Test', 
    author='Namkyun Kim', 
    packages=find_packages(),
    install_requires=[],
)