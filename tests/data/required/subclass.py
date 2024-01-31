from __future__ import annotations

from tests.data.base_class import SubClass
from tests.data.required.required_subclass import schema

cfg = schema.init_cfg()
cfg.REQUIRED_SUBCLASSES.ONE = SubClass
