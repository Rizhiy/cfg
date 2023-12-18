from __future__ import annotations

from cfg import CN

from ..base_cfg import cfg

cfg = cfg.inherit()

cfg.CLASSES.ANOTHER = CN()
