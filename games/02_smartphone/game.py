"""Game 2: Dungeon 2 – The Smartphone. Everything specific to this game lives here.

Map tokens are listed in engine/grid.py (shared) and engine/mechanics/*.py (per mechanic).
"""
from engine.grid import parse

GAME = dict(
    title="Dungeon 2 – The Smartphone",
    pdf_title="Dungeon 2 – The Smartphone (Computer Science Dungeon Adventures)",
    output="Dungeon_2_The_Smartphone_Booklet.pdf",
    start=dict(ram=10, data=0, max_ram=10),

    cover=dict(
        title_lines=["DUNGEON 2:", "THE SMARTPHONE"],
        subtitle="COMPUTER SCIENCE DUNGEON ADVENTURES",
        tagline="pencil  ·  paper  ·  one die",
        story="Your first crawl went so well that you have a new job: crawl <b>inside a smartphone</b>. Its "
              "owner says it has been acting strangely. The lock screen keeps looping, the camera roll is "
              "scrambled, and the photo app sorts pictures all wrong. Crawl five floors of the phone, index "
              "its <b>DATA</b>, and keep your <b>RAM</b> up. At the bottom, the photo app's AI is waiting to "
              "learn something new, and this time <b>you</b> are its teacher.",
        avatar="DRAW YOUR CRAWLER",
        fields=["Crawler name", "Real name", "Class", "Date started", "Date finished"],
        stat_notes="<b>RAM</b> is your energy. Broken code drains it.<br/><b>DATA</b> is what you index. "
                   "Spend it in the shop.<br/><b>MAX RAM</b> is the most RAM you can hold.",
        icons=["ST", "Q5", "o.", "P1", "C3", "HP", "B2", "Ma", "Mb", "EX"],
    ),

    shop=dict(
        intro="Visit the shop twice: <b>after Floor 2</b> and <b>after Floor 4</b>. Pay with DATA. "
              "Write the price in the <b>– LOST</b> box for DATA on the next floor. "
              "You can buy each thing once per visit.",
        # (name, price, what it does, has a "used" box)
        items=[
            ("CHARGER", 4, "Gain 4 RAM. Write +4 in the + GAINED box for RAM on the next floor.", False),
            ("UNDO", 3, "Roll again once, on any roll you do not like.", True),
            ("ANTIVIRUS", 5, "Ignore one bug or one malware. Cross it out without losing anything.", True),
            ("MEMORY CARD", 8, "Your Max RAM goes up by 2 for the rest of the game.", False),
        ],
    ),
    ranks=[("0 – 14", "App Tester"), ("15 – 29", "App Developer"), ("30 – 44", "Mobile Engineer"),
           ("45 +", "Chief Technology Officer")],
    think_back=["Which floor puzzle was hardest? What made it hard?",
                "On Floor 5, did your AI learn the right thing? What training data would have helped?",
                "Name one thing your real phone does that uses an idea from this booklet."],

    teacher=(
        "<b>WHAT EACH FLOOR TEACHES</b><br/>"
        "1. Algorithms and Design: flowcharts, decisions and a loop inside an algorithm, tracing.<br/>"
        "2. Programming: indefinite loops (REPEAT UNTIL), loop conditions, counting iterations.<br/>"
        "3. Data and Analysis: images as data, pixels and bits.<br/>"
        "4. Systems and Security: the input, processing, storage and output model of a computer.<br/>"
        "5. Computing and Society (AI): machine learning from labelled training data, and how a skewed "
        "sample produces a skewed model.<br/>"
        "Builds on Game 1 (loops, binary, the sorting AI) but does not require it. Match these to your "
        "state or CSTA standard codes before use; the codes are not listed here.<br/><br/>"
        "<b>RUNNING IT</b><br/>"
        "• Each student needs a booklet, a pencil and a die. Print single-sided.<br/>"
        "• If students have not played Game 1, teach the movement rules on the board first.<br/>"
        "• Floor 4's RUN square stays shut until the signal is finished, so this floor runs longest.<br/>"
        "• Real classroom timing is not yet tested: time your first session.<br/>"
        "• Code review pairs replace teacher marking. Keep this page for disputes.<br/><br/>"
        "<b>DISCUSSION STARTERS</b><br/>"
        "1. Could you draw the flowchart as a program with IF and REPEAT?<br/>"
        "2. When is a REPEAT UNTIL loop better than REPEAT 3? Can a loop run forever?<br/>"
        "3. How many bits does a real 12-megapixel colour photo need?<br/>"
        "4. Name an input, processor, storage and output in a games console or a car.<br/>"
        "5. Compare AIs across the class. Why did they learn different rules from the same floor?"
    ),

    floors=[
        dict(
            num=1,
            name="THE LOCK SCREEN",
            concept="Algorithms: flowcharts, decisions and loops",
            mechanic="flowchart",
            grid=parse("""
ST .. o. .. ## o. .. Q8 .. o.
.. o. ## Q3 .. .. ## .. B2 ..
o. .. .. .. o. B1 .. o. ## ..
## +2 ## o. .. ## .. .. o. +?
.. Q5 .. .. B? .. o. ## .. ..
o. .. ## .. .. Q2 .. .. o. ..
.. ## o. MW .. ## +2 .. ## o.
B2 .. .. o. .. o. .. Q7 .. ..
.. o. ## .. +3 .. ## .. o. ..
o. .. .. B1 .. o. .. .. DB EX
"""),
        ),
        dict(
            num=2,
            name="THE APP STORE",
            concept="Programming: loops that repeat until something happens",
            mechanic="until_loops",
            programs={
                "P1": [("until", ["R"])],
                "P2": [("until", ["D", "R"])],
                "P3": ["D", "D", ("until", ["L"])],
            },
            grid=parse("""
ST .. o. .. ## .. o. .. B2 ..
.. P1 .. o. .. o. .. ## .. o.
o. ## ## .. ## .. B1 .. .. ..
.. o. .. .. P2 .. ## o. +2 ..
B? .. ## o. .. o. .. .. ## o.
.. +2 .. ## .. .. o. B2 .. ..
o. .. o. .. .. ## .. .. P3 ..
## .. ## .. .. o. .. ## .. o.
.. o. .. B1 +3 MW o. .. o. ..
o. .. DB .. ## .. .. o. .. EX
"""),
        ),
        dict(
            num=3,
            name="THE CAMERA ROLL",
            concept="Data: pictures stored as pixels and bits",
            mechanic="pixels",
            image=["01010", "11111", "11111", "01110", "00100"],
            picture="a heart",
            grid=parse("""
.. o. .. C1 ## .. B1 o. .. ST
o. ## .. .. ## o. ## .. ## o.
.. .. C2 B2 .. .. .. o. .. ..
+2 ## o. ## ## o. ## ## C3 o.
.. .. B2 .. MW .. o. .. B2 ..
## o. ## .. ## .. ## o. ## ##
.. B? .. C4 .. +? .. .. .. o.
o. ## .. .. o. .. ## o. ## ..
.. .. o. .. .. .. B1 .. C5 +3
.. EX .. o. ## o. .. ## .. o.
"""),
        ),
        dict(
            num=4,
            name="THE BATTERY AND CHIP",
            concept="Systems: input, processing, storage and output",
            mechanic="hardware",
            # Four stops in order make this the longest floor: allow a longer slow tail.
            playtest_limits=dict(p90_turns=30),
            grid=parse("""
ST .. o. .. ## .. o. HO .. ..
.. HI .. .. .. o. ## .. HI o.
o. ## HI o. ## .. +2 .. B1 ..
.. HP .. .. HP .. .. ## .. HP
B2 .. B1 .. o. .. ## o. .. ..
.. o. ## HS .. .. HS .. ## HS
+? .. .. .. ## o. .. .. o. ..
.. ## o. HO .. MW ## HO .. B2
o. .. B1 .. .. o. .. .. ## HO
.. o. .. ## DB .. o. .. o. EX
"""),
        ),
        dict(
            num=5,
            name="THE PHOTO SORTER",
            concept="AI: how an AI learns from the examples it is given",
            mechanic="training",
            # bot: (square body, antenna, smiling)
            bots={
                "Ma": (True, True, False),
                "Mb": (False, True, False),
                "Mc": (True, False, False),
                "Md": (True, False, True),
                "Me": (False, True, False),
                "Mf": (False, False, True),
                "Mg": (True, True, True),
                "Mh": (True, False, True),
            },
            test=[(True, False, True), (True, True, True), (True, True, False),
                  (False, True, True), (False, False, False), (False, True, False)],
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
