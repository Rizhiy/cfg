from __future__ import annotations

from pathlib import Path

from ntc import CN
from tests.data.base_cfg import cfg
from tests.data.base_class import BaseClass

cfg = CN(cfg)
cfg.NEW.int = 1
cfg.NEW.str = "foo"
cfg.NEW.float = 3.14
cfg.NEW.path = Path("example")
cfg.NEW.type = BaseClass
