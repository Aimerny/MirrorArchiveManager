import functools

from mcdreforged.api.all import Serializable
from typing import List, Optional

from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig


class Config(Serializable):
    leader: bool = True
    # debug: bool = False
    mirrors: List[MirrorServerConfig] = [MirrorServerConfig()]

    @classmethod
    @functools.lru_cache
    def __get_default(cls) -> 'Config':
        return Config.get_default()

    @classmethod
    def get(cls) -> 'Config':
        if _config is None:
            return cls.__get_default()
        return _config


_config: Optional[Config] = None


def set_config_instance(cfg: Config):
    global _config
    _config = cfg
