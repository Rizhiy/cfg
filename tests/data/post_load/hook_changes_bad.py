from __future__ import annotations

from pycs import CN
from tests.data.post_load.hook import schema


def hook(cfg: CN) -> None:
    print(cfg.NAME + "Bad")


cfg = CN(schema)
cfg.add_hook(hook)
