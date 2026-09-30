"""Exact, depth-free Boolean sorting-prefix completion encoding (private probe)."""
import argparse
import hashlib
import itertools
import json
import pathlib
import resource
import time


def neg(literal):
    return not literal if isinstance(literal, bool) else -literal


class Writer:
    def __init__(self, path):
        self.stream = path.open('w+')
        self.stream.write(' ' * 100 + '\n')
        self.variables = self.clauses = 0

    def var(self):
        self.variables += 1
        return self.variables

    def add(self, *literals):
        if any(x is True for x in literals):
            return
        literals = list(dict.fromkeys(x for x in literals if x is not False))
        if any(-x in literals for x in literals):
            return
        self.stream.write(' '.join(map(str, literals)) + ' 0\n')
        self.clauses += 1

    def exactly_one(self, variables):
        self.add(*variables)
        if len(variables) <= 1:
            return
        aux = [self.var() for _ in range(len(variables) - 1)]
        self.add(-variables[0], aux[0])
        for i in range(1, len(variables) - 1):
            self.add(-variables[i], aux[i])
            self.add(-aux[i-1], aux[i])
            self.add(-variables[i], -aux[i-1])
        self.add(-variables[-1], -aux[-1])

    def equivalent_or(self, result, variables):
        self.add(-result, *variables)
        for variable in variables:
            self.add(-variable, result)

    def at_most(self, variables, bound):
        if bound >= len(variables):
            return
        if bound < 0:
            self.add()
            return
        if bound == 0:
            for variable in variables:
                self.add(-variable)
            return
        aux = [[self.var() for _ in range(bound)] for _ in variables[:-1]]
        self.add(-variables[0], aux[0][0])
        for j in range(1, bound):
            self.add(-aux[0][j])
        for i in range(1, len(variables) - 1):
            self.add(-variables[i], aux[i][0])
            for j in range(bound):
                self.add(-aux[i-1][j], aux[i][j])
            for j in range(1, bound):
                self.add(-variables[i], -aux[i-1][j-1], aux[i][j])
        for i in range(1, len(variables)):
            self.add(-variables[i], -aux[i-1][-1])

    def close(self):
        self.stream.seek(0)
        header = f'p cnf {self.variables} {self.clauses}'
        self.stream.write(header + ' ' * (100 - len(header)) + '\n')
        self.stream.close()


def sorted_state(n, weight):
    return ((1 << weight) - 1) << (n - weight)


