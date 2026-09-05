"""Root-clique encoding of a partially colored Ramsey template.

True means red. Core edges and root-to-central incidences are fixed;
unordered central pairs, in lexicographic order, are Boolean variables.
No symmetry breaking or auxiliary variables are used.
"""
from itertools import combinations


def layout(template, deleted=None):
    k = template['core_order']
    signatures = [s for s, n in template['cells'] for _ in range(n)]
    E = tuple(v for v in range(k) if v != deleted)
    C = tuple(v for v in range(k, k + len(signatures)) if v != deleted)
    fixed = {(u, v): template['core_mask'] >> bit & 1
             for bit, (u, v) in enumerate(combinations(range(k), 2))}
    fixed.update({(u, v): signatures[v-k] >> u & 1 for u in E for v in C})
    variables = tuple(combinations(C, 2))
    return E, C, fixed, variables


def formula(template, deleted=None, full=False):
    """Append a central monochromatic clique to a fixed root clique."""
    E, C, fixed, variables = layout(template, deleted)
    index = {pair: i+1 for i, pair in enumerate(variables)}
    clauses = set()
    for color in (0, 1):
        for count in range(0 if full else 1, 6):
            for roots in combinations(E, count):
                if any(fixed[e] != color for e in combinations(roots, 2)):
                    continue
                common = tuple(v for v in C if all(fixed[u, v] == color for u in roots))
                for tail in combinations(common, 5-count):
                    clause = tuple(sorted((1-2*color)*index[p] for p in combinations(tail, 2)))
                    clauses.add(clause)
    return variables, tuple(sorted(clauses, key=lambda c: (len(c), c)))


def dimacs(variables, clauses):
    return f'p cnf {len(variables)} {len(clauses)}\n' + ''.join(
        ' '.join(map(str, clause)) + ' 0\n' for clause in clauses)
