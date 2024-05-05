from typing import Any


def create_instance(c_instance: Any) -> Any:
    from .control_surface import EnablerOSCSurface

    return EnablerOSCSurface(c_instance)