def generate(n, states, gates, path, commute=True, budgets=None,
             encode_sorted=False, augment=None, fixed_edges=False):
    w = Writer(path)
    pairs = list(itertools.combinations(range(n), 2))
    choices = [[w.var() for _ in pairs] for _ in range(gates)]
    low = [[w.var() for _ in range(n)] for _ in range(gates)]
    high = [[w.var() for _ in range(n)] for _ in range(gates)]
    for t in range(gates):
        w.exactly_one(choices[t])
        for i in range(n):
            w.equivalent_or(low[t][i], [choices[t][k] for k, (a, b) in enumerate(pairs) if a == i])
            w.equivalent_or(high[t][i], [choices[t][k] for k, (a, b) in enumerate(pairs) if b == i])
        if commute and t:
            for k, p in enumerate(pairs):
                for j, q in enumerate(pairs[:k]):
                    if not set(p) & set(q):
                        w.add(-choices[t-1][k], -choices[t][j])
    unsorted = [x for x in states if x != sorted_state(n, x.bit_count())]
    # Sorted states need no transition equations unless their pruning budgets are used.
    encoded = states if budgets or encode_sorted else unsorted
    bits_by_state = {}
    for state in encoded:
        target = sorted_state(n, state.bit_count())
        bits = [[bool(state >> i & 1) for i in range(n)]]
        first_one = (state & -state).bit_length()-1 if state else n
        last_zero = (((1 << n)-1)^state).bit_length()-1
        bits.extend([[False if fixed_edges and i<first_one else
                      True if fixed_edges and i>last_zero else w.var()
                      for i in range(n)] for _ in range(gates - 1)])
        if gates:
            bits.append([bool(target >> i & 1) for i in range(n)])
        elif state != target:
            w.add()  # This unsorted state cannot be sorted by an empty network.
        bits_by_state[state] = bits
        for t in range(gates):
            X, Y = bits[t:t+2]
            for i in range(n):
                w.add(low[t][i], high[t][i], neg(X[i]), Y[i])
                w.add(low[t][i], high[t][i], X[i], neg(Y[i]))
                w.add(-low[t][i], neg(Y[i]), X[i])
                w.add(-high[t][i], neg(X[i]), Y[i])
            for k, (a, b) in enumerate(pairs):
                c = choices[t][k]
                w.add(-c, neg(Y[a]), X[b])
                w.add(-c, Y[a], neg(X[a]), neg(X[b]))
                w.add(-c, Y[b], neg(X[a]))
                w.add(-c, neg(Y[b]), X[a], X[b])
        if budgets and state in budgets:
            budget = budgets[state]
            for polarity, key in ((1, 'suffix_max_touch_bound'), (0, 'suffix_min_touch_bound')):
                # Saved budgets concern m=21; raising m raises each budget equally.
                limit = budget[key] + gates - 21
                if limit >= gates:
                    continue
                touch = [w.var() for _ in range(gates)]
                for t in range(gates):
                    for k, (a, b) in enumerate(pairs):
                        c = choices[t][k]
                        xa, xb = bits[t][a], bits[t][b]
                        if not polarity:
                            xa, xb = neg(xa), neg(xb)
                        w.add(-c, neg(xa), touch[t])
                        w.add(-c, neg(xb), touch[t])
                        w.add(-c, xa, xb, -touch[t])
                w.at_most(touch, limit)
    extra = augment(w, choices, pairs, bits_by_state) if augment else None
    w.close()
    metadata = dict(wires=n, gates=gates, states=states, active_states=len(unsorted),
                    encoded_states=len(encoded),
                    choices=choices, pairs=pairs, variables=w.variables, clauses=w.clauses,
                    commute_lexicographic=commute,
                    pruning_budgets=budgets,
                    cnf_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    if extra is not None:
        metadata['extra'] = extra
    if fixed_edges:
        metadata['fixed_edge_constants'] = True
    path.with_suffix('.meta.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return metadata


def replay(n, states, network):
    for state in states:
        out = state
        for a, b in network:
            if out >> a & 1 and not out >> b & 1:
                out ^= 1 << a | 1 << b
        assert out == sorted_state(n, state.bit_count()), (state, out, network)


def solve(path, conflicts):
    import pysat
    from pysat.solvers import Cadical195
    start = time.monotonic()
    metadata = json.loads(path.with_suffix('.meta.json').read_text())
    result = {'solver': 'CaDiCaL 1.9.5 via python-sat', 'pysat': pysat.__version__,
              'conflict_budget': conflicts, 'cnf_sha256': metadata['cnf_sha256']}
    with Cadical195(with_proof=True, use_timer=True) as solver:
        with path.open() as f:
            for line in f:
                if line.strip() and line[:1] not in 'cp':
                    solver.add_clause([int(x) for x in line.split()[:-1]])
        print(json.dumps({'stage': 'loaded', 'variables': solver.nof_vars(),
                          'clauses': solver.nof_clauses(), 'seconds': time.monotonic()-start}), flush=True)
        solver.conf_budget(conflicts)
        status = solver.solve_limited()
        result['status'] = 'SAT' if status is True else 'UNSAT_unchecked' if status is False else 'UNKNOWN'
        result['stats'] = solver.accum_stats()
        result['solver_seconds'] = solver.time()
        if status is True:
            assignment = solver.get_model()
            positive = {x for x in assignment if x > 0}
            result['network'] = [metadata['pairs'][next(k for k, v in enumerate(row) if v in positive)]
                                 for row in metadata['choices']]
            replay(metadata['wires'], metadata['states'], result['network'])
            path.with_suffix('.model.json').write_text(json.dumps(assignment))
        if status is False:
            # Preserve the native binary DRAT stream; it remains unchecked here.
            solver.prfile.flush()
            solver.prfile.seek(0)
            with path.with_suffix('.drat.bin').open('wb') as f:
                for block in iter(lambda: solver.prfile.read(1048576), b''):
                    f.write(block)
    result.update(seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path.with_suffix('.result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=('generate', 'solve'))
    ap.add_argument('--path', type=pathlib.Path, required=True)
    ap.add_argument('--input', type=pathlib.Path)
    ap.add_argument('--wires', type=int)
    ap.add_argument('--gates', type=int)
    ap.add_argument('--conflicts', type=int, default=5000)
    ap.add_argument('--budgets', type=pathlib.Path)
    args = ap.parse_args()
    if args.command == 'generate':
        if args.input:
            z = json.loads(args.input.read_text())
            n, X = z['residual_wires'], z['residual_states']
        else:
            n, X = args.wires, list(range(1 << args.wires))
        budgets = {entry['state']: entry for entry in json.loads(args.budgets.read_text())} if args.budgets else None
        m = generate(n, X, args.gates, args.path, budgets=budgets)
        print(json.dumps({k: v for k, v in m.items() if k not in ('states', 'choices', 'pairs', 'pruning_budgets')}), flush=True)
    else:
        solve(args.path, args.conflicts)
