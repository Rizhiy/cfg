from ntc import CN

from ..base_cfg import BaseClass
from .good import cfg


class SubClass(BaseClass):
    pass


cfg = CN(cfg)
cfg.SUBCLASSES.ONE = SubClass
