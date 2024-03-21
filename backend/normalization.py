from enum import Enum, auto


class CatNormType(Enum):
    ONE_HOT = auto()


class NumNormType(Enum):
    STANDARDIZATION = auto()
