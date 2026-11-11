# Mechanics catalogue

A **mechanic** is one computer science idea turned into squares on a map. Each one is a file in
[`engine/mechanics/`](../engine/mechanics) and owns everything about that idea: its icons, legend lines,
rule panel, how the playtest resolves its squares, and its lines on the teacher answer key.
A floor picks one with `mechanic="name"` in its game file.

## Engine squares (every floor)

| Token | Square | Effect |
|---|---|---|
| `##` | Wall | Blocks movement |
| `ST` / `EX` | Start / exit (RUN) | Exit by stopping on, next to (corners count) or passing over RUN |
| `o.` | Data | +1 DATA |
| `DB` | Database | Roll, gain that much DATA |
| `Bn` / `B?` | Bug / mystery bug | Lose n RAM / roll and lose that RAM |
| `+n` / `+?` | Power-up / mystery power-up | Gain n RAM / roll and gain that RAM |
| `MW` | Malware | Stop. Roll, lose that much DATA |
| `FA` | Function call pair | Jump to the other f( ) and keep moving |
| `Kn` / `Ln` | Key / locked door | A door is a wall until you hold its key |

## Mechanics

| Name | Domain | Concept | Tokens | Floor data | Used in |
|---|---|---|---|---|---|
| `programs` | Algorithms & Design | Sequences, loops, tracing | `Pn` | `programs` | Game 1, Floor 1 |
| `variables` | Programming | Variables, assignment, IF / ELSE | `A1 A3 X2 Z0 I1 I2` | `x_start` | Game 1, Floor 2 |
| `binary` | Data & Analysis | Binary numbers, data collection (roll log) | `Cn`, binary `Bn`, `Kn Ln` | none | Game 1, Floor 3 |
| `cipher` | Systems & Security | Authentication, Caesar cipher, cost of weak defences | `Kn Wn` | `cipher`, `force_cost` | Game 1, Floor 4 |
| `sorting_ai` | Computing & Society | Decision-tree classification and bias | `Ma`–`Mh` | `bots` | Game 1, Floor 5 |

**Fixed for now:** the variable mechanic's code squares and IF rules, the binary roll-log bonus and the
sorting AI's tree are written into their mechanic files. Make them floor data when a game needs different ones.

## Adding a mechanic

1. Copy the closest mechanic file in `engine/mechanics/` and subclass `Mechanic` (see `base.py` for every hook).
2. Pick tokens that don't clash with the engine squares above.
3. Register it in `engine/mechanics/__init__.py`.
4. Add a row to the table above.
5. Run `python build.py --playtest` and look at every page.

## Open rule questions (engine-wide, decide before Game 2)

- Are function squares mandatory every time, or only the first time? The playtest currently jumps on the
  first visit and half the time after that.
- Does malware stop a program partway through? The playtest currently stops it.
- Are leftover squares from a roll lost when you land on a program square? The playtest currently drops them.
