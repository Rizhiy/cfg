from __future__ import annotations

from rizhiy_cfg import CL, CN

from .base_class import BaseClass

cfg = CN(desc="Root config node")

cfg.NAME = CL(None, str)
cfg.DICT = CN()
cfg.DICT.INT = 1
cfg.DICT.FOO = "Default foo value"
cfg.DICT.FOO2 = "Default foo2 value"
cfg.DICT.X = "X"
cfg.LIST = [1, 2, 3, 4]
cfg.STR = "Default str value"
cfg.BOOL = False
cfg.CLASS = BaseClass()
cfg.CLASSES = CN(BaseClass)
cfg.SUBCLASS = BaseClass
cfg.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))
cfg.NEW = CN(new_allowed=True)


def transform(cfg: CN):
    cfg.DICT.X = "Y"


def validate(cfg: CN):
    assert cfg.NAME != "Bad"


cfg.add_transform(transform)
cfg.add_validator(validate)
