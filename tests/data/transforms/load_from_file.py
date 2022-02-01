from pathlib import Path

from ntc.transforms import LoadFromFile
from tests.data.base_cfg import cfg as base_cfg

cfg = base_cfg.inherit()
cfg.add_transform(LoadFromFile(Path(__file__).parent / "extra.yaml", require=True))
