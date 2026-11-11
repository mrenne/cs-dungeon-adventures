"""Flowchart squares: an algorithm with decisions and a loop (Algorithms & Design).

Tokens: Qn, a flowchart square holding the number n (1-9). Crossing one runs the flowchart:
  n even?  NO -> n = n + STEP, back to the question
           YES -> n > LIMIT?  YES -> +WIN DATA   NO -> -LOSE RAM
"""
from ..draw import MONO, SANS, blank, centred, label, panel, para
from ..grid import SIZE, coord
from .base import Mechanic

STEP, LIMIT, WIN, LOSE = 3, 6, 3, 1


def run_chart(n):
    """Returns (every value n takes, stat, amount)."""
    values = [n]
    while n % 2:
        n += STEP
        values.append(n)
    return (values, "data", WIN) if n > LIMIT else (values, "ram", -LOSE)


def link(c, pts, head=True):
    """Polyline through pts with an arrowhead at the end."""
    c.setLineWidth(1)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    if head:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        dx, dy = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)
        p = c.beginPath()
        p.moveTo(x1, y1)
        p.lineTo(x1 - dx * 5 - dy * 3, y1 - dy * 5 - dx * 3)
        p.lineTo(x1 - dx * 5 + dy * 3, y1 - dy * 5 + dx * 3)
        p.close()
        c.drawPath(p, fill=1, stroke=0)


def diamond(c, cx, cy, w, h, text):
    p = c.beginPath()
    p.moveTo(cx, cy + h / 2)
    p.lineTo(cx + w / 2, cy)
    p.lineTo(cx, cy - h / 2)
    p.lineTo(cx - w / 2, cy)
    p.close()
    c.setFillGray(1)
    c.setLineWidth(1.2)
    c.drawPath(p, fill=1, stroke=1)
    centred(c, text, cx, cy, 8)


def action(c, cx, cy, w, h, text, filled=False):
    c.setLineWidth(1.2)
    c.setFillGray(0.88 if filled else 1)
    c.rect(cx - w / 2, cy - h / 2, w, h, fill=1, stroke=1)
    centred(c, text, cx, cy, 8)


class Flowchart(Mechanic):
    name = "flowchart"
    key_title = "flowchart"

    def legend(self, floor):
        return [("Q5", "<b>Flowchart:</b> run the flowchart with this number")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "Q":
            cx, cy = x + s / 2, y + s / 2
            p = c.beginPath()
            p.moveTo(cx, cy + s * 0.42)
            p.lineTo(cx + s * 0.42, cy)
            p.lineTo(cx, cy - s * 0.42)
            p.lineTo(cx - s * 0.42, cy)
            p.close()
            c.setFillGray(1)
            c.setLineWidth(1.6)
            c.drawPath(p, fill=1, stroke=1)
            centred(c, t[1], cx, cy, s * 0.36, MONO)

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: FLOWCHART SQUARES")
        para(c, "An <b>algorithm</b> can make decisions. A <b>flowchart</b> draws one: boxes are steps, "
                "diamonds are questions. Cross a flowchart square and run the flowchart with its number as "
                "<b>n</b>. Follow the arrows until you reach a RAM or DATA box. Keep moving after.<br/><br/>"
                "Write every value n takes, so your partner can check it.",
             x + 12, yt - 16, 212, size=8.6, leading=10.6)
        label(c, "MY TRACES  (example:  3 → 6)", x + 12, yt - 98, 7.5)
        for k in range(6):
            bx, by = x + 12 + (k % 2) * 108, yt - 114 - (k // 2) * 13
            label(c, "Q", bx, by + 1, 8, MONO)
            blank(c, bx + 8, by, 10)
            label(c, ":", bx + 20, by + 1, 8, SANS)
            blank(c, bx + 26, by, 74)

        fx = x + 244
        c1, c2, c3 = fx + 52, fx + 160, fx + 250
        r1, r2, r3 = yt - 30, yt - 70, yt - 110
        action(c, c1, r1, 100, 20, "n = the number")
        diamond(c, c1, r2, 84, 30, "Is n even?")
        action(c, c2, r2, 76, 20, f"n = n + {STEP}", filled=True)
        diamond(c, c1, r3, 84, 30, f"Is n > {LIMIT}?")
        action(c, c2, r3, 76, 20, f"+{WIN} DATA")
        action(c, c3, r3, 66, 20, f"–{LOSE} RAM")
        link(c, [(c1, r1 - 10), (c1, r2 + 15)])
        link(c, [(c1 + 42, r2), (c2 - 38, r2)])
        link(c, [(c2, r2 + 10), (c2, r1 - 20), (c1 + 2, r1 - 20)])  # loop back up
        link(c, [(c1, r2 - 15), (c1, r3 + 15)])
        link(c, [(c1 + 42, r3), (c2 - 38, r3)])
        link(c, [(c1, r3 - 15), (c1, r3 - 24), (c3, r3 - 24), (c3, r3 - 10)])
        centred(c, "NO", c1 + 52, r2 + 6, 6.5)
        centred(c, "YES", c1 + 14, (r2 + r3) / 2 + 2, 6.5)
        centred(c, "YES", c1 + 54, r3 + 6, 6.5)
        centred(c, "NO", c1 + 14, r3 - 19, 6.5)
        centred(c, "loop back", c2 + 22, r1 - 14, 6.5, SANS)

    def answer_key(self, floor):
        rows = []
        for r in range(SIZE):
            for col in range(SIZE):
                t = floor["grid"][r][col]
                if t[0] == "Q":
                    values, stat, amt = run_chart(int(t[1]))
                    sign = "+" if amt > 0 else "–"
                    rows.append(f"{coord(r, col)}: {' → '.join(map(str, values))} = <b>{sign}{abs(amt)} {stat.upper()}</b>")
        return "<br/>".join(rows)

    def interact(self, run, t):
        if t[0] == "Q":
            _, stat, amt = run_chart(int(t[1]))
            if stat == "data":
                run.data_plus += amt
            else:
                run.ram_minus -= amt
