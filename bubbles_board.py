from image_lib import TILE_SIZE, ODD_TILE_SPACR, ROW, COLUMN, Screen, color_from_image
from lib import is_odd, HexagonHandler, Point, Line
import cv2


class Tile(object):
    def __init__(self, bubble_data, neighbors_count):
        self.bubble_data = bubble_data
        self.neighbors_count = neighbors_count
        self.shoot_location = None


class Board(object):
    def __init__(self, board_size, debug=False):
        self.x1, self.y1, self.x2, self.y2 = board_size
        self.board = self._init_board()
        self._debug = debug
        self.screen = Screen('')
        self.read_board_from_screen()
        self.last_shot = (5, 5)
        self.hexagon = HexagonHandler()

    def _init_board(self):
        return [[Tile('empty', 0) for x in range(ROW)] for y in range(COLUMN)]

    def read_board_from_screen(self):
        self.screen.read_screenshot()
        height_index = 0
        for height in xrange(self.x1, self.x1 + COLUMN * TILE_SIZE[0], TILE_SIZE[0]):
            width_index = 0
            for width in xrange(self.y1, self.y1 + ROW * TILE_SIZE[1], TILE_SIZE[1]):
                if is_odd(height_index):
                    width += ODD_TILE_SPACR
                single_tile_from_screen = self.screen.image[height:height + TILE_SIZE[0], width:width+ TILE_SIZE[1]]
                if self._debug:
                    cv2.imwrite("all_images/im{}.png".format(width_index + COLUMN * height_index), single_tile_from_screen)
                self.board[height_index][width_index].bubble_data = color_from_image(single_tile_from_screen)
                width_index += 1
            height_index += 1

    def accumulate_neighbors(self):
        height_index = 0
        for row in self.board:
            width_index = 0
            for tile in row:
                self.board[height_index][width_index].neighbors_count = 0
                width_index += 1
            height_index += 1

        height_index = 0
        for row in self.board:
            width_index = 0
            for tile in row:
                if self.board[height_index][width_index].neighbors_count == 0:
                    empty_set = set()
                    list_of = self.hexagon.get_neighbors_of_tile_and_list(tile, height_index, width_index, self.board, empty_set)
                    for h, w in list_of:
                        self.board[h][w].neighbors_count = len(list_of)
                width_index += 1
            height_index += 1

    def get_current_color(self):
        x, y = 209, 402
        cropped = self.screen.image[y:y+ TILE_SIZE[0], x:x+ TILE_SIZE[1]]
        cv2.imwrite('local.png', cropped)
        return color_from_image(cropped)

    def get_all_tiles_next_to_empty(self):
        reachable_tiles = []
        height_index = 0
        for row in self.board:
            width_index = 0
            for tile in row:
                if self.hexagon.is_empty_neighbor_exists(height_index, width_index, self.board):
                    reachable_tiles.append([tile, (height_index, width_index)])
                width_index += 1
            height_index += 1
        return reachable_tiles

    def get_lowest_reachable_bubble(self, color):
        found_color_index = []
        first_row_index = []
        height_index = COLUMN - 1
        for row in reversed(self.board):
            width_index = 0
            for tile in row:
                if width_index in first_row_index:
                    continue
                if tile.bubble_data != 'empty':
                    first_row_index.append(width_index)
                    if tile.bubble_data == color:
                        found_color_index.append([tile.neighbors_count, (width_index, height_index)])
                width_index += 1
            height_index -= 1
        return found_color_index

    def get_only_my_colors(self, tile_list, color):
        result = []
        for tile in tile_list:
            if tile[0].bubble_data == color:
                result.append(tile)
        return result

    def check_if_line_is_clear_from_obstacles(self, line):
        new_image = self.screen.image
        for location in line.all_points_in_line():
            if location[1] >= 377:
                continue

            single_pixel = self.screen.image[location[1], location[0]]
            #new_image[location[1], location[0]] = [0, 0, 0]
            #print single_pixel
            if not single_pixel[0] == 192 and not single_pixel[1] == 192 and not single_pixel[2] == 255:
                #print "Obstacle"
                #cv2.imwrite('tmp/{}_{}_test_line.png'.format(line.x2, line.y2), new_image)
                return True
                # cv2.imwrite('tmp/{}.png'.format(location[0]), single_pixel)
        #cv2.imwrite('tmp/{}_{}_test_line.png'.format(line.x2, line.y2), new_image)
        return False

    def check_if_line_is_clear_left(self, line):
        shoot_location = (0, 0)
        for location in line.left_wall():
            if location[1] >= 377:
                continue
            if location[0] == 17:
                shoot_location = (17, location[1])
            single_pixel = self.screen.image[location[1], location[0]]
            if not single_pixel[0] == 192 and not single_pixel[1] == 192 and not single_pixel[2] == 255:
                return True
        return shoot_location

    def check_if_line_is_clear_right(self, line):
        shoot_location = (0, 0)
        for location in line.right_wall():
            if location[1] >= 377:
                continue
            elif location[0] == 436:
                shoot_location = (436, location[1])
            single_pixel = self.screen.image[location[1], location[0]]
            if not single_pixel[0] == 192 and not single_pixel[1] == 192 and not single_pixel[2] == 255:
                return True
        return shoot_location

    def blocked_by_obstacle(self, bubble):
        starting_point_left = Point(209, 413)
        starting_point_right = Point(234, 413)

        bubble_x_offset = 24 if is_odd(bubble[1][0]) else 12
        #bubble_x_offset = 0
        bubble_middle = Point(17 + 24 * bubble[1][1] + bubble_x_offset - 12,  bubble[1][0] * 24 + 18 + 25)
        bubble_left = Point(bubble_middle.x - 12, bubble_middle.y)
        bubble_right = Point(bubble_middle.x + 12, bubble_middle.y)

        for offset in xrange(-4, 4, 4):
            line_left = Line(starting_point_left.x + offset, starting_point_left.y, bubble_left.x, bubble_left.y)
            line_right = Line(starting_point_right.x + offset, starting_point_right.y, bubble_right.x, bubble_right.y)
            if not self.check_if_line_is_clear_from_obstacles(line_left) and not self.check_if_line_is_clear_from_obstacles(line_right):
                bubble[0].shoot_location = Point(bubble_middle.x, bubble_middle.y)
                print "shoot at color:{} count:{} location:{},{} x:{} y:{}".format(bubble[0].bubble_data, bubble[0].neighbors_count, bubble[1][1], bubble[1][0], bubble[0].shoot_location.x, bubble[0].shoot_location.y)
                return False
        return True

    def blocked_via_left_wall_shot(self, bubble):
        starting_point_left = Point(209, 413)
        starting_point_right = Point(234, 413)

        bubble_x_offset = 24 if is_odd(bubble[1][0]) else 12
        # bubble_x_offset = 0
        bubble_middle = Point(17 + 24 * bubble[1][1] + bubble_x_offset - 12, bubble[1][0] * 24 + 18 + 25)
        bubble_left = Point(bubble_middle.x - 12, bubble_middle.y)
        bubble_right = Point(bubble_middle.x + 12, bubble_middle.y)

        for offset in xrange(-4, 4, 4):
            line_left = Line(starting_point_left.x + offset, starting_point_left.y, bubble_left.x, bubble_left.y)
            line_right = Line(starting_point_right.x + offset, starting_point_right.y, bubble_right.x, bubble_right.y)
            first = self.check_if_line_is_clear_left(line_left)
            second = self.check_if_line_is_clear_left(line_right)
            if not first and not second:
                bubble[0].shoot_location = Point(first[0], first[1])
                print "LEFT shoot at color:{} count:{} location:{},{} x:{} y:{}".format(bubble[0].bubble_data,
                                                                                   bubble[0].neighbors_count,
                                                                                   bubble[1][1], bubble[1][0],
                                                                                   bubble[0].shoot_location.x,
                                                                                   bubble[0].shoot_location.y)

                return False
        return True


    def blocked_via_right_wall_shot(self, bubble):
        starting_point_left = Point(209, 413)
        starting_point_right = Point(234, 413)

        bubble_x_offset = 24 if is_odd(bubble[1][0]) else 12
        # bubble_x_offset = 0
        bubble_middle = Point(17 + 24 * bubble[1][1] + bubble_x_offset - 12, bubble[1][0] * 24 + 18 + 25)
        bubble_left = Point(bubble_middle.x - 12, bubble_middle.y)
        bubble_right = Point(bubble_middle.x + 12, bubble_middle.y)

        for offset in xrange(-4, 4, 4):
            line_left = Line(starting_point_left.x + offset, starting_point_left.y, bubble_left.x, bubble_left.y)
            line_right = Line(starting_point_right.x + offset, starting_point_right.y, bubble_right.x, bubble_right.y)
            first = self.check_if_line_is_clear_right(line_left)
            second = self.check_if_line_is_clear_right(line_right)
            if not first and not second:
                bubble[0].shoot_location = Point(first[0], first[1])
                print "RIGHT shoot at color:{} count:{} location:{},{} x:{} y:{}".format(bubble[0].bubble_data,
                                                                                   bubble[0].neighbors_count,
                                                                                   bubble[1][1], bubble[1][0],
                                                                                   bubble[0].shoot_location.x,
                                                                                   bubble[0].shoot_location.y)

                return False
        return True

    def remove_blocked_bubbles(self, reachable_bubbles):
        regular_shot = []
        for bubble in reachable_bubbles:
            if not self.blocked_by_obstacle(bubble):
                regular_shot.append(bubble)
            elif not self.blocked_via_left_wall_shot(bubble):
                regular_shot.append(bubble)
            elif not self.blocked_via_right_wall_shot(bubble):
                regular_shot.append(bubble)
        return regular_shot

    def get_x_y_for_shot(self, board_x, board_y):
        current_color = self.get_current_color()
        reachable_bubbles = self.get_all_tiles_next_to_empty()
        reachable_bubbles = self.get_only_my_colors(reachable_bubbles, current_color)
        reachable_bubbles = self.remove_blocked_bubbles(reachable_bubbles)
        highest_neighbor = [Tile('empty', 0), self.last_shot]
        for array in reachable_bubbles:
            if highest_neighbor[0].neighbors_count == 0:
                highest_neighbor = array
                continue
            if array[0].neighbors_count > highest_neighbor[0].neighbors_count:
                highest_neighbor = array
        self.last_shot = highest_neighbor[1]
        if highest_neighbor[0].shoot_location:
            return board_x + highest_neighbor[0].shoot_location.x, board_y + highest_neighbor[0].shoot_location.y
        offset = 12 if is_odd(highest_neighbor[1][0]) else 0
        return board_x + 17 + 24*highest_neighbor[1][1] + offset, board_y + highest_neighbor[1][0]*24 + 20

    def random_shot(self):
        return (500, 500)

    def print_board(self):
        for line in self.board:
            print '{}'.format([x.bubble_data for x in line])

    def print_count(self):
        for line in self.board:
            print '{}'.format([x.neighbors_count for x in line])