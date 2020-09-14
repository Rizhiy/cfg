import codecs
import os

from setuptools import find_packages, setup

_module_name = "nt_config"


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name=_module_name,
    version=get_version(f"{_module_name}/__init__.py"),
    description="NeuroTrade Config Library",
    author="Artem Vasenin",
    author_email="a.vasenin@neurotrade.ru",
    packages=find_packages(exclude=["tests*"]),
)
