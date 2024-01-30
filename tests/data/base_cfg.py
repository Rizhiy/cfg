from __future__ import annotations

from pycs import CL, CN

from .base_class import BaseClass

schema = CN(desc="Root config node")

schema.NAME = CL(None, str)
schema.DICT = CN()
schema.DICT.INT = 1
schema.DICT.FOO = "Default foo value"
schema.DICT.FOO2 = "Default foo2 value"
schema.DICT.X = "X"
schema.LIST = [1, 2, 3, 4]
schema.STR = "Default str value"
schema.BOOL = False
schema.CLASS = BaseClass()
schema.CLASSES = CN(BaseClass)
schema.SUBCLASS = BaseClass
schema.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))
schema.NEW = CN(new_allowed=True)


def transform(cfg: CN):
    cfg.DICT.X = "Y"


def validate(cfg: CN):
    assert cfg.NAME != "Bad"


schema.add_transform(transform)
schema.add_validator(validate)
