from __future__ import annotations

from tests.data.base_class import BaseClass
from tests.data.required.bad_inherit import schema

cfg = schema.init_cfg()
cfg.REQUIRED_CLASSES.TWO = BaseClass()
