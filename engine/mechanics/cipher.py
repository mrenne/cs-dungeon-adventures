"""Cipher keys and firewalls (Systems & Security).

Floor data: cipher = {"1": (shift, password), ...}; force_cost (default 2).
Tokens: Kn cipher key n, Wn firewall: free with key n, otherwise costs force_cost RAM to smash.
"""
from ..draw import BOLD, MONO, SANS, blank, centred, key_shape, label, panel, para
from ..grid import SIZE, find
from .base import Mechanic

KEY_LETTER = "_ABCDEFGHI"  # key "1" is printed as KEY A, "2" as KEY B, ...


def encode(word, shift):
    return "".join(chr((ord(ch) - 65 + shift) % 26 + 65) for ch in word)


def force_cost(floor):
    return floor.get("force_cost", 2)


class Cipher(Mechanic):
    name = "cipher"
    key_title = "cipher"

    def legend(self, floor):
        return [("K1", "<b>Cipher key</b>"),
                ("W1", f"<b>Firewall:</b> free with key + password. No key: –{force_cost(floor)} RAM")]

    def is_background(self, t):
        return t[0] == "W"

    def icon(self, c, t, x, y, s, floor):
        cx, cy = x + s / 2, y + s / 2
        if t[0] == "K":
            key_shape(c, cx, cy + s * 0.2, s)
            centred(c, f"KEY {KEY_LETTER[int(t[1])]}", cx, cy - s * 0.08, s * 0.19)
            centred(c, f"shift {floor['cipher'][t[1]][0]}", cx, cy - s * 0.3, s * 0.18, SANS)
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
            centred(c, KEY_LETTER[int(t[1])], cx, cy, s * 0.34)

    def rule_panel(self, c, floor, x, yt, w, h):
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
        for kid, (shift, word) in floor["cipher"].items():
            label(c, f"Firewall {KEY_LETTER[int(kid)]}:", x + 12, y, 10, BOLD)
            label(c, "  ".join(encode(word, shift)), x + 84, y, 12, MONO)
            label(c, "shift:", x + 190, y, 9, SANS)
            blank(c, x + 218, y - 1, 22)
            label(c, "password:", x + 258, y, 9, SANS)
            for k in range(len(word)):
                blank(c, x + 308 + k * 24, y - 1, 18)
            y -= 20
        para(c, f"<b>Holding the key?</b> Decode the password, write it here, and walk through free. "
                f"<b>No key?</b> You can smash through, but it costs <b>{force_cost(floor)} RAM</b>. "
                f"Wrong password at code review: –3 DATA.", x + 12, y + 10, w - 24, size=8.5)

    def answer_key(self, floor):
        return "<br/>".join(f"<b>Firewall {KEY_LETTER[int(k)]}</b>: {encode(wd, sh)}, shift {sh} = <b>{wd}</b>"
                            for k, (sh, wd) in floor["cipher"].items())

    def interact(self, run, t):
        if t[0] == "W" and t[1] not in run.keys:
            run.ram_minus += force_cost(run.f)

    def exit_key(self, floor):
        """The key for the firewalls touching the exit: a planning player fetches it first."""
        er, ec = find(floor["grid"], "EX")[0]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = er + dr, ec + dc
                if 0 <= r < SIZE and 0 <= c < SIZE and floor["grid"][r][c][0] == "W":
                    return floor["grid"][r][c][1]
        return None

    def validate(self, floor):
        for r in floor["grid"]:
            for t in r:
                if t[0] in "KW" and t[1] not in floor["cipher"]:
                    raise ValueError(f"Floor {floor['num']}: {t} has no entry in cipher")
