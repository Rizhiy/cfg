from ntc import CN

from ..base_cfg import BaseClass
from .good import cfg

cfg = CN(cfg)
cfg.CLASSES.ONE = BaseClass()
