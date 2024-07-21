from abc import ABC, abstractmethod
from mcdreforged.api.all import *


class Processor(ABC):

    @abstractmethod
    def start_mirror(self, source: CommandSource, *args):
        pass

    @abstractmethod
    def stop_mirror(self, source: CommandSource, *args):
        pass

    @abstractmethod
    def sync_mirror(self, source: CommandSource, *args):
        pass
