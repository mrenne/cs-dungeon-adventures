"""Drawing toolkit shared by every booklet: text helpers, icons, map, tracker, legend, panels.

Everything is black and white for photocopying.
"""
import math

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from .grid import COLS, SIZE, tokens

W, H = letter
M = 40
CELL = 40
SANS, BOLD, MONO = "Helvetica", "Helvetica-Bold", "Courier-Bold"


# ---------- text helpers ----------
def para(c, text, x, y_top, width, size=9.5, leading=None, font=SANS, align=0):
    style = ParagraphStyle("p", fontName=font, fontSize=size, leading=leading or size * 1.28, alignment=align)
    p = Paragraph(text, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return h


def label(c, text, x, y, size=9, font=BOLD, gray=0):
    c.setFillGray(gray)
    c.setFont(font, size)
    c.drawString(x, y, text)
    c.setFillGray(0)


def centred(c, text, x, y, size, font=BOLD, gray=0):
    c.setFillGray(gray)
    c.setFont(font, size)
    c.drawCentredString(x, y - size * 0.35, text)
    c.setFillGray(0)


def blank(c, x, y, w):
    c.setLineWidth(0.8)
    c.line(x, y, x + w, y)


def box(c, x, y, s=12):
    c.setLineWidth(0.9)
    c.rect(x, y, s, s, fill=0, stroke=1)


def arrow(c, cx, cy, s, d):
    dx, dy = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}[d]
    px, py = -dy, dx
    x1, y1 = cx + dx * s / 2, cy + dy * s / 2
    c.saveState()
    c.setLineWidth(s * 0.14)
    c.line(cx - dx * s / 2, cy - dy * s / 2, x1 - dx * s * 0.3, y1 - dy * s * 0.3)
    p = c.beginPath()
    p.moveTo(x1, y1)
    p.lineTo(x1 - dx * s * 0.45 + px * s * 0.3, y1 - dy * s * 0.45 + py * s * 0.3)
    p.lineTo(x1 - dx * s * 0.45 - px * s * 0.3, y1 - dy * s * 0.45 - py * s * 0.3)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def panel(c, x, y_top, w, h, title):
    c.setLineWidth(1.2)
    c.roundRect(x, y_top - h, w, h, 6, fill=0, stroke=1)
    tw = c.stringWidth(title, BOLD, 9) + 14
    c.setFillGray(0)
    c.roundRect(x + 10, y_top - 8, tw, 16, 4, fill=1, stroke=0)
    c.setFillGray(1)
    c.setFont(BOLD, 9)
    c.drawString(x + 17, y_top - 3.5, title)
    c.setFillGray(0)


LICENCE_LINE = "© 2026 Mike Renne · CC BY-NC-SA 4.0 · free to copy for classrooms"


def footer(c, game, text):
    c.setFont(SANS, 7.5)
    c.setFillGray(0.35)
    c.drawString(M, 26, game["title"].upper())
    c.drawRightString(W - M, 26, text)
    c.drawCentredString(W / 2, 26, LICENCE_LINE)
    c.setFillGray(0)


# ---------- generic icons ----------
def bug(c, cx, cy, s, text):
    rx, ry = s * 0.27, s * 0.2
    c.setLineWidth(1)
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            c.line(cx + sx * rx * 0.8, cy + k * ry * 0.5, cx + sx * (rx + s * 0.1), cy + k * ry * 0.9)
        c.line(cx + sx * rx * 0.3, cy + ry * 0.9, cx + sx * rx * 0.6, cy + ry + s * 0.1)
    c.setFillGray(1)
    c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, fill=1, stroke=1)
    centred(c, text, cx, cy, s * (0.24 if len(text) < 3 else 0.2))


