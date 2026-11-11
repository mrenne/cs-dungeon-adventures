"""A biased sorting AI that classifies bots with a decision tree (Computing & Society, AI).

Floor data: bots = {"Ma": (square body, antenna, smiling), ...}. The tree looks only at body and
antenna; smiling decides whether a bot is really friendly, so some bots get sorted wrong.
"""
from ..draw import SANS, blank, centred, label, panel, para
from ..grid import SIZE, coord
from .base import Mechanic


def tree(square, antenna):
    """The sorting AI's decision tree: returns (label, stat, amount)."""
    if square:
        return ("VIRUS", "ram", -2) if antenna else ("BUG", "ram", -1)
    return ("DATA BOT", "data", 3) if antenna else ("HELPER", "ram", 2)


def scan(floor, bot):
    square, antenna, _ = floor["bots"][bot]
    return tree(square, antenna)


def draw_bot(c, cx, cy, s, square, antenna, smiling):
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


class SortingAI(Mechanic):
    name = "sorting_ai"
    key_title = "bots"

    def legend(self, floor):
        return [("Ma", "<b>Bot:</b> sort it with the AI's tree")]

    def icon(self, c, t, x, y, s, floor):
        if t[0] == "M":
            draw_bot(c, x + s / 2, y + s / 2, s, *floor["bots"][t])

    def rule_panel(self, c, floor, x, yt, w, h):
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
        results = [tree(True, True), tree(True, False), tree(False, True), tree(False, False)]
        for lf, (name, stat, amt) in zip(leaves, results):
            sign = "+" if amt > 0 else "–"
            leaf(lf[0], lf[1], name, f"{sign}{abs(amt)} {stat.upper()}")

    def answer_key(self, floor):
        g = floor["grid"]
        rows = []
        for r in range(SIZE):
            for col in range(SIZE):
                t = g[r][col]
                if t[0] == "M":
                    sq, an, sm = floor["bots"][t]
                    name, stat, amt = scan(floor, t)
                    wrong = (sm and amt < 0) or (not sm and amt > 0)
                    rows.append(f"{coord(r, col)}: {'square' if sq else 'round'}, "
                                f"{'antennas' if an else 'no antennas'}, {'smiling' if sm else 'frowning'} = "
                                f"<b>{name}</b>{' (sorting AI is wrong)' if wrong else ''}")
        return "<br/>".join(rows)

    def interact(self, run, t):
        if t[0] == "M":
            _, stat, amt = scan(run.f, t)
            if stat == "data":
                run.data_plus += amt
            elif amt > 0:
                run.ram_plus += amt
            else:
                run.ram_minus -= amt

    def validate(self, floor):
        for row in floor["grid"]:
            for t in row:
                if t[0] == "M" and t not in floor["bots"]:
                    raise ValueError(f"Floor {floor['num']}: bot {t} is missing from bots")
