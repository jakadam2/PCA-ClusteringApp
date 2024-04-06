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


class NonexistentClusteringID(HTTPException):
    """Exception raised when clustering with given id does not exist in cache."""

    def __init__(self):
        super().__init__(status_code=404, detail="Clustering result with given id does not exists in cache.")


class InvalidMethodException(HTTPException):
    """Raised when invalid method was provided."""

    def __init__(self, method: Any):
        super().__init__(status_code=404, detail=f"Method '{method}' not recognized.")


class InvalidMethodArguments(HTTPException):
    """Raised when invalid arguments are passed to a method."""

    def __init__(self, method: Any):
        super().__init__(status_code=422, detail=f"Method '{method}' got invalid arguments.")


class NoActiveDataset(HTTPException):
    """Raised when tried to access dataset with no active dataset present. Upload dataset first."""

    def __init__(self):
        super().__init__(status_code=404, detail=f"No active dataset present.")
