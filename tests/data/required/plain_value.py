from __future__ import annotations

from pycs import CN
from tests.data.required.required_plain_value import schema

cfg = CN(schema)
cfg.REQUIRED = 12
