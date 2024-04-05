from typing import Any

from fastapi import HTTPException


class NonexistentColumnsException(HTTPException):
    """Raised when nonexistent columns where provided."""

    def __init__(self):
        super().__init__(status_code=404, detail="Nonexistent columns provided.")


class NonNumericColumnsException(HTTPException):
    """Exception raised when columns expected to be numeric are not."""

    def __init__(self):
        super().__init__(status_code=422, detail="Columns must be numerical.")


class InvalidMethodException(HTTPException):
    """Raised when invalid method was provided."""

    def __init__(self, method: Any):
        super().__init__(status_code=404, detail=f"Clustering method {method} not recognized.")
