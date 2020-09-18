class ConfigError(Exception):
    pass


class TypeMismatch(ConfigError):
    pass


class NodeReassignment(ConfigError):
    pass


class ModuleError(ConfigError):
    pass


class SchemaError(ConfigError):
    pass


class SchemaFrozenError(SchemaError):
    pass


class SpecError(ConfigError):
    pass


class NodeFrozenError(ConfigError):
    pass


class SaveError(ConfigError):
    pass


class ValidationError(ConfigError):
    pass


class MissingRequired(ValidationError):
    pass
