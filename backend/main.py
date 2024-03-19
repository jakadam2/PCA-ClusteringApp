import numpy as np
from pandas import DataFrame

from data_transformer import DataTransformer
from data_type import DataType
from normalization import NumNormType, CatNormType

if __name__ == "__main__":
    data = {
        "column_1": np.random.randint(low=0, high=2, size=4),
        "column_2": np.random.randint(low=0, high=3, size=4),
        "column_3": np.random.randint(low=0, high=3, size=4),
        "column_4": [True, True, False, False],
        "column_5": [f"{x}" for x in np.random.randint(low=0, high=3, size=4)],
    }
    dataset = DataFrame.from_dict(data)
    print(dataset)

    dataset = DataTransformer.change_types(dataset,
                                           {
                                               'column_1': DataType.CATEGORICAL,
                                               'column_2': DataType.NUMERICAL,
                                               'column_4': DataType.NUMERICAL,
                                                }
                                           )
    print("=" * 80)
    print(dataset)

    dataset = DataTransformer.normalize(dataset, NumNormType.STANDARDIZATION, CatNormType.ONE_HOT)
    print("=" * 80)
    print(dataset)
