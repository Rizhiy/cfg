from __future__ import annotations

from rizhiy_cfg import CN
from tests.data.post_load.transform_inheritance import cfg

cfg = CN(cfg)


def transform(cfg: CN):
    cfg.NAME = "N"


cfg.add_transform(transform)
