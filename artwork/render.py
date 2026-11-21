"""Typeset the November 20 edition and export the competition's RGB PNG."""

from functools import lru_cache
import gzip
import json
from pathlib import Path
from random import Random
import sys

from PIL import Image, ImageDraw, ImageFont

import lead_scenes
import scenes

ROOT = Path(__file__).resolve().parent
SIZE = 1024
SCALE = 3
MARGIN = 34
RIGHT = SIZE - MARGIN

PAPER = '#f6efdf'
INK = '#14222b'
BODY = '#34413e'
RULE = '#b6ab94'
NAVY = '#29425b'
TEAL = '#29635a'
RED = '#973f3a'
GOLD = '#9c652f'
GREEN = '#416348'
PLUM = '#624252'
WHITE = '#fff7e7'

LEADS = (
    (1, 'EUROPE', 'KYIV, UKRAINE', NAVY, lead_scenes.kyiv, ('Russian strikes', 'hit Kyiv bridges'),
     ('A Russian missile and drone barrage', 'damaged three Dnipro crossings.')),
    (2, 'CLIMATE', 'ANTALYA, TÜRKİYE', TEAL, lead_scenes.climate, ('COP31 talks', 'go into overtime'),
     ('Countries debated a draft deal that', 'left out fossil fuels.')),
    (3, 'MARKETS', 'TOKYO, JAPAN', RED, lead_scenes.markets, ('AI sell-off', 'hits Asia'),
     ('Chip stocks fell across the region.', 'Japan’s Nikkei 225 closed down 5.06%.')),
)

SECONDARY = (
    (5, 'EUROPE', NAVY, scenes.brussels, ('EU and UK agree', 'youth scheme'),
     ('Brussels summit concludes', 'negotiations on youth stays.')),
    (6, 'SOUTH AMERICA', GOLD, scenes.peru, ('6.7 quake shakes', 'Peru’s Andes'),
     ('Peru’s seismic agency located', 'the epicentre in Junín.')),
    (7, 'SOUTH AFRICA', GREEN, scenes.south_africa, ('Phumzile', 'Mlambo-Ngcuka dies'),
     ('The former deputy president', 'and UN Women chief was 71.')),
    (8, 'ASIA–PACIFIC', PLUM, scenes.shenzhen, ('Xi meets Albanese', 'in Shenzhen'),
     ('China and Australia held talks', 'on trade and bilateral ties.')),
)

MARKERS = (
    (1, 'Kyiv', 30.52, 50.45, 16, -16, NAVY),
    (2, 'Antalya', 30.71, 36.90, 20, 1, TEAL),
    (3, 'Tokyo', 139.69, 35.69, 12, -7, RED),
    (4, 'Naypyidaw', 96.13, 19.75, 15, 15, NAVY),
    (5, 'Brussels', 4.35, 50.85, -11, -14, NAVY),
    (6, 'Junín', -76.19, -10.97, -19, 10, GOLD),
    (7, 'Pretoria', 28.19, -25.75, 21, 8, GREEN),
    (8, 'Shenzhen', 114.06, 22.54, 7, -17, PLUM),
    (9, 'Nuseirat', 34.39, 31.45, -7, 19, RED),
    (10, 'Port-au-Prince', -72.34, 18.54, -14, -9, TEAL),
)


@lru_cache(maxsize=None)
def face(style, size):
    files = {'serif': 'CormorantGaramond.ttf', 'bold': 'BarlowSemiCondensed-Bold.ttf',
             'body': 'BarlowSemiCondensed-SemiBold.ttf'}
    font = ImageFont.truetype(ROOT / 'fonts' / files[style], round(size * SCALE))
    if style == 'serif':
        font.set_variation_by_axes([680])
    return font


def scaled(coords):
    return tuple(round(item * SCALE) for item in coords)


