from typing import Optional

from mcdreforged.api.all import Serializable


class MirrorServerConfig(Serializable):
    name: Optional[str] = 'Mirror Server Name'
    server_path: Optional[str] = '../mirror-server/server'
    pb_archive_id: int = 0
    host: str = '127.0.0.1'
    port: int = 25576
