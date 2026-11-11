"""Training data: the player labels bots and an AI learns from those labels (Computing & Society, AI).

Floor data: bots = {"Ma": (square body, antenna, smiling), ...} on the map, and test = a list of
(square body, antenna, smiling) bots printed in the rule panel.
Meeting a bot: smiling = friendly (+1 RAM), frowning = hostile (-1 RAM); tally it under its body shape.
Leaving: the AI learns the majority label for each shape (a tie or no tallies teaches nothing), then
earns +1 DATA for each test bot it labels correctly.
"""
from ..draw import BOLD, SANS, box, centred, label, panel, para
from ..grid import SIZE, coord, find
from .base import Mechanic
from .sorting_ai import draw_bot


def learn(tally):
    """tally = {square?: [friendly, hostile]} -> {square?: True friendly / False hostile / None}."""
    return {shape: (None if f == h else f > h) for shape, (f, h) in tally.items()}


def score(rule, test):
    return sum(rule[sq] is not None and rule[sq] == sm for sq, _, sm in test)


class Training(Mechanic):
    name = "training"
    key_title = "training data"

    def legend(self, floor):
        return [("Ma", "<b>Bot:</b> label it from its face, tally it")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "M":
            draw_bot(c, x + s / 2, y + s / 2, s, *floor["bots"][t])

    def rule_panel(self, c, floor, x, yt, w, h):
        panel(c, x, yt, w, h, "FLOOR RULE: TRAIN THE AI")
        para(c, "The phone's photo sorter is an AI that <b>learns from you</b>. When you meet a bot, check its "
                "face. <b>Smiling</b> = friendly, +1 RAM. <b>Frowning</b> = hostile, –1 RAM. Then add a tally "
                "for its <b>body shape</b>: that tally is your training data.<br/><br/>"
                "When you leave, the AI learns: for each shape, the label with more tallies wins. A tie "
                "teaches it nothing. Then it sorts the test bots: <b>+1 DATA</b> for each one it gets right.",
             x + 12, yt - 16, 214, size=8.3, leading=10.2)

        tx = x + 236
        label(c, "TRAINING DATA", tx, yt - 26, 8)
        cols = [(tx + 50, "FRIENDLY"), (tx + 102, "HOSTILE")]
        for cx, hd in cols:
            centred(c, hd, cx + 26, yt - 38, 7)
        for i, shape in enumerate(("SQUARE", "ROUND")):
            ry = yt - 46 - i * 24
            label(c, shape, tx, ry - 15, 7.5)
            for cx, _ in cols:
                c.setLineWidth(0.8)
                c.rect(cx, ry - 22, 52, 22, fill=0, stroke=1)
        label(c, "THE AI LEARNED", tx, yt - 108, 8)
        label(c, "Square bots are: ________", tx, yt - 121, 7.5, SANS)
        label(c, "Round bots are: ________", tx, yt - 134, 7.5, SANS)

        vx = x + 408
        label(c, "TEST BOTS", vx, yt - 26, 8)
        for i, bot in enumerate(floor["test"]):
            bx, by = vx + (i % 3) * 38, yt - 64 - (i // 3) * 52
            draw_bot(c, bx + 15, by + 15, 30, *bot)
            box(c, bx + 9, by - 14, 11)
        label(c, "Tick each one the AI got right", vx, yt - 140, 6.5, SANS)

    def answer_key(self, floor):
        bots = floor["bots"]
        g = floor["grid"]
        rows = []
        for r in range(SIZE):
            for col in range(SIZE):
                t = g[r][col]
                if t[0] == "M":
                    sq, _, sm = bots[t]
                    rows.append(f"{coord(r, col)}: {'square' if sq else 'round'}, "
                                f"{'smiling (friendly)' if sm else 'frowning (hostile)'}")
        tally = {True: [0, 0], False: [0, 0]}
        for sq, _, sm in bots.values():
            tally[sq][0 if sm else 1] += 1
        rule = learn(tally)
        best = sum(max(sum(1 for s, _, m in floor["test"] if s == sq and m),
                       sum(1 for s, _, m in floor["test"] if s == sq and not m)) for sq in (True, False))
        words = {True: "friendly", False: "hostile", None: "nothing"}

        def taught(names):
            t = {True: [0, 0], False: [0, 0]}
            for n in names:
                sq, _, sm = bots[n]
                t[sq][0 if sm else 1] += 1
            rl = learn(t)
            return (f"square = {words[rl[True]]}, round = {words[rl[False]]}, "
                    f"<b>{score(rl, floor['test'])} of {len(floor['test'])}</b> test bots right")

        sr, sc = find(g, "ST")[0]
        near = sorted(bots, key=lambda n: max(abs(find(g, n)[0][0] - sr), abs(find(g, n)[0][1] - sc)))[:2]
        return ("<br/>".join(rows) +
                f"<br/>Meeting every bot teaches {taught(bots)}. Looking only at shape, no AI can get more "
                f"than {best}. Meeting only the two bots nearest the start "
                f"({', '.join(coord(*find(g, n)[0]) for n in near)}) teaches {taught(near)}: a skewed sample.")

    def start(self, run):
        run.tally = {True: [0, 0], False: [0, 0]}

    def interact(self, run, t):
        if t[0] == "M":
            sq, _, sm = run.f["bots"][t]
            run.tally[sq][0 if sm else 1] += 1
            if sm:
                run.ram_plus += 1
            else:
                run.ram_minus += 1

    def on_leave(self, run):
        run.data_plus += score(learn(run.tally), run.f["test"])

    def validate(self, floor):
        for row in floor["grid"]:
            for t in row:
                if t[0] == "M" and t not in floor["bots"]:
                    raise ValueError(f"Floor {floor['num']}: bot {t} is missing from bots")
