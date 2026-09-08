"""Independent bit-mask physical reconstruction and normalization controls."""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
import compile as compiler
import normalize
import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent_catalog():
    records = []
    for text in compiler.CATALOG.read_text().splitlines():
        packed = 0
        for c in text[1:]:
            packed = 64*packed + ord(c)-63
        matrix = [[0]*12 for _ in range(12)]; k = 65
        for v in range(1, 12):
            for u in range(v):
                matrix[u][v] = matrix[v][u] = (packed >> k) & 1; k -= 1
        for q in combinations(range(12), 3):
            require(not all(matrix[u][v] for u, v in combinations(q, 2)), 'catalog red triangle')
        for q in combinations(range(12), 5):
            require(any(matrix[u][v] for u, v in combinations(q, 2)), 'catalog blue five')
        records.append(matrix)
    require(len(records) == 12, 'catalog count')
    return records


def reference(factored=True):
    """All physical edges as either signed-variable expressions or 12-bit tables."""
    graphs = independent_catalog(); edges = {}; tables = {}; next_variable = 2
    for u, v in combinations(range(43), 2):
        if u >= 31:
            tables[u, v] = sum(g[u-31][v-31] << k for k, g in enumerate(graphs))
        elif u//4 == v//4 and v < 28:
            edges[u, v] = 1 if u < 20 else 794 if u < 24 else 795
        elif 28 <= u < v <= 30:
            edges[u, v] = 1
        else:
            edges[u, v] = next_variable; next_variable += 1
    require(next_variable == 794, 'reference physical numbering')
    masks = set()
    for size in range(2, 6):
        for q in combinations(range(31, 43), size):
            for color in (0, 1):
                active = 4095
                for pair in combinations(q, 2):
                    active &= tables[pair] if color else tables[pair] ^ 4095
                if active not in (0, 4095):
                    masks.add(min(active, active ^ 4095))
    predicates = {m: 808+i for i, m in enumerate(sorted(masks))} if factored else {}

    def sorted_clause(xs):
        positive = {x for x in xs if x > 0}
        negative = {-x for x in xs if x < 0}
        if 1 in positive or positive.intersection(negative):
            return None
        negative.discard(1)
        return tuple(x if x in positive else -x for x in sorted(positive | negative))

    def forbidden(q, color, guard=None):
        active = 4095; literals = [] if guard is None else [guard]
        for pair in combinations(q, 2):
            if pair in tables:
                active &= tables[pair] if color else 4095 ^ tables[pair]
            else:
                literals.append(-edges[pair] if color else edges[pair])
        if not active:
            return None
        if factored and active != 4095:
            misses = active ^ 4095; canonical = min(active, misses)
            literals.append(predicates[canonical] if misses == canonical else -predicates[canonical])
        elif not factored:
            literals.extend(796+k for k in range(12) if not (active >> k & 1))
        return sorted_clause(literals)

    yield 'constant', [(1,)]
    yield 'selectors', [tuple(range(796, 808))] + [(-a, -b) for a, b in combinations(range(796, 808), 2)]
    yield 'block_colors', [(794, -795)]
    yield 'tail_predicates', [(-(796+k), variable if mask & (1 << k) else -variable)
                              for mask, variable in predicates.items() for k in range(12)]
    comparisons = []
    def sig(vertex):
        return [edges[u, vertex] for u in (3, 2, 1, 0)]
    def blockkey(block):
        return [x for v in range(4*block, 4*block+4) for x in sig(v)]
    for block in [list(range(4*i, 4*i+4)) for i in range(1, 7)] + [[28, 29, 30]]:
        for u, v in zip(block, block[1:]):
            comparisons.append((sig(u), sig(v), []))
    for i in (1, 2, 3):
        comparisons.append((blockkey(i), blockkey(i+1), []))
    comparisons += [(blockkey(4), blockkey(5), [-794]),
                    (blockkey(5), blockkey(6), [794]),
                    (blockkey(5), blockkey(6), [-795])]
    symmetry = []; next_aux = 808+len(predicates)
    for left, right, guard in comparisons:
        prefix = 1
        for i in range(len(left)):
            x, y = left[i], right[i]
            raw = [guard+[-prefix, x, -y]]
            if i < len(left)-1:
                z = next_aux; next_aux += 1
                raw += [[-z, prefix], [-z, -x, y], [-z, x, -y],
                        [-prefix, -x, -y, z], [-prefix, x, y, z]]
                prefix = z
            for clause in raw:
                c = sorted_clause(clause)
                if c is not None:
                    symmetry.append(c)
    require(next_aux == 958+len(predicates), 'reference auxiliaries')
    yield 'symmetry', symmetry
    def target():
        for q in combinations(range(43), 5):
            for color in (1, 0):
                c = forbidden(q, color)
                if c is not None:
                    yield c
    yield 'target', target()
    def closure():
        for vertices, guard in [(range(20, 43), 794), (range(24, 43), 795)]:
            for q in combinations(vertices, 4):
                c = forbidden(q, 1, guard)
                if c is not None:
                    yield c
    yield 'greedy_closure', closure()


