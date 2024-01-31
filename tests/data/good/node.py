from __future__ import annotations

from tests.data.base_class import BaseClass

from .good import cfg

cfg = cfg.clone()
cfg.CLASSES.ONE = BaseClass()
