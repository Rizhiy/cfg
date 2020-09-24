from ntc import CL, CN

from .base_class import BaseClass

cfg = CN()

cfg.NAME = CL(None, str)
cfg.DICT = CN()
cfg.DICT.INT = 1
cfg.DICT.FOO = "foo"
cfg.DICT.X = "X"
cfg.LIST = [1, 2, 3, 4]
cfg.CLASS = BaseClass()
cfg.CLASSES = CN(BaseClass)
cfg.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))


def transform(cfg: CN):
    cfg.DICT.X = "Y"


def validate(cfg: CN):
    assert cfg.NAME != "Bad"


cfg.add_transform(transform)
cfg.add_validator(validate)
