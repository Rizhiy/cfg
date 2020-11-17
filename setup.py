from ntu.setup.utils import get_requirements, get_version
from setuptools import find_packages, setup

_module_name = "ntc"

setup(
    name=_module_name,
    version=get_version(f"{_module_name}/__init__.py"),
    description="NeuroTrade Config Library",
    author="Vladimir Mikhaylov",
    author_email="v.mikhaylov@neurotrade.ru",
    packages=find_packages(exclude=["tests*"]),
    install_requires=get_requirements(f"{_module_name}/requirements.txt"),
)
