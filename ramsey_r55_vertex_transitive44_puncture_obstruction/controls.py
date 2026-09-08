#!/usr/bin/env python3
"""Small exact controls for the independent checker primitives."""

import json

from verify import (N, generated_group, is_refinement, list_dpll,
                    orbit_partition)


cycle = tuple(list(range(1, N)) + [0])
cyclic_group = generated_group((cycle,), N)
partition = orbit_partition((cycle,))
tests = {
    "contradictory_units_unsat": list_dpll(((1,), (-1,)))[0] is False,
    "one_clause_sat": list_dpll(((1, 2),))[0] is True,
    "cyclic44_generated_order": len(cyclic_group) == N,
    "cyclic44_edge_orbits": len(set(partition)) == 22,
    "strict_refinement_positive": is_refinement((0, 1, 2, 3), (0, 0, 1, 1)),
    "strict_refinement_negative": not is_refinement((0, 0, 1, 1), (0, 1, 0, 1)),
}
if not all(tests.values()):
    raise AssertionError(tests)
print(json.dumps(tests, indent=2, sort_keys=True))
