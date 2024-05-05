from __future__ import annotations

from typing import Any

from fastosc.dispatcher import Dispatcher
from fastosc.server.udp.udp_pull_server import OSCUDPPullServer

import Live
from ableton.v2.control_surface import ControlSurface
from AbletonControlSurfaceOSC.live.application import LiveApplicationRouter
from AbletonControlSurfaceOSC.live.song import LiveSongRouter
from AbletonControlSurfaceOSC.log import logger

MIN_TIMER_INTERVAL_MS = 10
MILLISECONDS_PER_SECOND = 1000

BASE_ADDRESS = "/live"
SONG_ADDRESS = "/song"
APPLICATION_ADDRESS = "/app"


class AbletonControlSurfaceOSC(ControlSurface):
    _server_timer: Live.Base.Timer
    _local_addr = local_addr = ("0.0.0.0", 1337)

    def __init__(self, c_instance: Any) -> None:
        ControlSurface.__init__(self, c_instance)

        self._logger = logger
        self._dispatcher = Dispatcher(base_address=BASE_ADDRESS, logger=self._logger)
        self._server = OSCUDPPullServer(dispatcher=self._dispatcher, local_addr=self._local_addr, logger=self._logger)

        self._server_timer = Live.Base.Timer(  # type: ignore[call-arg]
            callback=self._server.process,
            interval=MIN_TIMER_INTERVAL_MS,
            repeat=True,
        )

        self._song_router = LiveSongRouter(song=self.song, dispatcher=self._dispatcher, namespace=SONG_ADDRESS)
        self._application_router = LiveApplicationRouter(
            app=self.application, dispatcher=self._dispatcher, namespace=APPLICATION_ADDRESS
        )

        self._server_timer.start()

    def _load_handlers(
        self,
    ) -> None:  # call when we are starting the surface to dynamically import modules, and set set up listeners etc
        pass

    def _clear(
        self,
    ) -> None:  # call when we are stopping the surface to clear all listeners etc. call on disconnect etc
        pass

    def disconnect(self) -> None:
        self._server_timer.stop()
        self._server.shutdown()
        ControlSurface.disconnect(self)
