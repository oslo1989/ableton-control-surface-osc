from typing import Any


def create_instance(c_instance: Any) -> Any:
    from .control_surface import AbletonControlSurfaceOSC

    return AbletonControlSurfaceOSC(c_instance)
