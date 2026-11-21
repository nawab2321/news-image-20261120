from math import cos, pi, sin
from random import Random

from PIL import Image, ImageDraw, ImageEnhance


class Scene:
    """A small drawing surface in editorial illustration coordinates."""

    SCALE = 3

    def __init__(self, size, sky, horizon):
        self.width, self.height = size
        self.image = Image.new('RGB', self.point(size), sky)
        self.pen = ImageDraw.Draw(self.image)
        self.horizon = horizon

    def point(self, xy):
        return tuple(round(value * self.SCALE) for value in xy)

    def box(self, xy, color, outline=None, width=1):
        self.pen.rectangle(self.point(xy), fill=color, outline=outline, width=width * self.SCALE)

    def oval(self, xy, color=None, outline=None, width=1):
        self.pen.ellipse(self.point(xy), fill=color, outline=outline, width=width * self.SCALE)

    def arc(self, xy, start, end, color, width=1):
        self.pen.arc(self.point(xy), start, end, color, width=width * self.SCALE)

    def poly(self, points, color):
        self.pen.polygon([self.point(point) for point in points], fill=color)

    def line(self, points, color, width=1):
        self.pen.line([self.point(point) for point in points], fill=color,
                      width=width * self.SCALE, joint='curve')

    def sky(self, color, seed, count=180):
        rng = Random(seed)
        for _ in range(count):
            x = rng.randrange(self.width)
            y = rng.randrange(self.horizon)
            self.pen.point(self.point((x, y)), fill=color)

    def printed(self):
        # A staggered ink screen gives the flat shapes a shared print texture.
        screen = Image.new('L', self.image.size)
        ink_dots = ImageDraw.Draw(screen)
        spacing = 5 * self.SCALE
        for row, y in enumerate(range(0, screen.height, spacing)):
            for x in range((row % 2) * spacing // 2, screen.width, spacing):
                ink_dots.ellipse((x, y, x + 4, y + 4), fill=74)
        darker = ImageEnhance.Brightness(self.image).enhance(0.81)
        return Image.composite(darker, self.image, screen)


def brussels():
    s = Scene((240, 84), '#395770', 82)
    s.oval((26, -22, 146, 98), '#304963', '#78918c')
    s.oval((105, -22, 225, 98), '#294059', '#78918c')
    gold = '#e5bc73'
    for index in range(12):
        angle = index * pi / 6
        x, y = 79 + 28 * cos(angle), 42 + 28 * sin(angle)
        s.oval((x - 2, y - 2, x + 2, y + 2), gold)
    s.box((131, 20, 185, 63), '#1f3652')
    s.line([(132, 21), (184, 62)], '#f0dec0', 5)
    s.line([(184, 21), (132, 62)], '#f0dec0', 5)
    s.line([(158, 20), (158, 63)], '#f0dec0', 9)
    s.line([(131, 41), (185, 41)], '#f0dec0', 9)
    s.line([(158, 20), (158, 63)], '#a64c4d', 4)
    s.line([(131, 41), (185, 41)], '#a64c4d', 4)
    return s


def peru():
    s = Scene((240, 84), '#d1a673', 82)
    s.oval((149, -6, 221, 66), '#edca91')
    s.poly([(0, 58), (26, 46), (43, 30), (72, 51), (102, 22), (121, 36), (153, 9),
            (185, 48), (208, 35), (240, 62), (240, 84), (0, 84)], '#566f69')
    s.poly([(132, 29), (153, 9), (176, 39), (159, 35), (149, 41), (144, 32)], '#ecdcbb')
    s.poly([(0, 64), (34, 60), (50, 55), (78, 64), (106, 49), (130, 62),
            (155, 58), (196, 47), (240, 65), (240, 84), (0, 84)], '#345952')
    s.line([(0, 72), (52, 72), (62, 66), (74, 73), (91, 73), (101, 53),
            (107, 79), (114, 61), (121, 72), (240, 72)], '#f2d29c', 2)
    return s


def south_africa():
    s = Scene((240, 84), '#405b48', 80)
    s.oval((53, -20, 155, 82), '#ceac70')
    s.poly([(0, 63), (45, 54), (71, 62), (99, 54), (126, 63), (162, 47),
            (194, 53), (214, 46), (240, 51), (240, 84), (0, 84)], '#2e493c')
    # A lectern and microphone evoke public service without inventing a portrait.
    s.poly([(77, 47), (121, 47), (116, 78), (83, 78)], '#9f8966')
    s.box((75, 45, 123, 50), '#e4ca91')
    s.line([(101, 44), (101, 31), (114, 26)], '#22362e', 2)
    s.oval((109, 23, 120, 28), '#22362e')
    s.line([(150, 70), (149, 21)], '#d5bc82', 2)
    s.poly([(150, 24), (202, 27), (202, 48), (150, 44)], '#1f344e')
    s.poly([(150, 24), (202, 27), (202, 36), (169, 34)], '#b95c47')
    s.line([(151, 25), (173, 35), (201, 37)], '#eee0bc', 3)
    s.line([(151, 44), (173, 35), (201, 37)], '#eee0bc', 3)
    s.line([(151, 25), (173, 35), (201, 37)], '#6e9567', 2)
    s.line([(151, 44), (173, 35), (201, 37)], '#6e9567', 2)
    return s


def shenzhen():
    s = Scene((240, 84), '#623f47', 68)
    s.oval((80, -30, 160, 50), '#be856b')
    s.sky('#b98374', 52)
    s.oval((60, 53, 180, 84), '#dbb784')
    s.oval((70, 57, 170, 77), '#a46659')
    for x, coat, facing in [(55, '#223852', 1), (186, '#3a4f50', -1)]:
        s.oval((x - 10, 19, x + 11, 40), '#e1ac82')
        s.arc((x - 11, 18, x + 12, 38), 180, 330, '#273040', 4)
        s.poly([(x - 16, 43), (x, 41), (x + 16, 43), (x + 26, 72),
                (x - 23, 74)], coat)
        s.poly([(x - 6, 43), (x, 56), (x + 7, 43)], '#f1d1aa')
        s.line([(x + facing * 10, 56), (x + facing * 39, 61)], coat, 6)
        s.oval((x + facing * 39 - 4, 58, x + facing * 39 + 4, 64), '#e1ac82')
    s.box((111, 41, 113, 65), '#f2dcb1')
    s.box((128, 41, 130, 65), '#f2dcb1')
    s.poly([(112, 43), (97, 44), (97, 52), (112, 51)], '#3a557b')
    s.poly([(129, 43), (144, 44), (144, 52), (129, 51)], '#b94d40')
    return s
