from __future__ import annotations

from pycs import CL, CN
from tests.data.description.base import cfg

cfg = CN(cfg)

cfg.DESCRIBED_NESTING.FOO = "foo"
cfg.DESCRIBED_NESTING.BAR = CL("bar", desc="Overrided description")
