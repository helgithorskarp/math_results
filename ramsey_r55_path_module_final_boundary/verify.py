"""Exact arithmetic controls for the written compatibility proof.

This is not a formalization, a random graph simulation, or a good43 solver.
The all-t statement is proved by the induction in PROOF.md.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from math import comb, factorial


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    pairs = list(combinations(range(5), 2))
    positions = {p: i for i, p in enumerate(pairs)}
    words = {
        sum(1 << positions[tuple(sorted((p[i], p[i + 1])))] for i in range(4))
        for p in permutations(range(5))
    }
    opposite = {1023 ^ w for w in words}
    # A second literal definition checks the claimed pattern count.
    degree_paths = set()
    for word in range(1024):
        neighbors = [set() for _ in range(5)]
        for i, (u, v) in enumerate(pairs):
            if word >> i & 1:
                neighbors[u].add(v)
                neighbors[v].add(u)
        if sorted(map(len, neighbors)) != [1, 1, 2, 2, 2]:
            continue
        seen, frontier = {0}, [0]
        while frontier:
            for v in neighbors[frontier.pop()] - seen:
                seen.add(v)
                frontier.append(v)
        if len(seen) == 5:
            degree_paths.add(word)
    require(words == degree_paths and len(words) == 60, 'literal path probability')
    require(len(opposite) == 60 and not words & opposite, 'two pattern colours')
    path_probability = F(len(words), 1024)
    require(path_probability == F(15, 256), 'probability fraction')
    ln2_series = sum((F(7, 10) ** i) / factorial(i) for i in range(5))
    require(ln2_series > 2, 'ln(2)<7/10 exponential-series certificate')
    require(3 ** 4 < 2 ** 7, 'large uniform-pair union estimate')
    require((F(1, 2) - F(3, 8)) / 10 == F(1, 80), 'test quadratic coefficient')
    require(F(-1, 2) / 10 == F(-1, 20), 'test linear coefficient')
    require(path_probability / 80 == F(3, 4096), 'path exponential coefficient')

    t = 16
    n, k, m = 2 ** t, 2 * t + 1, 1024 * t
    require(n >= m and n // 16 > 31, 'nonvacuous base parameters')
    require(F(3, 160) * t - F(3, 1024) > 0, 'path exponent base margin')
    require(F(3, 160) > 0, 'path margin increasing for all t')
    require(2 ** (t - 7) - 31 * t - 5 == 11, 'small-module exponent base')
    require(2 ** (t - 7) - 31 > 0, 'small-module exponent monotone thereafter')
    require(1024 * (t - 1) >= 0, 'n>=m induction remainder nonnegative thereafter')
    require(3 * n // 16 > 11, 'large-module dyadic exponent')
    require(32 * t * t - 1 > 11, 'path dyadic exponent')
    require(F(2, factorial(k)) < F(1, 2048), 'Ramsey base event')
    require(4 * F(1, 2048) == F(1, 512), 'complete event union')
    endpoint_expectation = F(2 * comb(43, 5), 2 ** comb(5, 2))
    require(endpoint_expectation == F(481299, 256) and endpoint_expectation > 1,
            'actual endpoint is not covered')
    out = {
        'status': 'EXACT_ARITHMETIC_CONTROLS_PASSED_FINAL_GATE_FAILED',
        'literal_five_vertex_words_checked': 1024,
        'red_path_words': len(words), 'blue_path_words': len(opposite),
        'path_probability': str(path_probability),
        'ln2_series_lower_bound': str(ln2_series),
        'base_parameters': {'t': t, 'n': n, 'k': k, 'm': m,
                            'prime_induced_order_threshold': 5 * n // 8,
                            'outside_every_path_free_core_at_least': n - m + 1},
        'small_module_log_bound_base': -11,
        'small_module_decay_increment_at_base': 2 ** (t - 7) - 31,
        'path_margin_base': str(F(3, 160) * t - F(3, 1024)),
        'failure_probability_strict_upper_bound': '1/512',
        'uniform_validity': 'Written induction and monotonicity in PROOF.md, not finite extrapolation',
        'ramsey43_first_moment_term': str(endpoint_expectation),
        'explicit_good_graph_produced': False,
        'new_good43_decisions': 0, 'new_ramsey_bound': False,
        'final_gate_met': False,
        'scope': 'Exact controls for a classical probabilistic compatibility argument at growing clique size; no order43 theorem',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
