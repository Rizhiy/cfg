from __future__ import annotations

from rizhiy_cfg import CL

from ..base_cfg import cfg
from ..base_class import BaseClass

cfg = cfg.clone()

cfg.CLASSES.ANOTHER = CL(None, BaseClass, subclass=True)
