from __future__ import annotations

from typing import Any

from fastosc.dispatcher import Dispatcher
from fastosc.server.udp.udp_pull_server import OSCUDPPullServer

import Live
from ableton.v2.control_surface import ControlSurface
from EnablerOSCSurface.live.application import LiveApplicationRouter
from EnablerOSCSurface.live.song import LiveSongRouter
from EnablerOSCSurface.log import logger

MIN_TIMER_INTERVAL_MS = 10
MILLISECONDS_PER_SECOND = 1000

"""
todo: need to have a request id that is associated with the response.
if ther server can append it, that would be the best

callback id

# format of messages
# parameters: Tuple, Signature: Tuple[timestamp, request_id] -> returned on GET requests
# have separate update messages for change -> what changed, like a track was moved etc.
# a scene was moved, a device was moved
# we could do a get to the callback dict, get the function, then replace the function with a new one
# corresponding to the new address parameters. but is the function already scoped to the old address / parameters?

If an handler now returns

we do [data... NIL timestamp request_id]   returned on GET requests, easy
               None   datetime   str

  have a utility to process this

TODO:
- create library / package / repo for doc generated code surface
- create library / package / repo  for live11 reverse engineered code
- create library / package / repo  for live12 reverse engineered code
- create library / package / repo  for osc code
- create repo for osc control surface
- https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock
- testing using dispatcher. no need for server
- test fastosc - hommage to FastAPI
- Automatic validation of types
- Automatic docs generation of types and return types
"""

BASE_ADDRESS = "/live"
SONG_ADDRESS = "/song"
APPLICATION_ADDRESS = "/app"


class EnablerOSCSurface(ControlSurface):
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
