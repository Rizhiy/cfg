from __future__ import annotations

from rizhiy_cfg import CN
from tests.data.base_class import SubClass
from tests.data.required.required_subclass import cfg

cfg = CN(cfg)
cfg.REQUIRED_SUBCLASSES.ONE = SubClass
