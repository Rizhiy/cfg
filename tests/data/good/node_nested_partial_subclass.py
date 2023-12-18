from __future__ import annotations

from functools import partial

from cfg import CN
from tests.data.base_class import SubClass

from .good import cfg

cfg = CN(cfg)
cfg.SUBCLASSES.ONE = partial(SubClass)
