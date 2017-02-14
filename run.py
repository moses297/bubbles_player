from bubbles_board import Board
from webpage import Webpage
from time import sleep
import pyautogui
from screenReader import Size, CaptureImage


def ensure_game_is_active(sleep_time):
    """
        Pauses the run while the game window isn't active.
        :param sleep_time: time to sleep between polling activeness of window
    """
    while not Webpage.is_active():
        sleep(sleep_time)

def make_fullscreen():
    pyautogui.keyDown('enter')
    pyautogui.keyDown('f11')

def main():
    sleep_time = 0.7
    object_location = Webpage.open_url()
    print object_location
    game_upper_x = object_location['x'] + 8
    game_upper_y = object_location['y'] - 448
    make_fullscreen()

    screen_size = Size(game_upper_x, game_upper_y, 600, 480)
    cap = CaptureImage(screen_size)
    cap.capture()
    board = Board((17, 18, 500, 500))

    for i in xrange(1000):
        ensure_game_is_active(sleep_time)
        pyautogui.moveTo(game_upper_x + 60, game_upper_y + 390)
        cap.capture()
        board.read_board_from_screen()
        board.accumulate_neighbors()
        x, y = board.get_x_y_for_shot(game_upper_x, game_upper_y)
        if x > 900 or y > 900:
            continue
        try:
            pyautogui.moveTo(x, y)
            pyautogui.click()
        except (WindowsError, ValueError) as e:
            pass  # Ignoring pyautogui exceptions
        sleep(sleep_time)
    Webpage.close()

if __name__ == '__main__':
    main()
