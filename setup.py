# This file is the build and installation script for this project
# The file tells pip the name, location, dependicies and how it should be installed

from setuptools import setup, find_packages

setup(
    name="pulseai",
    version="0.1.0",
    author="Khalil Ahmad Qamar",
    author_email="kaqamar@uwaterloo.ca",
    packages=find_packages(),
    # find the __init__.py file and install that package as a local package
    install_requires=[]
)