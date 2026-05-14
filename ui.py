import math
import pygame
import collapse as game
 
# colours
BG           = (15, 15, 20)
GRID_COL     = (45, 45, 60)
CELL_BG      = (22, 22, 30)
CELL_HOVER   = (32, 32, 45)
CELL_SEL     = (40, 28, 65)
CELL_WIN     = (40, 35, 20)
X_COLOR      = (130, 90, 255)
O_COLOR      = (0, 210, 185)
X_DIM        = (65, 42, 125)
O_DIM        = (0, 95, 85)
TEXT_PRI     = (225, 225, 235)
TEXT_SEC     = (110, 110, 135)
TEXT_HINT    = (55, 55, 72)
WIN_COLOR    = (255, 210, 60)
PANEL_BG     = (18, 18, 25)
PANEL_LINE   = (38, 38, 55)
 
# window layout
W, H      = 700, 620
GRID_L    = 30
GRID_T    = 90
GRID_SIZE = 420
PAD       = 8
PANEL_X   = 480
PANEL_W   = 195
PANEL_Y   = 90
 
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
 
 
def cell_rect(i):
    s = GRID_SIZE // 3
    return pygame.Rect(
        GRID_L + (i % 3) * s + PAD,
        GRID_T + (i // 3) * s + PAD,
        s - PAD * 2,
        s - PAD * 2
    )
 
 
def cell_at(pos):
    for i in range(9):
        if cell_rect(i).collidepoint(pos):
            return i
    return None
 
 
def winning_cells(winner):
    # return the three cells that form the winning line
    for a, b, c in LINES:
        if (isinstance(game.board[a], str) and
                game.board[a] == game.board[b] == game.board[c] == winner):
            return [a, b, c]
    return []
 
 
def run_ui(on_move, on_reset, state):
 
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Quantum Tic-Tac-Toe")
 
    f_title = pygame.font.SysFont("helvetica", 20, bold=True)
    f_body  = pygame.font.SysFont("helvetica", 14)
    f_small = pygame.font.SysFont("helvetica", 11)
    f_cell  = pygame.font.SysFont("helvetica", 50, bold=True)
    f_mark  = pygame.font.SysFont("helvetica", 12)
    f_win   = pygame.font.SysFont("helvetica", 28, bold=True)
 
    selected = []
    hovered  = None
    message  = "Player X — pick two cells"
    sub      = ""
    clock    = pygame.time.Clock()
    running  = True
 
    while running:
        clock.tick(60)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            elif event.type == pygame.MOUSEMOTION:
                hovered = cell_at(event.pos)
 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    on_reset()
                    selected = []
                    message  = "Player X — pick two cells"
                    sub      = ""
 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # reset button
                rrect = pygame.Rect(PANEL_X, H - 50, PANEL_W, 34)
                if rrect.collidepoint(event.pos):
                    on_reset()
                    selected = []
                    message  = "Player X — pick two cells"
                    sub      = ""
                    continue
 
                if state['game_over']:
                    continue
 
                cell = cell_at(event.pos)
                if cell is None:
                    continue
                if isinstance(game.board[cell], str):
                    continue
 
                if cell in selected:
                    selected.remove(cell)
                    if not selected:
                        message = f"Player {state['current_player']} — pick two cells"
                        sub     = ""
                    continue
 
                selected.append(cell)
 
                if len(selected) == 1:
                    message = f"Player {state['current_player']} — pick second cell"
                    sub     = f"first cell: {selected[0]}"
 
                elif len(selected) == 2:
                    a, b     = selected
                    selected = []
                    result   = on_move(a, b)
 
                    if result["collapsed"]:
                        bits    = result["bitstring"][:len(result["cycle_cells"])]
                        message = f"Collapsed — Quokka: {bits}"
                        sub     = f"cells {result['cycle_cells']} resolved"
 
                    if not result["collapsed"]:
                        message = f"Player {state['current_player']} — pick two cells"
                        sub     = ""
 
        # --- draw ---
        screen.fill(BG)
 
        # title
        screen.blit(f_title.render("Quantum Tic-Tac-Toe", True, TEXT_PRI), (GRID_L, 18))
        p    = state['current_player']
        pcol = X_COLOR if p == "X" else O_COLOR
        screen.blit(f_body.render(f"Player {p}", True, pcol), (GRID_L, 50))
 
        # grid
        s = GRID_SIZE // 3
        for i in range(1, 3):
            pygame.draw.line(screen, GRID_COL, (GRID_L + i*s, GRID_T), (GRID_L + i*s, GRID_T + GRID_SIZE), 1)
            pygame.draw.line(screen, GRID_COL, (GRID_L, GRID_T + i*s), (GRID_L + GRID_SIZE, GRID_T + i*s), 1)
        pygame.draw.rect(screen, GRID_COL, (GRID_L, GRID_T, GRID_SIZE, GRID_SIZE), 1)
 
        # figure out winning cells so we can highlight them
        win_cells = winning_cells(state['winner']) if state['winner'] else []
 
        # cells
        for i in range(9):
            rect = cell_rect(i)
            val  = game.board[i]
            cx, cy = rect.centerx, rect.centery
 
            # background
            if i in win_cells:
                bg = CELL_WIN
            elif i in selected:
                bg = CELL_SEL
            elif i == hovered and not state['game_over']:
                bg = CELL_HOVER
            else:
                bg = CELL_BG
            pygame.draw.rect(screen, bg, rect)
 
            # selection border
            if i in selected:
                pygame.draw.rect(screen, X_COLOR if p == "X" else O_COLOR, rect, 1)
 
            # win cell border
            if i in win_cells:
                pygame.draw.rect(screen, WIN_COLOR, rect, 2)
 
            # content
            if isinstance(val, str):
                color = X_COLOR if val == "X" else O_COLOR
                surf  = f_cell.render(val, True, color)
                screen.blit(surf, surf.get_rect(center=(cx, cy)))
 
            elif val:
                # superposition marks in a small grid
                n    = len(val)
                cols = 2 if n > 1 else 1
                mw   = rect.w // cols
                mh   = rect.h // math.ceil(n / cols)
                for idx, (player, mn) in enumerate(val):
                    mx  = rect.x + (idx % cols) * mw + mw // 2
                    my  = rect.y + (idx // cols) * mh + mh // 2
                    col = X_DIM if player == "X" else O_DIM
                    surf = f_mark.render(f"{player}{mn}", True, col)
                    screen.blit(surf, surf.get_rect(center=(mx, my)))
 
            else:
                screen.blit(f_small.render(str(i), True, TEXT_HINT), f_small.render(str(i), True, TEXT_HINT).get_rect(center=(cx, cy)))
 
        # draw a line through the winning three cells when win condtion met
        if win_cells:
            r0      = cell_rect(win_cells[0])
            r2      = cell_rect(win_cells[2])
            win_col = X_COLOR if state['winner'] == "X" else O_COLOR
            pygame.draw.line(screen, win_col, r0.center, r2.center, 4)
 
        # status bar
        # win message always overrides everything else
        if state['game_over']:
            if state['winner']:
                message = f"Player {state['winner']} wins!"
            else:
                message = "It's a draw!"
            sub = "Press R to reset"
 
        sy = GRID_T + GRID_SIZE + 14
        screen.blit(f_body.render(message, True, TEXT_PRI), (GRID_L, sy))
        if sub:
            screen.blit(f_small.render(sub, True, TEXT_SEC), (GRID_L, sy + 20))
 
        # side panel — entanglement links
        screen.blit(f_small.render("LINKS", True, TEXT_HINT), (PANEL_X, PANEL_Y))
        y = PANEL_Y + 18
        if not game.links:
            screen.blit(f_small.render("none yet", True, TEXT_HINT), (PANEL_X, y)); y += 15
        else:
            for ca, cb, player, mn in game.links[-10:]:
                col  = X_DIM if player == "X" else O_DIM
                screen.blit(f_small.render(f"{player}{mn}  {ca}↔{cb}", True, col), (PANEL_X, y)); y += 15
 
        pygame.draw.line(screen, PANEL_LINE, (PANEL_X, y + 4), (PANEL_X + PANEL_W, y + 4), 1); y += 14
 
        # board state
        screen.blit(f_small.render("BOARD", True, TEXT_HINT), (PANEL_X, y)); y += 18
        for i in range(9):
            val = game.board[i]
            if isinstance(val, str):
                col = X_COLOR if val == "X" else O_COLOR
                txt = f_small.render(f"{i}: {val}", True, col)
            elif val:
                marks = " ".join(f"{pl}{mn}" for pl, mn in val)
                txt   = f_small.render(f"{i}: {marks}", True, TEXT_SEC)
            else:
                txt = f_small.render(f"{i}: —", True, TEXT_HINT)
            screen.blit(txt, (PANEL_X, y)); y += 14
 
        # move counter
        pygame.draw.line(screen, PANEL_LINE, (PANEL_X, y + 4), (PANEL_X + PANEL_W, y + 4), 1); y += 14
        screen.blit(f_small.render(f"move {state['move_num']}", True, TEXT_HINT), (PANEL_X, y))
 
        # reset button
        rrect = pygame.Rect(PANEL_X, H - 50, PANEL_W, 34)
        rhov  = rrect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, PANEL_LINE if rhov else PANEL_BG, rrect)
        pygame.draw.rect(screen, PANEL_LINE, rrect, 1)
        lbl = f_body.render("↺  Reset  (R)", True, TEXT_SEC)
        screen.blit(lbl, lbl.get_rect(center=rrect.center))
 
        pygame.display.flip()
 
    pygame.quit()