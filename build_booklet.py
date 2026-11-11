"""Builds the printable black-and-white Computer Science Crawler booklet (US Letter)."""
import math

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from floors import BOTS, COLS, FLOORS, FORCE_COST, SIZE, coord, encode, expand, scan

W, H = letter
M = 40
CELL = 40
SANS, BOLD, MONO = "Helvetica", "Helvetica-Bold", "Courier-Bold"
CODE_LABEL = {"A1": "x+1", "A3": "x+3", "X2": "x×2", "Z0": "x=0", "I1": "IF 1", "I2": "IF 2"}
KEY_LETTER = {"1": "A", "2": "B"}
STEP = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


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


def draw_program(c, x, y, program, size=11):
    for step in program:
        if isinstance(step, tuple):
            txt = f"REPEAT {step[1]} ["
            c.setFont(MONO, size)
            c.drawString(x, y, txt)
            x += c.stringWidth(txt, MONO, size) + size * 0.4
            x = draw_program(c, x, y, step[2], size)
            c.setFont(MONO, size)
            c.drawString(x, y, "]")
            x += size * 1.0
        else:
            arrow(c, x + size * 0.5, y + size * 0.35, size, step)
            x += size * 1.4
    return x


# ---------- icons ----------
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


def bot(c, cx, cy, s, square, antenna, smiling):
    by, r = cy - s * 0.06, s * 0.23
    c.setLineWidth(1.3)
    if antenna:
        for sx in (-1, 1):
            c.line(cx + sx * r * 0.4, by + r * 0.9, cx + sx * r * 0.8, by + r + s * 0.14)
            c.circle(cx + sx * r * 0.8, by + r + s * 0.14, s * 0.04, fill=1, stroke=0)
    c.setFillGray(1)
    if square:
        c.rect(cx - r, by - r, 2 * r, 2 * r, fill=1, stroke=1)
    else:
        c.circle(cx, by, r * 1.08, fill=1, stroke=1)
    c.setFillGray(0)
    for sx in (-1, 1):
        c.circle(cx + sx * r * 0.42, by + r * 0.3, s * 0.035, fill=1, stroke=0)
    c.setLineWidth(1.1)
    mw, my = r * 0.62, by - r * 0.42
    if smiling:
        c.arc(cx - mw, my - r * 0.2, cx + mw, my + r * 0.5, 200, 140)
    else:
        c.arc(cx - mw, my - r * 0.45, cx + mw, my + r * 0.25, 20, 140)


def icon(c, t, x, y, s, fnum=0):
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
        text = t[1] if t[1] == "?" or fnum != 3 else bin(int(t[1]))[2:]
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
    elif t[0] == "P":
        c.setLineWidth(2)
        c.setFillGray(1)
        c.rect(x + s * 0.14, y + s * 0.14, s * 0.72, s * 0.72, fill=1, stroke=1)
        centred(c, t, cx, cy, s * 0.3)
    elif t in CODE_LABEL:
        c.setFillGray(0.88)
        c.roundRect(x + s * 0.06, y + s * 0.2, s * 0.88, s * 0.6, s * 0.12, fill=1, stroke=1)
        centred(c, CODE_LABEL[t], cx, cy, s * 0.24, MONO)
    elif t[0] == "C":
        w, h = s * 0.68, s * 0.42
        c.setFillGray(1)
        c.rect(cx - w / 2, cy - h / 2 - s * 0.06, w, h, fill=1, stroke=1)
        c.arc(cx - w / 2, cy + h / 2 - s * 0.06 - s * 0.14, cx + w / 2, cy + h / 2 - s * 0.06 + s * 0.14, 0, 180)
        centred(c, format(int(t[1]), "03b"), cx, cy - s * 0.06, s * 0.23, MONO)
    elif t[0] == "K" and fnum == 3:
        key_shape(c, cx, cy + s * 0.14, s)
        centred(c, t[1], cx, cy - s * 0.2, s * 0.3)
    elif t[0] == "K":
        key_shape(c, cx, cy + s * 0.2, s)
        centred(c, f"KEY {KEY_LETTER[t[1]]}", cx, cy - s * 0.08, s * 0.19)
        centred(c, f"shift {FLOORS[3]['cipher'][t[1]][0]}", cx, cy - s * 0.3, s * 0.18, SANS)
    elif t[0] == "L":
        c.setFillGray(0.33)
        c.rect(x, y, s, s, fill=1, stroke=0)
        c.setFillGray(1)
        c.setLineWidth(1.6)
        c.arc(cx - s * 0.14, cy, cx + s * 0.14, cy + s * 0.4, 0, 180)
        c.setStrokeGray(1)
        c.arc(cx - s * 0.14, cy, cx + s * 0.14, cy + s * 0.4, 0, 180)
        c.setStrokeGray(0)
        c.rect(cx - s * 0.36, cy - s * 0.34, s * 0.72, s * 0.5, fill=1, stroke=1)
        centred(c, format(int(t[1]), "03b"), cx, cy - s * 0.09, s * 0.24, MONO)
    elif t[0] == "W":
        c.setFillGray(0.8)
        c.rect(x, y, s, s, fill=1, stroke=0)
        c.setLineWidth(0.6)
        for k in range(1, 4):
            c.line(x, y + k * s / 4, x + s, y + k * s / 4)
        for k in range(4):
            off = s / 4 if k % 2 else 0
            for vx in (x + s / 4 + off, x + 3 * s / 4 + off):
                if vx < x + s:
                    c.line(vx, y + k * s / 4, vx, y + (k + 1) * s / 4)
        c.setFillGray(1)
        c.setLineWidth(1.2)
        c.circle(cx, cy, s * 0.27, fill=1, stroke=1)
        centred(c, KEY_LETTER[t[1]], cx, cy, s * 0.34)
    elif t[0] == "M":
        bot(c, cx, cy, s, *BOTS[t])
    c.restoreState()


