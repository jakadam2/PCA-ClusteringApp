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


class InvalidFileExtension(HTTPException):
    """Raised when an invalid file extension is provided."""

    def __init__(self, expected_extension: str, given_extension: str):
        detail = f"Invalid file extension provided. Expected: '{expected_extension}', Given: '{given_extension}'."
        super().__init__(status_code=422, detail=detail)


class EmptyFileException(HTTPException):
    """Raised when an empty file is provided."""

    def __init__(self, file_name: str):
        super().__init__(status_code=422, detail=f"The provided file '{file_name}' is empty.")


class InvalidMapping(HTTPException):
    """Raised when invalid mapping was encountered."""

    def __init__(self, reason: str):
        super().__init__(status_code=422, detail=reason)


class NaNValuesException(HTTPException):
    """Raised when data contains NaN values"""

    def __init__(self):
        super().__init__(status_code=422, detail='Data cannot contain missing values')


class ColumnConversionError(HTTPException):
    """Raised when conversion of a column to a new type fails."""

    def __init__(self, column_name: str, new_type: str, verbose_error: str):
        super().__init__(
            status_code=404,
            detail=f"Failed to convert column '{column_name}' to type {new_type}.\nReason: \"{verbose_error}\""
        )
