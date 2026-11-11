"""Pixels: an image stored as rows of bits (Data & Analysis).

Floor data: image = five strings of five bits; picture = what it shows (answer key only).
Tokens: Cn, an image chest holding row n of the image. +1 DATA per chest; every row: +BONUS DATA.
"""
from ..draw import MONO, SANS, blank, centred, label, panel, para
from .base import Mechanic

BONUS = 5


class Pixels(Mechanic):
    name = "pixels"
    key_title = "pixels"

    def legend(self, floor):
        return [("C1", "<b>Image chest:</b> +1 DATA. Copy its row of pixels")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "C":
            cx, cy = x + s / 2, y + s / 2
            c.setFillGray(1)
            c.setLineWidth(1.2)
            c.rect(x + s * 0.06, y + s * 0.14, s * 0.88, s * 0.72, fill=1, stroke=1)
            c.setFillGray(0)
            c.rect(x + s * 0.06, y + s * 0.56, s * 0.88, s * 0.3, fill=1, stroke=0)
            centred(c, f"ROW {t[1]}", cx, y + s * 0.71, s * 0.2, gray=1)
            centred(c, floor["image"][int(t[1]) - 1], cx, y + s * 0.36, s * 0.22, MONO)

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: PICTURES ARE NUMBERS")
        para(c, "A photo is a grid of tiny squares called <b>pixels</b>. In a black-and-white image each pixel "
                "is one <b>bit</b>: <b>1</b> = black, <b>0</b> = white.<br/><br/>"
                "This phone's photo is broken into rows and hidden in image chests. Open a chest: +1 DATA. "
                "Copy its row into the grid, shading every 1.<br/><br/>"
                f"Find all 5 rows: <b>+{BONUS} DATA</b>. Your partner checks the picture.",
             x + 12, yt - 16, 250, size=8.8, leading=10.8)
        gx, cell = x + 300, 19
        gy = yt - 26
        label(c, "THE PHOTO", gx, gy, 8)
        for r in range(5):
            centred(c, str(r + 1), gx - 8, gy - 12 - r * cell - cell / 2, 8, SANS, gray=0.3)
            for k in range(5):
                c.setLineWidth(0.8)
                c.rect(gx + k * cell, gy - 12 - (r + 1) * cell, cell, cell, fill=0, stroke=1)
        qx = gx + 5 * cell + 18
        label(c, "It is a picture of:", qx, gy - 22, 8, SANS)
        blank(c, qx, gy - 40, 100)
        for i, q in enumerate(("Pixels in the photo:", "Bits to store it:", "Bits, 10 × 10 photo:")):
            label(c, q, qx, gy - 58 - i * 18, 8, SANS)
            blank(c, qx + 86, gy - 59 - i * 18, 18)

    def answer_key(self, floor):
        rows = ", ".join(f"row {i + 1} {bits}" for i, bits in enumerate(floor["image"]))
        return (f"The picture is <b>{floor['picture']}</b>: {rows}. "
                "25 pixels, 25 bits (one per pixel); a 10 × 10 photo needs 100 bits.")

    def start(self, run):
        run.rows = 0

    def interact(self, run, t):
        if t[0] == "C":
            run.data_plus += 1
            run.rows += 1

    def on_leave(self, run):
        if run.rows == len(run.f["image"]):
            run.data_plus += BONUS

    def validate(self, floor):
        assert len(floor["image"]) == 5 and all(len(r) == 5 and set(r) <= {"0", "1"} for r in floor["image"])
        found = sorted(t for row in floor["grid"] for t in row if t[0] == "C")
        if found != [f"C{i}" for i in range(1, 6)]:
            raise ValueError(f"Floor {floor['num']}: needs exactly one chest for each row C1-C5, found {found}")
