"""Editorial drawings for the three leads and the justice feature."""

from math import sin, tau
from random import Random

from scenes import Scene


def kyiv():
    scene = Scene((320, 152), '#293c56', 93)
    for row, color in enumerate(('#2e415a', '#374b60', '#435669', '#50616d')):
        scene.box((0, 27 + row * 15, 320, 43 + row * 15), color)
    scene.oval((24, 15, 64, 55), '#e5b67a')
    for index in range(7):
        y = 41 + index * 2.5
        scene.line([(24 - index, y), (64 + index, y)], '#45566b')
    scene.sky('#697a86', 120)

    windows = Random(230)
    x = 0
    while x < 320:
        width = windows.randrange(6, 18)
        height = windows.randrange(10, 46)
        scene.box((x, 110 - height, x + width, 110), '#263548')
        scene.box((x + 1, 110 - height, x + 3, 110), '#485a66')
        for window in range(x + 4, x + width - 1, 4):
            for floor in range(115 - height, 108, 5):
                if windows.random() < 0.6:
                    scene.box((window, floor, window + 1.3, floor + 1.7), '#dca87a')
        x += width + 1
    for x, roof in ((33, 54), (248, 47), (290, 58)):
        scene.poly([(x - 5, roof + 11), (x, roof), (x + 5, roof + 11),
                    (x + 4, roof + 21), (x - 4, roof + 21)], '#253344')
        scene.line([(x, roof), (x, roof - 5)], '#253344')

    scene.box((0, 110, 320, 152), '#193c51')
    for _ in range(163):
        x, y = windows.randrange(320), windows.randrange(111, 152)
        tone = '#b78b65' if x < 83 and (x + y) % 4 == 0 else '#476473'
        end = min(x + windows.randrange(3, 22), 320)
        scene.line([(x, y), (end, y)], tone)

    for x in (59, 264):
        scene.poly([(x - 10, 99), (x + 9, 99), (x + 13, 133),
                    (x - 10, 134)], '#827d73')
        scene.line([(x - 9, 101), (x - 9, 131)], '#e3b988', 3)
        scene.line([(x + 13, 134), (x + 28, 134)], '#142d3e')
    ivory = '#ead2a1'
    ribs = [(x, 101 - 72 * sin(tau / 2 * (x - 37) / 247)) for x in range(37, 285, 4)]
    scene.line(ribs, '#152f42', 8)
    scene.line(ribs, ivory, 3)
    scene.line([(x, y + 7) for x, y in ribs], '#bf996e', 2)
    for index in range(3, len(ribs) - 5, 4):
        (x, upper), (next_x, lower) = ribs[index], ribs[index + 4]
        scene.line([(x, upper + 7), (x, 97)], '#ad967e')
        scene.line([(x, upper + 7), (next_x, lower + 7)], '#e2bb90')
    for x0, x1 in ((0, 196), (206, 320)):
        scene.box((x0, 97, x1, 106), '#172e3b')
        scene.line([(x0, 98), (x1, 98)], ivory, 2)
        scene.line([(x0, 103), (x1, 103)], '#997758')
        for x in range(x0 + 4, x1, 11):
            scene.line([(x, 93), (x, 97)], '#e2bb90')
    scene.poly([(192, 97), (198, 99), (196, 103), (200, 108), (194, 105)],
               '#b18765')
    for x, y in ((202, 111), (198, 116), (205, 107)):
        scene.box((x, y, x + 1.5, y + 1.5), '#cf9a6a')
    return scene


def climate():
    scene = Scene((320, 152), '#24524f', 134)
    for row in range(12):
        y = row * 13
        scene.box((0, y, 320, y + 13),
                  (31 + row * 4, 82 + row * 4, 77 + row * 3))
    scene.sky('#8ea890', 31, 300)
    sea, land, grid = '#8cb5a2', '#518575', '#6a9b89'
    scene.oval((11, 7, 145, 141), sea, '#d9d6ad', 2)
    scene.oval((27, 7, 129, 141), None, grid)
    scene.oval((53, 7, 102, 141), None, grid)
    for y, extent in ((31, 52), (48, 61), (73, 66), (96, 64), (121, 45)):
        scene.line([(78 - extent, y), (78 + extent, y)], grid)
    scene.poly([(28, 47), (42, 48), (48, 32), (64, 28), (69, 20),
                (96, 24), (106, 35), (89, 46), (75, 48), (64, 65),
                (54, 72), (50, 58), (34, 59)], land)
    scene.poly([(58, 76), (80, 80), (92, 90), (86, 108), (72, 129),
                (67, 109), (60, 97), (52, 91)], land)
    scene.poly([(109, 54), (139, 62), (143, 73), (131, 81),
                (116, 74), (102, 61)], land)
    scene.box((227, 119, 320, 152), '#53776b')
    for x, top in ((241, 71), (269, 55), (297, 42)):
        scene.poly([(x - 6, top), (x + 6, top), (x + 11, 144),
                    (x - 11, 144)], '#2a534c')
        scene.box((x - 5, top + 5, x + 5, top + 10), '#c78c61')
        scene.line([(x - 3, top + 16), (x - 5, 140)], '#628678')
    for x, y, radius in ((253, 58, 8), (267, 43, 10), (283, 33, 14),
                         (298, 27, 14), (314, 19, 18)):
        scene.oval((x - radius, y - radius / 2, x + radius, y + radius / 2), '#a1a68b')
    back = [(120, 30), (235, 51), (208, 143), (100, 118)]
    scene.poly([(x + 5, y + 6) for x, y in back], '#244943')
    scene.poly(back, '#b9b291')
    front = [(107, 39), (227, 54), (208, 122), (187, 140), (94, 121)]
    scene.poly(front, '#f8e4b9')
    scene.poly([(208, 122), (187, 140), (193, 121)], '#b5ad86')
    for row in range(6):
        x, y = 120 - 2 * row, 56 + 9 * row
        scene.line([(x, y), (x + 80 - 5 * (row % 3), y + 10)], '#8f8e73', 2)
    scene.line([(110, 91), (206, 74)], '#b84f40', 4)
    scene.line([(113, 98), (197, 83)], '#b84f40')
    scene.poly([(0, 138), (19, 131), (33, 110), (53, 102), (75, 125),
                (85, 147), (96, 152), (0, 152)], '#d6e2cb')
    scene.poly([(29, 117), (33, 110), (53, 102), (75, 125),
                (68, 140), (53, 127), (42, 133)], '#a2c0ae')
    return scene


