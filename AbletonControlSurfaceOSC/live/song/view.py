from __future__ import annotations

from typing import Any, Callable

from fastosc.dispatcher import Dispatcher
from fastosc.router import osc_get, osc_set

import Live
from AbletonControlSurfaceOSC.live import LiveBaseRouter
from AbletonControlSurfaceOSC.live.util import MASTER_TRACK, RETURN_TRACK, TRACK, index_of, int_color_to_hex, map_track

TRACKS = "/tracks"
SELECTED_TRACK = "/selected_track"
SCENES = "/scenes"
SELECTED_SCENE = "/selected_scene"
HIGHLIGHTED_CLIP_SLOT = "/highlighted_clip_slot"
APPOINTED_DEVICE = "/appointed_device"


# Todo: look at this for sending a diff when a track or scene or device has changed position change position:
#  https://stackoverflow.com/questions/36023728/comparing-two-lists-and-finding-indices-of-changes add or delete:
#  https://stackoverflow.com/questions/60842385/how-to-compare-two-list-and-find-out-added-deleted-unchanged-part it
#  will be very hard, if not impossible to change listeners that have already been set up, what should the logic be
#  let's try to think use cases. we could 1) just drop all listeners. 2) we could resent and "keep" listening to the
#  same index we could reset all listeners, we could just keep listeners as is, but update the address / index this
#  last one might be the easiest for the time being -> keep listeners but update the address I think its more likely
#  that if you change the index of a track you want to keep listening but also ensure that everything is in the right
#  position also have an endpoint to retrieve
#  tracks/update
#  scenes/update
#  track/devices/update
#  track/device/parameters/update


class LiveViewRouter(LiveBaseRouter):
    def __init__(self, *, dispatcher: Dispatcher, song: Live.Song.Song, namespace: str):
        dispatcher._logger.info("LiveViewRouter: Init...")
        super().__init__(dispatcher=dispatcher, song=song, namespace=namespace)
        self._logger = dispatcher._logger
        dispatcher._logger.info("LiveViewRouter: Init complete")

    def _map_tracks(self) -> list[tuple[int, str, str, bool, bool, bool, bool]]:
        tracks = [map_track(t, TRACK) for t in self._song.tracks]
        return_tracks = [map_track(t, RETURN_TRACK) for t in self._song.tracks]
        master_track = [map_track(t, MASTER_TRACK) for t in [self._song.master_track]]
        return tracks + return_tracks + master_track

    def _get_selected_track(self) -> tuple[int, int]:
        """
        utility function to get selected track
        """
        track_type = TRACK
        idx = index_of(self._song.tracks, self._song.view.selected_track)
        if idx < 0:
            idx = index_of(self._song.return_tracks, self._song.view.selected_track)
            track_type = RETURN_TRACK

        if idx < 0 and self._song.view.selected_track == self._song.master_track:
            idx = 0
            track_type = MASTER_TRACK

        return idx, track_type

    @osc_get(SELECTED_TRACK)
    def get_selected_track(self) -> tuple[int, int]:
        """
        get index of currently selected track
        the first number is the index of the track,
        the second is the track type :w- following the visual flow of Ableton mixer view
        0 = Track
        1 = Return Track
        2 = Master Track
        """
        return self._get_selected_track()

    @osc_set(SELECTED_TRACK)
    def set_selected_track(self, track_idx: int, track_type: int) -> tuple[int, int]:
        """
        set index of currently selected track
        the first number is the index of the track,
        the second is the track type - following the visual flow of Ableton mixer view
        0 = Track
        1 = Return Track
        2 = Master Track

        Will return an error if any index is beyond current number of tracks
        """
        if track_type == TRACK:
            self._song.view.selected_track = self._song.tracks[track_idx]
        elif track_type == RETURN_TRACK:
            self._song.view.selected_track = self._song.return_tracks[track_idx]
        elif track_type == MASTER_TRACK:
            self._song.view.selected_track = self._song.master_track
        return self._get_selected_track()

    @osc_get(TRACKS, listen=False)
    def get_tracks(self) -> list[tuple[int, str, str, bool, bool, bool, bool]]:
        """
        get tracks in current song
        """
        return self._map_tracks()

    @osc_get(SELECTED_SCENE)
    def get_selected_scene(self) -> int:
        """
        get index of currently selected scene
        """
        return index_of(self._song.scenes, self._song.view.selected_scene)

    @osc_set(SELECTED_SCENE)
    def set_selected_scene(self, scene_index: int) -> int:
        """
        set index of currently selected scene
        Will return an error if any index is beyond current number of scenes
        """
        self._song.view.selected_scene = self._song.scenes[scene_index]
        return scene_index

    @osc_get(SCENES, listen=False)
    def get_scenes(self) -> list[tuple[str, str, float, int, int]]:
        """
        get tracks in current song
        """
        return [
            (s.name, int_color_to_hex(s.color), s.tempo, s.time_signature_numerator, s.time_signature_denominator)
            for s in self._song.scenes
        ]

    @osc_get(HIGHLIGHTED_CLIP_SLOT, listen=False)
    def get_highlighted_clip_slot(self) -> tuple[str, bool]:
        """
        get currently highlighted_clip_slot
        """
        cs = self._song.view.highlighted_clip_slot
        return (
            int_color_to_hex(cs.color),
            cs.has_clip,
        )

    @osc_get(APPOINTED_DEVICE)
    def get_appointed_device(self) -> tuple[str]:
        """
        get tracks in current song
        """

        return (self._song.appointed_device.name,)

    def _add_listener(self, address: str, listener: Callable[[], None], args: list[Any]) -> Callable[[], None] | None:
        if address == SELECTED_TRACK:
            self._song.view.add_selected_track_listener(listener)
            return lambda: self._song.view.remove_selected_track_listener(listener)
        if address == SELECTED_SCENE:
            self._song.view.add_selected_scene_listener(listener)
            return lambda: self._song.view.remove_selected_scene_listener(listener)
        if address == APPOINTED_DEVICE:
            self._song.add_appointed_device_listener(listener)
            return lambda: self._song.remove_appointed_device_listener(listener)
        return None
