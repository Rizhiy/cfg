from __future__ import annotations

from pycs import CL
from tests.data.description.base import schema

cfg = schema.init_cfg()

cfg.DESCRIBED_NESTING.FOO = "foo"
cfg.DESCRIBED_NESTING.BAR = CL("bar", desc="Overrided description")
