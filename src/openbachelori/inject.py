from pathlib import Path
import sys

import frida


def script_on_message(message, data):
    print(message)


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
