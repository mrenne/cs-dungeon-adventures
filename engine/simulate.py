"""Monte-Carlo playtest of a game's floors using the printed movement rules.

The engine resolves its own squares here; anything else is handed to the floor's mechanic.
"""
import copy
import random
import statistics
from collections import deque

from .grid import SIZE, coord, find

ORTH = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
DIAG = {"UL": (-1, -1), "UR": (-1, 1), "DL": (1, -1), "DR": (1, 1)}
ALL = {**ORTH, **DIAG}
MAX_TURNS = 60

# Pass marks a floor must meet in build.py --playtest
LIMITS = dict(stuck_pct=2.0, median_turns=(6, 14), p90_turns=25)


def opposite(d):
    return d.translate(str.maketrans("UDLR", "DURL"))


class Run:
    def __init__(self, floor, rng, greedy=0.0):
        self.f, self.g, self.rng, self.greedy = floor, floor["grid"], rng, greedy
        self.mech = floor["mech"]
        self.used, self.keys = set(), set()
        self.ram_plus = self.ram_minus = self.data_plus = self.data_minus = 0
        self.last = None
        self.turns = 0
        self.done = False
        self.visited = set()
        self.pos = find(self.g, "ST")[0]
        self.exit = find(self.g, "EX")[0]
        self.exit_key = self.mech.exit_key(floor)
        self.mech.start(self)

    def roll(self):
        return self.rng.randint(1, 6)

    def passable(self, p, keys=None):
        r, c = p
        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return False
        t = self.g[r][c]
        if t == "##":
            return False
        if t[0] == "L":
            return t[1] in (self.keys if keys is None else keys)
        return True

    def step(self, p, d):
        return (p[0] + ALL[d][0], p[1] + ALL[d][1])

    def dist_map(self, *targets):
        dist = {t: 0 for t in targets}
        q = deque(targets)
        while q:
            p = q.popleft()
            for d in ALL:
                n = self.step(p, d)
                if n not in dist and self.passable(n):
                    dist[n] = dist[p] + 1
                    q.append(n)
        return dist

    def goal(self):
        """Distance map toward the exit, or toward the nearest useful key if the exit needs one."""
        targets = self.mech.targets(self)
        if targets:
            return self.dist_map(*targets)
        dm = self.dist_map(self.exit)
        needs_key = self.exit_key is not None and self.exit_key not in self.keys
        if self.pos in dm and not needs_key:
            return dm
        best = None
        for r in range(SIZE):
            for c in range(SIZE):
                t = self.g[r][c]
                if t[0] == "K" and t[1] not in self.keys and (t[1] == self.exit_key or not needs_key):
                    km = self.dist_map((r, c))
                    if self.pos in km and (best is None or km[self.pos] < best[self.pos]):
                        best = km
        return best or dm

    def pick(self, options):
        if self.greedy and self.rng.random() < self.greedy:
            dm = self.goal()
            return min(options, key=lambda d: dm.get(self.step(self.pos, d), 99) + self.rng.random() * 0.1)
        return self.rng.choice(options)

    def plan(self, options, n):
        """Preview where each starting direction ends up; pick the one nearest the goal."""
        dm = self.goal()
        best, best_score = None, None
        for d in options:
            ghost = copy.copy(self)
            ghost.used, ghost.keys, ghost.visited = set(self.used), set(self.keys), set(self.visited)
            ghost.rng = random.Random(0)
            ghost.greedy = 1.0
            ghost.move(n, d)
            score = -1 if ghost.done else dm.get(ghost.pos, 99)
            score += self.rng.random() * 0.1
            if best_score is None or score < best_score:
                best, best_score = d, score
        return best

    def interact(self, p):
        """Returns 'stop', 'program', 'teleport', 'exit' or None."""
        self.visited.add(p)
        t = self.g[p[0]][p[1]]
        if t == "EX":
            return "exit" if self.mech.can_exit(self) else None
        if t == "FA":
            return "teleport"
        if p in self.used or t in ("..", "ST"):
            return None
        self.used.add(p)
        if t == "o.":
            self.data_plus += 1
        elif t == "DB":
            self.data_plus += self.roll()
        elif t[0] == "B":
            self.ram_minus += self.roll() if t[1] == "?" else int(t[1])
        elif t[0] == "+":
            self.ram_plus += self.roll() if t[1] == "?" else int(t[1])
        elif t == "MW":
            self.data_minus += self.roll()
            return "stop"
        elif t[0] == "K":
            self.keys.add(t[1])
            return self.mech.interact(self, t)
        else:
            return self.mech.interact(self, t)
        return None

    def teleport(self, p):
        return next(q for q in find(self.g, "FA") if q != p)

    def run_program(self, name):
        for d in self.mech.program_steps(self, name):
            n = self.step(self.pos, d)
            if not self.passable(n):
                raise ValueError(f"program {name} hits a wall at {coord(*n)}")
            self.pos, self.last = n, d
            res = self.interact(n)
            if res == "exit":
                self.done = True
                return
            if res == "stop":  # malware stops a program partway through
                return
            if res == "teleport":
                self.pos = self.teleport(n)

    def turn(self):
        self.turns += 1
        n = self.roll()
        dirs = list(DIAG if n % 2 else ORTH)
        back = opposite(self.last) if self.last else None
        ok = [d for d in dirs if self.passable(self.step(self.pos, d))]
        fwd = [d for d in ok if d != back]

        def clear(d):
            p = self.pos
            for _ in range(n):
                p = self.step(p, d)
                if not self.passable(p):
                    return False
            return True

        full = [d for d in fwd if clear(d)]
        options = full or fwd or ok
        if not options:
            return
        if self.greedy and self.rng.random() < self.greedy:
            cur = self.plan(options, n)
        else:
            cur = self.rng.choice(options)
        self.move(n, cur)

    def move(self, n, cur):
        dirs = list(DIAG if n % 2 else ORTH)
        steps = 0
        while steps < n:
            nxt = self.step(self.pos, cur)
            if not self.passable(nxt):
                alt = [d for d in dirs if d != cur and self.passable(self.step(self.pos, d))]
                keep = [d for d in alt if d != opposite(cur)]
                if not (keep or alt):
                    break
                cur = self.pick(keep or alt)
                continue
            self.pos, self.last = nxt, cur
            steps += 1
            res = self.interact(nxt)
            if res == "exit":
                self.done = True
                return
            if res == "stop":
                break
            if res == "program":
                self.run_program(self.g[nxt[0]][nxt[1]])
                break
            if res == "teleport":  # function squares jump you every time
                self.pos = self.teleport(nxt)
        if self.done:
            return
        self.mech.after_move(self)
        if max(abs(self.pos[0] - self.exit[0]), abs(self.pos[1] - self.exit[1])) <= 1 and self.mech.can_exit(self):
            self.done = True

    def play(self):
        while not self.done and self.turns < MAX_TURNS:
            self.turn()
        self.mech.on_leave(self)
        return self


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def floor_stats(floor, rng, n, greedy):
    runs = [Run(floor, rng, greedy).play() for _ in range(n)]
    turns = [r.turns for r in runs]
    return dict(
        median_turns=statistics.median(turns),
        p90_turns=pct(turns, .9),
        stuck_pct=sum(not r.done for r in runs) / n * 100,
        ram_mean=statistics.mean(r.ram_plus - r.ram_minus for r in runs),
        ram_p10=pct([r.ram_plus - r.ram_minus for r in runs], .1),
        data_mean=statistics.mean(r.data_plus - r.data_minus for r in runs),
        seen=statistics.mean(len(r.visited) for r in runs),
    )


