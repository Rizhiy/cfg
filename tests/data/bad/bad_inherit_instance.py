from __future__ import annotations

from pycs import CL

from ..base_cfg import schema
from ..base_class import BaseClass


class BadClass:
    pass


schema = schema.clone()

schema.CLASSES.ANOTHER = CL(BadClass(), BaseClass)
