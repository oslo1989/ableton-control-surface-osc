# import random
#
# import Live
# from ableton.v2.control_surface.components import SessionRingComponent
# from Live.Song import Song
# from Live.Track import Track
#
#
# class Tracks:
#     _selected_track: Track
#     _song: Song
#     _session_ring: SessionRingComponent
#
#     def _track_selected(self) -> None:
#         self._selected_track = self._song.view.selected_track
#
#     def _select_random_track(self) -> None:
#         self._song.view.selected_track = random.choice(self._song.tracks)
#         self._set_num_tracks(num_tracks=random.randint(1, 10))
#         self._set_num_scenes(num_scenes=random.randint(1, 10))
#
#     def _set_num_tracks(self, *, num_tracks: int) -> None:
#         self._num_tracks = num_tracks
#         self._session_ring._session_ring.num_tracks = num_tracks
#         self._session_ring.on_enabled_changed()
#
#     def _set_num_scenes(self, *, num_scenes: int) -> None:
#         self._num_tracks = num_scenes
#         self._session_ring._session_ring.num_scenes = num_scenes
#         self._session_ring.on_enabled_changed()
#
#     def _enable_session_ring(self) -> None:
#         self._session_ring.set_enabled(True)
#         self._session_ring.on_enabled_changed()
#
#     def _disable_session_ring(self) -> None:
#         self._session_ring.set_enabled(False)
#         self._session_ring.on_enabled_changed()
#
#     def _toggle_session_ring(self) -> None:
#         if self._session_ring.is_enabled():
#             self._disable_session_ring()
#         else:
#             self._enable_session_ring()
#
#     def __init__(self, song: Live.Song.Song):
#         self._song = song
#         self._selected_track = self._song.view.selected_track
#         self._song.view.add_selected_track_listener(self._track_selected)
#         self._num_tracks = 8
#         self._num_scenes = 8
#         # remember component guard later
#         self._session_ring = SessionRingComponent(
#             num_tracks=self._num_tracks,
#             num_scenes=self._num_scenes,
#             tracks_to_use=lambda: tuple(self._song.tracks)
#             + tuple(self._song.return_tracks)
#             + (self._song.master_track,),
#         )
#         self._session_ring.set_enabled(False)
