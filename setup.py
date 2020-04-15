"""setup.py

Used for installing srelogging via pip.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(install_requires=["pyyaml"],
      name="srelogging",
      version="#{TAG_NAME}#",
      description="Common logging functions for SRE python scripts.",
      long_description=repo_file_as_string("README.md"),
      long_description_content_type="text/markdown",
      author="Sam Gibson",
      author_email="sgibson@glasswallsolutions.com",
      py_modules=['srelogging'],
      python_requires=">=3.7")
