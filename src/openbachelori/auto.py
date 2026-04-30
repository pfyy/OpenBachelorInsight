import time

import pyautogui
import pygetwindow


def try_to_click(region: tuple[int, int, int, int], btn_img_filepath: str) -> bool:
    try:
        x, y = pyautogui.locateCenterOnScreen(
            btn_img_filepath, region=region, confidence=0.8
        )
    except pyautogui.ImageNotFoundException:
        return False

    pyautogui.click(x, y)
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
    while True:
        oneshot()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
