from __future__ import annotations

from pycs import CN
from tests.data.transforms.load_from_file import cfg

cfg = CN(cfg)
cfg.DICT.FOO = "Foo value from changes"
cfg.DICT.FOO2 = "Foo2 value from changes"
