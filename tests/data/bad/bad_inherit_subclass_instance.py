from __future__ import annotations

from cfg import CL

from ..base_cfg import cfg
from ..base_class import BaseClass

cfg = cfg.clone()

cfg.SUBCLASSES.ANOTHER = CL(BaseClass(), BaseClass, subclass=True)
