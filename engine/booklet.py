"""Builds a game's printable black-and-white booklet (US Letter).

Page order: cover, how to play, one page per floor, shop and stats, teacher answer key.
Page layouts and the core rules live here; all game-specific text comes from the game's GAME dict.
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .draw import (BOLD, CELL, H, M, SANS, W, arrow, blank, box, centred, draw_map, floor_for, footer, icon,
                   label, legend, panel, para, tracker)
from .grid import SIZE


def floor_page(c, game, floor):
    top = H - M
    c.setFillGray(0)
    c.roundRect(M, top - 30, 76, 30, 5, fill=1, stroke=0)
    centred(c, f"FLOOR {floor['num']}", M + 38, top - 15, 14, gray=1)
    label(c, floor["name"], M + 88, top - 16, 17)
    label(c, floor["concept"], M + 88, top - 28, 8.5, SANS, gray=0.3)
    floor["mech"].rule_panel(c, floor, M, top - 46, W - 2 * M, 148)
    gx, gy = M + 16, 140
    draw_map(c, floor, gx, gy)
    legend(c, floor, gx + CELL * SIZE + 14, gy + CELL * SIZE, W - M - (gx + CELL * SIZE + 14))
    tracker(c, M, 126, W - 2 * M)
    footer(c, game, f"Floor {floor['num']}")
    c.showPage()


def cover(c, game):
    cv, st = game["cover"], game["start"]
    top = H - M
    c.setFillGray(0)
    c.rect(M, top - 150, W - 2 * M, 150, fill=1, stroke=0)
    for i, line in enumerate(cv["title_lines"]):
        centred(c, line, W / 2, top - 36 - i * 40, 38, gray=1)
    centred(c, cv["subtitle"], W / 2, top - 112, 14, gray=1)
    centred(c, cv["tagline"], W / 2, top - 132, 10, SANS, gray=1)
    para(c, cv["story"], M + 20, top - 166, W - 2 * M - 40, size=11, leading=15)
    bx, by, bw, bh = M, 250, 300, 250
    c.setLineWidth(1.5)
    c.setDash(4, 3)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    c.setDash()
    label(c, cv["avatar"], bx + 10, by + bh - 16, 9)
    rx = bx + bw + 24
    for i, name in enumerate(cv["fields"]):
        y = by + bh - 30 - i * 48
        label(c, name.upper(), rx, y, 8, BOLD, gray=0.3)
        blank(c, rx, y - 24, W - M - rx)
    label(c, "YOU START WITH", M, 216, 9)
    for i, (name, val) in enumerate((("RAM", st["ram"]), ("DATA", st["data"]), ("MAX RAM", st["max_ram"]))):
        x = M + i * 120
        c.setLineWidth(1.5)
        c.rect(x, 150, 104, 54, fill=0, stroke=1)
        centred(c, str(val), x + 52, 184, 24)
        centred(c, name, x + 52, 160, 9)
    para(c, cv["stat_notes"], M + 372, 206, W - 2 * M - 372, size=9.5, leading=14)
    for i, t in enumerate(cv["icons"]):
        icon(c, t, M + 20 + i * 50, 72, 46, floor_for(game, t))
    footer(c, game, "Cover")
    c.showPage()


def mini(c, x, y, cell, cols, rows, walls, path, title):
    for (r, col) in walls:
        icon(c, "##", x + col * cell, y + (rows - 1 - r) * cell, cell)
    c.setStrokeGray(0.55)
    c.setLineWidth(0.5)
    for k in range(1, cols):
        c.line(x + k * cell, y, x + k * cell, y + rows * cell)
    for k in range(1, rows):
        c.line(x, y + k * cell, x + cols * cell, y + k * cell)
    c.setStrokeGray(0)
    c.setLineWidth(1.5)
    c.rect(x, y, cols * cell, rows * cell, fill=0, stroke=1)
    pts = [(x + (col + 0.5) * cell, y + (rows - 0.5 - r) * cell) for r, col in path]
    icon(c, "ST", pts[0][0] - cell / 2, pts[0][1] - cell / 2, cell)
    c.setDash(2, 2)
    c.setLineWidth(1.4)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    c.setDash()
    for i, p in enumerate(pts[1:-1], 1):
        c.circle(p[0], p[1], 1.8, fill=1, stroke=0)
    ex, ey = pts[-1]
    c.setLineWidth(2)
    c.line(ex - 5, ey - 5, ex + 5, ey + 5)
    c.line(ex - 5, ey + 5, ex + 5, ey - 5)
    para(c, title, x + cols * cell + 10, y + rows * cell - 4, 112, size=8.5, leading=11)


def rules_page(c, game):
    st = game["start"]
    top = H - M
    label(c, "HOW TO PLAY", M, top - 20, 26)
    para(c, f"<b>Goal:</b> get through all {len(game['floors'])} floors. Collect DATA. Do not run out of RAM. "
            "<b>You need:</b> this booklet, a pencil and one die.", M, top - 32, W - 2 * M, size=10.5)
    colw = 258
    lx, rx = M, M + colw + 16
    y = top - 72
    panel(c, lx, y, colw, 250, "YOUR TURN")
    para(c, "<b>1. Roll the die.</b><br/><br/>"
            "<b>2. Odd or even?</b><br/>ODD (1, 3, 5): move <b>diagonally</b>.<br/>"
            "EVEN (2, 4, 6): move <b>straight</b> (up, down, left or right).<br/><br/>"
            "<b>3. Pick a direction</b> and move that many squares, one square at a time.<br/><br/>"
            "<b>4. Draw your path</b> as you go. Mark the square where you stop with an <b>X</b>. "
            "Start there next turn.<br/><br/>"
            "<b>5. Use everything you cross.</b> Every bug, data dot and power-up on your path happens to you, "
            "in order. Write each gain or loss in the boxes at the bottom of the page, then cross the thing "
            "out. It only works once.", lx + 12, y - 18, colw - 24, size=9.5)
    panel(c, rx, y, colw, 250, "MOVING RULES")
    para(c, "• If any direction lets you make your <b>whole move without hitting a wall</b>, you must pick "
            "one of those directions.<br/><br/>"
            "• <b>Keep going the same way.</b> You turn only when a wall or the edge of the map blocks "
            "you. Then pick a new direction of the same kind and keep counting.<br/><br/>"
            "• You may <b>not</b> turn to dodge a bug or to grab something.<br/><br/>"
            "• Go back the way you came <b>only</b> if there is no other way.<br/><br/>"
            "• Moving diagonally, only the square you land on matters. You can slip between two wall "
            "corners.", rx + 12, y - 18, colw - 24, size=9.5)
    y2 = y - 268
    panel(c, lx, y2, W - 2 * M, 110, "EXAMPLES")
    cell = 20
    mini(c, lx + 16, y2 - 100, cell, 6, 4, [(0, 4), (1, 4), (3, 1)],
         [(1, 0), (1, 1), (1, 2), (1, 3), (2, 3)],
         "<b>Rolled 4 (even).</b> Moved right 3 squares. A wall blocked the way, so turned and finished "
         "the last square going down.")
    mini(c, lx + 282, y2 - 100, cell, 6, 4, [(3, 2), (0, 5)],
         [(2, 0), (1, 1), (0, 2), (1, 3)],
         "<b>Rolled 3 (odd).</b> Moved up-right 2 squares. The edge blocked the way, so bounced "
         "down-right for the last square.")
    y3 = y2 - 128
    panel(c, lx, y3, colw, 196, "LEAVING A FLOOR")
    para(c, "Stop on the <b>RUN</b> square, stop on any square touching it (corners count), or pass over it. "
            "Then you may leave. You can also stay to collect more.<br/><br/>"
            "Now do the math, once for RAM and once for DATA:<br/>"
            "<b>START + gained – lost = END</b><br/><br/>"
            "Copy both END numbers to START on the next floor.<br/><br/>"
            "RAM cannot go above your Max RAM. DATA cannot go below 0. You do not crash in the middle of a "
            "floor: only the END number counts.", lx + 12, y3 - 18, colw - 24, size=9.5)
    panel(c, rx, y3, colw, 92, "CRASH!")
    para(c, "If your END RAM is <b>0 or less</b>, your crawler crashed. Tally one crash on the last page. "
            f"Start the next floor with <b>{st['ram']} RAM and {st['data']} DATA</b>. Keep playing!",
         rx + 12, y3 - 18, colw - 24, size=9.5)
    panel(c, rx, y3 - 104, colw, 92, "CODE REVIEW")
    para(c, "Real coders check each other's work. After every floor, swap booklets with a partner. "
            "Check their path, their math and their floor puzzle. Found a mistake? Fix it together.",
         rx + 12, y3 - 122, colw - 24, size=9.5)
    footer(c, game, "How to play")
    c.showPage()


def shop_page(c, game):
    top = H - M
    label(c, "THE SHOP", M, top - 20, 26)
    para(c, game["shop"]["intro"], M, top - 32, W - 2 * M, size=10.5)
    y = top - 92
    xs = [M, M + 104, M + 150, M + 372, M + 452]
    for hx, hd in zip(xs, ["ITEM", "PRICE", "WHAT IT DOES", "SHOP 1", "SHOP 2"]):
        label(c, hd, hx + 4, y + 5, 8, gray=0.3)
    for name, price, desc, usable in game["shop"]["items"]:
        c.setLineWidth(1)
        c.rect(M, y - 44, W - 2 * M, 44, fill=0, stroke=1)
        label(c, name, xs[0] + 6, y - 26, 10.5)
        label(c, f"{price} DATA", xs[1] + 4, y - 26, 9.5, SANS)
        para(c, desc, xs[2] + 4, y - 9, 212, size=9)
        for sx in (xs[3], xs[4]):
            box(c, sx + 4, y - 20)
            label(c, "bought", sx + 20, y - 17, 7.5, SANS)
            if usable:
                box(c, sx + 4, y - 38)
                label(c, "used", sx + 20, y - 35, 7.5, SANS)
        y -= 44
    label(c, "MY MAX RAM:", M, y - 30, 10)
    for i, v in enumerate((str(game["start"]["max_ram"]), "", "")):
        bx = M + 86 + i * 62
        c.rect(bx, y - 42, 36, 30, fill=0, stroke=1)
        if v:
            centred(c, v, bx + 18, y - 27, 14)
        if i < 2:
            arrow(c, bx + 49, y - 27, 14, "R")

    y -= 86
    label(c, "FINAL STATS", M, y, 26)
    y -= 22
    stats = [("CRASHES (tally)", 150), ("FINAL RAM", 110), ("FINAL DATA", 110), ("FLOORS CLEARED", 122)]
    x = M
    for name, wd in stats:
        c.setLineWidth(1.5)
        c.rect(x, y - 62, wd, 62, fill=0, stroke=1)
        label(c, name, x + 6, y - 13, 8)
        x += wd + 13
    y -= 86
    label(c, "YOUR RANK  (by final DATA)", M, y, 10)
    for i, (rng, name) in enumerate(game["ranks"]):
        bx = M + i * 134
        box(c, bx, y - 26)
        label(c, name, bx + 18, y - 22, 10)
        label(c, f"{rng} DATA", bx + 18, y - 34, 8, SANS, gray=0.3)
    y -= 66
    label(c, "THINK BACK", M, y, 10)
    for q in game["think_back"]:
        y -= 18
        label(c, q, M, y, 9.5, SANS)
        y -= 20
        blank(c, M, y, W - 2 * M)
        y -= 20
        blank(c, M, y, W - 2 * M)
    footer(c, game, "Shop and stats")
    c.showPage()


def teacher_page(c, game):
    top = H - M
    c.setFillGray(0)
    c.rect(M, top - 26, W - 2 * M, 26, fill=1, stroke=0)
    centred(c, "TEACHER PAGE: ANSWER KEY  (do not hand out)", W / 2, top - 13, 13, gray=1)
    colw = 258
    lx, rx = M, M + colw + 16
    y = top - 46
    left = "<br/><br/>".join(f"<b>FLOOR {f['num']}: {f['mech'].key_title}</b><br/>" + f["mech"].answer_key(f)
                             for f in game["floors"])
    para(c, left, lx, y, colw, size=8.8, leading=11.6)
    para(c, game["teacher"], rx, y, colw, size=8.8, leading=11.6)
    footer(c, game, "Teacher page")
    c.showPage()


def build(game, path=None):
    path = path or game["dir"] / game["output"]
    c = canvas.Canvas(str(path), pagesize=letter, invariant=1)  # same input, same bytes
    c.setTitle(game["pdf_title"])
    c.setAuthor(game["title"])
    cover(c, game)
    rules_page(c, game)
    for f in game["floors"]:
        floor_page(c, game, f)
    shop_page(c, game)
    teacher_page(c, game)
    c.save()
    return path
