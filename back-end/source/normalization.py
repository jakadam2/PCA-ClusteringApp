import abc
from enum import auto, Enum

from source.data_type import DataType


class NormalizationType(Enum):
    ...
    @property
    @abc.abstractmethod
    def compatible_types(self): ...

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Return the lower-cased version of the member name.
        """
        return name.lower()


class CatNormType(NormalizationType):
    ONE_HOT_ENCODING = auto()
    ORDINAL_ENCODING = auto()

    @property
    def compatible_types(self):
        return [DataType.CATEGORICAL]


class NumNormType(NormalizationType):
    STANDARDIZATION = auto()
    MIN_MAX_SCALING = auto()
    ROBUST_SCALING = auto()

    @property
    def compatible_types(self):
        return [DataType.NUMERICAL]
