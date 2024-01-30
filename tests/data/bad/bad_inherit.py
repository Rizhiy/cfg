from __future__ import annotations

from pycs import CN

from ..base_cfg import schema

schema = schema.inherit()

schema.CLASSES.ANOTHER = CN()
