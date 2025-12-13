# ...existing code...
import os
import random
import time
import sys

# Use msvcrt for single-key (no Enter) input on Windows
if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

# Simple text-based puzzle maze with moving ants and 3 lives.
# You are a lilliput represented by 'l'. Ants are 'a'. Exit is 'E'. Walls '#'.
# Controls: arrows or w/a/s/d (no Enter on Windows). q to quit. p to pause.

HEART = "♥"
try:
    HEART.encode('utf-8')
except Exception:
    HEART = "O"

MAZE_TEMPLATE = [
    "#####################",
    "#l    #       #     #",
    "# ### # ##### # ### #",
    "# #   #     #   #   #",
    "# # ##### # ##### ###",
    "# #     # #     #   #",
    "# ##### # ##### # # #",
    "#     # #   #   # # #",
    "##### # ### # ### # #",
    "#   # #     #     # #",
    "# # # ##### ##### # #",
    "# # #     #     # # #",
    "# # ##### # ### # # #",
    "# #     # # #   #   #",
    "# ### ### # # ##### #",
    "#     #   # #     #E#",
    "#####################",
]

# Convert to mutable grid
maze = [list(row) for row in MAZE_TEMPLATE]

def find_char(grid, ch):
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == ch:
                return (r, c)
    return None

start_pos = find_char(maze, 'l')
player_pos = start_pos
exit_pos = find_char(maze, 'E')

# remove original 'l' marker to allow movement (we'll track player_pos)
if start_pos:
    sr, sc = start_pos
    maze[sr][sc] = ' '

# Place ants at some predefined empty spaces (not on player/exit)
ant_positions = []
candidate_spots = []
for r, row in enumerate(maze):
    for c, v in enumerate(row):
        if v == ' ':
            pr, pc = start_pos
            er, ec = exit_pos
            if abs(r-pr) + abs(c-pc) > 4 and abs(r-er) + abs(c-ec) > 4:
                candidate_spots.append((r, c))
random.shuffle(candidate_spots)
for i in range(5):
    if i < len(candidate_spots):
        ant_positions.append(candidate_spots[i])

LIVES = 3
lives = LIVES

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render(grid, player, ants, lives_left, tick):
    clear_screen()
    display = [row.copy() for row in grid]
    pr, pc = player
    display[pr][pc] = 'l'
    for ar, ac in ants:
        if (ar, ac) != (pr, pc):
            display[ar][ac] = 'a'
    print("PUZZLE MAZE — Escape the maze! Reach 'E'.    Tick:", tick)
    print("You are a lilliput (l). Ants (a) try to kill you. Lives:", HEART * lives_left)
    print("Controls: arrows or w/a/s/d (no Enter on Windows). q to quit. p to pause.")
    print("-" * len(grid[0]))
    for row in display:
        print("".join(row))
    print("-" * len(grid[0]))

