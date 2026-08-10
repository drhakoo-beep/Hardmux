import curses

FONT = {
    "H": ["█   █", "█   █", "█████", "█   █", "█   █", "█   █"],
    "A": [" ███ ", "█   █", "█████", "█   █", "█   █", "█   █"],
    "R": ["████ ", "█   █", "████ ", "█ █  ", "█  █ ", "█   █"],
    "D": ["████ ", "█   █", "█   █", "█   █", "█   █", "████ "],
    "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █", "█   █"],
    "U": ["█   █", "█   █", "█   █", "█   █", "█   █", " ███ "],
    "X": ["█   █", " █ █ ", "  █  ", "  █  ", " █ █ ", "█   █"],
}

RED = 1
RED_BOLD = 2
WHITE_ON_RED = 3
DIM_WHITE = 4
BLACK_ON_RED = 5


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(RED, curses.COLOR_RED, -1)
    curses.init_pair(RED_BOLD, curses.COLOR_RED, -1)
    curses.init_pair(WHITE_ON_RED, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(DIM_WHITE, curses.COLOR_WHITE, -1)
    curses.init_pair(BLACK_ON_RED, curses.COLOR_BLACK, curses.COLOR_RED)


def build_big_banner(word):
    rows = ["" for _ in range(6)]
    for ch in word:
        glyph = FONT.get(ch, ["     "] * 6)
        for i in range(6):
            rows[i] += glyph[i] + " "
    return rows


def safe_addstr(stdscr, y, x, text, attr=0):
    height, width = stdscr.getmaxyx()
    if y < 0 or y >= height:
        return
    if x < 0:
        text = text[-x:]
        x = 0
    if x >= width:
        return
    max_len = width - x - 1
    if max_len <= 0:
        return
    try:
        stdscr.addstr(y, x, text[:max_len], attr)
    except curses.error:
        pass


def draw_box(stdscr, y1, x1, y2, x2, attr=0):
    height, width = stdscr.getmaxyx()
    y1, y2 = max(0, y1), min(height - 1, y2)
    x1, x2 = max(0, x1), min(width - 1, x2)
    if y2 <= y1 or x2 <= x1:
        return
    safe_addstr(stdscr, y1, x1, "┌" + "─" * (x2 - x1 - 1) + "┐", attr)
    for y in range(y1 + 1, y2):
        safe_addstr(stdscr, y, x1, "│", attr)
        safe_addstr(stdscr, y, x2, "│", attr)
    safe_addstr(stdscr, y2, x1, "└" + "─" * (x2 - x1 - 1) + "┘", attr)


def draw_banner(stdscr, subtitle=""):
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    start_y = 1
    if width >= 46:
        big = build_big_banner("HARDMUX")
        for i, line in enumerate(big):
            x = max((width - len(line)) // 2, 0)
            safe_addstr(stdscr, start_y + i, x, line, curses.color_pair(RED_BOLD) | curses.A_BOLD)
        next_y = start_y + len(big)
    else:
        line = "== HARDMUX =="
        x = max((width - len(line)) // 2, 0)
        safe_addstr(stdscr, start_y, x, line, curses.color_pair(RED_BOLD) | curses.A_BOLD)
        next_y = start_y + 1
    if subtitle:
        x = max((width - len(subtitle)) // 2, 0)
        safe_addstr(stdscr, next_y + 1, x, subtitle, curses.color_pair(WHITE_ON_RED) | curses.A_BOLD)
        next_y += 1
    line = "─" * min(width - 2, 60)
    x = max((width - len(line)) // 2, 0)
    safe_addstr(stdscr, next_y + 2, x, line, curses.color_pair(RED))
    return next_y + 4


def run_menu(stdscr, title, options, nav_hint=""):
    curses.curs_set(0)
    idx = 0
    while True:
        top = draw_banner(stdscr, title)
        height, width = stdscr.getmaxyx()
        max_label = max((len(o) for o in options), default=10)
        box_w = min(max_label + 8, width - 4)
        box_x1 = max((width - box_w) // 2, 1)
        box_x2 = box_x1 + box_w
        visible_rows = max(height - top - 3, 3)
        offset = 0
        if idx >= visible_rows:
            offset = idx - visible_rows + 1
        box_y1 = top - 1
        box_y2 = min(top + min(len(options), visible_rows) + 1, height - 2)
        draw_box(stdscr, box_y1, box_x1, box_y2, box_x2, curses.color_pair(RED))
        for row, i in enumerate(range(offset, min(offset + visible_rows, len(options)))):
            opt = options[i]
            y = top + row
            label = opt.ljust(box_w - 4)
            if i == idx:
                safe_addstr(stdscr, y, box_x1 + 2, "▶ " + label, curses.color_pair(WHITE_ON_RED) | curses.A_BOLD)
            else:
                safe_addstr(stdscr, y, box_x1 + 2, "  " + label, curses.color_pair(RED))
        if nav_hint:
            hy = height - 1
            hx = max((width - len(nav_hint)) // 2, 0)
            safe_addstr(stdscr, hy, hx, nav_hint, curses.A_DIM)
        stdscr.refresh()
        key = stdscr.getch()
        if key in (curses.KEY_UP, ord('k')):
            idx = (idx - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord('j')):
            idx = (idx + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return idx
        elif key in (ord('q'), ord('Q'), 27):
            return -1


def prompt_text(stdscr, label, hint=""):
    curses.curs_set(1)
    height, width = stdscr.getmaxyx()
    top = draw_banner(stdscr, "")
    box_w = min(max(len(label) + 10, 40), width - 4)
    box_x1 = max((width - box_w) // 2, 1)
    box_x2 = box_x1 + box_w
    box_y1 = top
    box_y2 = top + 4
    draw_box(stdscr, box_y1, box_x1, box_y2, box_x2, curses.color_pair(WHITE_ON_RED) | curses.A_BOLD)
    safe_addstr(stdscr, box_y1 + 1, box_x1 + 2, label, curses.color_pair(WHITE_ON_RED) | curses.A_BOLD)
    safe_addstr(stdscr, box_y1 + 2, box_x1 + 2, "> ", curses.color_pair(RED_BOLD) | curses.A_BOLD)
    if hint:
        safe_addstr(stdscr, box_y2 + 1, box_x1, hint[:box_w], curses.A_DIM)
    stdscr.refresh()
    curses.echo()
    input_x = box_x1 + 4
    input_y = box_y1 + 2
    max_input = max(box_x2 - input_x - 1, 5)
    try:
        raw = stdscr.getstr(input_y, input_x, max_input)
        text = raw.decode("utf-8")
    except Exception:
        text = ""
    curses.noecho()
    curses.curs_set(0)
    return text.strip()


def show_result(stdscr, title, text, footer_hint=""):
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    top = draw_banner(stdscr, title)
    box_x1, box_x2 = 1, width - 2
    box_y1 = top - 1
    box_y2 = height - 2
    draw_box(stdscr, box_y1, box_x1, box_y2, box_x2, curses.color_pair(RED))
    inner_w = max(box_x2 - box_x1 - 2, 10)
    y = top
    lines = text.split("\n") if text else [""]
    for line in lines:
        if not line:
            y += 1
            continue
        for i in range(0, len(line), inner_w):
            if y >= box_y2:
                break
            safe_addstr(stdscr, y, box_x1 + 2, line[i:i + inner_w], curses.color_pair(DIM_WHITE))
            y += 1
    hint = footer_hint if footer_hint else "ENTER / Q"
    hx = max((width - len(hint)) // 2, 0)
    safe_addstr(stdscr, height - 1, hx, hint, curses.color_pair(WHITE_ON_RED) | curses.A_BOLD)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in (curses.KEY_ENTER, 10, 13, ord('q'), ord('Q'), 27):
            break
