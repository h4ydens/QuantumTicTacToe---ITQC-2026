import collapse as game
from collapse import find_cycle, collapse_cycle
from ui import run_ui
 
# All in a dict so ui.py can read it by reference and is constantly updated
state = {
    "move_num":       0,
    "current_player": "X",
    "game_over":      False,
    "winner":         None,
}
# Wining line combos
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
 
# Checks if three collapsed board positions match, meaning a player has won the game
def check_winner():
    for a, b, c in LINES:
        if (isinstance(game.board[a], str)
                and game.board[a] == game.board[b] == game.board[c]):
            return game.board[a]
    return None
 
# Stores extra information for the UI, such as whether a collapse happened and what cells were involved
def on_move(cell_a, cell_b):
    state["move_num"] += 1
    game.board[cell_a].append((state["current_player"], state["move_num"]))
    game.board[cell_b].append((state["current_player"], state["move_num"]))
    game.links.append((cell_a, cell_b, state["current_player"], state["move_num"]))
 
    result = {"collapsed": False, "cycle_cells": [], "bitstring": ""}
 
    # Detects cycles in the quantum board, which trigger a collapse into classical states
    cycle = find_cycle()
    if cycle:
        bits = collapse_cycle(cycle)
        result.update(collapsed=True, cycle_cells=cycle, bitstring=bits)
 
    # check for winner every move
    state["winner"] = check_winner()
    if state["winner"] or not any(isinstance(game.board[i], list) for i in range(9)):
        state["game_over"] = True
     
    # Switches the active player after each valid move
    state["current_player"] = "O" if state["current_player"] == "X" else "X"
    return result
 
# Resets the board and all game variables back to their default starting state
def on_reset():
    state["move_num"]       = 0
    state["current_player"] = "X"
    state["game_over"]      = False
    state["winner"]         = None
    game.board[:] = [[] for _ in range(9)]
    game.links[:]  = []
 
# Starts the graphical UI and connects the game logic functions to the interface
if __name__ == "__main__":
    run_ui(on_move, on_reset, state)
