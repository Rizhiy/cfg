from . import good
from .subclass_class import SubClass
from ntc import CN

cfg = CN(good.cfg)
cfg.CLASS = SubClass()
