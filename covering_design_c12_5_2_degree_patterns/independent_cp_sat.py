#!/usr/bin/env python3
"""Independent CP-SAT formulation of the excluded degree pattern.

Requires OR-Tools.  This is a cross-check, not the proof-certificate path.
"""

from __future__ import annotations

import json

from ortools.sat.python import cp_model


def main() -> None:
    degrees = (5, 5, 5, 5, 4, 3, 3, 3, 3, 3, 3, 3)
    model = cp_model.CpModel()
    incidence = [[model.new_bool_var(f"x_{row}_{column}") for column in range(9)]
                 for row in range(12)]
    for row, degree in enumerate(degrees):
        model.add(sum(incidence[row]) == degree)
    for column in range(9):
        model.add(sum(incidence[row][column] for row in range(12)) == 5)
    for first in range(12):
        for second in range(first + 1, 12):
            together = []
            for column in range(9):
                conjunction = model.new_bool_var(f"z_{first}_{second}_{column}")
                model.add(conjunction <= incidence[first][column])
                model.add(conjunction <= incidence[second][column])
                model.add(conjunction >= incidence[first][column] + incidence[second][column] - 1)
                together.append(conjunction)
            model.add(sum(together) >= 1)
    column_values = [sum((1 << row) * incidence[row][column] for row in range(12))
                     for column in range(9)]
    for column in range(8):
        model.add(column_values[column] < column_values[column + 1])
    row_values = [sum((1 << column) * incidence[row][column] for column in range(9))
                  for row in range(12)]
    for first, last in ((0, 4), (5, 12)):
        for row in range(first, last - 1):
            model.add(row_values[row] < row_values[row + 1])
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    status = solver.solve(model)
    summary = {"status": solver.status_name(status), "branches": solver.num_branches,
               "conflicts": solver.num_conflicts, "wall_time": solver.wall_time}
    print(json.dumps(summary, sort_keys=True))
    assert status == cp_model.INFEASIBLE
    print("independent_cp_sat=PASS")


if __name__ == "__main__":
    main()
