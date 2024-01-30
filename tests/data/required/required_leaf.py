from __future__ import annotations

from pycs import CL

from ..base_cfg import schema

schema = schema.inherit()
schema.REQUIRED = CL(None, str, required=True)