# ---------- shared page pieces ----------
def footer(c, text):
    c.setFont(SANS, 7.5)
    c.setFillGray(0.35)
    c.drawString(M, 26, "COMPUTER SCIENCE CRAWLER")
    c.drawRightString(W - M, 26, text)
    c.setFillGray(0)


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


def draw_map(c, floor, x, y, cell=CELL):
    """x, y = lower-left corner of the grid."""
    g = floor["grid"]
    size = cell * SIZE
    for r in range(SIZE):
        for col in range(SIZE):
            if g[r][col] in ("##",) or g[r][col][0] in "LW":
                icon(c, g[r][col], x + col * cell, y + (SIZE - 1 - r) * cell, cell, floor["num"])
    c.setStrokeGray(0.55)
    c.setLineWidth(0.5)
    for k in range(1, SIZE):
        c.line(x + k * cell, y, x + k * cell, y + size)
        c.line(x, y + k * cell, x + size, y + k * cell)
    c.setStrokeGray(0)
    for r in range(SIZE):
        for col in range(SIZE):
            t = g[r][col]
            if t not in ("##", "..") and t[0] not in "LW":
                icon(c, t, x + col * cell, y + (SIZE - 1 - r) * cell, cell, floor["num"])
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
    "MW": "<b>Malware:</b> STOP. Roll, lose that DATA",
    "FA": "<b>Function:</b> jump to the other f( ), keep going",
    "P1": "<b>Program:</b> stop and run it",
    "A1": "<b>Code:</b> change x",
    "I1": "<b>IF:</b> check x, do what it says",
    "C5": "<b>Bit chest:</b> gain DATA (binary)",
    "K5": "<b>Key</b> for a door",
    "L5": "<b>Door:</b> a wall until you hold its key",
    "K1": "<b>Cipher key</b>",
    "W1": f"<b>Firewall:</b> free with key + password. No key: –{FORCE_COST} RAM",
    "Ma": "<b>Bot:</b> sort it with the AI's tree",
}
FLOOR_LEGEND = {
    1: ["P1"], 2: ["A1", "I1"], 3: ["C5", "K5", "L5"], 4: ["K1", "W1"], 5: ["Ma"],
}


def legend(c, floor, x, y_top, w):
    tokens = {t for row in floor["grid"] for t in row}
    items = ["ST", "EX", "o.", "DB", "B2", "B?", "+2", "+?", "MW", "FA"] + FLOOR_LEGEND[floor["num"]]
    if "FA" not in tokens:
        items.remove("FA")
    label(c, "KEY", x, y_top - 8, 9)
    y = y_top - 16
    s = 22
    for t in items:
        icon(c, t, x, y - s, s, floor["num"])
        h = para(c, LEGEND[t], x + s + 4, y - 1, w - s - 4, size=6.8, leading=7.8)
        y -= max(s, h) + 5.5


# ---------- floor rule panels ----------
def program_end(floor, name):
    g = floor["grid"]
    pos = next((r, col) for r in range(SIZE) for col in range(SIZE) if g[r][col] == name)
    for d in expand(floor["programs"][name]):
        pos = (pos[0] + STEP[d][0], pos[1] + STEP[d][1])
        assert 0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE and g[pos[0]][pos[1]] != "##", name
    return coord(*pos)


