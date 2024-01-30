from __future__ import annotations

from pycs import CN
from tests.data.base_class import BaseClass
from tests.data.required.bad_inherit import schema

cfg = CN(schema)
cfg.REQUIRED_CLASSES.TWO = BaseClass()
