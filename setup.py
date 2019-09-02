# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    package_data = {'project': ['URL/*.csv']},
    entry_points = {'scrapy': ['settings = scrapy_alibaba.settings']},
    zip_safe	 = False,
)
