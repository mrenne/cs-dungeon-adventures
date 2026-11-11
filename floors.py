"""Computer Science Crawler floor data: the single source of truth for maps and floor rules.

Grid tokens (10 x 10, columns A-J, rows 1-10):
  ##  wall            ..  empty          ST  start         EX  exit (RUN)
  o.  data packet     DB  database       Bn  bug, n damage B?  mystery bug
  +n  power-up        +?  mystery power  MW  malware       FA  function call pair
  Pn  program square (floor 1)
  A1 A3 X2 Z0  code squares, I1 I2  IF squares (floor 2)
  Cn  bit chest worth n, Kn key, Ln locked door (floor 3)
  Kn  cipher key, Wn firewall: free with key n, else costs FORCE_COST RAM (floor 4)
  Ma-Mh  bots (floor 5)
"""

SIZE = 10
FORCE_COST = 2
COLS = "ABCDEFGHIJ"


def parse(grid):
    rows = [r.split() for r in grid.strip().splitlines()]
    assert len(rows) == SIZE and all(len(r) == SIZE for r in rows), "grid must be 10x10"
    return rows


def coord(r, c):
    return f"{COLS[c]}{r + 1}"


# Programs: a step is 'U','D','L','R' or ('rep', n, [steps]).
def expand(program):
    out = []
    for step in program:
        if isinstance(step, tuple):
            out += expand(step[2]) * step[1]
        else:
            out.append(step)
    return out


# Floor 5 bots: (square body, antenna, smiling)
BOTS = {
    "Ma": (True, True, False),
    "Mb": (False, True, True),
    "Mc": (True, False, True),
    "Md": (False, False, True),
    "Me": (True, True, True),
    "Mf": (False, True, False),
    "Mg": (True, False, False),
    "Mh": (False, False, True),
}


def scan(bot):
    """The sorting AI's decision tree: returns (label, stat, amount)."""
    square, antenna, _ = BOTS[bot]
    if square:
        return ("VIRUS", "ram", -2) if antenna else ("BUG", "ram", -1)
    return ("DATA BOT", "data", 3) if antenna else ("HELPER", "ram", 2)


FLOORS = [
    dict(
        num=1,
        name="THE HOME PAGE",
        concept="Algorithms: follow steps in order, repeat with loops",
        grid=parse("""
ST .. o. o. ## DB .. o. B2 ..
.. o. ## .. ## .. o. ## .. o.
o. B1 ## P1 .. .. o. ## +2 ..
.. +2 .. o. ## ## .. .. o. ..
## ## o. .. B2 .. .. ## ## o.
FA .. .. ## o. P2 .. .. B? ..
o. .. +? ## o. .. ## o. .. o.
.. ## ## o. .. MW ## .. FA ..
o. B2 .. .. o. .. .. P3 ## ..
.. o. .. ## +3 o. .. .. o. EX
"""),
        programs={
            "P1": ["R", "R", "U", "U"],
            "P2": [("rep", 2, ["D", "L"])],
            "P3": ["D", ("rep", 2, ["R"])],
        },
    ),
    dict(
        num=2,
        name="THE SOURCE CODE",
        concept="Programming: variables and IF / ELSE",
        x_start=1,
        grid=parse("""
o. .. .. MW .. o. .. .. +3 EX
.. .. B2 .. .. ## I2 o. .. FA
## o. ## ## A3 .. .. .. ## ..
+? .. .. o. .. Z0 ## B3 .. o.
.. o. ## .. ## .. +2 o. .. ..
FA .. A1 .. B? .. X2 .. ## DB
## ## .. ## ## o. ## .. o. ..
o. B1 .. .. I1 .. .. .. +2 ##
.. ## o. ## .. ## o. ## .. ..
ST o. .. ## o. A1 .. B2 .. o.
"""),
    ),
    dict(
        num=3,
        name="THE DATABASE",
        concept="Data: binary numbers, collecting and reading data",
        grid=parse("""
.. o. .. C3 ## .. B1 o. .. ST
o. ## ## .. ## o. ## .. ## o.
.. .. .. B2 .. .. .. K5 ## ..
+2 ## o. ## ## o. ## ## .. o.
.. .. +2 .. MW .. o. .. B3 ..
## o. ## C5 ## .. ## o. ## ##
.. B? .. .. .. +? .. .. L5 C8
o. ## .. .. o. .. ## o. ## ##
.. .. C6 .. .. .. B2 .. .. +3
.. EX .. o. ## o. .. ## .. o.
"""),
    ),
    dict(
        num=4,
        name="THE LOGIN PAGE",
        concept="Security: passwords, keys and secret codes",
        cipher={"1": (1, "BYTE"), "2": (3, "CODE")},
        grid=parse("""
ST .. o. .. B2 .. o. .. K2 ..
.. ## .. ## .. .. .. ## .. o.
o. .. MW .. o. K1 +2 .. .. ..
.. ## .. +3 .. .. .. ## B1 ..
o. .. B? .. o. .. o. .. .. o.
.. o. .. .. ## W1 ## .. o. ..
+? ## o. .. W1 EX W1 .. ## ##
.. .. K1 .. ## W1 ## o. W2 DB
o. ## B1 .. o. .. o. .. ## DB
.. .. o. +3 .. o. o. .. ## ##
"""),
    ),
    dict(
        num=5,
        name="THE SORTING ROOM",
        concept="AI: how the site's old AI sorts things, and when it gets it wrong",
        grid=parse("""
EX o. .. ## o. .. DB ## o. ..
.. .. Mh .. .. ## .. o. .. +?
FA .. ## o. .. Mg .. ## ## ..
.. B? .. .. ## .. o. .. .. o.
.. .. ## Mf .. .. ## Me ## ..
o. .. +2 .. o. ## .. .. .. FA
## Md ## .. .. B? o. ## .. ##
.. .. .. +2 ## .. .. Mc .. o.
o. .. ## .. .. o. ## .. ## ..
.. Mb .. o. ## .. Ma o. .. ST
"""),
    ),
]


def encode(word, shift):
    return "".join(chr((ord(ch) - 65 + shift) % 26 + 65) for ch in word)
