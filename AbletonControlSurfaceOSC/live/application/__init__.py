from __future__ import annotations

from typing import Any, Callable

from fastosc.dispatcher import Dispatcher
from fastosc.router import OSCRouter, osc_get

import Live

VERSION = "/version"
AVERAGE_PROCESS_USAGE = "/avg_process_usage"
PEAK_PROCESS_USAGE = "/peak_process_usage"


class LiveApplicationRouter(OSCRouter):
    def __init__(self, *, dispatcher: Dispatcher, app: Live.Application.Application, namespace: str):
        dispatcher._logger.info("LiveApplicationRouter Init...")
        super().__init__(
            dispatcher=dispatcher,
            namespace=namespace,
        )
        self._app = app
        dispatcher._logger.info("LiveApplicationRouter: Init complete")

    @osc_get(VERSION, listen=False)
    def get_version(self) -> tuple[int, int, int, str, str]:
        return (
            self._app.get_major_version(),
            self._app.get_minor_version(),
            self._app.get_bugfix_version(),
            self._app.get_variant(),
            self._app.get_version_string(),
        )

    @osc_get(AVERAGE_PROCESS_USAGE)
    def get_average_process_usage(self) -> float:
        return self._app.average_process_usage

    @osc_get(PEAK_PROCESS_USAGE)
    def get_peak_process_usage(self) -> float:
        return self._app.peak_process_usage

    def _add_listener(self, *, address: str, listener: Callable, args: list[Any]) -> Callable[[], None] | None:
        if address == AVERAGE_PROCESS_USAGE:
            self._app.add_average_process_usage_listener(listener)
            return lambda: self._app.remove_average_process_usage_listener(listener)
        elif address == PEAK_PROCESS_USAGE:
            self._app.add_peak_process_usage_listener(listener)
            return lambda: self._app.remove_peak_process_usage_listener(listener)
        return None
