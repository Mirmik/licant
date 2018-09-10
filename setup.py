#!/usr/bin/env python3

from setuptools import setup
import glob
import os

setup(
	name = 'licant',
	packages = ['licant'],
	version = '0.18.9',
	license='MIT',
	description = 'licant make system',
	author = 'Sorokin Nikolay',
	author_email = 'mirmikns@yandex.ru',
	url = 'https://github.com/mirmik/licant',
	keywords = ['testing', 'make'],
	classifiers = [],

	scripts = ["configurator/licant-config", "configurator/licant-init"],
	package_data={'licant': [
    	'templates/cxx/make.py',
    	'templates/cxx/main.cpp',
    	'templates/cxxgxx/make.py',
    	'templates/cxxgxx/main.cpp',
    ]}
)
