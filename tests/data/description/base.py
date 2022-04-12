from __future__ import annotations

from ntc import CL, CN
from tests.data.base_cfg import cfg

cfg = cfg.inherit()

cfg.DESCRIBED = CL("described", desc="Described leaf")
cfg.DESCRIBED_NESTING = CN(CL(str, desc="Described nesting"))
