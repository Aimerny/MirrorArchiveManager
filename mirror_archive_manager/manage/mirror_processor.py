import threading

from mirror_archive_manager.config.config import Config
from mcdreforged.api.all import *
from fastapi import FastAPI
import uvicorn

from mirror_archive_manager.manage.processor import Processor


class MirrorHttpServer:

    def __init__(self, api: FastAPI, config: Config):
        self.api = api
        self.server = None
        self.config = config
        self.server_thread = None

    def start(self):
        def __start_server():
            server_config = uvicorn.Config(app=self.api, host='0.0.0.0', port=self.config.port, log_level='error')
            self.server = uvicorn.Server(server_config)
            self.server.run()

        self.server_thread = threading.Thread(name='mirror-http-server', target=__start_server)
        self.server_thread.start()

    def stop(self):
        self.server.should_exit = True
        self.server_thread.join()


class MirrorProcessor(Processor):
    config: Config
    server: PluginServerInterface
    __http_server: MirrorHttpServer

    def __init__(self, server: PluginServerInterface, config: Config):
        self.api = FastAPI()
        self.server = server
        self.config = config
        self.add_routes()

    def add_routes(self):
        @self.api.post('/start')
        async def start_mirror():
            self.server.logger.info('start mirror')
            if self.server.is_server_running():
                return 'skip'
            else:
                self.server.start()
            return 'ok'

        @self.api.post('/stop')
        async def stop_mirror():
            self.server.logger.info('stop mirror')
            if self.server.is_server_running():
                self.server.stop()
                return 'ok'
            else:
                return 'server has been down'

    def start(self):
        self.__init_http_server()

    def __init_http_server(self):
        self.__http_server = MirrorHttpServer(self.api, self.config)
        self.__http_server.start()
        self.server.logger.info(f'mirror http server started...')

    def stop(self):
        self.server.logger.info('mirror http server shutdown...')
        self.__http_server.stop()

