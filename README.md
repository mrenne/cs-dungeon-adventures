# Computer Science Crawler series

Unplugged, paper-based computer science games for grades 6–10. Students play solo with a pre-printed
booklet, one six-sided die and a pencil. No devices needed. The series is planned at about 10 games, each
organised around five domains: Algorithms & Design, Programming, Data & Analysis, Systems & Security, and
Computing & Society (with AI integrated across domains).

## Games

| # | Game | Booklet | Status |
|---|---|---|---|
| 1 | Computer Science Crawler | [PDF](games/01_crawler/Computer_Science_Crawler_Booklet.pdf) | Built; not yet classroom tested |

**Game 1.** You are a brand-new web crawler bot, sent to index an old website five floors deep before it shuts
down on Friday.

| Floor | Name | Domain |
|---|---|---|
| 1 | The Home Page | Algorithms & Design: sequences and loops |
| 2 | The Source Code | Programming: variables and IF / ELSE |
| 3 | The Database | Data & Analysis: binary numbers |
| 4 | The Login Page | Systems & Security: passwords, keys and ciphers |
| 5 | The Sorting Room | Computing & Society: how an AI sorts, and when it gets it wrong |

Each booklet is 9 pages, US Letter, black and white: a cover and tracker, how to play, five floors, a shop and
ranks page, and a teacher answer key.

## How the project is organised

```
engine/                 shared by every game
  grid.py               map format and the squares every game uses
  draw.py               icons, map, tracker, legend, panels
  booklet.py            page layouts and the core rules text
  simulate.py           Monte-Carlo playtest of the printed movement rules
  mechanics/            one file per CS mechanic (programs, variables, binary, cipher, sorting_ai)
games/
  01_crawler/game.py    everything specific to Game 1: story, floors, maps, shop, ranks, teacher notes
docs/
  series_plan.md        the 10 games mapped against the five domains
  mechanics.md          catalogue of mechanics, and open rule questions
  style_guide.md        play, print, writing and balance rules for every booklet
  playtest_log.md       real classroom results
build.py                builds and checks every game
```

A game folder contains only data. Rules, drawing and playtesting live in the engine, so a fix there reaches every
game. The same game files can later drive the website and a digital version.

## Building

Requires Python 3 and reportlab.

```bash
pip install reportlab
python build.py                  # build every booklet
python build.py 01_crawler       # build one game
python build.py --playtest       # build, then playtest every floor and fail if a floor misses the pass marks
```

Loading a game also checks its data: for example, that every program stays on the map and every key has a password.

## Adding a game

1. Copy `games/01_crawler` to `games/NN_name` and edit `game.py`.
2. Each floor picks a mechanic by name. A new CS idea gets a new file in `engine/mechanics/` (see `docs/mechanics.md`).
3. Run `python build.py NN_name --playtest` and look at every page of the PDF.
4. Add the game to the table above and to `docs/series_plan.md`.
