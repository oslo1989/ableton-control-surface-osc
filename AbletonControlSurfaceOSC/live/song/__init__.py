from __future__ import annotations

from fastosc.dispatcher import Dispatcher

import Live
from EnablerOSCSurface.live import LiveBaseRouter
from EnablerOSCSurface.live.song.tempo import LiveTempoRouter
from EnablerOSCSurface.live.song.time import LiveTimeRouter
from EnablerOSCSurface.live.song.view import LiveViewRouter


class LiveSongRouter(LiveBaseRouter):
    def __init__(self, *, dispatcher: Dispatcher, song: Live.Song.Song, namespace: str):
        dispatcher._logger.info("LiveTempoRouter Init...")
        super().__init__(
            dispatcher=dispatcher,
            song=song,
            namespace=namespace,
            sub_routers=[LiveTempoRouter, LiveTimeRouter, LiveViewRouter],
        )
        dispatcher._logger.info("LiveTempoRouter: Init complete")
