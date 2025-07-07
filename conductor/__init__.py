import string
from flask import Flask

# Expose public API imports for easier use
from .conductor import Conductor
from .routing import Router
from .configuration import Config
from .rendering import renderer
from .accessors import gvar, gvars, rvar, rvars, rmval, rmvals

# Internally used variables
# Version numbers for Conductor components
_CONDUCTOR_VERSION = "0.1"
_CONDUCTOR_ROUTER_VERSION = "0.1"
_CONDUCTOR_CONFIG_VERSION = "0.1"

_VALID_ENDPOINT_CHARS = string.ascii_letters + string.digits + '_'


# Used as the default for starting the app if no custom starter is provided.
def _default_app_starter(app: Flask, host: str, port: int):
    app.run(host=host, port=port)


# __all__ list to define the public API of the module.
# This allows users to import only the specified components.
# Good to prevent users from accessing internal components directly.
__all__ = [
    "Conductor",
    "Router",
    "Config",
    "renderer",
    "gvar",
    "gvars",
    "rvar",
    "rvars",
    "rmval",
    "rmvals"
]
