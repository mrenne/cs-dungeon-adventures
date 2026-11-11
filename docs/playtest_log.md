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
| 1 | 9 | 19 | 0% |
| 2 | 9 | 19 | 0% |
| 3 | 11 | 22 | 0% |
| 4 | 9 | 19 | 0% |
| 5 | 9 | 20 | 0% |

Whole game, without the shop: 0.44 crashes on average, 58% of games with no crash, median final DATA 31.
Shop prices and rank thresholds are untested.

Game 2 (Dungeon 2 – The Smartphone), same settings:

| Floor | Median turns | Slowest 10% | Stuck |
|---|---|---|---|
| 1 | 6 | 17 | 0.1% |
| 2 | 7 | 17 | 0% |
| 3 | 11 | 23 | 0% |
| 4 | 14 | 29 | 0.9% |
| 5 | 9 | 20 | 0% |

Whole game, without the shop: 0.34 crashes on average, 67% of games with no crash, median final DATA 34.
Floor 4 has an exception (awaiting review): its slowest 10% may take up to 30 turns, because it needs four stops in order.
