from typing import Optional


class ValidationError(Exception):
    """
    Exception that implements to_dict() method to be used by Flask error
    handler.
    Args:
        message: error detailed message describing the reason
        status_code: HTTP status code.
        payload: additional attributes to be included to serialized body.
    """

    def __init__(self,
                 message: str,
                 status_code: Optional[int] = 400,
                 payload: Optional[dict] = None):
        super().__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload or dict()

    def to_dict(self) -> dict:
        """Returns a dict with an error payload."""
        self.payload['message'] = self.message
        return self.payload
