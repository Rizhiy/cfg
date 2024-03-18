from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

if TYPE_CHECKING:
    import boto3

    from .node import CN


@dataclass
class TransformBase(ABC):
    @abstractmethod
    def get_updates(self, cfg: CN) -> dict[str, Any] | None:
        """
        :param cfg: Config before transformations, should not be modified directly, return updates as a nested dict
        """

    def __call__(self, cfg: CN) -> None:
        updates = self.get_updates(cfg)
        if updates is not None:
            cfg.update(updates)


@dataclass
class LoadFromFile(TransformBase):
    filepath: str | Path
    require: bool = True

    def __post_init__(self) -> None:
        self.filepath = self.filepath if isinstance(self.filepath, Path) else Path(self.filepath).expanduser()

    def get_updates(self, _) -> dict[str, Any] | None:
        try:
            with self.filepath.open() as fobj:  # type: ignore not aware of __post_init__
                return yaml.safe_load(fobj)
        except FileNotFoundError:
            if self.require:
                raise
            return None


def _flat_to_structured(kv: dict[str, Any], sep=".") -> dict[str, Any]:
    """
    >>> _flat_to_structured({"a.b.c": 1, "a.b2": 2})
    {'a': {'b': {'c': 1}, 'b2': 2}}
    """
    structured = {}
    for key, value in kv.items():
        key_pieces = key.split(sep)
        here = structured
        for piece in key_pieces[:-1]:
            here = here.setdefault(piece, {})
        here[key_pieces[-1]] = value
    return structured


@dataclass
class LoadFromKeyValue(TransformBase):
    flat_data: dict[str, Any]

    def __post_init__(self) -> None:
        self._structured_data = _flat_to_structured(self.flat_data)

    def get_updates(self, _) -> dict[str, Any] | None:
        return self._structured_data


@dataclass
class LoadFromEnvVars(TransformBase):
    prefix: str

    def _normalize_key(self, key: str) -> str | None:
        if not key.startswith(self.prefix):
            return None
        key = key[len(self.prefix) :]  # key.removeprefix(prefix)  # noqa: E203
        # dots are not quite valid identifiers (in shell syntax).
        return key.replace("__", ".")

    def get_updates(self, _) -> dict[str, Any] | None:
        flat = {self._normalize_key(key): val for key, val in os.environ.items()}
        flat_loaded = {key: yaml.safe_load(value) if value else "" for key, value in flat.items() if key is not None}
        return _flat_to_structured(flat_loaded)


@dataclass
class LoadFromAWSAppConfig(TransformBase):
    key: str
    required = False
    session: boto3.Session | None = None

    def get_updates(self, cfg: CN) -> dict[str, Any] | None:
        try:
            import boto3
        except ModuleNotFoundError as e:
            raise ImportError("Please install with aws extra: pip install pycs[aws]") from e
        if self.key not in cfg:
            raise ValueError(f"Can't find AppConfig key '{self.key}' in cfg")
        ac_cfg = cfg[self.key]

        required_keys = ["APP", "ENV", "PROFILE"]
        for key in required_keys:
            if key not in ac_cfg:
                raise ValueError(f"Specified key ({self.key}) must contain {required_keys} subkeys, missing {key}")

        if not ac_cfg.APP:
            if self.required:
                raise ValueError("Got empty APP for AppConfig")
            return None

        client = (self.session or boto3).client("appconfigdata")
        # Maybe actually create a proper client for this
        config_token = client.start_configuration_session(
            ApplicationIdentifier=ac_cfg.APP,
            ConfigurationProfileIdentifier=ac_cfg.PROFILE,
            EnvironmentIdentifier=ac_cfg.ENV,
            RequiredMinimumPollIntervalInSeconds=15,
        )["InitialConfigurationToken"]
        response = client.get_latest_configuration(ConfigurationToken=config_token)

        content_type = response["ContentType"]
        content: bytes = response["Configuration"].read()
        if content_type == "application/x-yaml":
            return yaml.safe_load(content)
        if content_type == "application/json":
            return json.loads(content.decode("utf-8"))
        raise ValueError(f"Got config in invalid type: {content_type}")


@dataclass
class LoadFromAWSSecretsManager(TransformBase):
    key: str
    required = False
    session: boto3.Session | None = None

    def get_updates(self, cfg: CN) -> dict[str, Any] | None:
        try:
            import boto3
        except ModuleNotFoundError as e:
            raise ImportError("Please install with aws extra: pip install pycs[aws]") from e
        if self.key not in cfg:
            raise ValueError(f"Can't find SecretsManager key '{self.key}' in cfg")
        sm_cfg = cfg[self.key]

        if "NAME" not in sm_cfg:
            raise ValueError(f"Specified key ({self.key}) must contain Name subkey")

        if not sm_cfg.NAME:
            if self.required:
                raise ValueError("Got empty NAME for SecretsManager")
            return None

        secrets_manager = (self.session or boto3).client("secretsmanager")
        return json.loads(secrets_manager.get_secret_value(SecretId=sm_cfg.NAME)["SecretString"])
