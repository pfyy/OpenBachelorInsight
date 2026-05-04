from pathlib import Path
import sys

import frida
import requests

from openbachelori.models.baseline_lgb.pred import get_y_pred


def script_on_message(message, data):
    payload = message["payload"]

    print("----------")

    print(payload)

    y_pred = get_y_pred(payload)

    print("y_pred:", y_pred)


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
