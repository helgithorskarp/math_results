"""Complete s=1 physical family, with a canonical 12-vertex residual selector."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
CATALOG = HERE.parent / 'ramsey_r55_global_greedy_closure' / 'r35_12.g6'
CATALOG_SHA = '322e7a54e67f4201bd37998ab420afb3eee41b1dcd6b277b7f055bda152da95e'


def catalog():
    raw = CATALOG.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA:
        raise ValueError('catalog identity')
    graphs = []
    for line in raw.decode('ascii').splitlines():
        if len(line) != 12 or line[0] != 'K':
            raise ValueError('graph6 format')
        bits = ''.join(format(ord(c) - 63, '06b') for c in line[1:])
        order = [(i, j) for j in range(1, 12) for i in range(j)]
        graphs.append({p for p, bit in zip(order, bits) if bit == '1'})
    if len(graphs) != 12:
        raise ValueError('catalog cardinality')
    return graphs


def clean(literals):
    """Canonical clause; None means satisfied by constants or a tautology."""
    values = set(literals)
    if 1 in values or any(-x in values for x in values if x != -1):
        return None
    values.discard(-1)
    return tuple(sorted(values, key=lambda x: (abs(x), x)))


class Model:
    def __init__(self, factored=True):
        self.factored = factored
        self.graphs = catalog()
        self.blocks = [list(range(4*i, 4*i+4)) for i in range(7)] + [[28, 29, 30]]
        self.fixed = {}
        for i, block in enumerate(self.blocks):
            for edge in combinations(block, 2):
                self.fixed[edge] = 1 if i < 5 or i == 7 else 794 + i - 5
        self.free = {p: i+2 for i, p in enumerate(p for p in combinations(range(43), 2)
                                               if p not in self.fixed and p[0] < 31)}
        if len(self.free) != 792:
            raise ValueError('physical variables')
        self.selectors = list(range(796, 808))
        self.tail_masks = {}
        for size in range(2, 6):
            for q in combinations(range(31, 43), size):
                for color in (1, 0):
                    allowed = [k for k, g in enumerate(self.graphs)
                               if all(((u-31, v-31) in g) == bool(color)
                                      for u, v in combinations(q, 2))]
                    self.tail_masks[q, color] = tuple(self.selectors[k] for k in range(12) if k not in allowed)
        masks = {sum(1 << (z-796) for z in misses) for misses in self.tail_masks.values()}
        canonical = sorted({min(m, 4095 ^ m) for m in masks} - {0})
        self.predicates = {mask: 808+i for i, mask in enumerate(canonical)} if factored else {}
        self.first_prefix = 808+len(self.predicates)
        self.symmetry, self.variables, self.comparisons = self.make_symmetry()

    def edge(self, u, v, selected):
        if u > v:
            u, v = v, u
        if u >= 31:
            return int((u-31, v-31) in self.graphs[selected])
        return self.fixed.get((u, v), self.free.get((u, v)))

    def make_symmetry(self):
        clauses, comparisons = [], []
        next_aux = self.first_prefix

        def compare(xs, ys, guards, description):
            nonlocal next_aux
            prefix = 1
            for position, (x, y) in enumerate(zip(xs, ys)):
                clauses.append(clean((*guards, -prefix, x, -y)))
                if position+1 < len(xs):
                    z = next_aux; next_aux += 1
                    # Prefix equalities are unconditional, including for an inactive order.
                    for c in [(-z, prefix), (-z, -x, y), (-z, x, -y),
                              (-prefix, -x, -y, z), (-prefix, x, y, z)]:
                        clauses.append(clean(c))
                    prefix = z
            comparisons.append({'left': list(xs), 'right': list(ys),
                                'guards': list(guards), 'description': description})

        def signature(v):
            return [self.free[row, v] for row in range(3, -1, -1)]
        def key(block):
            return [bit for v in self.blocks[block] for bit in signature(v)]
        for index, block in enumerate(self.blocks[1:], 1):
            for a, b in zip(block, block[1:]):
                compare(signature(a), signature(b), (), f'vertices {a}>={b}')
        for a, b in [(1, 2), (2, 3), (3, 4)]:
            compare(key(a), key(b), (), f'red blocks {a}>={b}')
        compare(key(4), key(5), (-794,), 'blocks 4>=5 when block5 red')
        # c6 <= c5. Compare blocks 5 and 6 if both blue OR both red.
        # Two independently encoded conditional comparators avoid a selector auxiliary.
        compare(key(5), key(6), (794,), 'blocks 5>=6 when block5 blue')
        compare(key(5), key(6), (-795,), 'blocks 5>=6 when block6 red')
        return [c for c in clauses if c is not None], next_aux-1, comparisons

    def forbidden(self, q, color, guards=()):
        tail = tuple(v for v in q if v >= 31)
        gate = self.tail_masks[tail, color] if len(tail) >= 2 else ()
        if len(gate) == 12:
            return None
        if self.factored and gate:
            mask = sum(1 << (z-796) for z in gate)
            canonical = min(mask, 4095 ^ mask)
            flag = self.predicates[canonical]
            gate = (flag if mask == canonical else -flag,)
        literals = list(guards) + list(gate)
        for edge in combinations(q, 2):
            if edge[0] >= 31:
                continue
            variable = self.fixed.get(edge, self.free.get(edge))
            literals.append(-variable if color else variable)
        return clean(literals)

    def sections(self):
        yield 'constant', [(1,)]
        yield 'selectors', [tuple(self.selectors)] + [(-a, -b) for a, b in combinations(self.selectors, 2)]
        yield 'block_colors', [(794, -795)]
        yield 'tail_predicates', [(-z, flag if mask >> k & 1 else -flag)
                                  for mask, flag in self.predicates.items()
                                  for k, z in enumerate(self.selectors)]
        yield 'symmetry', self.symmetry
        def targets():
            for q in combinations(range(43), 5):
                for color in (1, 0):
                    c = self.forbidden(q, color)
                    if c is not None:
                        yield c
        yield 'target', targets()
        def closure():
            for start, color_variable in [(20, 794), (24, 795)]:
                for q in combinations(range(start, 43), 4):
                    c = self.forbidden(q, 1, (color_variable,))
                    if c is not None:
                        yield c
        yield 'greedy_closure', closure()

    def assignment(self, graph, selected):
        """Complete auxiliary extension; used for normalizer controls and SAT decoding."""
        values = {1: True}
        values.update({v: bool(graph[u][w]) for (u, w), v in self.free.items()})
        values[794] = bool(graph[20][21]); values[795] = bool(graph[24][25])
        values.update({v: i == selected for i, v in enumerate(self.selectors)})
        values.update({flag: bool(mask >> selected & 1) for mask, flag in self.predicates.items()})
        next_aux = self.first_prefix
        for comp in self.comparisons:
            equal = True
            for x, y in list(zip(comp['left'], comp['right']))[:-1]:
                equal = equal and values[x] == values[y]
                values[next_aux] = equal; next_aux += 1
        if next_aux != self.variables + 1:
            raise ValueError('auxiliary extension')
        return values


def write(path, factored=True):
    model = Model(factored); path = Path(path)
    if path.exists():
        raise ValueError('refusing to overwrite')
    counts = {name: sum(1 for _ in clauses) for name, clauses in model.sections()}
    count = sum(counts.values()); digest = hashlib.sha256(); sizes = {}
    with path.open('wb') as f:
        line = f'p cnf {model.variables} {count}\n'.encode(); f.write(line); digest.update(line)
        for name, clauses in model.sections():
            actual = 0
            for c in clauses:
                line = (' '.join(map(str, c)) + ' 0\n').encode(); f.write(line); digest.update(line)
                actual += 1; sizes[len(c)] = sizes.get(len(c), 0) + 1
            if actual != counts[name]:
                raise ValueError('section cardinality')
    return {'status': 'GENERATED_COMPLETE_NINE_BRANCH_SELECTOR', 'variables': model.variables,
            'free_physical_edges': 792, 'block_color_variables': 2, 'tail_selectors': 12,
            'prefix_variables': model.variables-model.first_prefix+1,
            'tail_predicate_variables': len(model.predicates), 'factored': factored,
            'clauses': count, 'sections': counts,
            'bytes': path.stat().st_size, 'sha256': digest.hexdigest(),
            'clause_lengths': sizes, 'catalog_sha256': CATALOG_SHA,
            'covered_gc1_branches': [[r, 1, t] for r in (5, 6, 7) for t in (0, 1, 2)]}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--cnf', type=Path, required=True)
    p.add_argument('--metadata', type=Path); p.add_argument('--direct', action='store_true'); a = p.parse_args()
    result = json.dumps(write(a.cnf, not a.direct), indent=2, sort_keys=True)+'\n'
    if a.metadata:
        a.metadata.write_text(result)
    print(result, end='')
