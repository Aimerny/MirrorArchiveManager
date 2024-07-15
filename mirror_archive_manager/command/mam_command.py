from mcdreforged.api.all import *

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.util.mcdr_util import reply_message
from mirror_archive_manager.globals import disable

COMMAND_HELP_LIST = ['start', 'stop', 'sync', 'info']


class CommandManager:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.config = Config.get()

    def cmd_help(self, source: CommandSource, context: dict):
        reply_message(source, "help")

    def register_commands(self):
        builder = SimpleCommandBuilder()
        builder.command('help', self.cmd_help)
        builder.command('help <what>', self.cmd_help)
        builder.arg('what', Text).suggests(lambda: COMMAND_HELP_LIST)
        self.server.logger.info(f'disable={disable}')
        root = (
            Literal('!!mam').
            requires(lambda: not disable, lambda: RText('mam has been disabled').set_color(RColor.red))
            .runs(self.cmd_help)
        )
        builder.add_children_for(root)

        self.server.register_command(root)
