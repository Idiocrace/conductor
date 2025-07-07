from conductor import _CONDUCTOR_CONFIG_VERSION

import json


class Config:
    """
    The configuration class for the Conductor framework. Configurations are
    loaded from a JSON string and parsed into attributes. It also contains
    overrides and defaults.
    Args:
        config (str): A string containing the path for the JSON config file.
    Usage:
        config = Config(config_file_path)
        config.some_attribute  # Access parsed configuration values
    """
    def __init__(self, config: str) -> None:
        # load the config
        self._config_parsed = json.loads(config)

        # Get the version from the config file
        self.version = self._config_parsed.get("$version", "unset")
        # Versioning checks
        if self.version != _CONDUCTOR_CONFIG_VERSION:
            raise ValueError(
                f"Configuration file version {self.version} does not match"
                " the expected Conductor Config version "
                "{_CONDUCTOR_CONFIG_VERSION}. Please update the configuration "
                "file or the Conductor framework."
            )

        self.defaults = self._config_parsed.get('$defaults', {})
        self.overrides = self._config_parsed.get('$overrides', {})

        for key, value in self._config_parsed.items():
            if key.startswith('$') or key.startswith('#'):
                continue
            setattr(self, key, value)

    def __setattr__(self, name, value):
        # Allow setting attributes if they do not already exist.
        # This is to ensure that config attributes are immutable once set.
        # They are immutable to maintain parity between all uses of the config.
        if not hasattr(self, name):
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"Unable to set attribute '{name}': "
                "Config attributes are immutable once set."
            )
