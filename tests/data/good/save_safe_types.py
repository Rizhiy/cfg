from __future__ import annotations

import math
from pathlib import Path

from rizhiy_cfg import CN
from tests.data.base_cfg import cfg
from tests.data.base_class import BaseClass

cfg = CN(cfg)
cfg.NEW.int = 1
cfg.NEW.str = "foo"
cfg.NEW.float = math.pi
cfg.NEW.path = Path("example")
cfg.NEW.type = BaseClass
