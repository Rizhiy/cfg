import codecs
import os

from setuptools import find_packages, setup

_module_name = "ntc"


def _read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def _get_version(rel_path):
    for line in _read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def _get_requirements(rel_path):
    reqs = []
    for line in _read(rel_path).splitlines():
        if not line.startswith("#"):
            reqs.append(line.strip())
    return reqs


setup(
    name=_module_name,
    version=_get_version(f"{_module_name}/__init__.py"),
    description="NeuroTrade Config Library",
    author="Vladimir Mikhaylov",
    author_email="v.mikhaylov@neurotrade.ru",
    packages=find_packages(exclude=["tests*"]),
    install_requires=_get_requirements(f"{_module_name}/requirements.txt"),
)
