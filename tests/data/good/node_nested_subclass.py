from __future__ import annotations

from tests.data.base_class import SubClass

from .good import cfg

cfg = cfg.clone()
cfg.SUBCLASSES.ONE = SubClass
