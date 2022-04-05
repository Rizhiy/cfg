from __future__ import annotations

from ntc import CN
from tests.data.post_load.validate import cfg

cfg = CN(cfg)


def validate(cfg: CN):
    assert cfg.NAME == "Name"


cfg.add_validator(validate)
