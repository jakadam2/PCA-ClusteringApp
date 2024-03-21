from enum import auto, StrEnum


class CatNormType(StrEnum):
    ONE_HOT = auto()


class NumNormType(StrEnum):
    STANDARDIZATION = auto()
