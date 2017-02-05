from bubbles import bubbles_board
from webpage import open_url
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


def main():
    screen_size = Size(316, 280, 600, 480)
    cap = CaptureImage(screen_size)
    open_url('file:///' + abspath('Bubble%20Game.html'))
    cap.capture()
    board = bubbles_board.Board((17, 18, 500, 500))
    offset = 0
    for i in xrange(1000):
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
        sleep(0.7)

if __name__ == '__main__':
    main()