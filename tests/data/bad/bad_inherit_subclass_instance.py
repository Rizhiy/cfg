from __future__ import annotations

from pycs import CL

from ..base_cfg import schema
from ..base_class import BaseClass

schema = schema.clone()

schema.SUBCLASSES.ANOTHER = CL(BaseClass(), BaseClass, subclass=True)
