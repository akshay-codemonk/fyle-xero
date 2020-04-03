class MissingMappingsError(Exception):
    def __init__(self, message):
        super(MissingMappingsError, self).__init__(message)
        self.message = message

    def __str__(self):
        return repr(self.message)
