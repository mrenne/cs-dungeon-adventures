"""Game 1: Dungeon 1 – The Web. Everything specific to this game lives here; the engine draws it.

Map tokens are listed in engine/grid.py (shared) and engine/mechanics/*.py (per mechanic).
"""
from engine.grid import parse

GAME = dict(
    title="Dungeon 1 – The Web",
    pdf_title="Dungeon 1 – The Web (Computer Science Dungeon Adventures)",
    output="Dungeon_1_The_Web_Booklet.pdf",
    start=dict(ram=10, data=0, max_ram=10),

    cover=dict(
        title_lines=["DUNGEON 1:", "THE WEB"],
        subtitle="COMPUTER SCIENCE DUNGEON ADVENTURES",
        tagline="pencil  ·  paper  ·  one die",
        story="You are a brand-new <b>web crawler</b>: a bot that search engines send out to read the internet. "
              "Your first job is an old website, five floors deep, that shuts down forever on Friday. Crawl each "
              "floor, index its <b>DATA</b>, and survive the broken code that drains your <b>RAM</b>. Reach the "
              "RUN square to follow the link down to the next floor. One warning from the last crawler sent "
              "here: something at the bottom has been sorting visitors all wrong.",
        avatar="DRAW YOUR CRAWLER",
        fields=["Crawler name", "Real name", "Class", "Date started", "Date finished"],
        stat_notes="<b>RAM</b> is your energy. Broken code drains it.<br/><b>DATA</b> is what you index. "
                   "Spend it in the shop.<br/><b>MAX RAM</b> is the most RAM you can hold.",
        icons=["ST", "B2", "o.", "DB", "+2", "MW", "FA", "Ma", "Mb", "EX"],
    ),

    shop=dict(
        intro="Visit the shop twice: <b>after Floor 2</b> and <b>after Floor 4</b>. Pay with DATA. "
              "Write the price in the <b>– LOST</b> box for DATA on the next floor. "
              "You can buy each thing once per visit.",
        # (name, price, what it does, has a "used" box)
        items=[
            ("PATCH", 4, "Gain 4 RAM. Write +4 in the + GAINED box for RAM on the next floor.", False),
            ("DEBUGGER", 3, "Roll again once, on any roll you do not like.", True),
            ("ANTIVIRUS", 5, "Ignore one bug or one malware. Cross it out without losing anything.", True),
            ("RAM UPGRADE", 8, "Your Max RAM goes up by 2 for the rest of the game.", False),
        ],
    ),
    ranks=[("0 – 14", "Intern"), ("15 – 29", "Junior Coder"), ("30 – 44", "Senior Engineer"),
           ("45 +", "System Architect")],
    think_back=["Which floor puzzle was hardest? What made it hard?",
                "On Floor 5, was the sorting AI fair to every bot? Why or why not?",
                "Where have you seen one of these ideas in real life?"],

    teacher=(
        "<b>WHAT EACH FLOOR TEACHES</b><br/>"
        "1. Algorithms and Design: sequence, loops, tracing a program.<br/>"
        "2. Programming: variables, assignment, IF / ELSE.<br/>"
        "3. Data and Analysis: binary representation, collecting and summarising data (the roll log).<br/>"
        "4. Systems and Security: authentication, encryption, the cost of weak defences.<br/>"
        "5. Computing and Society (AI): classification with a decision tree, and bias from features a model "
        "was never trained on.<br/>"
        "Match these to your state or CSTA standard codes before use; the codes are not listed here.<br/><br/>"
        "<b>RUNNING IT</b><br/>"
        "• Each student needs a booklet, a pencil and a die. Print single-sided so nothing shows "
        "through the maps.<br/>"
        "• Teach the movement rules with Floor 1 on a projector or the board, playing 3 or 4 turns "
        "together.<br/>"
        "• In computer playtests a floor took about 9 to 11 turns, and 9 in 10 finished within 22. "
        "Real classroom timing is not yet tested: time your first session.<br/>"
        "• About 4 in 10 simulated players crashed at least once. A crash is a reset, not a loss.<br/>"
        "• Code review pairs replace teacher marking. Keep this page for disputes.<br/><br/>"
        "<b>DISCUSSION STARTERS</b><br/>"
        "1. A program square moved you without a die. What makes a program predictable?<br/>"
        "2. Did the order you crossed the code squares change x? Why?<br/>"
        "3. Was your most common roll the same as your partner's? What would a class-wide log show?<br/>"
        "4. Smashing a firewall cost RAM. What does a break-in cost a real organisation?<br/>"
        "5. The sorting AI hurt friendly square bots. Who is responsible when a model is unfair: the model, "
        "its training data, or the people who built it?"
    ),

    floors=[
        dict(
            num=1,
            name="THE HOME PAGE",
            concept="Algorithms: follow steps in order, repeat with loops",
            mechanic="programs",
            programs={
                "P1": ["R", "R", "U", "U"],
                "P2": [("rep", 2, ["D", "L"])],
                "P3": ["D", ("rep", 2, ["R"])],
            },
            grid=parse("""
ST .. o. o. ## DB .. o. B2 ..
.. o. ## .. ## .. o. ## .. o.
o. B1 ## P1 .. .. o. ## +2 ..
.. +2 .. o. ## ## .. .. o. ..
## ## o. .. B2 .. .. ## ## o.
FA .. .. ## o. P2 .. .. B? ..
o. .. +? ## o. .. ## o. .. o.
.. ## ## o. .. MW ## .. FA ..
o. B2 .. .. o. .. .. P3 ## ..
.. o. .. ## +3 o. .. .. o. EX
"""),
        ),
        dict(
            num=2,
            name="THE SOURCE CODE",
            concept="Programming: variables and IF / ELSE",
            mechanic="variables",
            x_start=1,
            grid=parse("""
o. .. .. MW .. o. .. .. +3 EX
.. .. B2 .. .. ## I2 o. .. FA
## o. ## ## A3 .. .. .. ## ..
+? .. .. o. .. Z0 ## B3 .. o.
.. o. ## .. ## .. +2 o. .. ..
FA .. A1 .. B? .. X2 .. ## DB
## ## .. ## ## o. ## .. o. ..
o. B1 .. .. I1 .. .. .. +2 ##
.. ## o. ## .. ## o. ## .. ..
ST o. .. ## o. A1 .. B2 .. o.
"""),
        ),
        dict(
            num=3,
            name="THE DATABASE",
            concept="Data: binary numbers, collecting and reading data",
            mechanic="binary",
            grid=parse("""
.. o. .. C3 ## .. B1 o. .. ST
o. ## ## .. ## o. ## .. ## o.
.. .. .. B2 .. .. .. K5 ## ..
+2 ## o. ## ## o. ## ## .. o.
.. .. +2 .. MW .. o. .. B3 ..
## o. ## C5 ## .. ## o. ## ##
.. B? .. .. .. +? .. .. L5 C8
o. ## .. .. o. .. ## o. ## ##
.. .. C6 .. .. .. B2 .. .. +3
.. EX .. o. ## o. .. ## .. o.
"""),
        ),
        dict(
            num=4,
            name="THE LOGIN PAGE",
            concept="Security: passwords, keys and secret codes",
            mechanic="cipher",
            cipher={"1": (1, "BYTE"), "2": (3, "CODE")},
            force_cost=2,
            grid=parse("""
ST .. o. .. B2 .. o. .. K2 ..
.. ## .. ## .. .. .. ## .. o.
o. .. MW .. o. K1 +2 .. .. ..
.. ## .. +3 .. .. .. ## B1 ..
o. .. B? .. o. .. o. .. .. o.
.. o. .. .. ## W1 ## .. o. ..
+? ## o. .. W1 EX W1 .. ## ##
.. .. K1 .. ## W1 ## o. W2 DB
o. ## B1 .. o. .. o. .. ## DB
.. .. o. +3 .. o. o. .. ## ##
"""),
        ),
        dict(
            num=5,
            name="THE SORTING ROOM",
            concept="AI: how the site's old AI sorts things, and when it gets it wrong",
            mechanic="sorting_ai",
            # bot: (square body, antenna, smiling)
            bots={
                "Ma": (True, True, False),
                "Mb": (False, True, True),
                "Mc": (True, False, True),
                "Md": (False, False, True),
                "Me": (True, True, True),
                "Mf": (False, True, False),
                "Mg": (True, False, False),
                "Mh": (False, False, True),
            },
            grid=parse("""
EX o. .. ## o. .. DB ## o. ..
.. .. Mh .. .. ## .. o. .. +?
FA .. ## o. .. Mg .. ## ## ..
.. B? .. .. ## .. o. .. .. o.
.. .. ## Mf .. .. ## Me ## ..
o. .. +2 .. o. ## .. .. .. FA
## Md ## .. .. B? o. ## .. ##
.. .. .. +2 ## .. .. Mc .. o.
o. .. ## .. .. o. ## .. ## ..
.. Mb .. o. ## .. Ma o. .. ST
"""),
        ),
    ],
)
