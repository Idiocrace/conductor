import importlib.util
import json
import os
import string
from typing import Any, Dict, Optional, List

from flask import Flask, render_template, g


# Internally used variables
_CONDUCTOR_VERSION = "0.1"
_VALID_ENDPOINT_CHARS = string.ascii_letters + string.digits + '_'


# Decorator to mark a function as a renderer view method.
def viewmethod(func) -> callable:
    """
    Decorator to mark a function as a Conductor view method.
    """
    func._is_conductor_view_method = True
    return func


# Used to wrap view methods to inject global variables and route data into the
# view method. These can be fetched using gvar<s>() and rvar<s>().
def wrap_viewmethod(
        view_func,
        route_data: Dict[str, Any],
        accessed_globals: List[str]
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
        return view_func(*args, **kwargs)
    return wrapped_view


# ==== Fetch Methods ====
# gvar = global variable (or data). Used to get any global variables to pass
# into the method. Globals are defined in the route definition under $global.
def gvar(name: str) -> Any:
    return getattr(g, "_GLOBALS", {}).get(name)


# gvars = global variables (or data). Used to get all global variables to pass
# into the method. Globals are defined in the route definition under $global.
def gvars() -> Dict[str, Any]:
    return getattr(g, "_GLOBALS", {})


# rvar = route variable (or data). Used to get any route data found under the
# route definition in the router file.
def rvar(name: str) -> Any:
    return getattr(g, "_ROUTEDATA", {}).get(name)


# rvars = route variables (or data). Used to get all route data found under the
# route definition in the router file.
def rvars() -> Dict[str, Any]:
    return getattr(g, "_ROUTEDATA", {})



class Conductor:
    app: Flask
    router: Optional[Router] = None

    def 