class PantherException(Exception):
    """Base class for all Panther exceptions."""

    def __init__(self, message: str, **kwargs):
        """
        Exception raised during Panther operations.
        """
        super().__init__(message)
        self.error_message: str = message

        # Set default values for attributes
        self.http_status: str = "500 Internal Server Error"
        self.api_endpoint: str = "NA"
        self.http_method: str = "NA"

        # Set attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
