# Series plan

About 10 games, each a pre-printed booklet played with one d6 and a pencil, for grades 6–10.

## Progression model: spiral with a new setting per game (decided 2026-11-11)

- **Every game has five floors, one per domain, in the same order:**
  1. Algorithms & Design
  2. Programming
  3. Data & Analysis
  4. Systems & Security
  5. Computing & Society (AI)
- **Each game goes one step deeper in every domain** than the game before it. A floor may assume the
  concepts from the same domain in earlier games, but its rule panel must still teach enough to play
  without them, so any game works on its own.
- **The same hero, a new setting.** The crawler bot from Game 1 returns in every game and is sent into a new
  system. The setting gives each game its story; the Floor 5 twist is always about computing and society.
- **Rough grade fit:** games 1–2 for grade 6, 3–4 for grade 7, 5–6 for grade 8, 7–8 for grade 9 and 9–10 for
  grade 10. Teachers can start anywhere.
- **The engine stays the same.** Movement, RAM, DATA, the tracker, the shop and code review are identical in
  every game. Only the floor mechanics and the story change.

## Draft spiral (for review: nothing past Game 1 is built)

| # | Setting | Algorithms & Design | Programming | Data & Analysis | Systems & Security | Computing & Society (AI) |
|---|---|---|---|---|---|---|
| 1 | Old website | Sequences and loops | Variables, IF / ELSE | Binary numbers, roll log | Caesar cipher, passwords | Decision tree and bias |
| 2 | A smartphone | Flowcharts: decisions inside an algorithm | Loops with a counter (REPEAT UNTIL) | Pixels: images as binary grids | Hardware: input, processing, storage, output | Training data: an AI learns from labelled examples |
| 3 | A video game console | Decomposition: big task into named steps | Functions with a parameter | Text as numbers (ASCII) | Networks: packets and routing | Recommendation algorithms and filter bubbles |
| 4 | A music streaming service | Linear search vs. binary search | Lists: indexes and items | Compression: run-length encoding | Password strength and brute force | Privacy and digital footprint |
| 5 | A smart city's traffic system | Sorting algorithms | Boolean logic: AND, OR, NOT | Tables: filtering and sorting records | IP addresses and DNS | Automation and jobs |
| 6 | A hospital's records system | Counting steps: comparing algorithm efficiency | Debugging: find and fix the bug | Mean, median and mode from collected data | Phishing and social engineering | Accessibility: who can use this system? |
| 7 | A space station | Shortest path on a map | Events: WHEN this happens, DO that | Error detection: parity bits | Malware types and defences | Generative AI and deepfakes |
| 8 | A bank's vault network | Nested loops | Nested IF / ELSE IF | Hexadecimal and colour codes | Public-key locks (the lock-box idea) | Intellectual property and licences |
| 9 | A self-driving car | Algorithm trade-offs: fast vs. correct | State machines | Sampling and bias in data collection | Protocols and handshakes | AI mistakes: checking what an AI tells you |
| 10 | A supercomputer at the centre of the internet | Recursion: a task that contains itself | Objects: data with its own rules | Predictions from data: a simple model | Defence in depth (capstone) | Ethics capstone: who decides what AI should do? |

How to read it: each column is one domain's ladder, read top to bottom. For example, Programming goes:
variables → loops → functions → lists → Boolean logic → debugging → events → nested conditionals →
state machines → objects.

**Every cell must pass the paper test before it is built.** A student must be able to resolve it alone, in
black and white, with a die and pencil, and no teacher judging. Cells most at risk:
- Game 6, debugging: the bug has to be findable and checkable at code review.
- Game 9, protocols and handshakes.
- Game 10, recursion.

Prototype a risky cell on one floor before committing a whole game to it.

Standards codes: match each cell to state or CSTA codes when the spiral is settled. No codes are listed yet.

## Game 2 sketch: the smartphone

Story: the crawler is sent into a phone that has started acting strangely. The phone's parts are the floors.
Each floor below is a new mechanic file; only the setting and maps are new content.

| Floor | Name | Mechanic | How it plays on paper |
|---|---|---|---|
| 1 | The Lock Screen | `flowchart` | Diamond squares hold a question about your current roll or your RAM, with YES and NO arrows printed on the map. Follow the arrow that matches. |
| 2 | The App Store | `counter_loop` | Program squares hold `REPEAT UNTIL` loops, for example "move R UNTIL you reach a wall" or "UNTIL you have crossed 2 data". The student traces the loop. |
| 3 | The Camera Roll | `pixels` | A blank 5 × 5 image grid in the rule panel. Each bit chest you open gives one row as binary; fill in that row. The finished picture is checked at code review. Bonus DATA for a complete image. |
| 4 | The Battery and Chip | `hardware` | Four zone colours (INPUT, PROCESS, STORAGE, OUTPUT). A signal must pass through the zones in order to reach RUN; squares in the wrong order cost RAM. |
| 5 | The Photo Sorter | `training` | The phone's AI learns from the bots you label. A tally box counts the labels you give; at the end, the AI's rule is whatever you labelled most often. Students see a skewed sample produce a skewed AI. |

Open questions for Game 2:
- Does the flowchart floor need the die result to stay visible? Players could write the roll on the
  tracker first.
- Should Floor 5 build on Game 1's decision tree, so students "retrain" it, or stand alone?

## Status

| # | Game | Status |
|---|---|---|
| 1 | Computer Science Crawler | Booklet built; not classroom tested |
| 2–10 | | Draft above only |
