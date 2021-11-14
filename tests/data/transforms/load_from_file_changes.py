from ntc import CN
from tests.data.transforms.load_from_file import cfg

cfg = CN(cfg)
cfg.DICT.FOO = "foo_value_from_changes"
cfg.DICT.FOO2 = "foo2_value_from_changes"
