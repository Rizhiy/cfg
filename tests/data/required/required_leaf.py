from __future__ import annotations

from rizhiy_cfg import CL

from ..base_cfg import cfg

cfg = cfg.inherit()
cfg.REQUIRED = CL(None, str, required=True)
