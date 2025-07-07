from typing import Any, Dict

from flask import g


# gvar = global variable (or data). Used to get any global variables to pass
# into the method. Globals are defined in the route definition under $global.
def gvar(name: str) -> Any:
    """
    Gets a global variable by name from the Flask `g` object.
    Global variables are included in the route definition under $global and are
    gotten from the app main module. This allows access to any global
    variables defined in the main application.
    """
    return getattr(g, "_GLOBALS", {}).get(name)


# gvars = global variables (or data). Used to get all global variables to pass
# into the method. Globals are defined in the route definition under $global.
def gvars() -> Dict[str, Any]:
    """
    Gets all global variables from the Flask `g` object.
    Global variables are included in the route definition under $global and are
    gotten from the app main module. This allows access to any global
    variables defined in the main application.
    """
    return getattr(g, "_GLOBALS", {})


# rvar = route variable (or data). Used to get any route data found under the
# route definition in the router file.
def rvar(name: str) -> Any:
    """
    Gets a route variable by name from the Flask `g` object.
    Route variables include all data found under the route definition in the
    router file, such as $endpoint, template, $methods, etc.
    """
    return getattr(g, "_ROUTEDATA", {}).get(name)


# rvars = route variables (or data). Used to get all route data found under the
# route definition in the router file.
def rvars() -> Dict[str, Any]:
    """
    Gets all route variables from the Flask `g` object.
    Route variables include all data found under the route definition in the
    router file, such as $endpoint, template, $methods, etc.
    """
    return getattr(g, "_ROUTEDATA", {})


# rmval = route metadata value. A value that is computed when a route is being
# activated. Includes endpoint, template, methods, etc.
def rmval() -> Dict[str, Any]:
    """
    Gets a route metadata value from the Flask `g` object.
    Route metadata includes all values that are computed when a route is
    being activated, such as endpoint, template, methods, etc.
    """
    return getattr(g, "_ROUTEMETA", {}).get("value")


# rmvals = route metadata values. Contains all values that are computed when a
# route is being activated. Includes endpoint, template, methods, etc.
def rmvals() -> Dict[str, Any]:
    """
    Gets all route metadata values from the Flask `g` object.
    Route metadata includes all values that are computed when a route is
    being activated, such as endpoint, template, methods, etc.
    """
    return getattr(g, "_ROUTEMETA", {})
