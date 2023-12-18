from __future__ import annotations

from cfg import CL, CN

from ..base_cfg import cfg
from ..base_class import BaseClass

cfg = cfg.inherit()
cfg.REQUIRED_SUBCLASSES = CN(CL(None, BaseClass, required=True, subclass=True))
