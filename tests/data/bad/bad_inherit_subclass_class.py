from __future__ import annotations

from ..base_cfg import schema
from ..base_class import BaseClass

schema = schema.clone()

schema.CLASSES.ANOTHER = BaseClass
