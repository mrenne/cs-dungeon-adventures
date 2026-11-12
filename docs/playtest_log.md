# Playtest log

Record every real classroom session here. The simulation proves floors are finishable; only real students
show whether the rules are clear and the timing works.

## Template

```
### Game N, YYYY-MM-DD, grade X, N students
- Session length / floors finished:
- Rules students misread:
- Squares or puzzles that caused disputes at code review:
- Crashes and final DATA (rough spread):
- Changes to make:
```

## Sessions

None yet. Game 1 (Dungeon 1 – The Web) has only been playtested by simulation (1500 runs per floor, 80% steering):

| Floor | Median turns | Slowest 10% | Stuck |
|---|---|---|---|
| 1 | 9 | 20 | 0% |
| 2 | 9 | 20 | 0.1% |
| 3 | 11 | 22 | 0% |
| 4 | 9 | 19 | 0% |
| 5 | 9 | 19 | 0.1% |

Whole game, without the shop: 0.43 crashes on average, 59% of games with no crash, median final DATA 32.
Shop prices and rank thresholds are untested. Numbers updated 2026-11-11 after function squares became mandatory every visit.

Game 2 (Dungeon 2 – The Smartphone), same settings:

| Floor | Median turns | Slowest 10% | Stuck |
|---|---|---|---|
| 1 | 6 | 17 | 0.1% |
| 2 | 7 | 16 | 0% |
| 3 | 11 | 22 | 0% |
| 4 | 14 | 29 | 0.9% |
| 5 | 9 | 19 | 0.1% |

Whole game, without the shop: 0.35 crashes on average, 66% of games with no crash, median final DATA 35.
Floor 2: the malware square sits on P3's loop route (F9), so a program gets stopped partway through.
Floor 4 has an exception (awaiting review): its slowest 10% may take up to 30 turns, because it needs four stops in order.
