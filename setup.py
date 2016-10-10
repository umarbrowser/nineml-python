#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="nineml",
    version="0.1.0",
    packages=find_packages(),
    # add your name here if you contribute to the code
    author="Andrew P. Davison, Thomas G. Close, Mike Hull, Eilif Muller",
    author_email="nineml-users@incf.org",
    description=(
        "A tool for reading, writing and generally working with 9ML files."),
    long_description=open("README.rst").read(),
    license="BSD 3 License",
    keywords="computational neuroscience modeling interoperability XML",
    url="http://nineml.net",
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2',
                 'Topic :: Scientific/Engineering'],
    install_requires=['lxml', 'sympy'], # NB: sympy 1.0 has a bug in ccode, which is fixed in the master branch 30/7/16
    tests_require=['nose', 'numpy']
)
