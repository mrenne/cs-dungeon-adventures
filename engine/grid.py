"""Map grids shared by every game.

Grid tokens (10 x 10, columns A-J, rows 1-10). The engine handles these in every game:
  ##  wall            ..  empty          ST  start         EX  exit (RUN)
  o.  data packet     DB  database       Bn  bug, n damage B?  mystery bug
  +n  power-up        +?  mystery power  MW  malware       FA  function call pair
  Kn  key n           Ln  locked door, a wall until you hold key n
Every other token belongs to the floor's mechanic (see engine/mechanics).
"""

SIZE = 10
COLS = "ABCDEFGHIJ"


def parse(grid):
    rows = [r.split() for r in grid.strip().splitlines()]
    assert len(rows) == SIZE and all(len(r) == SIZE for r in rows), "grid must be 10x10"
    return rows


def coord(r, c):
    return f"{COLS[c]}{r + 1}"


def find(grid, token):
    """All (row, col) positions holding token."""
    return [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == token]


def tokens(grid):
    return {t for row in grid for t in row}


# Programs: a step is 'U','D','L','R' or ('rep', n, [steps]).
def expand(program):
    out = []
    for step in program:
        if isinstance(step, tuple):
            out += expand(step[2]) * step[1]
        else:
            out.append(step)
    return out
