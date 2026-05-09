from functools import lru_cache
import json

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class Enemy:
    enemy_id: str
    num_appearance: int = 0
    num_win: int = 0
    win_rate: float = 0


@dataclass
class EnemyMeta:
    enemy_id: str
    orig_enemy_id: str
    enemy_name: str


@lru_cache
def get_enemy_id_meta_dict() -> dict[str, EnemyMeta]:
    enemy_id_meta_dict: dict[str, EnemyMeta] = {}

    with open("res/excel/activity_table.json", encoding="utf-8") as f:
        activity_table = json.load(f)

    with open("res/excel/enemy_handbook_table.json", encoding="utf-8") as f:
        enemy_handbook_table = json.load(f)

    for enemy_id, enemy_obj in activity_table["activity"]["ENEMY_DUEL"][
        "act3enemyduel"
    ]["enemyData"].items():
        orig_enemy_id = enemy_obj["originalEnemyId"]

        enemy_name = enemy_handbook_table["enemyData"][orig_enemy_id]["name"]

        enemy_id_meta_dict[enemy_id] = EnemyMeta(
            enemy_id=enemy_id,
            orig_enemy_id=orig_enemy_id,
            enemy_name=enemy_name,
        )

    return enemy_id_meta_dict


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

    enemy_id_meta_dict = get_enemy_id_meta_dict()

    result_row_lst = []

    for enemy_obj in enemy_lst:
        enemy_meta = enemy_id_meta_dict[enemy_obj.enemy_id]

        result_row_lst.append(
            [
                enemy_obj.enemy_id,
                enemy_meta.orig_enemy_id,
                enemy_meta.enemy_name,
                enemy_obj.num_appearance,
                enemy_obj.num_win,
                enemy_obj.win_rate,
            ]
        )

    result_df = pd.DataFrame(
        result_row_lst,
        columns=[
            "Enemy ID",
            "Original Enemy ID",
            "Enemy Name",
            "Num of Appearances",
            "Num of Wins",
            "Win Rate",
        ],
    )

    Path("winrate/multiOperationMatch_act3enemyduel_01b.md").write_text(
        result_df.to_markdown(index=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
