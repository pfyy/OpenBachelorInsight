from functools import lru_cache


import lightgbm as lgb
import pandas as pd
import numpy as np


@lru_cache
def get_model():
    model = lgb.Booster(model_file="src/openbachelori/models/baseline_lgb/model.txt")
    return model


@lru_cache
def get_column_name_dict():
    df = pd.read_csv("csv/multiOperationMatch_act3enemyduel_01b.csv", nrows=0)

    column_name_lst = df.columns.to_list()[:-1]

    column_name_dict = {column_name: i for i, column_name in enumerate(column_name_lst)}

    return column_name_dict


def get_y_pred(column_val_dict: dict[str, int]):
    column_name_dict = get_column_name_dict()

    feature_vec = np.zeros(len(column_name_dict))

    for column_name, val in column_val_dict.items():
        column_idx = column_name_dict[column_name]
        feature_vec[column_idx] = val

    model = get_model()

    y_pred = model.predict([feature_vec])[0]

    return y_pred