def cylinder(c, cx, cy, s):
    w, eh = s * 0.5, s * 0.14
    x0, yb, yt = cx - w / 2, cy - s * 0.2, cy + s * 0.2
    c.setFillGray(1)
    c.rect(x0, yb, w, yt - yb, fill=1, stroke=0)
    c.ellipse(x0, yb - eh / 2, x0 + w, yb + eh / 2, fill=1, stroke=0)
    c.setLineWidth(1)
    c.ellipse(x0, yt - eh / 2, x0 + w, yt + eh / 2, fill=1, stroke=1)
    c.line(x0, yb, x0, yt)
    c.line(x0 + w, yb, x0 + w, yt)
    for y in (yb, cy):
        c.arc(x0, y - eh / 2, x0 + w, y + eh / 2, 180, 180)


def battery(c, cx, cy, s, text):
    w, h = s * 0.56, s * 0.34
    c.setLineWidth(1)
    c.setFillGray(1)
    c.rect(cx - w / 2 - s * 0.03, cy - h / 2, w, h, fill=1, stroke=1)
    c.setFillGray(0)
    c.rect(cx + w / 2 - s * 0.03, cy - s * 0.07, s * 0.06, s * 0.14, fill=1, stroke=0)
    centred(c, text, cx - s * 0.03, cy, s * 0.24)


def virus(c, cx, cy, s):
    c.setLineWidth(1)
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = cx + math.cos(a) * s * 0.3, cy + math.sin(a) * s * 0.3
        c.line(cx, cy, x1, y1)
        c.circle(x1, y1, s * 0.035, fill=1, stroke=0)
    c.circle(cx, cy, s * 0.15, fill=1, stroke=0)


def key_shape(c, cx, cy, s):
    c.setLineWidth(1.4)
    c.setFillGray(1)
    c.circle(cx - s * 0.18, cy, s * 0.09, fill=1, stroke=1)
    c.line(cx - s * 0.09, cy, cx + s * 0.26, cy)
    c.line(cx + s * 0.26, cy, cx + s * 0.26, cy - s * 0.1)
    c.line(cx + s * 0.15, cy, cx + s * 0.15, cy - s * 0.08)
    c.setFillGray(0)


def icon(c, t, x, y, s, floor=None):
    """Draw token t in the square with lower-left (x, y) and side s.
    Engine tokens are drawn here; anything else is passed to the floor's mechanic."""
    mech = floor["mech"] if floor else None
    cx, cy = x + s / 2, y + s / 2
    c.saveState()
    c.setStrokeGray(0)
    c.setFillGray(0)
    c.setLineWidth(1)
    if t == "##":
        c.setFillGray(0.33)
        c.rect(x, y, s, s, fill=1, stroke=0)
    elif t == "o.":
        c.circle(cx, cy, s * 0.09, fill=1, stroke=0)
    elif t == "ST":
        c.circle(cx, cy, s * 0.3, fill=1, stroke=0)
        c.setFillGray(1)
        c.setStrokeGray(1)
        for sx in (-1, 1):
            c.circle(cx + sx * s * 0.11, cy + s * 0.08, s * 0.04, fill=1, stroke=0)
        c.setLineWidth(1.4)
        c.arc(cx - s * 0.15, cy - s * 0.17, cx + s * 0.15, cy + s * 0.1, 200, 140)
    elif t == "EX":
        c.roundRect(x + s * 0.08, y + s * 0.24, s * 0.84, s * 0.52, s * 0.1, fill=1, stroke=0)
        centred(c, "RUN", cx, cy, s * 0.3, gray=1)
    elif t == "DB":
        cylinder(c, cx, cy, s)
    elif t[0] == "B":
        text = t[1] if t[1] == "?" or mech is None else mech.bug_text(t[1])
        bug(c, cx, cy, s, text)
    elif t[0] == "+":
        battery(c, cx, cy, s, t)
    elif t == "MW":
        virus(c, cx, cy, s)
    elif t == "FA":
        c.setFillGray(1)
        c.circle(cx, cy, s * 0.36, fill=1, stroke=1)
        c.circle(cx, cy, s * 0.3, fill=1, stroke=1)
        centred(c, "f( )", cx, cy, s * 0.21, MONO)
    elif mech is not None:
        mech.icon(c, t, x, y, s, floor)
    c.restoreState()


