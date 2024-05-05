from __future__ import annotations

from typing import TypeVar

from Live.Track import Track

T = TypeVar("T", bound=object)


def index_of(ls: list[T], obj: T) -> int:
    idx = 0
    for el in ls:
        if el == obj:
            return idx
        idx += 1
    return -1


TRACK = 0
RETURN_TRACK = 1
MASTER_TRACK = 2


def int_color_to_hex(color: int) -> str:
    return f"{color:06X}"


def hex_color_to_rgb(color: str) -> tuple[int, int, int]:
    return tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def map_track(t: Track, track_type: int) -> tuple[int, str, str, bool, bool, bool, bool]:
    hex_color = int_color_to_hex(t.color)
    return (
        track_type,
        t.name,
        hex_color,
        t.has_audio_input,
        t.has_audio_output,
        t.has_midi_input,
        t.has_midi_output,
    )