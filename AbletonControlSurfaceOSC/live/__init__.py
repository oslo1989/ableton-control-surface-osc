from __future__ import annotations

from fastosc.dispatcher import Dispatcher
from fastosc.router import OSCRouter

import Live


class LiveBaseRouter(OSCRouter):
    def _add_sub_router(self, *, router_cls: type[LiveBaseRouter]) -> None:
        self._add_router(router=router_cls(dispatcher=self._dispatcher, song=self._song, namespace=self._namespace))

    def __init__(
        self,
        *,
        dispatcher: Dispatcher,
        song: Live.Song.Song,
        sub_routers: list[type[LiveBaseRouter]] | None = None,
        namespace: str,
    ):
        super().__init__(dispatcher=dispatcher, namespace=namespace)
        self._song = song
        for router_cls in sub_routers or []:
            self._add_sub_router(router_cls=router_cls)