def rule_f1(c, x, yt, w, h):
    panel(c, x, yt, w, h, "FLOOR RULE: PROGRAM SQUARES")
    para(c, "A program is a list of steps. Step on a program square (<b>P1</b>, <b>P2</b>, <b>P3</b>) and your "
            "move stops. Now <b>run the program</b>: move one square for each arrow, in order.<br/><br/>"
            "<b>REPEAT 2 [ ... ]</b> is a loop. Do the steps inside the brackets 2 times.<br/><br/>"
            "Use everything you cross. You stop where the program ends. Each program runs once, "
            "then cross it out.", x + 12, yt - 18, 250)
    px = x + 285
    label(c, "THE PROGRAMS", px, yt - 26, 8.5)
    for i, (name, prog) in enumerate(FLOORS[0]["programs"].items()):
        y = yt - 52 - i * 34
        label(c, name, px, y, 12)
        draw_program(c, px + 28, y, prog, 12)
        label(c, "I ended on square:", px + 28, y - 14, 7.5, SANS)
        blank(c, px + 100, y - 15, 40)


def rule_f2(c, x, yt, w, h):
    panel(c, x, yt, w, h, "FLOOR RULE: THE VARIABLE x")
    para(c, "A <b>variable</b> is a box that holds a value. Yours is called <b>x</b> and it starts at <b>1</b>."
            "<br/><br/>Cross a code square: change x, cross out the old value and write the new one in the "
            "next box. Careful: <b>x=0</b> is a bug that wipes your variable!<br/><br/>"
            "When you leave the floor: <b>gain x DATA</b>.", x + 12, yt - 18, 235)
    px = x + 268
    label(c, "x", px, yt - 40, 20, MONO)
    label(c, "=", px + 16, yt - 40, 16, MONO)
    for k in range(7):
        bx = px + 36 + k * 30
        c.setLineWidth(1.2 if k == 0 else 0.8)
        c.rect(bx, yt - 48, 26, 26, fill=0, stroke=1)
        if k == 0:
            centred(c, "1", bx + 13, yt - 35, 14)
    c.setFont(MONO, 9.5)
    lines = [
        ("IF 1", "IF x > 3:      +3 RAM", "ELSE:          –2 RAM"),
        ("IF 2", "IF x is even:  +4 DATA", "ELSE:          –1 RAM"),
    ]
    for i, (name, a, b) in enumerate(lines):
        y = yt - 74 - i * 36
        c.setFillGray(0.88)
        c.roundRect(px, y - 14, 40, 22, 4, fill=1, stroke=1)
        centred(c, name, px + 20, y - 3, 9.5, MONO)
        c.setFont(MONO, 9.5)
        c.drawString(px + 50, y, a)
        c.drawString(px + 50, y - 12, b)


