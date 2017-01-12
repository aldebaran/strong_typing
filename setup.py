#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

CONTAINING_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

package_list = find_packages(where=CONTAINING_DIRECTORY, exclude=(), include=())

setup(
    name='strong-typing-py',
    version=open(os.path.join(CONTAINING_DIRECTORY,"strong_typing/VERSION")).read().split()[0],
    author='Surya Ambrose',
    author_email='sambrose@softbankrobotics.com',
    packages=package_list,
    package_data={"strong_typing":["VERSION"]},
    url='.',
    license='LICENSE.txt',
    description='Classes to create strongly typed structures in Python',
    long_description=open(os.path.join(CONTAINING_DIRECTORY,'README.rst')).read(),
    test_suite="tests",
    install_requires=[
        "enum34 >= 1.0.4"
    ]
)
