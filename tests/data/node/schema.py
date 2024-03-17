from pycs import CN


class Base:
    def __eq__(self, other: object) -> bool:
        return other.__class__ == Base


schema = CN()
schema.NAME = ""
schema.BOOL = False
schema.INT = 0
schema.FLOAT = 0.0
schema.STR = ""
schema.NESTED = CN()
schema.NESTED.FOO = "bar"
schema.DEFAULT = "default"
schema.CUSTOM = Base()
