from collections import namedtuple

Point = namedtuple('Point', ['x','y'])

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    RED = (255, 0, 0)
    GRAY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    ORANGE = (252, 111, 3)

    BG_COLOR = (32, 60, 49)
    GRID_COLOR = (18, 29, 13)
    BTN_COLOR = (20, 80, 0)

class Size:
    BLOCK_SIZE = 20

    DISPLAY_W = 640
    DISPLAY_H = 480
