import http
import logging
from enum import Enum

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mirror_archive_manager.util.mcdr_util import reply_message, tr, deco_message
from mirror_archive_manager.manage.processor import Processor
from mcdreforged.api.all import *
import requests


class OperateType(Enum):
    START = 1
    STOP = 2
    SYNC = 3
    INFO = 4

    def __str__(self):
        return self.name.lower()


class MainProcessor(Processor):
    server: PluginServerInterface
    config: Config
    __logger: logging.Logger

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config
        self.__logger = server.logger

    def start(self):
        pass

    def stop(self):
        pass

    def start_mirror(self, source: CommandSource, *args):
        mirror = args[0]
        self.__logger.debug(f'starting mirror: {mirror.name}')
        success = self.__request_mirror(source, mirror, OperateType.START)
        if not success:
            self.server.broadcast(deco_message(
                tr('start.start_failed', RText(mirror.name, RColor.dark_aqua)).set_color(RColor.dark_red)))
        else:
            self.server.broadcast(deco_message(
                tr('start.start_success', RText(mirror.name, RColor.dark_aqua).set_color(RColor.green)))
            )

    def stop_mirror(self, source: CommandSource, *args):
        mirror = args[0]
        self.__logger.debug(f'stopping mirror: {mirror.name}')
        success = self.__request_mirror(source, mirror, OperateType.STOP)
        if not success:
            self.server.broadcast(deco_message(
                tr('stop.stop_failed', RText(mirror.name, RColor.dark_aqua)).set_color(RColor.dark_red)))
        else:
            self.server.broadcast(deco_message(
                tr('stop.stop_success', RText(mirror.name, RColor.dark_aqua).set_color(RColor.green)))
            )

    def get_mirror_info(self, source: CommandSource):
        pass

    def sync_mirror(self, source: CommandSource, *args):
        pass

    def __request_mirror(self, source: CommandSource, mirror: MirrorServerConfig, op_type: OperateType) -> bool:
        try:
            url = f'http://{mirror.host}:{mirror.port}/{op_type}'
            resp = requests.post(url=url, timeout=3)
            return resp.status_code == 200
        except Exception as e:
            reply_message(source,
                          tr('connection_error', RText(mirror.name, RColor.dark_aqua), RText(e, RColor.dark_red)))
            return False