def full_audit(path, factored=True):
    digest = hashlib.sha256(); counts = {}; literals = 0
    with Path(path).open('rb') as f:
        line = f.readline(); digest.update(line)
        header = line.decode().split()
        require(len(header) == 4 and header[:3] == ['p', 'cnf', '1184' if factored else '957'], 'CNF header')
        for name, clauses in reference(factored):
            count = 0
            for expected in clauses:
                actual = f.readline(); digest.update(actual)
                wanted = (' '.join(map(str, expected))+' 0\n').encode()
                require(actual == wanted, f'physical literal mismatch {name}:{count}')
                count += 1; literals += len(expected)
            counts[name] = count
        require(f.read() == b'', 'trailing formula content')
        require(sum(counts.values()) == int(header[3]), 'header clause count')
    return {'status': 'VERIFIED_EVERY_AGGREGATE_LITERAL', 'sections': counts,
            'clauses': sum(counts.values()), 'literals': literals,
            'sha256': digest.hexdigest(), 'physical_five_subsets': 962598,
            'independent_representation': '12-bit edge truth tables and direct physical pairs'}


def controls():
    model = compiler.Model(); catalogs = independent_catalog()
    for i, matrix in enumerate(catalogs):
        require(model.graphs[i] == {p for p in combinations(range(12), 2) if matrix[p[0]][p[1]]}, 'independent graph6 parse')
    # Exact one-hot condition for every Boolean assignment to the 12 selectors.
    onehot = dict(model.sections())['selectors']; selector_checks = 0
    for bits in range(4096):
        values = {796+k: bool(bits >> k & 1) for k in range(12)}
        sat = all(any(values[abs(x)] == (x > 0) for x in c) for c in onehot)
        require(sat == (bits.bit_count() == 1), 'selector truth table'); selector_checks += 1
    # Exhaustively check the local prefix recurrence (the inductive comparator step).
    recurrence_checks = 0
    for p, x, y, z in product([False, True], repeat=4):
        clauses = [(not z or p), (not z or not x or y), (not z or x or not y),
                   (not p or not x or not y or z), (not p or x or y or z)]
        require(all(clauses) == (z == (p and x == y)), 'prefix equivalence')
        recurrence_checks += 1
    gate_checks = 0
    for (q, color), misses in model.tail_masks.items():
        for k, graph in enumerate(catalogs):
            active = all(graph[u-31][v-31] == color for u, v in combinations(q, 2))
            require((796+k not in misses) == active, 'selector clique predicate'); gate_checks += 1
    definition_checks = 0
    definitions = dict(model.sections())['tail_predicates']
    for k in range(12):
        for mask, flag in model.predicates.items():
            for value in (False, True):
                relevant = [c for c in definitions if abs(c[1]) == flag]
                accepted = all((abs(c[0])-796 != k) or (value == (c[1] > 0)) for c in relevant)
                require(accepted == (value == bool(mask >> k & 1)), 'predicate definition')
                definition_checks += 1
    rng = random.Random(3863); fixtures = 0; transports = 0; closure_checks = 0; reverse_edges = 0
    for r, selected in product((5, 6, 7), range(12)):
        matrix = [[0]*43 for _ in range(43)]
        for u, v in combinations(range(43), 2):
            if u >= 31:
                color = catalogs[selected][u-31][v-31]
            elif (u, v) in model.fixed:
                expression = model.fixed[u, v]
                color = 1 if expression == 1 else int(r > (5 if expression == 794 else 6))
            else:
                color = rng.randrange(2)
            matrix[u][v] = matrix[v][u] = color
        # Force a non-target fixture without disturbing any fixed core or tail edge.
        for u in range(4):
            matrix[u][4] = matrix[4][u] = 1
        tail = list(range(31, 43)); rng.shuffle(tail)
        matrix = normalize.transport(matrix, list(range(31))+tail)
        result = normalize.normalize(matrix); new = result['matrix']; order = result['order']
        require(sorted(order) == list(range(43)), 'fixture permutation')
        for u, v in combinations(range(43), 2):
            require(new[u][v] == matrix[order[u]][order[v]], 'physical transport'); transports += 1
        require(result['r'] == r, 'r preserved')
        k = result['catalog_index']
        require(all(new[u+31][v+31] == catalogs[k][u][v] for u, v in combinations(range(12), 2)), 'canonical tail')
        reverse = normalize.repack(new); back = reverse['matrix']; permutation = reverse['order']
        for u, v in combinations(range(43), 2):
            require(back[u][v] == new[permutation[u]][permutation[v]], 'reverse physical transport'); reverse_edges += 1
        for start in (31, 34, 37):
            require(not any(back[u][v] for u, v in combinations(range(start, start+3), 2)), 'reverse blue triple')
            sigs = [sum(back[row][v] << row for row in range(4)) for v in range(start, start+3)]
            require(sigs == sorted(sigs, reverse=True), 'reverse root sorting')
        expected_mask = (0, 1, 3)[reverse['t']]
        require(sum(back[u][v] << i for i, (u, v) in enumerate(combinations(range(40, 43), 2))) == expected_mask, 'reverse final shape')
        comparable = [(0, 1), (1, 2)] if reverse['t'] == 0 else [(0, 1)] if reverse['t'] == 1 else [(1, 2)]
        signatures = [sum(back[row][v] << row for row in range(4)) for v in range(40, 43)]
        require(all(signatures[a] >= signatures[b] for a, b in comparable), 'reverse final root sorting')
        values = model.assignment(new, k)
        for name, clauses in model.sections():
            if name in ('target', 'greedy_closure'):
                continue
            require(all(any(values[abs(x)] == (x > 0) for x in c) for c in clauses), 'normal form clause')
        if r < 7:
            vertices = list(range(4*r, 43))
            require(set(order[v] for v in vertices) == set(vertices), 'closure union invariant')
            old_count = sum(all(matrix[u][v] for u, v in combinations(q, 2)) for q in combinations(vertices, 4))
            new_count = sum(all(new[u][v] for u, v in combinations(q, 2)) for q in combinations(vertices, 4))
            require(old_count == new_count, 'closure count transported'); closure_checks += 1
        fixtures += 1
    negatives = 0
    for values in [{}, {1: True}, {i: False for i in range(1, model.variables+1)}, {i: True for i in range(1, model.variables+1)}]:
        try:
            verify.decode(values)
        except ValueError:
            negatives += 1
        else:
            raise ValueError('invalid model accepted')
    for graph in [{'n': 42, 'red_hex': '0'*226}, {'n': True, 'red_hex': '0'*226},
                  {'n': 43, 'red_hex': 'f'*226}, {'n': 43, 'red_hex': '0'}]:
        try:
            verify.graph_check(graph)
        except ValueError:
            negatives += 1
        else:
            raise ValueError('malformed graph accepted')
    for bits, expected in [(0, (0, 962598)), (2**903-1, (962598, 0))]:
        checked = verify.graph_check({'n': 43, 'red_hex': format(bits, '0226x')})
        require((checked['red_fives'], checked['blue_fives']) == expected, 'known physical graph')
        negatives += 1
    from run_decision import classify
    result_controls = [(0, '', 'c UNKNOWN\n', 'UNKNOWN'),
                       (0, '', '', 'UNEXPECTED_SOLVER_RESULT'),
                       (10, '', 'c UNKNOWN\n', 'UNEXPECTED_SOLVER_RESULT'),
                       (0, 's UNSATISFIABLE\n', 'c UNKNOWN\n', 'UNEXPECTED_SOLVER_RESULT'),
                       (10, '', 's SATISFIABLE\nv 1 0\n', 'SATISFIABLE'),
                       (20, '', 's UNSATISFIABLE\n', 'UNSATISFIABLE')]
    for code, stdout, witness, expected in result_controls:
        require(classify(code, stdout, witness) == expected, 'result reader control')
    return {'status': 'VERIFIED_SELECTOR_AND_NORMALIZATION_CONTROLS', 'catalogs': 12,
            'onehot_assignments': selector_checks, 'prefix_recurrence_assignments': recurrence_checks,
            'tail_predicate_cases': gate_checks, 'normalization_fixtures': fixtures,
            'predicate_definition_cases': definition_checks,
            'physical_edges_transported': transports, 'closure_count_transports': closure_checks,
            'reverse_repacking_edges': reverse_edges, 'reverse_repacking_fixtures': fixtures,
            'negative_controls': negatives, 'result_reader_controls': len(result_controls),
            'target_fixture_claims': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--cnf', type=Path)
    parser.add_argument('--output', type=Path); parser.add_argument('--direct', action='store_true')
    a = parser.parse_args(); start = time.monotonic()
    result = {'controls': controls()}
    if a.cnf:
        result['full_formula'] = full_audit(a.cnf, not a.direct)
    result['seconds'] = time.monotonic()-start
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if a.output:
        a.output.write_text(text)
    print(text, end='')
