from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import qasm2
from quokka_client import run_on_quokka
 
# shared game state where board and links are imported/used by main and ui
board = [[] for _ in range(9)]
links = []  # (cell_a, cell_b, player, move_num)
 
def find_cycle():
    # build adjacency map then DFS looking for a back-edge
    adj = {}
    for cell_a, cell_b, _, _ in links:
        adj.setdefault(cell_a, set()).add(cell_b)
        adj.setdefault(cell_b, set()).add(cell_a)
 
    visited = set()
 
    def dfs(node, parent, path):
        visited.add(node)
        path.append(node)
        for neighbour in adj.get(node, []):
            if neighbour not in visited:
                result = dfs(neighbour, node, path)
                if result:
                    return result
            elif neighbour != parent:
                cycle_start = path.index(neighbour)
                return path[cycle_start:]
        path.pop()
        return None
 
    for cell in list(adj.keys()):
        if cell not in visited:
            result = dfs(cell, -1, [])
            if result:
                return result
    return None
 
 
def collapse_cycle(cycle_cells: list):
    n = len(cycle_cells)
 
    # GHZ circuit: H on first qubit, CNOT chain, then measure
    qr = QuantumRegister(n, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    for i in range(n - 1):
        qc.cx(qr[i], qr[i + 1])
    qc.measure(qr, cr)
 
    print(f"\nCollapse triggered on cells {cycle_cells}")
    print(qc.draw(output="text"))
    bitstring = run_on_quokka(qasm2.dumps(qc))
    print(f"Quokka bitstring: {bitstring}\n")
 
    # if bit read 1 first mark wins
    # if bit read 0 second mark wins
    for idx, cell in enumerate(cycle_cells):
        bit = bitstring[idx]
        marks = board[cell]
        if isinstance(marks, list) and marks:
            winner = marks[0] if (bit == "1" or len(marks) == 1) else marks[1]
            board[cell] = winner[0]
 
    # drop links that touched collapsed cells
    global links
    links = [l for l in links if l[0] not in cycle_cells and l[1] not in cycle_cells]
 
    return bitstring
