# QuantumTicTacToe---ITQC-2026
 
A quantum application on tic-tac-toe. Marks exist in superposition across two cells until an entanglement cycle forces a collapse, measured by the Quokka qasm backend.
 
## Requirements

Must use python 3.11!
 
```bash
pip install pygame qiskit requests
```
 
## How to Run
 
```bash
python main.py
```
 
## How to Play
 
1. Each turn, click two cells to place your quantum marks in superposition
2. Your mark exists in superposition across both cells (shown as X1, O2 etc.)
3. Once a cycle forms in the entanglement graph, Quokka measures the qubits
4. Each cell in the cycle collapses to a classical X or O
5. First to get three in a row wins
Press button to RESET, press ESC to quit or close window.
 
## Files
 
Files and Description
`main.py` - Game loop and win detection
`ui.py` - Pygame interface
`collapse.py` - Cycle detection and Quokka collapse logic
`quokka_client.py` - Quokka API call
 
### Students
Creator: H4y