def floor_for(game, token):
    """The first floor whose map holds token, so its mechanic can draw it (used on the cover)."""
    return next((f for f in game["floors"] if token in tokens(f["grid"])), None)


# ---------- map, tracker, legend ----------
def draw_map(c, floor, x, y, cell=CELL):
    """x, y = lower-left corner of the grid."""
    g, mech = floor["grid"], floor["mech"]

    def background(t):
        return t == "##" or mech.is_background(t)

    size = cell * SIZE
    for r in range(SIZE):
        for col in range(SIZE):
            if background(g[r][col]):
                icon(c, g[r][col], x + col * cell, y + (SIZE - 1 - r) * cell, cell, floor)
    c.setStrokeGray(0.55)
    c.setLineWidth(0.5)
    for k in range(1, SIZE):
        c.line(x + k * cell, y, x + k * cell, y + size)
        c.line(x, y + k * cell, x + size, y + k * cell)
    c.setStrokeGray(0)
    for r in range(SIZE):
        for col in range(SIZE):
            t = g[r][col]
            if t != ".." and not background(t):
                icon(c, t, x + col * cell, y + (SIZE - 1 - r) * cell, cell, floor)
    c.setLineWidth(2.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    for k in range(SIZE):
        centred(c, COLS[k], x + (k + 0.5) * cell, y + size + 8, 9, gray=0.3)
        centred(c, str(k + 1), x - 9, y + (SIZE - 0.5 - k) * cell, 9, gray=0.3)


def tracker(c, x, y_top, w):
    cols = [62, 86, 149, 149, 86]
    heads = ["", "START", "+  GAINED", "–  LOST", "END"]
    row_h, head_h = 31, 14
    c.setLineWidth(1)
    cx = x
    for wd, hd in zip(cols, heads):
        if hd:
            centred(c, hd, cx + wd / 2, y_top - head_h / 2, 8)
        cx += wd
    for i, name in enumerate(("RAM", "DATA")):
        yt = y_top - head_h - i * row_h
        cx = x
        for j, wd in enumerate(cols):
            if j == 0:
                c.setFillGray(0)
                c.rect(cx, yt - row_h, wd, row_h, fill=1, stroke=1)
                centred(c, name, cx + wd / 2, yt - row_h / 2, 13, gray=1)
            else:
                c.rect(cx, yt - row_h, wd, row_h, fill=0, stroke=1)
            cx += wd
    c.setFont(SANS, 7.5)
    c.drawString(x, y_top - head_h - 2 * row_h - 10,
                 "END = START + gained – lost.   RAM cannot go above your Max RAM.   DATA cannot go below 0.   "
                 "END RAM of 0 or less = CRASH.")


LEGEND = {
    "ST": "<b>Start</b>",
    "EX": "<b>Exit.</b> Stop on it, next to it, or pass over it",
    "o.": "<b>Data:</b> +1 DATA",
    "DB": "<b>Database:</b> roll, gain that much DATA",
    "B2": "<b>Bug:</b> lose that much RAM",
    "B?": "<b>Mystery bug:</b> roll, lose that much RAM",
    "+2": "<b>Power-up:</b> gain that much RAM",
    "+?": "<b>Mystery power-up:</b> roll, gain that RAM",
    "MW": "<b>Malware:</b> STOP, even in a program. Roll, lose that DATA",
    "FA": "<b>Function:</b> jump to the other f( ) every time, keep going",
}


def legend(c, floor, x, y_top, w):
    present = tokens(floor["grid"])
    items = [(t, txt) for t, txt in LEGEND.items() if t != "FA" or "FA" in present]
    items += floor["mech"].legend(floor)
    label(c, "KEY", x, y_top - 8, 9)
    y = y_top - 16
    s = 22
    for t, txt in items:
        icon(c, t, x, y - s, s, floor)
        h = para(c, txt, x + s + 4, y - 1, w - s - 4, size=6.8, leading=7.8)
        y -= max(s, h) + 5.5
