from itertools import chain

import jsonlines
import pandas as pd
import numpy as np


def main():
    enemy_id_dict = {}
    enemy_id_lst = []

    device_id_dict = {}
    device_id_lst = []

    for i in range(1, 13):
        with jsonlines.open(
            f"data/multiOperationMatch_act3enemyduel_01b_{i}.jsonl"
        ) as reader:
            for obj in reader:
                for round_id in range(10):
                    for enemy_id in chain(
                        obj["born_units"][round_id]["leftUnitIds"],
                        obj["born_units"][round_id]["rightUnitIds"],
                    ):
                        if enemy_id not in enemy_id_dict:
                            enemy_id_dict[enemy_id] = len(enemy_id_lst)
                            enemy_id_lst.append(enemy_id)

                for key in obj.keys():
                    if "|" in key and key not in device_id_dict:
                        device_id_dict[key] = len(device_id_lst)
                        device_id_lst.append(key)

    num_enemy = len(enemy_id_lst)
    num_device = len(device_id_lst)

    sample_vec_lst = []

    for i in range(1, 13):
        with jsonlines.open(
            f"data/multiOperationMatch_act3enemyduel_01b_{i}.jsonl"
        ) as reader:
            for obj in reader:
                device_vec = np.zeros(num_device, dtype=int)
                for device_idx, device_id in enumerate(device_id_lst):
                    if device_id in obj:
                        device_vec[device_idx] = 1

                for round_id in range(10):
                    sample_vec = np.zeros(num_enemy + num_device + 1, dtype=int)

                    round_obj = obj["born_units"][round_id]

                    for enemy_id, enemy_cnt in round_obj["leftUnitIds"].items():
                        enemy_idx = enemy_id_dict[enemy_id]
                        sample_vec[enemy_idx] = enemy_cnt

                    for enemy_id, enemy_cnt in round_obj["rightUnitIds"].items():
                        enemy_idx = enemy_id_dict[enemy_id]
                        sample_vec[enemy_idx] = -enemy_cnt

                    sample_vec[num_enemy : num_enemy + num_device] = device_vec

                    if obj[f"round_{round_id}_victor"] == 1:
                        sample_vec[num_enemy + num_device] = 1
                    elif obj[f"round_{round_id}_victor"] == 2:
                        sample_vec[num_enemy + num_device] = -1
                    else:
                        sample_vec[num_enemy + num_device] = 0

                    sample_vec_lst.append(sample_vec)

    column_name_lst = enemy_id_lst + device_id_lst + ["label"]

    df = pd.DataFrame(sample_vec_lst, columns=column_name_lst)

    df.to_csv("csv/multiOperationMatch_act3enemyduel_01b.csv", index=False)


if __name__ == "__main__":
    main()
