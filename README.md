<p align="center"><img src="assets/cs-offline-logo.jpg" alt="Computer Science Offline" width="560"></p>

# Computer Science Dungeon Adventures

Part of the **Computer Science (CS) Offline** project.

Unplugged, paper-based computer science games for grades 6–10. Students play solo with a pre-printed
booklet, one six-sided die and a pencil. No devices needed. The series is planned at about 10 games, each
organised around five domains: Algorithms & Design, Programming, Data & Analysis, Systems & Security, and
Computing & Society (with AI integrated across domains).

## Games

| # | Game | Booklet | Status |
|---|---|---|---|
| 1 | Dungeon 1 – The Web | [PDF](games/01_web/Dungeon_1_The_Web_Booklet.pdf) | Built; not yet classroom tested |
| 2 | Dungeon 2 – The Smartphone | [PDF](games/02_smartphone/Dungeon_2_The_Smartphone_Booklet.pdf) | Built; not yet classroom tested |

**Dungeon 1 – The Web.** You are a brand-new adventurer, a bot that works like a web crawler, sent to index an old website five floors deep before it shuts
down on Friday.

| Floor | Name | Domain |
|---|---|---|
| 1 | The Home Page | Algorithms & Design: sequences and loops |
| 2 | The Source Code | Programming: variables and IF / ELSE |
| 3 | The Database | Data & Analysis: binary numbers |
| 4 | The Login Page | Systems & Security: passwords, keys and ciphers |
| 5 | The Sorting Room | Computing & Society: how an AI sorts, and when it gets it wrong |

**Dungeon 2 – The Smartphone.** The adventurer goes inside a smartphone that has been acting strangely: The Lock Screen (flowcharts),
The App Store (REPEAT UNTIL loops), The Camera Roll (pixels), The Battery and Chip (input, processing,
storage, output) and The Photo Sorter (training an AI, and how a skewed sample skews it).

Each booklet is 9 pages, US Letter, black and white: a cover and tracker, how to play, five floors, a shop and
ranks page, and a teacher answer key.

## How the project is organised

```
engine/                 shared by every game
  grid.py               map format and the squares every game uses
  draw.py               icons, map, tracker, legend, panels
  booklet.py            page layouts and the core rules text
  simulate.py           Monte-Carlo playtest of the printed movement rules
  mechanics/            one file per CS mechanic (Game 1: programs, variables, binary, cipher, sorting_ai;
                        Game 2: flowchart, until_loops, pixels, hardware, training)
games/
  01_web/game.py    everything specific to Game 1: story, floors, maps, shop, ranks, teacher notes
  02_smartphone/game.py Game 2
docs/
  series_plan.md        the 10 games mapped against the five domains
  mechanics.md          catalogue of mechanics, and open rule questions
  style_guide.md        play, print, writing and balance rules for every booklet
  playtest_log.md       real classroom results
assets/                 Computer Science (CS) Offline logos (README and booklet covers)
build.py                builds and checks every game
```

A game folder contains only data. Rules, drawing and playtesting live in the engine, so a fix there reaches every
game. The same game files can later drive the website and a digital version.

## Building

Requires Python 3 and reportlab.

```bash
pip install reportlab
python build.py                  # build every booklet
python build.py 01_web       # build one game
python build.py --playtest       # build, then playtest every floor and fail if a floor misses the pass marks
```

Loading a game also checks its data: for example, that every program stays on the map and every key has a password.

## Adding a game

1. Copy `games/01_web` to `games/NN_name` and edit `game.py`.
2. Each floor picks a mechanic by name. A new CS idea gets a new file in `engine/mechanics/` (see `docs/mechanics.md`).
3. Run `python build.py NN_name --playtest` and look at every page of the PDF.
4. Add the game to the table above and to `docs/series_plan.md`.

## Licence

This project uses two licences, both © 2026 Mike Renne:

| What | Licence | File |
|---|---|---|
| **Software:** `build.py` and `engine/` | [MIT](https://opensource.org/licenses/MIT) | [LICENSE](LICENSE) |
| **Booklets and game content:** `games/` (the booklet PDFs and each game's `game.py`: stories, maps and puzzles) and `docs/` | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) | [LICENSE-BOOKLETS](LICENSE-BOOKLETS) |

The Computer Science (CS) Offline logos in `assets/` are not covered by either licence.

You can reuse the engine for anything, including commercial projects, as long as you keep the copyright notice.
You may copy, print and adapt the booklets for non-commercial use, such as in classrooms, as long as you credit
the author and share any adapted versions under the same licence.
