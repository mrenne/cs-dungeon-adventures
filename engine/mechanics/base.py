"""The interface every floor mechanic implements.

A mechanic is one computer science idea turned into squares on a map. It owns everything about
that idea: how its squares look, its legend lines, its rule panel, how the playtest resolves
its squares, and its lines in the teacher answer key. Floors choose a mechanic by name.
"""


class Mechanic:
    name = ""        # registry key used in game.py: mechanic="programs"
    key_title = ""   # heading for this floor on the teacher answer key

    # ---- booklet ----
    def legend(self, floor):
        """Extra legend lines after the engine's: [(token, html), ...]."""
        return []

    def icon(self, c, t, x, y, s, floor):
        """Draw a mechanic token. Called inside saveState/restoreState with black fill and stroke."""

    def is_background(self, t):
        """Tokens that fill the whole square and are drawn under the grid lines (like walls)."""
        return False

    def bug_text(self, digit):
        """How bug strength is printed on this floor."""
        return digit

    def rule_panel(self, c, floor, x, yt, w, h):
        """The FLOOR RULE panel at the top of the floor page."""

    def answer_key(self, floor):
        """HTML lines for the teacher page."""
        return ""

    # ---- playtest ----
    def start(self, run):
        """Set up any per-floor state on the run (for example a variable)."""

    def interact(self, run, t):
        """Resolve a mechanic token the first time it is crossed.
        Return None, or 'stop' / 'program' to end the move like the engine's squares do."""

    def program_steps(self, run, name):
        """Directions a program square moves the player, worked out from where they stand."""
        from ..grid import expand
        return expand(run.f["programs"][name])

    def after_move(self, run):
        """Called where a move ends, before the exit check (for example, squares that count when touched)."""

    def can_exit(self, run):
        """False while the RUN square is still closed (for example, a task is unfinished)."""
        return True

    def targets(self, run):
        """Squares a planning player should head for before the exit, or None."""
        return None

    def exit_key(self, floor):
        """Key the player must hold before heading for the exit, or None."""
        return None

    def on_leave(self, run):
        """Bonuses applied when the floor ends."""

    # ---- checks ----
    def validate(self, floor):
        """Raise if the floor's data is inconsistent (run when a game loads)."""
