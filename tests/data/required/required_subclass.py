from ntc import CL, CN

from ..base_cfg import cfg
from ..base_class import BaseClass

cfg = cfg.clone()
cfg.REQUIRED_SUBCLASSES = CN(CL(None, BaseClass, required=True, subclass=True))
