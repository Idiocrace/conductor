from typing import Dict, Any, List

from flask import g


# Decorator to mark a function as a renderer view method.
def renderer(func) -> callable:
    """
    Decorator to mark a function as a Conductor renderer method.
    If there are more than one renderer method defined in the same file, the
    first one will be chosen.
    Usage:
        @renderer
        def my_renderer():
            ...
    """
    func._is_conductor_renderer = True
    return func


# Used to wrap renderer methods to inject global variables and route data into
# the renderer method. These can be fetched using gvar<s>() and rvar<s>().
def _wrap_renderer(
        renderer_func: callable,
        route_data: Dict[str, Any],
        accessed_globals: List[str],
        route_computed_metadata: Dict[str, Any]

) -> callable:
    import __main__

    def wrapped_view(*args, **kwargs):
        GLOBALS = {}
        for name in accessed_globals:
            # Fetch the current value of the global variable
            value = getattr(__main__, name, None)
            GLOBALS[name] = value
        g._GLOBALS = GLOBALS
        g._ROUTEDATA = route_data
        g._ROUTEMETA = route_computed_metadata
        return renderer_func(*args, **kwargs)
    return wrapped_view
