import os
from setuptools import setup, find_packages


path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
  long_description = "docker-compose helper"

setup(
    name = "dc-help",
    version = "0.0.2",
    keywords = ["pip", "docker-compose", "cli", "docker", "helper"],
    description = "docker-compose helper",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=2.7",
    license = "MIT Licence",

    url = "https://github.com/perfectstorm88/dchelp",
    author = "perfectstorm88",
    author_email = "perfectstorm88@163.com",

    packages = find_packages(),
    include_package_data = True,
    install_requires = [""],
    platforms = "any",

    scripts = [],
    entry_points = {
        'console_scripts': [
            'dc-help=dchelp:main_cli'
        ]
    }
)
