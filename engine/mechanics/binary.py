"""Everything in binary: bit chests, binary bugs, keys and doors, and a roll log (Data & Analysis).

Tokens: Cn bit chest worth n DATA, Kn key n, Ln door that opens with key n. A complete roll log
earns ROLL_LOG_BONUS DATA when the floor ends.
"""
from ..draw import MONO, SANS, blank, centred, key_shape, label, panel, para
from ..grid import tokens
from .base import Mechanic

ROLL_LOG_BONUS = 2


class Binary(Mechanic):
    name = "binary"
    key_title = "binary"

    def legend(self, floor):
        return [("C5", "<b>Bit chest:</b> gain DATA (binary)"), ("K5", "<b>Key</b> for a door"),
                ("L5", "<b>Door:</b> a wall until you hold its key")]

    def bug_text(self, digit):
        return bin(int(digit))[2:]

    def is_background(self, t):
        return t[0] == "L"

    def icon(self, c, t, x, y, s, floor):
        cx, cy = x + s / 2, y + s / 2
        if t[0] == "C":
            w, h = s * 0.68, s * 0.42
            c.setFillGray(1)
            c.rect(cx - w / 2, cy - h / 2 - s * 0.06, w, h, fill=1, stroke=1)
            c.arc(cx - w / 2, cy + h / 2 - s * 0.06 - s * 0.14, cx + w / 2, cy + h / 2 - s * 0.06 + s * 0.14, 0, 180)
            centred(c, format(int(t[1]), "03b"), cx, cy - s * 0.06, s * 0.23, MONO)
        elif t[0] == "K":
            key_shape(c, cx, cy + s * 0.14, s)
            centred(c, t[1], cx, cy - s * 0.2, s * 0.3)
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

    def rule_panel(self, c, floor, x, yt, w, h):
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
        para(c, f"Most common roll: ____<br/>Total rolls: ____<br/><b>Log complete: +{ROLL_LOG_BONUS} DATA</b>",
             lx, yt - 115, 114, size=7.5, leading=9.5)

    def answer_key(self, floor):
        found = sorted(t for t in tokens(floor["grid"]) if t[0] in "CBL" and t[1].isdigit())
        conv = ", ".join(dict.fromkeys(
            f"{format(int(t[1]), '03b' if t[0] in 'CL' else 'b')} = {t[1]}" for t in found))
        doors = sorted({t[1] for t in found if t[0] == "L"})
        door = (f"The door opens with key {doors[0]}. " if len(doors) == 1
                else f"Doors open with keys {', '.join(doors)}. " if doors else "")
        return conv + f".<br/>{door}Roll log: any complete tally earns +{ROLL_LOG_BONUS} DATA."

    def interact(self, run, t):
        if t[0] == "C":
            run.data_plus += int(t[1])

    def on_leave(self, run):
        run.data_plus += ROLL_LOG_BONUS
