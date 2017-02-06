from bubbles_board import Board
from webpage import Webpage
from image_lib import ODD_TILE_SPACR
from lib import is_odd
from time import sleep
from os.path import abspath
import pyautogui
from screenReader import Size, CaptureImage


def add_offsets(y, x):
    offset_oddline = ODD_TILE_SPACR if is_odd(y) else 0
    if x < 2:
        offset = - 3
    elif x < 4:
        offset = -12
    elif x < 8:
        offset = -4
    elif x < 12:
        offset = 4
    else:
        offset = 18
    return offset_oddline + offset


def ensure_game_is_active(sleep_time):
    """
        Pauses the run while the game window isn't active.
        :param sleep_time: time to sleep between polling activeness of window
    """
    while not Webpage.is_active():
        sleep(sleep_time)


def main():
    sleep_time = 0.7
    screen_size = Size(316, 280, 600, 480)
    cap = CaptureImage(screen_size)
    Webpage.open_url()
    cap.capture()
    board = Board((17, 18, 500, 500))
    offset = 0
    for i in xrange(1000):
        ensure_game_is_active(sleep_time)
        pyautogui.moveTo(316 + 17 + 34, 280 + 389)
        cap.capture()
        board.read_board_from_screen()
        board.accumulate_neighbors()
        x, y = board.get_x_y_for_shot()
        #offset = add_offsets(y, x)
        try:
            #print x,y
            if x > 900 or y > 900:
                print "exit"
                exit()
            pyautogui.moveTo(x, y)
            pyautogui.click()
        except Exception:
            pass
        sleep(sleep_time)

if __name__ == '__main__':
    main()
