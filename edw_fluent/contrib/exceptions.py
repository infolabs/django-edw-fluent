class WarmingUpException(Exception):
    def __init__(self, message="An error occurred", urn=None, error=None, *args):
        self.message = f"{message} (urn: {urn}, error: {error})"
        super().__init__(self.message, *args)

    def __str__(self):
        return self.message