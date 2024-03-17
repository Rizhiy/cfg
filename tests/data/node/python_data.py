from pycs import CN

cfg = CN()
cfg.BOOL = True
cfg.INT = 1
cfg.FLOAT = 1.1
cfg.STR = "py"
cfg.NESTED = CN()
cfg.NESTED.FOO = "zoo"
