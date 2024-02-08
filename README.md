# Python Configuration System

![tests](https://github.com/Rizhiy/pycs/actions/workflows/test_and_version.yml/badge.svg)
[![codecov](https://codecov.io/gh/Rizhiy/pycs/graph/badge.svg?token=7CAJG2EBLG)](https://codecov.io/gh/Rizhiy/pycs)
![publish](https://github.com/Rizhiy/pycs/actions/workflows/publish.yml/badge.svg)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FRizhiy%2Fpycs%2Fmaster%2Fpyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/pycs)](https://pypi.org/project/pycs/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Description

Library to define configurations using python files.

## Installation

Recommended installation with pip:

```bash
pip install pycs
```

### Usage

1. Define config schema:

```python
# project/config.py
from pycs import CL, CN

class BaseClass:
    pass

schema = CN()  # Basic config node
schema.DICT = CN()  # Nested config node
schema.DICT.FOO = "FOO"  # Config leaf with actual value
schema.DICT.INT = 1
schema.NAME = CL(None, str, required=True)  # Specification of config leaf to be defined with type
schema.CLASSES = CN(BaseClass)  # Config node with type specification of its config leaves
schema.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))  # Config node with subclass specification of its config leaves
schema.VAL = CL(1, desc="Interesting description") # Config leaf with description

def transform(cfg: CN) -> None:
    cfg.NAME = cfg.NAME or "__static__"
    cfg.DICT.FOO = "BAR"

def validate(cfg: CN) -> None:
    assert len(cfg.NAME) > 0

def hook(cfg: CN) -> None:
    print("Loaded")

# Add transform, validation & hooks function
# Transforms are run after config is loaded and can change values in config
# Can also be run at runtime using .transform()
# If you plan to transform multiple times we strongly recommend to make them idempotent
schema.add_transform(transform)
# Validators are run after transforms and freeze, with them you can verify additional restrictions
schema.add_validator(validate)
# Hooks are run after validators and can perform additional actions outside of config
schema.add_hook(hook)
# Validators and hooks should not (and mostly cannot) modify the config
```

1. If you want to use configuration with default values or make changes in the program you can use `.static_init()`:

```python
from project.config import schema

cfg = schema.static_init() # 'Loaded'
print(cfg.DICT.FOO) # 'BAR'
```

1. If you want to store changes more permanently, please create a config file:

```python
# my_cfg.py
from pycs import CN

from project.config import schema

# Use init_cfg() to separate changes from base variable and freeze schema
cfg = schema.init_cfg()

# Schema changes are not allowed here, only leaves can be altered.
cfg.NAME = "Hello World!"
cfg.DICT.INT = 2
```

You can also create another file to inherit from first and add more changes:

```python
# my_cfg2.py
from ntc import CN

from .my_cfg import cfg

# Separate changes from parent, important when inheriting in multiple files
cfg = cfg.clone()
cfg.DICT.FOO = "BAR"
```

There a few restrictions on imports in configs:

- If you are inheriting changes from another config, please import variable as `cfg`
- No other import should be named `cfg`

1. Load actual config and use it in the code.

```python
# main.py
from pycs import CN

cfg = CN.load("my_cfg.py")
# Access values as attributes
assert cfg.NAME == "Hello World!"
assert cfg.DICT.FOO == "BAR"
```

## Development

- Install dev dependencies: `pip install -e ".[dev]"`
- For linting and basic fixes [ruff](https://docs.astral.sh/ruff/) is used: `ruff check . --fix`
- This repository follows strict formatting style which will be checked by the CI.
  To properly format the code, use the [black](https://black.readthedocs.io) format: `black .`
- To test code, use [pytest](https://pytest.org): `pytest .`
- This repository follows semantic-release, which means all commit messages have to follow a [style](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html).
  You can use tools like [commitizen](https://github.com/commitizen-tools/commitizen) to write your commits.

## Acknowledgements

This library was inspired by [yacs](https://github.com/rbgirshick/yacs).
