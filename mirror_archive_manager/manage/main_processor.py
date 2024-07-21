import logging

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mcdreforged.api.all import *


class MainProcessor:
    server: PluginServerInterface
    config: Config
    __logger: logging.Logger

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config
        self.__logger = server.logger

    def start_mirror(self, mirror: MirrorServerConfig):
        self.__logger.info(f'start mirror: {mirror.name}')
        pass

    def stop_mirror(self, mirror: str):
        pass

    def get_mirror_info(self, mirror: str):
        pass

    def sync_mirror(self, mirror: str):
        pass
