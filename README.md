# Computer Science Crawler

An unplugged, paper-based computer science game for grades 6–10. Students play solo with a pre-printed booklet, one six-sided die and a pencil — no devices needed.

You are a brand-new web crawler bot, sent to index an old website five floors deep before it shuts down on Friday. Each floor teaches one area of computer science through its mechanics:

| Floor | Name | Domain |
|---|---|---|
| 1 | The Home Page | Algorithms & Design: sequences and loops |
| 2 | The Source Code | Programming: variables and IF / ELSE |
| 3 | The Database | Data & Analysis: binary numbers |
| 4 | The Login Page | Systems & Security: passwords, keys and ciphers |
| 5 | The Sorting Room | Computing & Society: how an AI sorts, and when it gets it wrong |

The printable booklet is [`Computer_Science_Crawler_Booklet.pdf`](Computer_Science_Crawler_Booklet.pdf) (9 pages, US Letter, black and white): cover and tracker, how to play, five floors, shop and ranks, and a teacher answer key.

## Files

- `floors.py` — the maps and floor data (single source of truth)
- `build_booklet.py` — draws the booklet PDF
- `simulate.py` — Monte-Carlo playtest of every floor using the printed rules

## Building

Requires Python 3 and reportlab.

```bash
pip install reportlab
python build_booklet.py      # writes Computer_Science_Crawler_Booklet.pdf
python simulate.py 0.8       # playtest: 0.8 = player steers toward the exit 80% of the time
```