class FrontPage:
    def __init__(self):
        self.image = Image.new('RGB', (SIZE * SCALE, SIZE * SCALE), PAPER)
        self.pen = ImageDraw.Draw(self.image)

    def box(self, xy, fill):
        self.pen.rectangle(scaled(xy), fill=fill)

    def rule(self, points, fill=RULE, width=1):
        self.pen.line([scaled(point) for point in points], fill=fill, width=max(1, round(width * SCALE)))

    def hline(self, y, x1=MARGIN, x2=RIGHT, color=RULE, width=1):
        self.rule([(x1, y), (x2, y)], color, width)

    def vline(self, x, y1, y2, color=RULE, width=1):
        self.rule([(x, y1), (x, y2)], color, width)

    def label(self, txt, x, y, size, style='body', color=INK, align='l'):
        self.pen.text(scaled((x, y)), txt, font=face(style, size), fill=color,
                      anchor=align + 's', features=['lnum'])

    def fitted_label(self, txt, x, y, width, size, style='serif', color=INK, align='l'):
        while self.pen.textlength(txt, font=face(style, size), features=['lnum']) > width * SCALE:
            size -= 0.5
            if size < 12:
                raise ValueError(f'Line exceeds editorial column width: {txt}')
        self.label(txt, x, y, size, style, color, align)

    def lines(self, text, x, y, width, size, leading, style, color=INK):
        for index, line in enumerate(text):
            self.fitted_label(line, x, y + leading * index, width, size, style, color)

    def picture(self, factory, x, y, width, height):
        # Crop within the illustration box and keep the figures' proportions.
        image = factory().printed()
        fit = max(width * SCALE / image.width, height * SCALE / image.height)
        resized = image.resize((round(image.width * fit), round(image.height * fit)), Image.Resampling.LANCZOS)
        left = (resized.width - width * SCALE) // 2
        top = (resized.height - height * SCALE) // 2
        self.image.paste(resized.crop((left, top, left + width * SCALE, top + height * SCALE)), scaled((x, y)))

    def marker(self, x, y, number, color, radius=9):
        self.pen.ellipse(scaled((x - radius, y - radius, x + radius, y + radius)), fill=color)
        self.label(str(number), x, y + 4.1, 12, 'bold', WHITE, 'm')

    def masthead(self):
        self.hline(22, MARGIN, 345, NAVY, 1)
        self.hline(22, 679, RIGHT, NAVY, 1)
        self.label('T H E   W O R L D   I N   O N E   P A G E', 512, 27, 18, 'bold', RED, 'm')
        self.fitted_label('FRIDAY 20 NOVEMBER 2026', 512, 89, RIGHT - MARGIN, 81,
                          color=INK, align='m')
        self.hline(101, color=NAVY, width=1.4)
        self.label('KYIV BRIDGES HIT  /  COP31 OVERTIME  /  ASIAN MARKETS SLIDE  /  MYANMAR DISPUTES ICJ RULING',
                   512, 122, 16.5, 'bold', NAVY, 'm')

    def figures(self):
        items = (
            ('3', 'KYIV BRIDGES DAMAGED', NAVY),
            ('−5.06%', 'NIKKEI 225 AT CLOSE', RED),
            ('6.7', 'JUNÍN QUAKE MAGNITUDE', GOLD),
            ('100,000', 'EU–UK YOUTH SCHEME PLACES', TEAL),
        )
        self.box((MARGIN, 134, RIGHT, 193), '#eee4d0')
        self.hline(134, color=RULE, width=0.8)
        self.hline(193, color=RULE, width=0.8)
        cell = (RIGHT - MARGIN) / len(items)
        for index, (value, caption, color) in enumerate(items):
            left = MARGIN + index * cell
            if index:
                self.vline(left, 144, 183, RULE)
            self.label(value, left + cell / 2, 166, 37, 'serif', color, 'm')
            self.label(caption, left + cell / 2, 185, 13.75, 'bold', INK, 'm')

    def leads(self):
        width, gap = 308, 16
        for index, (number, beat, place, color, picture, headline, caption) in enumerate(LEADS):
            x = MARGIN + index * (width + gap)
            self.box((x, 204, x + width, 226), color)
            self.label(f'{number:02}  {beat}', x + 9, 220, 15, 'bold', WHITE)
            self.label(place, x + width - 9, 220, 14, 'body', WHITE, 'r')
            self.picture(picture, x, 231, width, 139)
            self.lines(headline, x, 401, width, 36, 31, 'serif')
            self.lines(caption, x, 454, width, 17.5, 19, 'body', BODY)
            if index < len(LEADS) - 1:
                self.vline(x + width + gap / 2, 231, 474, RULE, 0.8)

    def justice(self):
        self.box((MARGIN, 487, RIGHT, 626), '#e9e2cd')
        self.picture(lead_scenes.court, MARGIN, 487, 350, 139)
        self.box((384, 487, 389, 626), '#c29157')
        self.label('04  GLOBAL JUSTICE   /   THE HAGUE & MYANMAR', 406, 511, 16, 'bold', NAVY)
        self.fitted_label('Myanmar disputes ICJ ruling', 406, 548, 570, 43)
        self.lines(('Myanmar’s foreign ministry disputed the genocide finding on Friday.',
                    'On Nov. 19 the ICJ ruled that Myanmar committed genocide against',
                    'the Rohingya in 2017.'), 406, 574, 570, 18, 19, 'body', BODY)

    def round_up(self):
        self.section('AROUND THE WORLD', MARGIN, 649, RIGHT, NAVY)
        width, gap = 229, 13
        for index, (number, beat, color, picture, headline, caption) in enumerate(SECONDARY):
            x = MARGIN + index * (width + gap)
            self.hline(658, x, x + width, color, 2)
            self.label(f'{number:02}  {beat}', x, 673, 13.75, 'bold', color)
            self.picture(picture, x, 680, width, 68)
            self.lines(headline, x, 772, width, 25.5, 21, 'serif')
            self.lines(caption, x, 811, width, 15, 15.5, 'body', BODY)
            if index < len(SECONDARY) - 1:
                self.vline(x + width + gap / 2, 658, 826, RULE, 0.75)

    def section(self, title, x, y, right, color):
        self.label(title, x, y, 17, 'bold', color)
        title_width = self.pen.textlength(title, font=face('bold', 17)) / SCALE
        self.hline(y - 4, x + title_width + 11, right, color, 1.2)

    def short_reads(self):
        self.section('IN BRIEF', 497, 854, 748, NAVY)
        self.label('09  CENTRAL GAZA', 497, 875, 14, 'bold', RED)
        self.lines(('Israeli strikes hit Nuseirat,', 'Deir al-Balah and Bureij.'),
                   497, 893, 249, 16, 17, 'body', BODY)
        self.hline(922, 497, 748, RULE, 0.7)
        self.label('10  HAITI', 497, 940, 14, 'bold', TEAL)
        self.lines(('Haiti announced an El Salvador', 'deal to build new prisons.'),
                   497, 958, 249, 16, 17, 'body', BODY)

    def context(self):
        self.box((768, 862, RIGHT, 993), '#eae5d3')
        self.section('DAY IN NUMBERS', 768, 854, RIGHT, NAVY)
        self.label('129 km', 783, 894, 32, 'serif', GOLD)
        self.label('Depth of the Junín quake', 783, 911, 15, 'body', BODY)
        self.hline(921, 782, RIGHT - 14, RULE, 0.7)
        self.label('Up to 3 years', 783, 955, 31, 'serif', TEAL)
        self.label('EU–UK youth scheme stays', 783, 974, 15, 'body', BODY)

    def world_map(self):
        self.section('THE DAY ON THE MAP', MARGIN, 854, 475, NAVY)
        left, top, width, height = 34, 859, 322, 132

        def project(lon, lat):
            return left + (lon + 180) / 360 * width, top + (81 - lat) / 140 * height

        self.box((left, top, left + width, top + height), '#eee7d8')
        for lon in range(-150, 180, 30):
            x, _ = project(lon, 0)
            self.vline(x, top, top + height, '#ddd4bf', 0.6)
        for lat in (-40, -20, 0, 20, 40, 60):
            _, y = project(0, lat)
            self.hline(y, left, left + width, '#ddd4bf', 0.6)
        with gzip.open(ROOT / 'land.geojson.gz', 'rt', encoding='utf-8') as source:
            land = json.load(source)
        for feature in land['features']:
            outline, *holes = feature['geometry']['coordinates']
            if max(lat for _, lat in outline) < -59:
                continue
            points = [scaled(project(lon, min(81, max(-59, lat)))) for lon, lat in outline]
            self.pen.polygon(points, fill='#b1b7a4', outline='#818d7d')
            for hole in holes:
                points = [scaled(project(lon, lat)) for lon, lat in hole]
                self.pen.polygon(points, fill='#eee7d8')
        for number, _, lon, lat, dx, dy, color in MARKERS:
            x, y = project(lon, lat)
            self.rule([(x, y), (x + dx, y + dy)], '#51594e', 0.8)
            self.pen.ellipse(scaled((x - 1.6, y - 1.6, x + 1.6, y + 1.6)), fill=INK)
            self.marker(x + dx, y + dy, number, color, 7.5)
        for index, (number, place, *_, color) in enumerate(MARKERS):
            y = 870 + index * 13.4
            self.label(f'{number:02}', 368, y, 12.5, 'bold', color)
            self.fitted_label(place, 389, y, 86, 13, 'body', BODY)

    def export(self, filename):
        self.masthead()
        self.figures()
        self.leads()
        self.justice()
        self.round_up()
        self.hline(836, color=NAVY, width=1.4)
        self.world_map()
        self.vline(485, 853, 994, RULE, 0.8)
        self.short_reads()
        self.context()
        self.hline(1003, color=NAVY, width=1.3)
        self.hline(1007, color=RULE, width=0.7)

        output = self.image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        output.save(filename, 'PNG', optimize=True)


if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / 'assets' / 'world-in-one-page.png'
    FrontPage().export(target)
