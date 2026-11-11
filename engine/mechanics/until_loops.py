"""Program squares with REPEAT UNTIL WALL loops and a loop counter (Programming).

Floor data: programs = {"P1": [steps], ...}; a step is 'U','D','L','R' or ('until', [steps]).
Before each pass through the brackets, look ahead: if any step would hit a wall or the edge,
the loop ends. Each full pass is one run of the loop and earns 1 DATA.
"""
from ..draw import SANS, blank, centred, label, panel, para
from ..grid import SIZE, coord, find
from .base import Mechanic
from .programs import STEP, draw_program

MAX_RUNS = 20


def open_square(grid, p):
    r, c = p
    return 0 <= r < SIZE and 0 <= c < SIZE and grid[r][c] != "##" and grid[r][c][0] != "L"


def trace(grid, start, program):
    """Returns (directions, loop runs, end position)."""
    pos, dirs, runs = start, [], 0
    for step in program:
        if isinstance(step, tuple):
            body = step[1]
            while runs < MAX_RUNS:
                p, ok = pos, True
                for d in body:
                    p = (p[0] + STEP[d][0], p[1] + STEP[d][1])
                    ok = ok and open_square(grid, p)
                if not ok:
                    break
                for d in body:
                    pos = (pos[0] + STEP[d][0], pos[1] + STEP[d][1])
                    dirs.append(d)
                runs += 1
        else:
            pos = (pos[0] + STEP[step][0], pos[1] + STEP[step][1])
            if not open_square(grid, pos):
                raise ValueError(f"a fixed step runs into a wall at {coord(*pos)}")
            dirs.append(step)
    return dirs, runs, pos


class UntilLoops(Mechanic):
    name = "until_loops"
    key_title = "REPEAT UNTIL loops"

    def legend(self, floor):
        return [("P1", "<b>Program:</b> stop and run it. Count the loops")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "P":
            c.setLineWidth(2)
            c.setFillGray(1)
            c.rect(x + s * 0.14, y + s * 0.14, s * 0.72, s * 0.72, fill=1, stroke=1)
            centred(c, t, x + s / 2, y + s / 2, s * 0.3)

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: REPEAT UNTIL")
        para(c, "Step on a program square and your move stops. Run the program.<br/><br/>"
                "<b>REPEAT [ ... ] UNTIL WALL</b> is a loop that does not know how many times it will run. "
                "Before each repeat, look ahead: if any step in the brackets would hit a wall or the edge, "
                "<b>the loop ends</b>. It might even run 0 times.<br/><br/>"
                "Count each repeat: <b>+1 DATA per repeat</b>. Each program runs once.",
             x + 12, yt - 16, 250, size=8.8, leading=10.8)
        px = x + 285
        label(c, "THE PROGRAMS", px, yt - 26, 8.5)
        for i, (name, prog) in enumerate(floor["programs"].items()):
            y = yt - 50 - i * 34
            label(c, name, px, y, 12)
            draw_program(c, px + 28, y, prog, 11)
            label(c, "Ended on:", px + 28, y - 14, 7.5, SANS)
            blank(c, px + 66, y - 15, 34)
            label(c, "Loop ran:", px + 112, y - 14, 7.5, SANS)
            blank(c, px + 148, y - 15, 22)
            label(c, "times", px + 174, y - 14, 7.5, SANS)

    def answer_key(self, floor):
        rows = []
        for name, prog in floor["programs"].items():
            _, runs, end = trace(floor["grid"], find(floor["grid"], name)[0], prog)
            rows.append(f"<b>{name}</b> ends on <b>{coord(*end)}</b>; the loop runs {runs} times (+{runs} DATA)")
        return "<br/>".join(rows)

    def interact(self, run, t):
        if t[0] == "P":
            return "program"

    def program_steps(self, run, name):
        dirs, runs, _ = trace(run.g, run.pos, run.f["programs"][name])
        run.data_plus += runs
        return dirs

    def validate(self, floor):
        for name, prog in floor["programs"].items():
            for step in prog:
                if isinstance(step, tuple):
                    dr = sum(STEP[d][0] for d in step[1])
                    dc = sum(STEP[d][1] for d in step[1])
                    if dr == dc == 0:
                        raise ValueError(f"Floor {floor['num']}: {name}'s loop never moves, so it never ends")
            trace(floor["grid"], find(floor["grid"], name)[0], prog)
