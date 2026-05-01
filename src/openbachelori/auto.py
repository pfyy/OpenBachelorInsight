import time
import traceback
import sys

import pyautogui
import pygetwindow
from elevate import elevate


def try_to_click(region: tuple[int, int, int, int], btn_img_filepath: str) -> bool:
    try:
        left, top, width, height = pyautogui.locateOnScreen(
            btn_img_filepath, region=region, confidence=0.8
        )
    except pyautogui.ImageNotFoundException:
        return False

    pyautogui.click(left + width, top + height)
    return True


def oneshot():
    window = pygetwindow.getWindowsWithTitle("明日方舟")[0]

    region = (window.left, window.top, window.width, window.height)

    if try_to_click(region, "btn/1.png"):
        return
    if try_to_click(region, "btn/2.png"):
        return
    if try_to_click(region, "btn/3.png"):
        return


def main():
    try:
        elevate()
        while True:
            oneshot()
            time.sleep(0.1)
    except Exception:
        traceback.print_exc()
        sys.stdin.read()


if __name__ == "__main__":
    main()
