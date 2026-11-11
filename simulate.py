"""Monte-Carlo playtest of the Computer Science Crawler floors using the printed movement rules."""
import copy
import random
import statistics
import sys
from collections import deque

from floors import FLOORS, FORCE_COST, SIZE, coord, expand, scan

ORTH = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
DIAG = {"UL": (-1, -1), "UR": (-1, 1), "DL": (1, -1), "DR": (1, 1)}
ALL = {**ORTH, **DIAG}
MAX_TURNS = 60


def opposite(d):
    return d.translate(str.maketrans("UDLR", "DURL"))


class Run:
    def __init__(self, floor, rng, greedy=0.0):
        self.f, self.g, self.rng, self.greedy = floor, floor["grid"], rng, greedy
        self.used, self.keys = set(), set()
        self.ram_plus = self.ram_minus = self.data_plus = self.data_minus = 0
        self.x = floor.get("x_start", 0)
        self.last = None
        self.turns = 0
        self.done = False
        self.visited = set()
        for r in range(SIZE):
            for c in range(SIZE):
                if self.g[r][c] == "ST":
                    self.pos = (r, c)
                if self.g[r][c] == "EX":
                    self.exit = (r, c)

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

    def dist_map(self, target):
        dist = {target: 0}
        q = deque([target])
        while q:
            p = q.popleft()
            for d in ALL:
                n = self.step(p, d)
                if n not in dist and self.passable(n):
                    dist[n] = dist[p] + 1
                    q.append(n)
        return dist

    def goal(self):
        dm = self.dist_map(self.exit)
        needs_key = self.f["num"] == 4 and "1" not in self.keys
        if self.pos in dm and not needs_key:
            return dm
        best = None
        for r in range(SIZE):
            for c in range(SIZE):
                t = self.g[r][c]
                if t[0] == "K" and t[1] not in self.keys and (t[1] == "1" or not needs_key):
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
            return "exit"
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
        elif t[0] == "P":
            return "program"
        elif t[0] == "A":
            self.x += int(t[1])
        elif t == "X2":
            self.x *= 2
        elif t == "Z0":
            self.x = 0
        elif t == "I1":
            if self.x > 3:
                self.ram_plus += 3
            else:
                self.ram_minus += 2
        elif t == "I2":
            if self.x % 2 == 0:
                self.data_plus += 4
            else:
                self.ram_minus += 1
        elif t[0] == "C":
            self.data_plus += int(t[1])
        elif t[0] == "W":
            if t[1] not in self.keys:
                self.ram_minus += FORCE_COST
        elif t[0] == "K":
            self.keys.add(t[1])
        elif t[0] == "M":
            _, stat, amt = scan(t)
            if stat == "data":
                self.data_plus += amt
            elif amt > 0:
                self.ram_plus += amt
            else:
                self.ram_minus -= amt
        return None

    def teleport(self, p):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.g[r][c] == "FA" and (r, c) != p:
                    return (r, c)

    def run_program(self, name):
        for d in expand(self.f["programs"][name]):
            n = self.step(self.pos, d)
            if not self.passable(n):
                raise ValueError(f"program {name} hits a wall at {coord(*n)}")
            self.pos, self.last = n, d
            res = self.interact(n)
            if res == "exit":
                self.done = True
                return
            if res == "stop":
                return

    def turn(self):
        self.turns += 1
        n = self.roll()
        if self.f["num"] == 3:
            pass  # roll tally is bookkeeping only
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
            if res == "teleport":
                first = nxt not in self.used
                self.used.add(nxt)
                if first or self.rng.random() < 0.5:
                    self.pos = self.teleport(nxt)
                    self.used.add(self.pos)
        if self.done:
            return
        if max(abs(self.pos[0] - self.exit[0]), abs(self.pos[1] - self.exit[1])) <= 1:
            self.done = True

    def play(self):
        while not self.done and self.turns < MAX_TURNS:
            self.turn()
        if self.f["num"] == 2:
            self.data_plus += self.x
        if self.f["num"] == 3:
            self.data_plus += 2
        return self


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def report(n=1500, greedy=0.8, seed=1):
    rng = random.Random(seed)
    print(f"{n} runs per floor, player steers toward the exit {int(greedy*100)}% of choices\n")
    print("floor  turns(med/p90)  stuck%  RAM net(mean/p10)  DATA net(mean)  squares seen")
    for f in FLOORS:
        runs = [Run(f, rng, greedy).play() for _ in range(n)]
        turns = [r.turns for r in runs]
        ram = [r.ram_plus - r.ram_minus for r in runs]
        data = [r.data_plus - r.data_minus for r in runs]
        stuck = sum(not r.done for r in runs) / n * 100
        seen = statistics.mean(len(r.visited) for r in runs)
        print(f"  {f['num']}    {statistics.median(turns):4.0f} / {pct(turns, .9):3d}     {stuck:4.1f}"
              f"     {statistics.mean(ram):+5.1f} / {pct(ram, .1):+3d}        {statistics.mean(data):+5.1f}"
              f"          {seen:4.0f}")

    crashes, finals = [], []
    for _ in range(n):
        ram, data, c = 10, 0, 0
        for f in FLOORS:
            r = Run(f, rng, greedy).play()
            ram = min(10, ram + r.ram_plus - r.ram_minus)
            data = max(0, data + r.data_plus - r.data_minus)
            if ram <= 0:
                c, ram, data = c + 1, 10, 0
        crashes.append(c)
        finals.append(data)
    print(f"\nwhole game (no shop): mean crashes {statistics.mean(crashes):.2f}, "
          f"no-crash games {sum(c == 0 for c in crashes) / n * 100:.0f}%, "
          f"final DATA median {statistics.median(finals):.0f}")


if __name__ == "__main__":
    g = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
    report(greedy=g)