def rule_f3(c, x, yt, w, h):
    panel(c, x, yt, w, h, "FLOOR RULE: EVERYTHING IS BINARY")
    para(c, "Computers store every number using only <b>1</b> and <b>0</b>. On this floor, bug strength and "
            "chest values are in <b>binary</b>.<br/><br/>Each place is worth 8, 4, 2 or 1. Add up the places "
            "that hold a 1.<br/><br/>A door shows a binary number. It opens only if you hold the key with the "
            "same number.", x + 12, yt - 18, 205)
    px = x + 232
    label(c, "EXAMPLE", px, yt - 26, 8)
    for k, (pv, bit) in enumerate(zip("8421", "0101")):
        bx = px + k * 24
        centred(c, pv, bx + 11, yt - 38, 8, SANS, gray=0.3)
        c.setLineWidth(0.8)
        c.rect(bx, yt - 66, 22, 22, fill=0, stroke=1)
        centred(c, bit, bx + 11, yt - 55, 13, MONO)
    label(c, "= 4 + 1 = 5", px + 102, yt - 59, 10, SANS)
    label(c, "MY CONVERSIONS  (binary = number)", px, yt - 86, 8)
    for k in range(9):
        bx, by = px + (k % 3) * 58, yt - 104 - (k // 3) * 18
        blank(c, bx, by, 22)
        label(c, "=", bx + 26, by + 1, 9, SANS)
        blank(c, bx + 36, by, 16)
    lx = x + w - 122
    label(c, "ROLL LOG", lx, yt - 26, 8)
    para(c, "Tally every roll you make.", lx, yt - 30, 112, size=7.5)
    for k in range(6):
        by = yt - 52 - k * 12
        c.setLineWidth(0.6)
        c.rect(lx, by, 16, 12, fill=0, stroke=1)
        c.rect(lx + 16, by, 94, 12, fill=0, stroke=1)
        centred(c, str(k + 1), lx + 8, by + 6, 8)
    para(c, "Most common roll: ____<br/>Total rolls: ____<br/><b>Log complete: +2 DATA</b>",
         lx, yt - 115, 114, size=7.5, leading=9.5)


def rule_f4(c, x, yt, w, h):
    cipher = FLOORS[3]["cipher"]
    panel(c, x, yt, w, h, "FLOOR RULE: SECRET CODES")
    para(c, "Each firewall is locked with a scrambled password. A <b>key</b> tells you how many letters to "
            "shift <b>back</b> along the alphabet to unscramble it. Example: with shift 2, <b>D C V</b> "
            "becomes <b>B A T</b>.", x + 12, yt - 15, w - 24)
    ax, ay = x + 12, yt - 46
    cw = (w - 24) / 26
    for k in range(26):
        c.setLineWidth(0.6)
        c.rect(ax + k * cw, ay - 15, cw, 15, fill=0, stroke=1)
        centred(c, chr(65 + k), ax + (k + 0.5) * cw, ay - 7.5, 9.5, MONO)
    y = ay - 32
    for kid, (shift, word) in cipher.items():
        letter_ = KEY_LETTER[kid]
        label(c, f"Firewall {letter_}:", x + 12, y, 10)
        label(c, "  ".join(encode(word, shift)), x + 84, y, 12, MONO)
        label(c, "shift:", x + 190, y, 9, SANS)
        blank(c, x + 218, y - 1, 22)
        label(c, "password:", x + 258, y, 9, SANS)
        for k in range(len(word)):
            blank(c, x + 308 + k * 24, y - 1, 18)
        y -= 20
    para(c, f"<b>Holding the key?</b> Decode the password, write it here, and walk through free. "
            f"<b>No key?</b> You can smash through, but it costs <b>{FORCE_COST} RAM</b>. "
            f"Wrong password at code review: –3 DATA.", x + 12, y + 10, w - 24, size=8.5)


def rule_f5(c, x, yt, w, h):
    panel(c, x, yt, w, h, "FLOOR RULE: THE SORTING AI")
    para(c, "You found it: the site's old <b>sorting AI</b>, and you cannot overrule it. For every bot you "
            "meet, follow its tree and do what it says, <b>even if it seems wrong</b>.<br/><br/>"
            "The truth: <b>smiling</b> bots are friendly, <b>frowning</b> bots are hostile. Its builders "
            "trained it on body shape and antennas only. It never learned to look at faces.",
         x + 12, yt - 16, 208, size=8.5, leading=10.5)
    y = yt - 112
    label(c, "Friendly bots the AI hurt: ____", x + 12, y, 8.5, SANS)
    label(c, "Hostile bots the AI trusted: ____", x + 12, y - 14, 8.5, SANS)
    label(c, "A better question for the tree:", x + 12, y - 28, 8.5, SANS)
    blank(c, x + 132, y - 29, 85)

    def node(cx, cy, text, wd=74, filled=False):
        c.setLineWidth(1)
        c.setFillGray(0 if filled else 1)
        c.roundRect(cx - wd / 2, cy - 9, wd, 18, 4, fill=1, stroke=1)
        centred(c, text, cx, cy, 8, gray=1 if filled else 0)

    def leaf(cx, cy, name, effect):
        c.setLineWidth(1)
        c.setFillGray(0.9)
        c.rect(cx - 33, cy - 15, 66, 30, fill=1, stroke=1)
        centred(c, name, cx, cy + 6, 8)
        centred(c, effect, cx, cy - 6, 8, SANS)

    tx = x + 232
    root = (tx + 150, yt - 28)
    mids = [(tx + 76, yt - 72), (tx + 224, yt - 72)]
    leaves = [(tx + 36, yt - 122), (tx + 112, yt - 122), (tx + 188, yt - 122), (tx + 264, yt - 122)]
    c.setLineWidth(1)
    for m in mids:
        c.line(root[0], root[1] - 9, m[0], m[1] + 9)
    for i, lf in enumerate(leaves):
        m = mids[i // 2]
        c.line(m[0], m[1] - 9, lf[0], lf[1] + 15)
        centred(c, "YES" if i % 2 == 0 else "NO", (m[0] + lf[0]) / 2 + (-11 if i % 2 == 0 else 11),
                (m[1] + lf[1]) / 2 + 4, 6.5)
    centred(c, "YES", (root[0] + mids[0][0]) / 2 - 12, (root[1] + mids[0][1]) / 2 + 3, 6.5)
    centred(c, "NO", (root[0] + mids[1][0]) / 2 + 12, (root[1] + mids[1][1]) / 2 + 3, 6.5)
    node(root[0], root[1], "Square body?", 84, True)
    node(mids[0][0], mids[0][1], "Antennas?")
    node(mids[1][0], mids[1][1], "Antennas?")
    results = [scan("Ma"), scan("Mg"), scan("Mb"), scan("Md")]
    for lf, (name, stat, amt) in zip(leaves, results):
        sign = "+" if amt > 0 else "–"
        leaf(lf[0], lf[1], name, f"{sign}{abs(amt)} {stat.upper()}")


RULES = {1: rule_f1, 2: rule_f2, 3: rule_f3, 4: rule_f4, 5: rule_f5}


def floor_page(c, floor):
    top = H - M
    c.setFillGray(0)
    c.roundRect(M, top - 30, 76, 30, 5, fill=1, stroke=0)
    centred(c, f"FLOOR {floor['num']}", M + 38, top - 15, 14, gray=1)
    label(c, floor["name"], M + 88, top - 16, 17)
    label(c, floor["concept"], M + 88, top - 28, 8.5, SANS, gray=0.3)
    RULES[floor["num"]](c, M, top - 46, W - 2 * M, 148)
    gx, gy = M + 16, 140
    draw_map(c, floor, gx, gy)
    legend(c, floor, gx + CELL * SIZE + 14, gy + CELL * SIZE, W - M - (gx + CELL * SIZE + 14))
    tracker(c, M, 126, W - 2 * M)
    footer(c, f"Floor {floor['num']}")
    c.showPage()


# ---------- other pages ----------
def cover(c):
    top = H - M
    c.setFillGray(0)
    c.rect(M, top - 150, W - 2 * M, 150, fill=1, stroke=0)
    centred(c, "COMPUTER SCIENCE", W / 2, top - 36, 38, gray=1)
    centred(c, "CRAWLER", W / 2, top - 76, 38, gray=1)
    centred(c, "AN UNPLUGGED CODING DUNGEON", W / 2, top - 112, 14, gray=1)
    centred(c, "pencil  ·  paper  ·  one die", W / 2, top - 132, 10, SANS, gray=1)
    para(c, "You are a brand-new <b>web crawler</b>: a bot that search engines send out to read the internet. "
            "Your first job is an old website, five floors deep, that shuts down forever on Friday. Crawl each "
            "floor, index its <b>DATA</b>, and survive the broken code that drains your <b>RAM</b>. Reach the "
            "RUN square to follow the link down to the next floor. One warning from the last crawler sent "
            "here: something at the bottom has been sorting visitors all wrong.", M + 20, top - 166,
         W - 2 * M - 40, size=11, leading=15)
    bx, by, bw, bh = M, 250, 300, 250
    c.setLineWidth(1.5)
    c.setDash(4, 3)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    c.setDash()
    label(c, "DRAW YOUR CRAWLER", bx + 10, by + bh - 16, 9)
    rx = bx + bw + 24
    for i, name in enumerate(("Crawler name", "Real name", "Class", "Date started", "Date finished")):
        y = by + bh - 30 - i * 48
        label(c, name.upper(), rx, y, 8, BOLD, gray=0.3)
        blank(c, rx, y - 24, W - M - rx)
    label(c, "YOU START WITH", M, 216, 9)
    for i, (name, val) in enumerate((("RAM", "10"), ("DATA", "0"), ("MAX RAM", "10"))):
        x = M + i * 120
        c.setLineWidth(1.5)
        c.rect(x, 150, 104, 54, fill=0, stroke=1)
        centred(c, val, x + 52, 184, 24)
        centred(c, name, x + 52, 160, 9)
    para(c, "<b>RAM</b> is your energy. Broken code drains it.<br/><b>DATA</b> is what you index. Spend it in the shop."
            "<br/><b>MAX RAM</b> is the most RAM you can hold.", M + 372, 206, W - 2 * M - 372, size=9.5, leading=14)
    icons = ["ST", "B2", "o.", "DB", "+2", "MW", "FA", "Ma", "Mb", "EX"]
    for i, t in enumerate(icons):
        icon(c, t, M + 20 + i * 50, 72, 46, 5)
    footer(c, "Cover")
    c.showPage()


def mini(c, x, y, cell, cols, rows, walls, path, title):
    for (r, col) in walls:
        icon(c, "##", x + col * cell, y + (rows - 1 - r) * cell, cell)
    c.setStrokeGray(0.55)
    c.setLineWidth(0.5)
    for k in range(1, cols):
        c.line(x + k * cell, y, x + k * cell, y + rows * cell)
    for k in range(1, rows):
        c.line(x, y + k * cell, x + cols * cell, y + k * cell)
    c.setStrokeGray(0)
    c.setLineWidth(1.5)
    c.rect(x, y, cols * cell, rows * cell, fill=0, stroke=1)
    pts = [(x + (col + 0.5) * cell, y + (rows - 0.5 - r) * cell) for r, col in path]
    icon(c, "ST", pts[0][0] - cell / 2, pts[0][1] - cell / 2, cell)
    c.setDash(2, 2)
    c.setLineWidth(1.4)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    c.setDash()
    for i, p in enumerate(pts[1:-1], 1):
        c.circle(p[0], p[1], 1.8, fill=1, stroke=0)
    ex, ey = pts[-1]
    c.setLineWidth(2)
    c.line(ex - 5, ey - 5, ex + 5, ey + 5)
    c.line(ex - 5, ey + 5, ex + 5, ey - 5)
    para(c, title, x + cols * cell + 10, y + rows * cell - 4, 112, size=8.5, leading=11)


def rules_page(c):
    top = H - M
    label(c, "HOW TO PLAY", M, top - 20, 26)
    para(c, "<b>Goal:</b> get through all 5 floors. Collect DATA. Do not run out of RAM. "
            "<b>You need:</b> this booklet, a pencil and one die.", M, top - 32, W - 2 * M, size=10.5)
    colw = 258
    lx, rx = M, M + colw + 16
    y = top - 72
    panel(c, lx, y, colw, 250, "YOUR TURN")
    para(c, "<b>1. Roll the die.</b><br/><br/>"
            "<b>2. Odd or even?</b><br/>ODD (1, 3, 5): move <b>diagonally</b>.<br/>"
            "EVEN (2, 4, 6): move <b>straight</b> (up, down, left or right).<br/><br/>"
            "<b>3. Pick a direction</b> and move that many squares, one square at a time.<br/><br/>"
            "<b>4. Draw your path</b> as you go. Mark the square where you stop with an <b>X</b>. "
            "Start there next turn.<br/><br/>"
            "<b>5. Use everything you cross.</b> Every bug, data dot and power-up on your path happens to you, "
            "in order. Write each gain or loss in the boxes at the bottom of the page, then cross the thing "
            "out. It only works once.", lx + 12, y - 18, colw - 24, size=9.5)
    panel(c, rx, y, colw, 250, "MOVING RULES")
    para(c, "• If any direction lets you make your <b>whole move without hitting a wall</b>, you must pick "
            "one of those directions.<br/><br/>"
            "• <b>Keep going the same way.</b> You turn only when a wall or the edge of the map blocks "
            "you. Then pick a new direction of the same kind and keep counting.<br/><br/>"
            "• You may <b>not</b> turn to dodge a bug or to grab something.<br/><br/>"
            "• Go back the way you came <b>only</b> if there is no other way.<br/><br/>"
            "• Moving diagonally, only the square you land on matters. You can slip between two wall "
            "corners.", rx + 12, y - 18, colw - 24, size=9.5)
    y2 = y - 268
    panel(c, lx, y2, W - 2 * M, 110, "EXAMPLES")
    cell = 20
    mini(c, lx + 16, y2 - 100, cell, 6, 4, [(0, 4), (1, 4), (3, 1)],
         [(1, 0), (1, 1), (1, 2), (1, 3), (2, 3)],
         "<b>Rolled 4 (even).</b> Moved right 3 squares. A wall blocked the way, so turned and finished "
         "the last square going down.")
    mini(c, lx + 282, y2 - 100, cell, 6, 4, [(3, 2), (0, 5)],
         [(2, 0), (1, 1), (0, 2), (1, 3)],
         "<b>Rolled 3 (odd).</b> Moved up-right 2 squares. The edge blocked the way, so bounced "
         "down-right for the last square.")
    y3 = y2 - 128
    panel(c, lx, y3, colw, 196, "LEAVING A FLOOR")
    para(c, "Stop on the <b>RUN</b> square, stop on any square touching it (corners count), or pass over it. "
            "Then you may leave. You can also stay to collect more.<br/><br/>"
            "Now do the math, once for RAM and once for DATA:<br/>"
            "<b>START + gained – lost = END</b><br/><br/>"
            "Copy both END numbers to START on the next floor.<br/><br/>"
            "RAM cannot go above your Max RAM. DATA cannot go below 0. You do not crash in the middle of a "
            "floor: only the END number counts.", lx + 12, y3 - 18, colw - 24, size=9.5)
    panel(c, rx, y3, colw, 92, "CRASH!")
    para(c, "If your END RAM is <b>0 or less</b>, your crawler crashed. Tally one crash on the last page. "
            "Start the next floor with <b>10 RAM and 0 DATA</b>. Keep playing!",
         rx + 12, y3 - 18, colw - 24, size=9.5)
    panel(c, rx, y3 - 104, colw, 92, "CODE REVIEW")
    para(c, "Real coders check each other's work. After every floor, swap booklets with a partner. "
            "Check their path, their math and their floor puzzle. Found a mistake? Fix it together.",
         rx + 12, y3 - 122, colw - 24, size=9.5)
    footer(c, "How to play")
    c.showPage()


def box(c, x, y, s=12):
    c.setLineWidth(0.9)
    c.rect(x, y, s, s, fill=0, stroke=1)


def shop_page(c):
    top = H - M
    label(c, "THE SHOP", M, top - 20, 26)
    para(c, "Visit the shop twice: <b>after Floor 2</b> and <b>after Floor 4</b>. Pay with DATA. "
            "Write the price in the <b>– LOST</b> box for DATA on the next floor. "
            "You can buy each thing once per visit.", M, top - 32, W - 2 * M, size=10.5)
    items = [
        ("PATCH", "4", "Gain 4 RAM. Write +4 in the + GAINED box for RAM on the next floor.", False),
        ("DEBUGGER", "3", "Roll again once, on any roll you do not like.", True),
        ("ANTIVIRUS", "5", "Ignore one bug or one malware. Cross it out without losing anything.", True),
        ("RAM UPGRADE", "8", "Your Max RAM goes up by 2 for the rest of the game.", False),
    ]
    y = top - 92
    xs = [M, M + 104, M + 150, M + 372, M + 452]
    for hx, hd in zip(xs, ["ITEM", "PRICE", "WHAT IT DOES", "SHOP 1", "SHOP 2"]):
        label(c, hd, hx + 4, y + 5, 8, gray=0.3)
    for name, price, desc, usable in items:
        c.setLineWidth(1)
        c.rect(M, y - 44, W - 2 * M, 44, fill=0, stroke=1)
        label(c, name, xs[0] + 6, y - 26, 10.5)
        label(c, f"{price} DATA", xs[1] + 4, y - 26, 9.5, SANS)
        para(c, desc, xs[2] + 4, y - 9, 212, size=9)
        for sx in (xs[3], xs[4]):
            box(c, sx + 4, y - 20)
            label(c, "bought", sx + 20, y - 17, 7.5, SANS)
            if usable:
                box(c, sx + 4, y - 38)
                label(c, "used", sx + 20, y - 35, 7.5, SANS)
        y -= 44
    label(c, "MY MAX RAM:", M, y - 30, 10)
    for i, v in enumerate(("10", "", "")):
        bx = M + 86 + i * 62
        c.rect(bx, y - 42, 36, 30, fill=0, stroke=1)
        if v:
            centred(c, v, bx + 18, y - 27, 14)
        if i < 2:
            arrow(c, bx + 49, y - 27, 14, "R")

    y -= 86
    label(c, "FINAL STATS", M, y, 26)
    y -= 22
    stats = [("CRASHES (tally)", 150), ("FINAL RAM", 110), ("FINAL DATA", 110), ("FLOORS CLEARED", 122)]
    x = M
    for name, wd in stats:
        c.setLineWidth(1.5)
        c.rect(x, y - 62, wd, 62, fill=0, stroke=1)
        label(c, name, x + 6, y - 13, 8)
        x += wd + 13
    y -= 86
    label(c, "YOUR RANK  (by final DATA)", M, y, 10)
    ranks = [("0 – 14", "Intern"), ("15 – 29", "Junior Coder"), ("30 – 44", "Senior Engineer"),
             ("45 +", "System Architect")]
    for i, (rng, name) in enumerate(ranks):
        bx = M + i * 134
        box(c, bx, y - 26)
        label(c, name, bx + 18, y - 22, 10)
        label(c, f"{rng} DATA", bx + 18, y - 34, 8, SANS, gray=0.3)
    y -= 66
    label(c, "THINK BACK", M, y, 10)
    qs = ["Which floor puzzle was hardest? What made it hard?",
          "On Floor 5, was the sorting AI fair to every bot? Why or why not?",
          "Where have you seen one of these ideas in real life?"]
    for q in qs:
        y -= 18
        label(c, q, M, y, 9.5, SANS)
        y -= 20
        blank(c, M, y, W - 2 * M)
        y -= 20
        blank(c, M, y, W - 2 * M)
    footer(c, "Shop and stats")
    c.showPage()


def teacher_page(c):
    top = H - M
    c.setFillGray(0)
    c.rect(M, top - 26, W - 2 * M, 26, fill=1, stroke=0)
    centred(c, "TEACHER PAGE: ANSWER KEY  (do not hand out)", W / 2, top - 13, 13, gray=1)
    colw = 258
    lx, rx = M, M + colw + 16
    y = top - 46
    f1, f3, f4 = FLOORS[0], FLOORS[2], FLOORS[3]
    progs = "<br/>".join(f"<b>{n}</b> ends on <b>{program_end(f1, n)}</b>" for n in f1["programs"])
    tokens3 = sorted({t for row in f3["grid"] for t in row if t[0] in "CBL" and t[1].isdigit()})
    conv = ", ".join(dict.fromkeys(
        f"{format(int(t[1]), '03b' if t[0] in 'CL' else 'b')} = {t[1]}" for t in tokens3))
    ciph = "<br/>".join(f"<b>Firewall {KEY_LETTER[k]}</b>: {encode(wd, sh)}, shift {sh} = <b>{wd}</b>"
                        for k, (sh, wd) in f4["cipher"].items())
    g5 = FLOORS[4]["grid"]
    rows = []
    for r in range(SIZE):
        for col in range(SIZE):
            t = g5[r][col]
            if t[0] == "M":
                sq, an, sm = BOTS[t]
                name, stat, amt = scan(t)
                wrong = (sm and amt < 0) or (not sm and amt > 0)
                rows.append(f"{coord(r, col)}: {'square' if sq else 'round'}, "
                            f"{'antennas' if an else 'no antennas'}, {'smiling' if sm else 'frowning'} = "
                            f"<b>{name}</b>{' (sorting AI is wrong)' if wrong else ''}")
    left = (
        "<b>FLOOR 1: programs</b><br/>" + progs + "<br/><br/>"
        "<b>FLOOR 2: variable x</b><br/>x starts at 1. Order matters: x+1 then x×2 gives 4, but x×2 "
        "then x+1 gives 3. The x=0 square models a bug that overwrites a variable. Players gain x DATA on "
        "leaving.<br/><br/>"
        "<b>FLOOR 3: binary</b><br/>" + conv + ".<br/>The door opens with key 5. Roll log: any complete tally "
        "earns +2 DATA.<br/><br/>"
        "<b>FLOOR 4: cipher</b><br/>" + ciph + "<br/><br/>"
        "<b>FLOOR 5: bots</b><br/>" + "<br/>".join(rows)
    )
    para(c, left, lx, y, colw, size=8.8, leading=11.6)
    right = (
        "<b>WHAT EACH FLOOR TEACHES</b><br/>"
        "1. Algorithms and Design: sequence, loops, tracing a program.<br/>"
        "2. Programming: variables, assignment, IF / ELSE.<br/>"
        "3. Data and Analysis: binary representation, collecting and summarising data (the roll log).<br/>"
        "4. Systems and Security: authentication, encryption, the cost of weak defences.<br/>"
        "5. Computing and Society (AI): classification with a decision tree, and bias from features a model "
        "was never trained on.<br/>"
        "Match these to your state or CSTA standard codes before use; the codes are not listed here.<br/><br/>"
        "<b>RUNNING IT</b><br/>"
        "• Each student needs a booklet, a pencil and a die. Print single-sided so nothing shows "
        "through the maps.<br/>"
        "• Teach the movement rules with Floor 1 on a projector or the board, playing 3 or 4 turns "
        "together.<br/>"
        "• In computer playtests a floor took about 9 to 11 turns, and 9 in 10 finished within 22. "
        "Real classroom timing is not yet tested: time your first session.<br/>"
        "• About 4 in 10 simulated players crashed at least once. A crash is a reset, not a loss.<br/>"
        "• Code review pairs replace teacher marking. Keep this page for disputes.<br/><br/>"
        "<b>DISCUSSION STARTERS</b><br/>"
        "1. A program square moved you without a die. What makes a program predictable?<br/>"
        "2. Did the order you crossed the code squares change x? Why?<br/>"
        "3. Was your most common roll the same as your partner's? What would a class-wide log show?<br/>"
        "4. Smashing a firewall cost RAM. What does a break-in cost a real organisation?<br/>"
        "5. The sorting AI hurt friendly square bots. Who is responsible when a model is unfair: the model, "
        "its training data, or the people who built it?"
    )
    para(c, right, rx, y, colw, size=8.8, leading=11.6)
    footer(c, "Teacher page")
    c.showPage()


def build(path="Computer_Science_Crawler_Booklet.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle("Computer Science Crawler: an unplugged coding dungeon")
    c.setAuthor("Computer Science Crawler")
    cover(c)
    rules_page(c)
    for i, f in enumerate(FLOORS):
        floor_page(c, f)
    shop_page(c)
    teacher_page(c)
    c.save()
    return path


if __name__ == "__main__":
    print("wrote", build())