def markets():
    scene = Scene((320, 152), '#372a39', 126)
    for y in range(13, 152, 16):
        scene.line([(0, y), (320, y)], '#603e50')
    for x in range(16, 320, 24):
        scene.line([(x, 0), (x, 152)], '#603e50')
    scene.oval((237, 8, 285, 56), '#aa605d')
    for y in range(32, 58, 4):
        scene.line([(231, y), (291, y)], '#734950')
    scene.sky('#8d595d', 225)
    towers = Random(225)
    x = 0
    while x < 320:
        width = towers.randrange(9, 26)
        top = towers.randrange(73, 121)
        scene.box((x, top, x + width, 152), '#293144')
        scene.poly([(x + width - 5, top), (x + width + 2, top + 5),
                    (x + width + 2, 152), (x + width - 5, 152)], '#232638')
        for y in range(top + 6, 149, 6):
            for pane in range(x + 3, x + width - 5, 4):
                if (pane * y) % 8 < 3:
                    scene.box((pane, y, pane + 1.5, y + 1), '#c58b76')
        x += width + 3
    scene.poly([(199, 147), (209, 127), (212, 73), (218, 51), (224, 78),
                (228, 125), (240, 147)], '#d1aa85')
    scene.line([(218, 51), (218, 34)], '#e3bf97', 2)
    scene.box((209, 79, 226, 84), '#e6c49a')
    scene.line([(211, 90), (225, 102), (209, 115), (231, 125),
                (203, 138)], '#6b5260', 2)

    graph = [(14, 40), (44, 29), (73, 43), (101, 37), (135, 68),
             (159, 55), (190, 83), (222, 76), (250, 94), (292, 119)]
    drop = '#f08866'
    scene.line(graph, '#241b26', 9)
    scene.line(graph, drop, 5)
    scene.poly([(300, 124), (277, 124), (288, 105)], drop)
    for x, y in graph[1:-1:2]:
        scene.oval((x - 2, y - 2, x + 2, y + 2), '#f1b58d')
    return scene


def court():
    scene = Scene((354, 140), '#233b52', 123)
    scene.sky('#607483', 1945)
    for radius, color in ((78, '#a67750'), (69, '#c4925c'), (61, '#d7ac74')):
        scene.oval((277 - radius, 59 - radius, 277 + radius, 59 + radius), color)
    scene.arc((211, -6, 343, 126), 0, 360, '#e4c292', 1)

    stone, face, shadow = '#d4bd99', '#edd2a4', '#53616e'
    scene.poly([(10, 115), (15, 72), (29, 68), (48, 68), (48, 47),
                (60, 34), (60, 21), (67, 8), (74, 22), (74, 34), (86, 46),
                (86, 68), (110, 68), (124, 51), (142, 51), (162, 69),
                (190, 69), (201, 79), (205, 116)], stone)
    scene.poly([(47, 48), (67, 36), (85, 48), (78, 52), (51, 52)], face)
    scene.poly([(32, 88), (108, 58), (176, 88)], face)
    scene.poly([(48, 86), (108, 68), (158, 86)], '#a39983')
    scene.box((24, 89, 193, 116), stone)
    for x in (31, 49, 67, 85, 104, 123, 142, 161, 179):
        scene.box((x, 92, x + 9, 112), shadow)
        scene.line([(x + 1, 93), (x + 1, 111)], '#766f65')
    for x, rise in ((55, 56), (66, 51), (77, 56)):
        scene.box((x, rise, x + 4, 73), shadow)
    for y, inset in ((114, 17), (119, 12), (124, 7), (129, 2)):
        scene.line([(inset, y), (210 - inset, y)], face, 2)
        scene.line([(inset + 2, y + 2), (208 - inset, y + 2)], '#132c42')

    brass = '#f5e0aa'
    scene.line([(278, 37), (278, 110)], brass, 4)
    scene.oval((272, 28, 284, 40), brass)
    scene.line([(232, 51), (250, 44), (278, 42), (304, 44), (323, 51)],
               brass, 3)
    for x in (232, 323):
        scene.line([(x, 48), (x - 17, 80), (x + 17, 80), (x, 48)], brass, 2)
        scene.arc((x - 19, 70, x + 19, 93), 1, 179, brass, 3)
        scene.line([(x - 19, 80), (x + 19, 80)], brass, 2)
    scene.poly([(257, 116), (266, 107), (288, 107), (299, 116)], brass)
    scene.box((250, 118, 306, 122), brass)
    return scene
