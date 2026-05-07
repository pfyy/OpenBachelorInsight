from pathlib import Path
import sys
from functools import lru_cache

import frida
import requests

from openbachelori.models.baseline_lgb.pred import get_y_pred


@lru_cache
def get_multi_tag_dict():
    return {
        "enemy_15072_dqlbgg": [
            "enemy_15070_dqhlgy",
            "enemy_15071_dqyrzf",
        ],
        "enemy_15073_dqkght": [
            "enemy_15074_dqdght",
        ],
        "enemy_15075_dqzklz": [
            "enemy_15076_dqzmst",
        ],
    }


def process_multi_tag(payload):
    multi_tag_dict = get_multi_tag_dict()

    for multi_tag, enemy_id_lst in multi_tag_dict.items():
        if multi_tag in payload:
            print(f"multi_tag {multi_tag} found in {payload}")
            for enemy_id in enemy_id_lst:
                payload[enemy_id] = payload[multi_tag]


def script_on_message(message, data):
    payload = message["payload"]

    process_multi_tag(payload)

    print("----------")

    print(payload)

    y_pred = get_y_pred(payload)

    print(f"y_pred: {y_pred:.4f}")


def main():
    device = frida.get_remote_device()
    session = device.attach("Gadget")

    script = session.create_script(Path("rel/reader.js").read_text())
    script.on("message", script_on_message)
    script.load()

    print("----------")

    sys.stdin.read()


if __name__ == "__main__":
    main()
