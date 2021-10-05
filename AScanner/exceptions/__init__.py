
"""Exceptions to throw."""


class ConfigurationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ConfigurationError: %s' % self.value


class ConfigurationNotFound(ConfigurationError):
    def __init__(self, filename):
        super(ConfigurationNotFound, self).__init__(None)
        self.filename = filename

    def __str__(self):
        return 'Unable to find the configuration file %s' % self.filename
