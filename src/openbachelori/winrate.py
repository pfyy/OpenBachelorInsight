from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Enemy:
    enemy_id: str
    num_appearance: int = 0
    num_win: int = 0
    win_rate: float = 0


def column_is_enemy_id(column_name: str) -> bool:
    return column_name.startswith("enemy_")


def main():
    df_orig = pd.read_csv("csv/multiOperationMatch_act3enemyduel_01b.csv")

    enemy_dict: dict[str, Enemy] = {}
    enemy_lst: list[Enemy] = []

    for column_name in df_orig.columns:
        if not column_is_enemy_id(column_name):
            continue
        enemy_obj = Enemy(enemy_id=column_name)
        enemy_dict[column_name] = enemy_obj
        enemy_lst.append(enemy_obj)

    for row_idx, row in df_orig.iterrows():
        victor = row["label"]
        for column_name, val in row.items():
            if not column_is_enemy_id(column_name):
                continue

            if not val:
                continue

            enemy_dict[column_name].num_appearance += 1

            if victor * val >= 0:
                enemy_dict[column_name].num_win += 1

    for enemy_obj in enemy_lst:
        enemy_obj.win_rate = enemy_obj.num_win / enemy_obj.num_appearance

    enemy_lst.sort(key=lambda x: x.win_rate, reverse=True)

    result_row_lst = []

    for enemy_obj in enemy_lst:
        result_row_lst.append(
            [
                enemy_obj.enemy_id,
                enemy_obj.num_appearance,
                enemy_obj.num_win,
                enemy_obj.win_rate,
            ]
        )

    result_df = pd.DataFrame(
        result_row_lst,
        columns=["Enemy ID", "Num of Appearances", "Num of Wins", "Win Rate"],
    )

    Path("winrate/multiOperationMatch_act3enemyduel_01b.md").write_text(
        result_df.to_markdown(index=False)
    )


if __name__ == "__main__":
    main()
