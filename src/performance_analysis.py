import csv
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import search_algorithm as sa
from src import manifest_parser as mp

def run_experiments(test_files):
    results = []

    for use_astar in [False, True]:
        sa.USE_ASTAR = use_astar
        algorithm = "A*" if use_astar else "UCS"

        for test_file in test_files:
            print(f"\nRunning {algorithm} on {test_file}")
            manifest = []
            with open(test_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        manifest.append(mp.parse_manifest_line(line))
            state = mp.create_initial_state(manifest)

            start_time = time.time()
            result = sa.uniformCostSearch(state)
            run_time = time.time() - start_time

            cost, final_state, moves, cost_list, move_count, nodes_expanded = result

            ph, sh = sa.getCurrentWeight(final_state)
            balance_diff = abs(ph - sh)

            results.append({
                "algorithm": algorithm,
                "test_file": test_file,
                "cost": cost,
                "moves": move_count,
                "nodes_expanded": nodes_expanded,
                "time": run_time,
                "balance_diff": balance_diff
            })

    with open('performance_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['algorithm', 'test_file', 'cost', 'moves', 'nodes_expanded', 'time', 'balance_diff']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print("Performance results written to performance_results.csv")

if __name__ == "__main__":
    test_files = [
        "data/ShipCase1.txt",
        "data/ShipCase2.txt",
        "data/ShipCase3.txt",
        "data/ShipCase4.txt",
        "data/ShipCase5.txt",
        "data/ShipCase6.txt"
    ]
    run_experiments(test_files)