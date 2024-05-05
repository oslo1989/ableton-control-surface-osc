from ableton.v2.control_surface import ControlSurface


def create_instance(c_instance: ControlSurface) -> ControlSurface:
    from .control_surface import AbletonControlSurfaceOSC

    return AbletonControlSurfaceOSC(c_instance)
