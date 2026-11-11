"""Build and check the games in the series.

  python build.py                    build every game's booklet
  python build.py 01_crawler         build one game
  python build.py --playtest         build, then playtest every floor and fail if any floor misses the pass marks
  python build.py 01_crawler --playtest --runs 500 --steer 0.8
"""
import argparse
import sys

from engine import game_dirs, load_game
from engine.booklet import build
from engine.simulate import report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("games", nargs="*", help="game folders under games/ (default: all)")
    ap.add_argument("--playtest", action="store_true", help="run the Monte-Carlo playtest after building")
    ap.add_argument("--runs", type=int, default=1500, help="playtest runs per floor (default 1500)")
    ap.add_argument("--steer", type=float, default=0.8,
                    help="how often the simulated player steers toward the exit, 0-1 (default 0.8)")
    args = ap.parse_args()

    folders = args.games or [p.name for p in game_dirs()]
    ok = True
    for name in folders:
        game = load_game(name)  # loading also validates every floor's data
        print("wrote", build(game).relative_to(game["dir"].parent.parent))
        if args.playtest:
            ok &= report(game, n=args.runs, greedy=args.steer)
            print()
    if not ok:
        print("PLAYTEST FAILED: see FAIL lines above")
        sys.exit(1)


if __name__ == "__main__":
    main()
