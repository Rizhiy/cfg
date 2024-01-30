from __future__ import annotations

from pycs import CN
from tests.data.base_class import SubClass
from tests.data.required.required_subclass import schema

cfg = CN(schema)
cfg.REQUIRED_SUBCLASSES.ONE = SubClass
