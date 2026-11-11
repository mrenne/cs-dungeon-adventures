"""Hardware: a signal must pass input, processing, storage and output in order (Systems & Security).

Tokens: HI input, HP processor, HS storage, HO output. Crossing the next part in the order, or ending a
move touching it (corners count, like RUN), ticks it (+1 DATA) and crosses it out. A part out of
order does nothing and stays on the map.
The RUN square only opens once all four are ticked.
"""
from ..draw import BOLD, SANS, box, centred, label, panel, para
from ..grid import SIZE, coord, find
from .base import Mechanic

ORDER = ["HI", "HP", "HS", "HO"]
NAMES = {"HI": "IN", "HP": "CPU", "HS": "SAVE", "HO": "OUT"}
WHAT = {"HI": "touchscreen, microphone", "HP": "the processor follows instructions",
        "HS": "storage keeps it", "HO": "screen, speaker"}


def part(c, t, cx, cy, s):
    """Icon for a hardware part, centred on (cx, cy), side s."""
    c.setLineWidth(1.2)
    c.setFillGray(1)
    if t == "HP":
        c.setLineWidth(1)
        for k in (-1, 0, 1):
            off = k * s * 0.16
            for a, b in (((cx + off, cy + s * 0.3), (cx + off, cy + s * 0.4)),
                         ((cx + off, cy - s * 0.3), (cx + off, cy - s * 0.4)),
                         ((cx + s * 0.3, cy + off), (cx + s * 0.4, cy + off)),
                         ((cx - s * 0.3, cy + off), (cx - s * 0.4, cy + off))):
                c.line(a[0], a[1], b[0], b[1])
        c.setFillGray(0)
        c.rect(cx - s * 0.3, cy - s * 0.3, s * 0.6, s * 0.6, fill=1, stroke=0)
        centred(c, "CPU", cx, cy, s * 0.21, gray=1)
        return
    if t == "HS":
        p = c.beginPath()
        x0, y0, w, h = cx - s * 0.28, cy - s * 0.34, s * 0.56, s * 0.68
        p.moveTo(x0, y0)
        p.lineTo(x0 + w, y0)
        p.lineTo(x0 + w, y0 + h)
        p.lineTo(x0 + w * 0.3, y0 + h)
        p.lineTo(x0, y0 + h - w * 0.3)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        centred(c, "SAVE", cx, cy - s * 0.06, s * 0.18)
        return
    c.roundRect(cx - s * 0.38, cy - s * 0.24, s * 0.76, s * 0.48, s * 0.1, fill=1, stroke=1)
    centred(c, NAMES[t], cx, cy, s * 0.22)


class Hardware(Mechanic):
    name = "hardware"
    key_title = "hardware"

    def legend(self, floor):
        return [(t, f"<b>{i + 1}. {NAMES[t]}:</b> {WHAT[t]}") for i, t in enumerate(ORDER)]

    def icon(self, c, t, x, y, s, floor):
        if t in NAMES:
            part(c, t, x + s / 2, y + s / 2, s)

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: FOLLOW THE SIGNAL")
        para(c, "Every computer does four jobs, always in this order: it takes <b>input</b>, "
                "<b>processes</b> it, <b>stores</b> the result, then shows the <b>output</b>.<br/><br/>"
                "Carry a signal through the phone. Cross the part that is <b>next</b> in the order, or stop "
                "touching it (corners count): tick it, <b>+1 DATA</b>, cross it out. A part out of order "
                "does nothing.<br/><br/>"
                "<b>The RUN square stays shut</b> until all four are ticked.",
             x + 12, yt - 16, 250, size=8.8, leading=10.8)
        sx = x + 282
        label(c, "THE SIGNAL", sx, yt - 26, 8.5)
        for i, t in enumerate(ORDER):
            cx = sx + 26 + i * 62
            part(c, t, cx, yt - 58, 40)
            box(c, cx - 6, yt - 98, 12)
            centred(c, ["1st", "2nd", "3rd", "4th"][i], cx, yt - 108, 7, SANS, gray=0.3)
            if i < 3:
                c.setLineWidth(1.2)
                c.line(cx + 22, yt - 58, cx + 38, yt - 58)
                c.line(cx + 34, yt - 55, cx + 38, yt - 58)
                c.line(cx + 34, yt - 61, cx + 38, yt - 58)
        label(c, "All four ticked: the RUN square opens.", sx, yt - 128, 8, BOLD)

    def answer_key(self, floor):
        where = "; ".join(f"{NAMES[t]} at {', '.join(coord(*p) for p in find(floor['grid'], t))}" for t in ORDER)
        return (f"{where}. Parts crossed out of order stay on the map. "
                "A finished signal earns +4 DATA; the RUN square is shut until then.")

    def start(self, run):
        run.stage = 0

    def interact(self, run, t):
        if t in NAMES:
            if run.stage < len(ORDER) and t == ORDER[run.stage]:
                run.stage += 1
                run.data_plus += 1
            else:
                run.used.discard(run.pos)

    def after_move(self, run):
        if run.stage < len(ORDER):
            r, c = run.pos
            for p in find(run.g, ORDER[run.stage]):
                if p not in run.used and max(abs(p[0] - r), abs(p[1] - c)) <= 1:
                    run.used.add(p)
                    run.stage += 1
                    run.data_plus += 1
                    return

    def can_exit(self, run):
        return run.stage == len(ORDER)

    def targets(self, run):
        if run.stage < len(ORDER):
            return [p for p in find(run.g, ORDER[run.stage]) if p not in run.used]

    def validate(self, floor):
        for t in ORDER:
            if not find(floor["grid"], t):
                raise ValueError(f"Floor {floor['num']}: no {NAMES[t]} square, so the signal can never finish")
