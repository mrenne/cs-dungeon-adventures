"""The variable x with code squares and IF / ELSE squares (Programming).

Floor data: x_start (default 1). Leaving the floor gains x DATA.
The code squares and IF rules below are fixed for now; make them floor data when a game needs others.
"""
from ..draw import MONO, centred, label, panel, para
from .base import Mechanic

# token: (label on the map, function applied to x)
CODE = {
    "A1": ("x+1", lambda x: x + 1),
    "A3": ("x+3", lambda x: x + 3),
    "X2": ("x×2", lambda x: x * 2),
    "Z0": ("x=0", lambda x: 0),
}
# token: (test, (stat, amount) if true, (stat, amount) if false, printed IF line, printed ELSE line)
IFS = {
    "I1": (lambda x: x > 3, ("ram", 3), ("ram", -2), "IF x > 3:      +3 RAM", "ELSE:          –2 RAM"),
    "I2": (lambda x: x % 2 == 0, ("data", 4), ("ram", -1), "IF x is even:  +4 DATA", "ELSE:          –1 RAM"),
}
LABELS = {**{t: v[0] for t, v in CODE.items()}, "I1": "IF 1", "I2": "IF 2"}


def apply(run, stat, amount):
    if stat == "ram":
        if amount > 0:
            run.ram_plus += amount
        else:
            run.ram_minus -= amount
    else:
        if amount > 0:
            run.data_plus += amount
        else:
            run.data_minus -= amount


class Variables(Mechanic):
    name = "variables"
    key_title = "variable x"

    def legend(self, floor):
        return [("A1", "<b>Code:</b> change x"), ("I1", "<b>IF:</b> check x, do what it says")]

    def icon(self, c, t, x, y, s, floor):
        if t in LABELS:
            c.setFillGray(0.88)
            c.roundRect(x + s * 0.06, y + s * 0.2, s * 0.88, s * 0.6, s * 0.12, fill=1, stroke=1)
            centred(c, LABELS[t], x + s / 2, y + s / 2, s * 0.24, MONO)

    def rule_panel(self, c, floor, x, yt, w, h):
        x0 = floor.get("x_start", 1)
        panel(c, x, yt, w, h, "FLOOR RULE: THE VARIABLE x")
        para(c, f"A <b>variable</b> is a box that holds a value. Yours is called <b>x</b> and it starts at <b>{x0}</b>."
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
                centred(c, str(x0), bx + 13, yt - 35, 14)
        c.setFont(MONO, 9.5)
        for i, (name, (_, _, _, a, b)) in enumerate(IFS.items()):
            y = yt - 74 - i * 36
            c.setFillGray(0.88)
            c.roundRect(px, y - 14, 40, 22, 4, fill=1, stroke=1)
            centred(c, LABELS[name], px + 20, y - 3, 9.5, MONO)
            c.setFont(MONO, 9.5)
            c.drawString(px + 50, y, a)
            c.drawString(px + 50, y - 12, b)

    def answer_key(self, floor):
        x0 = floor.get("x_start", 1)
        return (f"x starts at {x0}. Order matters: x+1 then x×2 gives {(x0 + 1) * 2}, but x×2 "
                f"then x+1 gives {x0 * 2 + 1}. The x=0 square models a bug that overwrites a variable. "
                "Players gain x DATA on leaving.")

    def start(self, run):
        run.x = run.f.get("x_start", 1)

    def interact(self, run, t):
        if t in CODE:
            run.x = CODE[t][1](run.x)
        elif t in IFS:
            test, yes, no, _, _ = IFS[t]
            apply(run, *(yes if test(run.x) else no))

    def on_leave(self, run):
        run.data_plus += run.x
