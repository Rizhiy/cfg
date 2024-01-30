from __future__ import annotations

from pycs import CN
from tests.data.base_cfg import schema

cfg = CN(schema)
cfg.NEW.one = "one"