def check(stats, floor=None):
    """List of reasons a floor fails the pass marks (empty = pass).
    A floor can loosen a mark with playtest_limits=dict(...); say why in a comment there."""
    limits = {**LIMITS, **(floor or {}).get("playtest_limits", {})}
    lo, hi = limits["median_turns"]
    fails = []
    if stats["stuck_pct"] > limits["stuck_pct"]:
        fails.append(f"{stats['stuck_pct']:.1f}% of players never reached the exit")
    if not lo <= stats["median_turns"] <= hi:
        fails.append(f"median {stats['median_turns']:.0f} turns is outside {lo}-{hi}")
    if stats["p90_turns"] > limits["p90_turns"]:
        fails.append(f"slowest 10% took {stats['p90_turns']} turns (limit {limits['p90_turns']})")
    return fails


def report(game, n=1500, greedy=0.8, seed=1):
    """Print the playtest table for every floor plus a whole-game run. Returns True if every floor passes."""
    rng = random.Random(seed)
    print(f"{game['title']}: {n} runs per floor, player steers toward the exit {int(greedy*100)}% of choices\n")
    print("floor  turns(med/p90)  stuck%  RAM net(mean/p10)  DATA net(mean)  squares seen")
    passed = True
    for f in game["floors"]:
        s = floor_stats(f, rng, n, greedy)
        fails = check(s, f)
        passed &= not fails
        print(f"  {f['num']}    {s['median_turns']:4.0f} / {s['p90_turns']:3d}     {s['stuck_pct']:4.1f}"
              f"     {s['ram_mean']:+5.1f} / {s['ram_p10']:+3d}        {s['data_mean']:+5.1f}"
              f"          {s['seen']:4.0f}" + ("" if not fails else "   FAIL: " + "; ".join(fails)))

    st = game["start"]
    crashes, finals = [], []
    for _ in range(n):
        ram, data, c = st["ram"], st["data"], 0
        for f in game["floors"]:
            r = Run(f, rng, greedy).play()
            ram = min(st["max_ram"], ram + r.ram_plus - r.ram_minus)
            data = max(0, data + r.data_plus - r.data_minus)
            if ram <= 0:
                c, ram, data = c + 1, st["ram"], st["data"]
        crashes.append(c)
        finals.append(data)
    print(f"\nwhole game (no shop): mean crashes {statistics.mean(crashes):.2f}, "
          f"no-crash games {sum(c == 0 for c in crashes) / n * 100:.0f}%, "
          f"final DATA median {statistics.median(finals):.0f}")
    return passed
