"""Computer Science Crawler series engine: shared rules, drawing, mechanics and playtesting.

A game is a folder under games/ holding a game.py that defines GAME (see games/01_crawler/game.py).
"""
import importlib.util
from pathlib import Path

from . import mechanics

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "games"


def game_dirs():
    return sorted(p for p in GAMES.iterdir() if (p / "game.py").exists())


def load_game(folder):
    """Load games/<folder>/game.py and attach each floor's mechanic object."""
    folder = Path(folder)
    if not folder.is_absolute() and not folder.exists():
        folder = GAMES / folder
    spec = importlib.util.spec_from_file_location(f"game_{folder.name}", folder / "game.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    game = mod.GAME
    game["dir"] = folder
    for floor in game["floors"]:
        floor["mech"] = mechanics.get(floor["mechanic"])
        floor["mech"].validate(floor)
    return game
