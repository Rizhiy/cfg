from __future__ import annotations

from pycs import CL

from ..base_cfg import cfg
from ..base_class import BaseClass


class BadClass:
    pass


cfg = cfg.clone()

cfg.CLASSES.ANOTHER = CL(BadClass(), BaseClass)
