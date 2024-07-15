from mcdreforged.api.all import *
from typing import Union


def reply_message(source: CommandSource, msg: Union[str, RTextBase], *, with_prefix: bool = True):
    if with_prefix:
        msg = RTextList(RTextList(RText('[MAM]', RColor.dark_aqua).h('Mirror Archive Manager'), ' '), msg)
    source.reply(msg)
