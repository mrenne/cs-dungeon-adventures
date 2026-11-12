# Style guide

Rules every booklet in the series follows.

## Play

- Fully unplugged: printed booklet, one six-sided die, a pencil. No cut-outs, cards or extra pieces.
- Maps are pre-printed. Students draw their path on them; they never draw maps.
- A student must be able to resolve every square alone, on paper. No teacher judging: partner **code review**
  checks work after each floor.
- The CS idea lives in the floor's mechanic, not in quiz questions.
- Each floor: a 10 × 10 grid, one start, one RUN exit, and a FLOOR RULE panel explaining its mechanic.

## Print

- US Letter, black and white only (grey fills are fine). It must photocopy cleanly.
- Print single-sided so nothing shows through the maps.
- Fonts: Helvetica for text, Helvetica Bold for headings, Courier Bold for code.
- No text may run outside its panel. Look at every page after a change.

## Writing

- Reading level: grades 6–10. Short sentences, second person ("you"), present tense.
- Bold the one word or phrase per sentence that carries the rule.
- Use RAM for health and DATA for score in every game, so students moving between games keep the same vocabulary.

## Balance (checked by `python build.py --playtest`)

- Every floor must be finishable: under 2% of simulated players stuck.
- Median 6–14 turns per floor; slowest 10% within 25 turns. A floor may loosen a mark with
  `playtest_limits` in its game file, with a comment saying why (Game 2, Floor 4 does).
- Aim for most players to finish a whole game without crashing. Game 1: 59% with no crash, 0.43 crashes on average.
