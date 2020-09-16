from .good import cfg
from .base_cfg import BaseClass


class SubClass(BaseClass):
    pass


cfg.CLASS = SubClass()
