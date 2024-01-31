from __future__ import annotations

from pycs import CN
from tests.data.post_load.validate import schema

cfg = schema.init_cfg()


def validate(cfg: CN):
    assert cfg.NAME == "Name"


cfg.add_validator(validate)
