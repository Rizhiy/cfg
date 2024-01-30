from __future__ import annotations

from pycs import CN
from tests.data.post_load.transform_inheritance import schema

schema = CN(schema)


def transform(cfg: CN):
    cfg.NAME = "N"


schema.add_transform(transform)
