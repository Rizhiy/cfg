from __future__ import annotations

from cfg import CN
from tests.data.base_class import BaseClass
from tests.data.required.bad_inherit import cfg

cfg = CN(cfg)
cfg.REQUIRED_CLASSES.TWO = BaseClass()