def is_free(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    return grid[r][c] != '#'

def move_ants(grid, ants, player):
    new_positions = []
    pr, pc = player
    for (ar, ac) in ants:
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(directions)
        moved = False
        if random.random() < 0.45:
            directions.sort(key=lambda d: abs((ar+d[0])-pr) + abs((ac+d[1])-pc))
        for dr, dc in directions:
            nr, nc = ar + dr, ac + dc
            if is_free(grid, nr, nc) and (nr, nc) not in new_positions:
                new_positions.append((nr, nc))
                moved = True
                break
        if not moved:
            new_positions.append((ar, ac))
    return new_positions

def check_collisions(player, ants):
    return player in ants

def respawn_player():
    return start_pos

def read_key_nonblocking():
    # Returns single-character command or None
    if msvcrt:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            # handle special keys (arrows) which start with b'\xe0' or b'\x00'
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                code = ch2
                arrows = {b'H':'w', b'P':'s', b'K':'a', b'M':'d'}
                return arrows.get(code, None)
            else:
                try:
                    key = ch.decode('utf-8').lower()
                except Exception:
                    return None
                return key
        else:
            return None
    else:
        # Non-Windows fallback: blocking input, so not ideal for nonblocking loop.
        # We return None to avoid blocking; user will have to use enter-based play below.
        return None

def read_key_blocking():
    if msvcrt:
        while True:
            k = read_key_nonblocking()
            if k:
                return k
            time.sleep(0.01)
    else:
        s = input().strip().lower()
        return s[0] if s else None

def interactive_instructions():
    clear_screen()
    print("Lilliput Maze - Interactive mode")
    print("Controls:")
    print("  - Arrow keys or w/a/s/d to move (no Enter required on Windows).")
    print("  - q to quit, p to pause/resume.")
    print("Press Enter to start...")
    input()

def game_loop():
    global player_pos, ant_positions, lives
    tick = 0
    paused = False
    render(maze, player_pos, ant_positions, lives, tick)
    last_ant_move = 0
    # main loop ticks every 0.25s
    TICK_DURATION = 0.20
    while True:
        tick += 1
        # read key (non-blocking on Windows)
        key = read_key_nonblocking()
        # fallback to blocking read when not on Windows and no key - prompt user for command
        if key is None and not msvcrt:
            render(maze, player_pos, ant_positions, lives, tick)
            key = read_key_blocking()

        if key:
            if key == 'q':
                clear_screen()
                print("Quitting. Bye.")
                break
            if key == 'p':
                paused = not paused
                if paused:
                    print("Paused. Press 'p' to resume.")
                time.sleep(0.3)
            # movement keys
            if not paused:
                dr = dc = 0
                if key == 'w':
                    dr, dc = -1, 0
                elif key == 's':
                    dr, dc = 1, 0
                elif key == 'a':
                    dr, dc = 0, -1
                elif key == 'd':
                    dr, dc = 0, 1
                if (dr, dc) != (0, 0):
                    nr, nc = player_pos[0] + dr, player_pos[1] + dc
                    if is_free(maze, nr, nc) or (nr, nc) == exit_pos:
                        player_pos = (nr, nc)
                    else:
                        # bump into wall (small visual feedback)
                        pass

        if paused:
            render(maze, player_pos, ant_positions, lives, tick)
            time.sleep(TICK_DURATION)
            continue

        # Check reach exit
        if player_pos == exit_pos:
            render(maze, player_pos, ant_positions, lives, tick)
            print("You found the exit! You escaped as a brave lilliput. 🎉")
            break

        # Check collision after move
        if check_collisions(player_pos, ant_positions):
            lives -= 1
            render(maze, player_pos, ant_positions, lives, tick)
            print("An ant attacked you! Lives left:", lives)
            time.sleep(1.0)
            if lives > 0:
                player_pos = respawn_player()
            else:
                render(maze, player_pos, ant_positions, lives, tick)
                print("You are out of lives. The ants got you. Game over.")
                break

        # Move ants every N ticks (so movement is visible)
        if tick - last_ant_move >= 2:
            ant_positions = move_ants(maze, ant_positions, player_pos)
            last_ant_move = tick

        # Check if ant moved onto player
        if check_collisions(player_pos, ant_positions):
            lives -= 1
            render(maze, player_pos, ant_positions, lives, tick)
            print("An ant moved onto you! Lives left:", lives)
            time.sleep(1.0)
            if lives > 0:
                player_pos = respawn_player()
            else:
                render(maze, player_pos, ant_positions, lives, tick)
                print("You are out of lives. The ants got you. Game over.")
                break

        render(maze, player_pos, ant_positions, lives, tick)
        time.sleep(TICK_DURATION)

if __name__ == "__main__":
    random.seed()
    interactive_instructions()
    game_loop()
# filepath: c:\Users\hp\OneDrive\Desktop\Studies\Social eagle\10DPC\Day10.py
# ...existing code...
import os
import random
import time
import sys

# Use msvcrt for single-key (no Enter) input on Windows
if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

# Simple text-based puzzle maze with moving ants and 3 lives.
# You are a lilliput represented by 'l'. Ants are 'a'. Exit is 'E'. Walls '#'.
# Controls: arrows or w/a/s/d (no Enter on Windows). q to quit. p to pause.

HEART = "♥"
try:
    HEART.encode('utf-8')
except Exception:
    HEART = "O"

MAZE_TEMPLATE = [
    "#####################",
    "#l    #       #     #",
    "# ### # ##### # ### #",
    "# #   #     #   #   #",
    "# # ##### # ##### ###",
    "# #     # #     #   #",
    "# ##### # ##### # # #",
    "#     # #   #   # # #",
    "##### # ### # ### # #",
    "#   # #     #     # #",
    "# # # ##### ##### # #",
    "# # #     #     # # #",
    "# # ##### # ### # # #",
    "# #     # # #   #   #",
    "# ### ### # # ##### #",
    "#     #   # #     #E#",
    "#####################",
]

# Convert to mutable grid
maze = [list(row) for row in MAZE_TEMPLATE]

def find_char(grid, ch):
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == ch:
                return (r, c)
    return None

start_pos = find_char(maze, 'l')
player_pos = start_pos
exit_pos = find_char(maze, 'E')

# remove original 'l' marker to allow movement (we'll track player_pos)
if start_pos:
    sr, sc = start_pos
    maze[sr][sc] = ' '

# Place ants at some predefined empty spaces (not on player/exit)
ant_positions = []
candidate_spots = []
for r, row in enumerate(maze):
    for c, v in enumerate(row):
        if v == ' ':
            pr, pc = start_pos
            er, ec = exit_pos
            if abs(r-pr) + abs(c-pc) > 4 and abs(r-er) + abs(c-ec) > 4:
                candidate_spots.append((r, c))
random.shuffle(candidate_spots)
for i in range(5):
    if i < len(candidate_spots):
        ant_positions.append(candidate_spots[i])

LIVES = 3
lives = LIVES

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render(grid, player, ants, lives_left, tick):
    clear_screen()
    display = [row.copy() for row in grid]
    pr, pc = player
    display[pr][pc] = 'l'
    for ar, ac in ants:
        if (ar, ac) != (pr, pc):
            display[ar][ac] = 'a'
    print("PUZZLE MAZE — Escape the maze! Reach 'E'.    Tick:", tick)
    print("You are a lilliput (l). Ants (a) try to kill you. Lives:", HEART * lives_left)
    print("Controls: arrows or w/a/s/d (no Enter on Windows). q to quit. p to pause.")
    print("-" * len(grid[0]))
    for row in display:
        print("".join(row))
    print("-" * len(grid[0]))

def is_free(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False
    return grid[r][c] != '#'

def move_ants(grid, ants, player):
    new_positions = []
    pr, pc = player
    for (ar, ac) in ants:
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(directions)
        moved = False
        if random.random() < 0.45:
            directions.sort(key=lambda d: abs((ar+d[0])-pr) + abs((ac+d[1])-pc))
        for dr, dc in directions:
            nr, nc = ar + dr, ac + dc
            if is_free(grid, nr, nc) and (nr, nc) not in new_positions:
                new_positions.append((nr, nc))
                moved = True
                break
        if not moved:
            new_positions.append((ar, ac))
    return new_positions

def check_collisions(player, ants):
    return player in ants

def respawn_player():
    return start_pos

def read_key_nonblocking():
    # Returns single-character command or None
    if msvcrt:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            # handle special keys (arrows) which start with b'\xe0' or b'\x00'
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                code = ch2
                arrows = {b'H':'w', b'P':'s', b'K':'a', b'M':'d'}
                return arrows.get(code, None)
            else:
                try:
                    key = ch.decode('utf-8').lower()
                except Exception:
                    return None
                return key
        else:
            return None
    else:
        # Non-Windows fallback: blocking input, so not ideal for nonblocking loop.
        # We return None to avoid blocking; user will have to use enter-based play below.
        return None

def read_key_blocking():
    if msvcrt:
        while True:
            k = read_key_nonblocking()
            if k:
                return k
            time.sleep(0.01)
    else:
        s = input().strip().lower()
        return s[0] if s else None

def interactive_instructions():
    clear_screen()
    print("Lilliput Maze - Interactive mode")
    print("Controls:")
    print("  - Arrow keys or w/a/s/d to move (no Enter required on Windows).")
    print("  - q to quit, p to pause/resume.")
    print("Press Enter to start...")
    input()

def game_loop():
    global player_pos, ant_positions, lives
    tick = 0
    paused = False
    render(maze, player_pos, ant_positions, lives, tick)
    last_ant_move = 0
    # main loop ticks every 0.25s
    TICK_DURATION = 0.20
    while True:
        tick += 1
        # read key (non-blocking on Windows)
        key = read_key_nonblocking()
        # fallback to blocking read when not on Windows and no key - prompt user for command
        if key is None and not msvcrt:
            render(maze, player_pos, ant_positions, lives, tick)
            key = read_key_blocking()

        if key:
            if key == 'q':
                clear_screen()
                print("Quitting. Bye.")
                break
            if key == 'p':
                paused = not paused
                if paused:
                    print("Paused. Press 'p' to resume.")
                time.sleep(0.3)
            # movement keys
            if not paused:
                dr = dc = 0
                if key == 'w':
                    dr, dc = -1, 0
                elif key == 's':
                    dr, dc = 1, 0
                elif key == 'a':
                    dr, dc = 0, -1
                elif key == 'd':
                    dr, dc = 0, 1
                if (dr, dc) != (0, 0):
                    nr, nc = player_pos[0] + dr, player_pos[1] + dc
                    if is_free(maze, nr, nc) or (nr, nc) == exit_pos:
                        player_pos = (nr, nc)
                    else:
                        # bump into wall (small visual feedback)
                        pass

        if paused:
            render(maze, player_pos, ant_positions, lives, tick)
            time.sleep(TICK_DURATION)
            continue

        # Check reach exit
        if player_pos == exit_pos:
            render(maze, player_pos, ant_positions, lives, tick)
            print("You found the exit! You escaped as a brave lilliput. 🎉")
            break

        # Check collision after move
        if check_collisions(player_pos, ant_positions):
            lives -= 1
            render(maze, player_pos, ant_positions, lives, tick)
            print("An ant attacked you! Lives left:", lives)
            time.sleep(1.0)
            if lives > 0:
                player_pos = respawn_player()
            else:
                render(maze, player_pos, ant_positions, lives, tick)
                print("You are out of lives. The ants got you. Game over.")
                break

        # Move ants every N ticks (so movement is visible)
        if tick - last_ant_move >= 2:
            ant_positions = move_ants(maze, ant_positions, player_pos)
            last_ant_move = tick

        # Check if ant moved onto player
        if check_collisions(player_pos, ant_positions):
            lives -= 1
            render(maze, player_pos, ant_positions, lives, tick)
            print("An ant moved onto you! Lives left:", lives)
            time.sleep(1.0)
            if lives > 0:
                player_pos = respawn_player()
            else:
                render(maze, player_pos, ant_positions, lives, tick)
                print("You are out of lives. The ants got you. Game over.")
                break

        render(maze, player_pos, ant_positions, lives, tick)
        time.sleep(TICK_DURATION)

if __name__ == "__main__":
    random.seed()
    interactive_instructions()
    game_loop()