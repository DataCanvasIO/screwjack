
from setuptools import setup, find_packages
import os

setup(
    name="screwjack",
    version='0.0.1',
    author="Xiaolin Zhang",
    author_email="leoncamel@gmail.com",
    license='MIT',
    install_requires=['click', 'jinja2', 'requests'],
    packages=['screwjack'],
    include_package_data = True,
    package_data = {
        '': ['templates/*']
    },
    scripts=[
        'bin/screwjack'
    ]
)
