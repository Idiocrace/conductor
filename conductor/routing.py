from conductor import (
    _CONDUCTOR_ROUTER_VERSION,
    _VALID_ENDPOINT_CHARS
)
from .rendering import _wrap_renderer
from .accessors import rvar

import importlib.util
import json
import os

from flask import Flask, render_template


class Router:
    """
    The Router class for the Conductor Framework. It is responsible for loading
    and activating the router file, which defines the routes and their handlers
    for the Flask application. It also handles error routes and global
    variables defined in the router file.
    Args:
        rtr_file (str): The path to the router file in JSON format.
    Raises:
        FileNotFoundError: If the router file does not exist.
        ValueError: If the router file is not a valid JSON file or if the
        version does not match the current Conductor Router version.
        PermissionError: If the router file is not readable.
        IsADirectoryError: If the router file is a directory, not a file.
    Usage:
        router = Router('path/to/router.json')
        router.activate_router(app)  # app is a Flask object instance
    """
    def __init__(self, rtr_file: str):
        self.rtr_file = rtr_file
        # Throw all the error handling here to avoid cluttering the main logic
        if not os.path.exists(self.rtr_file):
            raise FileNotFoundError(
                f"Router file {self.rtr_file} does not exist."
                " Ensure you entered a valid path to the router file."
            )
        if not self.rtr_file.endswith('.json'):
            raise ValueError(
                f"Router file {self.rtr_file} is not a valid JSON file."
                " Ensure you entered a valid path to the router file."
            )
        if not os.access(self.rtr_file, os.R_OK):
            raise PermissionError(
                f"Router file {self.rtr_file} is not readable."
                " Ensure you have the necessary permissions to read this file."
            )
        if not os.path.isfile(self.rtr_file):
            raise IsADirectoryError(
                f"Router file {self.rtr_file} is a directory, not a file."
                " Ensure you entered a valid path to the router file."
            )

        with open(self.rtr_file, 'r') as router_file:
            self.routercontent = json.load(router_file)

        self.version = self.routercontent.get('$version', "unset")

        # Versioning checks
        if self.version != _CONDUCTOR_ROUTER_VERSION:
            raise ValueError(
                f"Router file version {self.version} does not match current"
                f" Conductor Router version {_CONDUCTOR_ROUTER_VERSION}. "
                "Please update the router file or the Conductor framework."
            )

        # Defaults are not required, but are incredibly useful
        self.defaults = self.routercontent.get('defaults', {})
        # Not yet implemented, but will be heavily used in the future

    def activate_router(self, app: Flask) -> None:
        """
        Activates the router by creating all necessary routes.
        """
        # Remove metadata keys
        self.routercontent = {
            k: v for k, v in self.routercontent.items()
            if not k.startswith('$')
            and not k.startswith('#')
        }

        for raw_route, route_data in self.routercontent.items():
            if not isinstance(route_data, dict):
                raise ValueError(
                    f"Invalid route data for {raw_route}. "
                    f"Expected a dictionary, got {type(route_data).__name__}."
                )

            route_cmeta = {
                'raw_route': raw_route,
                'route_data': route_data,
                'route': None,
                'error_code': None,
                'methods': None,
                'globals_list': None,
                'endpoint': None,
                'template': None,
                'renderer': None
            }

            if raw_route.startswith('@'):
                if raw_route.startswith('@error'):
                    # Handle error routes
                    error_code = int(raw_route.split('/')[1])
                    methods = route_data.get('$methods', ['GET'])
                    globals_list = route_data.get('$global', [])
                    endpoint = route_data.get('$endpointurl', None)
                    template = route_data.get('template')
                    renderer = route_data.get('python-renderer')

                    route_cmeta['route'] = raw_route
                    route_cmeta['error_code'] = error_code
                    route_cmeta['methods'] = methods
                    route_cmeta['globals_list'] = globals_list
                    route_cmeta['endpoint'] = endpoint
                    route_cmeta['template'] = template
                    route_cmeta['renderer'] = renderer

                    if not template and not renderer:
                        raise ValueError(
                            f"Error route {raw_route} must have either a "
                            f"template or a python-renderer defined."
                        )

                    # Validate methods
                    if not isinstance(methods, list):
                        raise ValueError(
                            f"Invalid methods for error route {raw_route}. "
                            f"Expected a list, got {type(methods).__name__}."
                        )
                    for method in methods:
                        if method not in ['GET', 'POST', 'PUT', 'DELETE']:
                            raise ValueError(
                                f"Invalid method for error route {raw_route}. "
                                f"Allowed methods are GET, POST, PUT, DELETE."
                            )

                    view_func = None
                    if renderer:
                        abs_path = os.path.abspath(renderer)
                        if not os.path.exists(abs_path):
                            raise FileNotFoundError(
                                f"Renderer file {renderer} not found. "
                                f"Ensure the path is correct."
                            )
                        spec = importlib.util.spec_from_file_location(
                            "renderer_module", abs_path
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if (
                                callable(attr)
                                and getattr(
                                    attr,
                                    '_is_conductor_renderer',
                                    False
                                )
                            ):
                                view_func = attr
                                break
                        if not view_func:
                            raise ValueError(
                                f"No @renderer found in renderer {renderer} "
                                f"for error route {raw_route}."
                            )

                    wrapped_func = _wrap_renderer(
                        view_func if view_func
                        else lambda: render_template(rvar('template')),
                        route_data, globals_list
                    )

                    app.errorhandler(error_code)(wrapped_func)

                    continue  # Skip to next route after handling error

            # Route and endpoint
            route = '/' + '/'.join(raw_route.split('/')[1:])
            methods = route_data.get('$methods', ['GET'])
            globals_list = route_data.get('$global', [])
            endpoint = route_data.get(
                '$endpointurl',
                ''.join(
                    c if c in _VALID_ENDPOINT_CHARS else '_' for c in raw_route
                )
            )
            template = route_data.get('template')
            renderer = route_data.get('python-renderer')

            route_cmeta['route'] = raw_route
            route_cmeta['error_code'] = 200
            route_cmeta['methods'] = methods
            route_cmeta['globals_list'] = globals_list
            route_cmeta['endpoint'] = endpoint
            route_cmeta['template'] = template
            route_cmeta['renderer'] = renderer

            if not template and not renderer:
                raise ValueError(
                    f"Route {raw_route} must have either a template "
                    f"or a python-renderer defined."
                )

            # Validate methods
            if not isinstance(methods, list):
                raise ValueError(
                    f"Invalid methods for route {raw_route}. "
                    f"Expected a list, got {type(methods).__name__}."
                )
            for method in methods:
                if method not in ['GET', 'POST', 'PUT', 'DELETE']:
                    raise ValueError(
                        f"Invalid method for route {raw_route}. "
                        f"Allowed methods are GET, POST, PUT, DELETE."
                    )

            # Renderer logic
            view_func = None
            if renderer:
                abs_path = os.path.abspath(renderer)
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(
                        f"Renderer file {renderer} not found. "
                        f"Ensure the path is correct."
                    )
                spec = importlib.util.spec_from_file_location(
                    "renderer_module", abs_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        callable(attr)
                        and getattr(attr, '_is_conductor_renderer', False)
                    ):
                        view_func = attr
                        break
                if not view_func:
                    raise ValueError(
                        f"No @renderer found in renderer {renderer} "
                        f"for route {raw_route}."
                    )

            wrapped_func = _wrap_renderer(
                view_func if view_func
                else lambda: render_template(rvar('template')),
                route_data, globals_list
            )

            app.add_url_rule(
                rule=route,
                endpoint=endpoint if endpoint else None,
                view_func=wrapped_func,
                methods=methods
            )
