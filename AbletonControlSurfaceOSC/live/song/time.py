from __future__ import annotations

from typing import Any, Callable

import Live
from fastosc.dispatcher import Dispatcher
from fastosc.router import osc_get

from AbletonControlSurfaceOSC.live import LiveBaseRouter

TIME = "/time"
BEAT_WHOLE = "/beat/whole"
BEAT_QUARTER = "/beat/quarter"
BEAT_SIXTEENTH = "/beat/sixteenth"
QUARTER = 0.25
HALF = 0.5
THREE_QUARTERS = 0.75
FIRST_BEAT = 1
SECOND_BEAT = 2
THIRD_BEAT = 3


class LiveTimeRouter(LiveBaseRouter):
    def __init__(self, *, dispatcher: Dispatcher, song: Live.Song.Song, namespace: str) -> None:
        dispatcher._logger.info("LiveTimeRouter: Init...")
        super().__init__(dispatcher=dispatcher, song=song, namespace=namespace)
        self._logger = self._dispatcher._logger
        self._sixteenth_beat = 1
        self._quarter_beat = 1
        self._whole_beat = 1
        self._last_song_time = -1.0
        self._song.add_current_song_time_listener(self._song_time_changed)
        self._whole_beat_listeners: list[Callable[[], None]] = []
        self._quarter_beat_listeners: list[Callable[[], None]] = []
        self._sixteenth_beat_listeners: list[Callable[[], None]] = []
        dispatcher._logger.info("LiveTimeRouter: Init complete")

    @osc_get(TIME)
    def get_time(self) -> float:
        """
        returns the current raw internal time from Ableton
        """
        return self._song.current_song_time

    @osc_get(BEAT_SIXTEENTH)
    def get_sixteenth_beat(self) -> int:
        """
        returns the current 16th note beat
        """
        return self._sixteenth_beat

    @osc_get(BEAT_QUARTER)
    def get_quarter_beat(self) -> int:
        """
        returns the current quarter note beat
        """
        return self._quarter_beat

    @osc_get(BEAT_WHOLE)
    def get_whole_beat(self) -> int:
        """
        returns the current whole note beat
        """
        return self._whole_beat

    def _add_listener(self, address: str, listener: Callable[[], None], args: list[Any]) -> Callable[[], None] | None:
        if address == TIME:
            self._song.add_current_song_time_listener(listener)
            return lambda: self._song.remove_tempo_listener(listener)
        if address == BEAT_SIXTEENTH:
            self._sixteenth_beat_listeners.append(listener)
            return lambda: self._sixteenth_beat_listeners.remove(listener)
        if address == BEAT_QUARTER:
            self._quarter_beat_listeners.append(listener)
            return lambda: self._quarter_beat_listeners.remove(listener)
        if address == BEAT_WHOLE:
            self._whole_beat_listeners.append(listener)
            return lambda: self._whole_beat_listeners.remove(listener)
        return None

    def _trigger_sixteenth_listeners(self) -> None:
        for listener in self._sixteenth_beat_listeners:
            listener()

    def _song_time_changed(self) -> None:
        if (self._song.current_song_time < self._last_song_time) or (
            int(self._song.current_song_time) > int(self._last_song_time)
        ):
            self._quarter_beat = int(self._song.current_song_time) % 4 + 1
            if self._quarter_beat == 1:
                self._whole_beat = int(self._song.current_song_time / 4) + 1
                for listener in self._whole_beat_listeners:
                    listener()
            self._sixteenth_beat = 1
            for listener in self._quarter_beat_listeners:
                listener()
            self._trigger_sixteenth_listeners()
        if self._song.current_song_time > QUARTER and self._sixteenth_beat == FIRST_BEAT:
            self._sixteenth_beat = 2
            self._trigger_sixteenth_listeners()
        elif self._song.current_song_time > HALF and self._sixteenth_beat == SECOND_BEAT:
            self._sixteenth_beat = 3
            self._trigger_sixteenth_listeners()
        elif self._song.current_song_time > THREE_QUARTERS and self._sixteenth_beat == THIRD_BEAT:
            self._sixteenth_beat = 4
            self._trigger_sixteenth_listeners()

        self._last_song_time = self._song.current_song_time
