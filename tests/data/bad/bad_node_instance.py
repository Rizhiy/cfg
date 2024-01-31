from __future__ import annotations

from tests.data.base_class import BaseClass

from ..good.good import cfg


class SubClass(BaseClass):
    pass


cfg = cfg.clone()
cfg.SUBCLASSES.ONE = SubClass()
