from typing import Optional

from mcdreforged.api.all import *

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.util.mcdr_util import reply_message, tr
from mirror_archive_manager.globals import disable

COMMAND_HELP_LIST = ['start', 'stop', 'sync', 'info']


class CommandManager:
    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.config = Config.get()

    def cmd_help(self, source: CommandSource, context: dict):
        what = context.get('what')
        if what is not None and what not in COMMAND_HELP_LIST:
            reply_message(source, tr('help.unknown_help', RText(f'!!mam {what}', RColor.red)))
            return
        else:
            self.help_process(source, what)

    @classmethod
    def help_process(cls, source: CommandSource, what: Optional[str]):
        reply_message(source, tr('help.help_header'))
        if what is None:
            reply_message(source, tr('help.start_help', RText(f'!!mam start <server_name>', RColor.gray)))
            reply_message(source, tr('help.stop_help', RText(f'!!mam stop <server_name>', RColor.gray)))
            reply_message(source, tr('help.sync_help', RText(f'!!mam sync <server_name> <id>', RColor.gray)))
            reply_message(source, tr('help.info_help', RText(f'!!mam info <server_name>', RColor.gray)))
        reply_message(source, tr('help.help_footer'))

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
