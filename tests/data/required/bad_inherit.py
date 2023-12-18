from __future__ import annotations

from cfg import CL

from ..base_class import BaseClass
from .required_spec import cfg

cfg = cfg.clone()
cfg.REQUIRED_CLASSES.ONE = CL(BaseClass(), BaseClass)
