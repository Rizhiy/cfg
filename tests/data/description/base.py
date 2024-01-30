from __future__ import annotations

from pycs import CL, CN
from tests.data.base_cfg import schema

schema = schema.inherit()

schema.DESCRIBED = CL("described", desc="Described leaf")
schema.DESCRIBED_NESTING = CN(CL(str, desc="Described nesting"))
