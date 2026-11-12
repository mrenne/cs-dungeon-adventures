"""Program squares: sequences and loops (Algorithms & Design).

Floor data: programs = {"P1": [steps], ...}; a step is 'U','D','L','R' or ('rep', n, [steps]).
"""
from ..draw import MONO, arrow, blank, centred, label, panel, para
from ..grid import SIZE, coord, expand, find
from .base import Mechanic

STEP = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def draw_program(c, x, y, program, size=11):
    for step in program:
        if isinstance(step, tuple) and step[0] == "until":
            c.setFont(MONO, size)
            c.drawString(x, y, "REPEAT [")
            x += c.stringWidth("REPEAT [", MONO, size) + size * 0.4
            x = draw_program(c, x, y, step[1], size)
            c.setFont(MONO, size)
            c.drawString(x, y, "] UNTIL WALL")
            x += c.stringWidth("] UNTIL WALL", MONO, size)
        elif isinstance(step, tuple):
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


def program_end(floor, name):
    g = floor["grid"]
    pos = find(g, name)[0]
    for d in expand(floor["programs"][name]):
        pos = (pos[0] + STEP[d][0], pos[1] + STEP[d][1])
        if not (0 <= pos[0] < SIZE and 0 <= pos[1] < SIZE) or g[pos[0]][pos[1]] == "##":
            raise ValueError(f"Floor {floor['num']}: program {name} runs into a wall or off the map")
    return coord(*pos)


class Programs(Mechanic):
    name = "programs"
    key_title = "programs"

    def legend(self, floor):
        return [("P1", "<b>Program:</b> stop and run it")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "P":
            c.setLineWidth(2)
            c.setFillGray(1)
            c.rect(x + s * 0.14, y + s * 0.14, s * 0.72, s * 0.72, fill=1, stroke=1)
            centred(c, t, x + s / 2, y + s / 2, s * 0.3)

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: PROGRAM SQUARES")
        para(c, "A program is a list of steps. Step on a program square (<b>P1</b>, <b>P2</b>, <b>P3</b>) and your "
                "move stops: the rest of your roll is lost. Now <b>run the program</b>: move one square for each arrow, in order.<br/><br/>"
                "<b>REPEAT 2 [ ... ]</b> is a loop. Do the steps inside the brackets 2 times.<br/><br/>"
                "Use everything you cross. You stop where the program ends. Each program runs once, "
                "then cross it out.", x + 12, yt - 18, 250)
        px = x + 285
        label(c, "THE PROGRAMS", px, yt - 26, 8.5)
        for i, (name, prog) in enumerate(floor["programs"].items()):
            y = yt - 52 - i * 34
            label(c, name, px, y, 12)
            draw_program(c, px + 28, y, prog, 12)
            label(c, "I ended on square:", px + 28, y - 14, 7.5, "Helvetica")
            blank(c, px + 100, y - 15, 40)

    def answer_key(self, floor):
        return "<br/>".join(f"<b>{n}</b> ends on <b>{program_end(floor, n)}</b>" for n in floor["programs"])

    def interact(self, run, t):
        if t[0] == "P":
            return "program"

    def validate(self, floor):
        for name in floor["programs"]:
            program_end(floor, name)
