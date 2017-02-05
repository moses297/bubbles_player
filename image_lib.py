from lib import GAME_TILES
import cv2

TILE_SIZE, ODD_TILE_SPACR = [24, 24], 12
ROW, COLUMN = 17, 16


class Screen(object):
    def __init__(self, size):
        pass

    def read_screenshot(self):
        self.image = cv2.imread("test.png")


def compare_pixels(pixel1, pixel2, diff=5):
    pixel_true = [False, False, False]
    for i in xrange(3):
        if pixel2[i] + diff >= pixel1[i] >= pixel2[i] - diff:
            pixel_true[i] = True

    return pixel_true[0] and pixel_true[1] and pixel_true[2]


def compare_cv2_middle_pixel(image1, image2):
    width, height, _ = image1.shape
    return compare_pixels(image1[width/2, height/2], image2[width/2, height/2])


def compare_cv2_images(image1, image2):
    width, height, _ = image1.shape
    threshold = int((width * height) * 0.9)
    compration_increment = 0
    for w in xrange(width):
        for h in xrange(height):
            if compare_pixels(image1[w, h], image2[w, h]):
                compration_increment += 1
    return compration_increment >= threshold


def color_from_image(image):
    for color in GAME_TILES:
        if compare_cv2_middle_pixel(image, GAME_TILES[color]):
            return color
    return 'empty'