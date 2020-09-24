from ntc import CN

from ..base_class import BaseClass
from ..good.good import cfg

cfg = CN(cfg)
cfg.CLASSES.ONE = BaseClass()
