from mirror_archive_manager.config.config import Config
from mcdreforged.api.all import *


class MirrorProcessor:
    config: Config
    server: PluginServerInterface

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config

