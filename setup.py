
from setuptools import setup, find_packages
import os
import screwjack

setup(
    name="screwjack",
    version=screwjack.__version__,
    description="ScrewJack is a tiny command line tool for manipulating modules.",
    author="Xiaolin Zhang",
    author_email="leoncamel@gmail.com",
    url="https://github.com/DataCanvasIO/screwjack",
    license='BSD',
    install_requires=['click==0.6', 'jinja2>=2.7.2', 'requests>=2.2.1', 'python-dateutil==2.2', 'pytz>=2014.3'],
    packages=['screwjack'],
    include_package_data = True,
    package_data = {
        '': ['templates/*']
    },
    scripts=[
        'bin/screwjack'
    ],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities"
    ]
)
