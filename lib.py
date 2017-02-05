import cv2

GAME_TILES = {
    'red': cv2.imread("colors/red.png"),
    'blue': cv2.imread("colors/blue.png"),
    'purple': cv2.imread("colors/purple.png"),
    'yellow': cv2.imread("colors/yellow.png"),
    'green': cv2.imread("colors/green.png"),
    'cyan': cv2.imread("colors/cyan.png"),
    'empty': cv2.imread("colors/empty.png")
}


def is_odd(num):
    return not num % 2 == 0


class HexagonHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def hexagon_neighbors(y, x):
        even_decrement = 1 if is_odd(y) else 0
        list_of_neigbords = [(y - 1, x - 1 + even_decrement), (y - 1, x + even_decrement),
                             (y, x - 1), (y, x + 1),
                             (y + 1, x - 1 + even_decrement), (y + 1, x + even_decrement)]

        return list_of_neigbords

    def iterate_neighbors(self, tile, y, x, board, set_of):
        list_of_neigh = set()
        for y1, x1 in self.hexagon_neighbors(y, x):
            if x1 < 0 or y1 < 0 or x1 >= 16 or y1 >= 17:
                continue
            #print "{} {} {}".format(y1, x1, board[y1][x1].bubble_data)
            if tile.bubble_data == board[y1][x1].bubble_data and (y1, x1) not in set_of:
                list_of_neigh.add((y1, x1))
        return list_of_neigh

    def get_neighbors_of_tile_and_list(self, tile, y, x, game_board, set_of):
        if tile.bubble_data == 'empty':
            return set()
        set_of.add((y, x))
        found_set = self.iterate_neighbors(tile, y, x, game_board, set_of)
        set_of.update(found_set)
        for y1, x1 in found_set:
            set_of.update(self.get_neighbors_of_tile_and_list(tile, y1, x1, game_board, set_of))
        return set_of

    def is_empty_neighbor_exists(self, y, x, board):
        if board[y][x].bubble_data == 'empty':
            return False
        for y1, x1 in self.hexagon_neighbors(y, x):
            if x1 < 0 or y1 < 0 or x1 >= 17 or y1 >= 16:
                continue
            if board[y1][x1].bubble_data == 'empty':
                return True
        return False


class Line(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        try:
            self.slope = float(y1 - y2) / float(x1 - x2)
        except ZeroDivisionError:
            self.slope = 1
        self.y_intercept = -(x1 * self.slope) + y1

    def all_points_in_line(self):
        result = []
        y3, y4 = self.y1, self.y2
        if self.y1 > self.y2:
            y3, y4 = self.y2, self.y1
        for y in range(y3, y4):
            x = int(self.get_x_for_y(y))
            result.append((x, y))
        return result

    def left_wall(self):
        result = []
        LEFT_WALL = 17
        RIGHT_WALL = 436
        increment = 1
        self.slope = float(self.y1 - self.y2) / float(self.x1 - (self.x2 - LEFT_WALL) * -1)
        self.y_intercept = -(self.x1 * self.slope) + self.y1
        direction_left = False
        if self.x1 > (self.x2 - LEFT_WALL) * -1:
            increment = -1
            direction_left = True
        new_x = self.x1
        for x in range(self.x1, (self.x2 - LEFT_WALL) * -1, increment):
            y = int(self.get_y_for_x(x))
            new_x += increment
            if new_x <= LEFT_WALL and direction_left:
                direction_left = False
                increment = 1
            if new_x >= RIGHT_WALL and not direction_left:
                direction_left = True
                increment = -1
            result.append((new_x, y))
        return result

    def right_wall(self):
        RIGHT_WALL = 436
        LEFT_WALL = 17
        result = []
        x3, x4 = self.x1, (RIGHT_WALL - self.x2) * 2 + self.x2
        self.slope = float(self.y1 - self.y2) / float(self.x1 - x4)
        self.y_intercept = -(self.x1 * self.slope) + self.y1
        direction_right = True
        increment = 1
        new_x = x3
        if x3 > x4:
            direction_right = False
            increment = -1
        for x in range(x3, x4, increment):
            y = int(self.get_y_for_x(x))
            new_x += increment
            if direction_right and new_x >= RIGHT_WALL:
                direction_right = False
                increment = -1
            elif not direction_right and new_x <= LEFT_WALL:
                direction_right = True
                increment = 1
            result.append((new_x, y))
        return result

    def get_y_for_x(self, x):
        return x*self.slope + self.y_intercept

    def get_x_for_y(self, y):
        try:
            return (y - self.y_intercept) / self.slope
        except ZeroDivisionError:
            return 0


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x,y