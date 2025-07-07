from .routing import Router
from .configuration import Config
from conductor import _default_app_starter

import functools
from typing import Dict, Optional

from flask import Flask


class Conductor:
    """
    The Conductor class is the full orchestration of the Conductor framework.
    It initializes the Flask application and the router, and provides methods
    for managing the application lifecycle.

    Args:
        app (Flask): The Flask application instance.
        router (Router): The Router instance for routing requests.
        config (Config): The configurations for the application.
        host (str, optional): The host to run the application on. Default None.
        port (int, optional): The port to run the application on. Default None.
        **kwargs: Additional keyword arguments, such as config for configuring
        the flask app
    """
    def __init__(
        self, app: Flask,   router: Router, config: Optional[Config],
        host: str = None,   port: int = None,
        **kwargs: Dict
    ) -> None:
        """
        App initializer.
        Args: inherited from the Conductor class.
        """
        self.app: Flask = app
        self.config: Config = config
        self.router: Router = router
        self.host: str = host
        self.port: int = port
        self.app.config.update(kwargs['config'] if 'config' in kwargs else {})

        self.starter: callable = kwargs.get('starter', _default_app_starter)

    def start(self) -> None:
        """
        Starts the Conductor application.
        First, it activates the router, then it starts the Flask app using the
        user specified starter function or the default starter if none is set.
        Throws an error when the host or port is not set. Otherwise, it starts.
        """
        if self.host and self.port:
            self.router.activate_router(self.app)
            self.starter(self.app, host=self.host, port=self.port)
        else:
            raise ValueError("Host and port must be set to start application.")

    def before_start(self, func: callable) -> callable:
        """
        Decorator to register a function to be called before the app starts.
        Usage:
            @conductor.before_start
            def my_func():
                # Code to run before the app starts
                pass
        """
        self.app.before_first_request(func)
        return func

    def after_start(self, func: callable) -> callable:
        """
        Decorator to register a function to be called after the app starts.
        Usage:
            @conductor.after_start
            def my_func():
                # Code to run after the app starts
                pass
        """
        self.app.after_request(func)
        return func

    def on_shutdown(self, func: callable) -> callable:
        """
        Decorator to register a function to be called when app is stopping.
        Usage:
            @conductor.on_shutdown
            def my_func():
                # Code to run when the app is stopping
                pass
        """
        self.app.teardown_appcontext(func)
        return func

    def register_hook(hook_func, when='before'):
        """
        Decorator factory to add hook_func before or after the decorated func.
        Usage:
            @conductor.register_hook(my_hook, when='before')
            def my_func(...): ...
        """
        def decorator(target_func):
            @functools.wraps(target_func)
            def wrapper(*args, **kwargs):
                if when == 'before':
                    hook_func(*args, **kwargs)
                    return target_func(*args, **kwargs)
                elif when == 'after':
                    result = target_func(*args, **kwargs)
                    hook_func(*args, **kwargs)
                    return result
                else:
                    raise ValueError("when must be 'before' or 'after'")
            return wrapper
        return decorator
