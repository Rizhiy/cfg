# Python Configuration System

![tests](https://github.com/Rizhiy/pycs/actions/workflows/test_and_version.yml/badge.svg)
![publish](https://github.com/Rizhiy/pycs/actions/workflows/publish.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io)

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

cfg = CN()  # Basic config node
cfg.DICT = CN()  # Nested config node
cfg.DICT.FOO = "FOO"  # Config leaf with actual value
cfg.DICT.INT = 1
cfg.NAME = CL(None, str, required=True)  # Specification of config leaf to be defined with type
cfg.CLASSES = CN(BaseClass)  # Config node with type specification of its config leafs
cfg.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))  # Config node with subclass specification of its config leafs
cfg.VAL = CL(1, desc="Interesting description") # Config leaf with description

def transform(cfg: CN) -> None:
    cfg.DICT.FOO = "BAR"

def validate(cfg: CN) -> None:
    assert len(cfg.NAME) > 0

def hook(cfg: CN) -> None:
    print("Loaded")

# Add transform, validation & hooks function
# Transforms are run after config is loaded and can change values in config
cfg.add_transform(transform)
# Validators are run after transforms and freeze, with them you can verify additional restrictions
cfg.add_validator(validate)
# Hooks are run after validators and can perform additional actions outside of config
cfg.add_hook(hook)
# Validators and hooks should not (and mostly cannot) modify the config
```

1. Set actual values for each leaf in the config, **the import has to be absolute**:

```python
# my_cfg.py
from pycs import CN

from project.config import cfg # Import has to be absolute

# Pass schema as an argument to the CN() to init the schema
cfg = CN(cfg)

# Schema changes are not allowed here, only leafs can be altered.
cfg.NAME = "Hello World!"
cfg.DICT.INT = 2
```

You can also create another file to inherit from first and add more changes:

```python
# my_cfg2.py
from ntc import CN

from .my_cfg import cfg # This import has to be relative and should only import cfg variable

cfg = CN(cfg)
cfg.DICT.FOO = "BAR"
```

There a few restrictions on imports in configs:

- When you are importing config schema from project that import has to be **absolute**
- When you inherit config values from another file, that import has to be **relative**
- Other than config inheritance, all other imports have to be **absolute**

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
