from pathlib import Path
import sys

import frida
import requests


def script_on_message(message, data):
    randomSpawnGroupKey = message["payload"]["randomSpawnGroupKey"]
    randomSpawnGroupPackKey = message["payload"]["randomSpawnGroupPackKey"]

    device_id = f"{randomSpawnGroupKey}|{randomSpawnGroupPackKey}"

    r = requests.post(
        "http://127.0.0.1:7443/obi/update",
        json={
            device_id: True,
        },
    )
    r.raise_for_status()


def main():
    device = frida.get_remote_device()
    session = device.attach("Gadget")

    script = session.create_script(Path("rel/main.js").read_text())
    script.on("message", script_on_message)
    script.load()

    print("----------")

    sys.stdin.read()


if __name__ == "__main__":
    main()
