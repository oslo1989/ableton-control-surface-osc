from __future__ import annotations

from typing import Any, Callable

from fastosc.dispatcher import Dispatcher
from fastosc.router import osc_get, osc_set

import Live
from EnablerOSCSurface.live import LiveBaseRouter

TEMPO = "/tempo"


class LiveTempoRouter(LiveBaseRouter):
    def __init__(self, *, dispatcher: Dispatcher, song: Live.Song.Song, namespace: str):
        dispatcher._logger.info("LiveTempoRouter: Init...")
        super().__init__(dispatcher=dispatcher, song=song, namespace=namespace)
        self._logger = dispatcher._logger
        dispatcher._logger.info("LiveTempoRouter: Init complete")

    @osc_get(TEMPO)
    def get_tempo(self) -> float:
        """
        get current tempo of the song
        """
        return self._song.tempo

    @osc_set(TEMPO)
    def set_tempo(self, tempo: float) -> float:
        """
        set current tempo of the song
        """
        self._song.tempo = tempo
        return self._song.tempo

    def _add_listener(self, address: str, listener: Callable[[], None], args: list[Any]) -> Callable[[], None] | None:
        if address == TEMPO:
            self._song.add_tempo_listener(listener)
            return lambda: self._song.remove_tempo_listener(listener)
        return None
