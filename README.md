# Conductor Framework

Conductor is a modular, extensible framework for building Flask-based web applications with a focus on clean routing, configuration, and lifecycle management.

## Features

- Modular router system with JSON-based route definitions
- Dynamic configuration loading and versioning
- Lifecycle hooks (startup, shutdown, error handling)
- Support for Flask blueprints and extensions
- Easy-to-use decorators for view registration and hooks
- Immutability and safety for configuration objects

## Public API

- `Conductor` - Main orchestrator class
- `Router` - JSON-based router
- `Config` - Immutable configuration loader
- `viewmethod` - Decorator for view functions
- Lifecycle decorators: `before_start`, `after_start`, `on_shutdown`
- `register_hook` - General-purpose hook decorator

## License

CC BY-SA 4.0

## Docs

Docs can be found at [rtfm.pixelateddream.net/conductor](https://rtfm.pixelateddream.net/conductor)

***All links***
*[Pixelated Dream](https://pixelateddream.net/home)*
*[Software](https://pixelateddream.net/software)*
*[Conductor Page](https://pixelateddream.net/software/conductor)*
*[Conductor Issues](https://pixelateddream.net/software/conductor/issues)*
*[Read the f!$#ing docs!](https://rtfm.pixelateddream.net/)*
*[Conductor Documentation](https://rtfm.pixelateddream.net/conductor)*
*[Pixelated Dream Github](https://github.com/pixelateddream)*
