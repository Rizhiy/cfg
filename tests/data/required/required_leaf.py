from __future__ import annotations

from ntc import CL

from ..base_cfg import cfg

cfg = cfg.inherit()
cfg.REQUIRED = CL(None, str, required=True)
