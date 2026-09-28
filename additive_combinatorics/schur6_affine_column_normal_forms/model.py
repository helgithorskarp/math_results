"""Two independent short columns in a reflected cyclic Schur construction.

The modulus is 5*a. Q1(q) is residual (colour 0) or a common colour;
Q2(q) is residual (colour 1) or a common colour. Values at the negative
positions agree. Multiples of 5 have an independent symmetric axis E.
There is no Qj(0) restriction and no independent special-axis permutation.
"""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path


def variable_maps(a, colours=6):
    if a < 1 or a % 2 != 1 or colours < 3:
        raise ValueError('require odd a>=1 and at least three colours')
    h = a // 2
    common = tuple(range(2, colours))
    labels = (0, *common)
    E, Q = {}, {}
    top = 0
    for u in range(1, h + 1):
        for c in range(colours):
            top += 1
            E[u, c] = top
    for b in (1, 2):
        for q in range(a):
            for c in labels:
                top += 1
                Q[b, q, c] = top
    return dict(a=a, h=h, colours=colours, common=common, labels=labels,
                E=E, Q=Q, variables=top)


def criterion_clauses(m):
    a, E, Q = m['a'], m['E'], m['Q']
    clauses = set()
    def add(values):
        clauses.add(tuple(sorted({-v for v in values})))
    # Every symmetric axis class is sum-free, including repeated summands.
    for x in range(1, a):
        for y in range(x, a):
            z = (x+y) % a
            if z:
                for c in range(m['colours']):
                    add(E[min(v, a-v), c] for v in (x, y, z))
    # Ai+Ai misses Bi, and Ai+Bi+Bi misses -1. Individual Ai/Bi need not
    # be sum-free. Both equations include coincident long coordinates.
    for x in range(a):
        for y in range(x, a):
            for c in m['common']:
                add((Q[1, x, c], Q[1, y, c], Q[2, (x+y) % a, c]))
                add((Q[2, x, c], Q[2, y, c], Q[1, (-1-x-y) % a, c]))
    # Each column's difference sets constrain its permitted axis colours.
    for b in (1, 2):
        for x, y in itertools.combinations(range(a), 2):
            d = min(y-x, a-y+x)
            add((Q[b, x, 0], Q[b, y, 0], E[d, b-1]))
            for c in m['common']:
                add((Q[b, x, c], Q[b, y, c], E[d, c]))
    return clauses


def encoding(a, colours=6, symmetry=True, fixed=None, normalize_axis=False):
    m = variable_maps(a, colours)
    E, Q = m['E'], m['Q']
    cnf = []
    for row in [[E[u, c] for c in range(colours)] for u in range(1, m['h']+1)] + [
            [Q[b, q, c] for c in m['labels']] for b in (1, 2) for q in range(a)]:
        cnf.append(row)
        cnf.extend([[-v, -w] for v, w in itertools.combinations(row, 2)])
    schur = criterion_clauses(m)
    cnf.extend(map(list, sorted(schur, key=lambda row: (len(row), row))))
    distinguished = set()
    if fixed is not None:
        c = fixed['colour']
        if c not in m['common']:
            raise ValueError('only common fixed class supported')
        distinguished.add(c)
        for b, key in ((1, 'first_column'), (2, 'second_column')):
            support = set(fixed[key])
            if not support <= set(range(a)):
                raise ValueError('column support outside Z_a')
            for q in range(a):
                cnf.append([Q[b, q, c] * (1 if q in support else -1)])
        axis = set(fixed['axis_class'])
        if 0 in axis or not axis <= set(range(1, a)) or {a-u for u in axis} != axis:
            raise ValueError('axis support must be symmetric and omit zero')
        for u in range(1, m['h']+1):
            cnf.append([E[u, c] * (1 if u in axis else -1)])
    if symmetry:
        # A simultaneous global permutation of the undistinguished common
        # colours is valid. Neither residual colour is permuted.
        palette = [c for c in m['common'] if c not in distinguished]
        seen = {c: [] for c in palette}
        rows = [{c: Q[b, q, c] for c in palette} for b in (1, 2) for q in range(a)]
        rows += [{c: E[u, c] for c in palette} for u in range(1, m['h']+1)]
        for row in rows:
            for prev, c in zip(palette, palette[1:]):
                cnf.append([-row[c], *seen[prev]])
            for c in palette:
                seen[c].append(row[c])
    if normalize_axis:
        # Unit dilation and the corresponding exchange of BOTH special
        # colours justify this only for the free prime-axis six-colour model.
        # S(4)=44 forces a special colour somewhere on this axis.
        if fixed is not None or colours != 6 or a <= 45 or any(a % d == 0 for d in range(2, math.isqrt(a)+1)):
            raise ValueError('axis normalization needs free model and prime a>45, six colours')
        cnf.append([E[1, 0]])
    m.update(schur_clauses=len(schur), symmetry=symmetry,
             distinguished=sorted(distinguished), normalize_axis=normalize_axis)
    return m, cnf


def decode(m, truth):
    a, E, Q = m['a'], m['E'], m['Q']
    row = [-1] * (5*a)
    for u in range(1, m['h']+1):
        colours = [c for c in range(m['colours']) if E[u, c] in truth]
        assert len(colours) == 1
        row[5*u] = row[5*(a-u)] = colours[0]
    for b in (1, 2):
        for q in range(a):
            states = [c for c in m['labels'] if Q[b, q, c] in truth]
            assert len(states) == 1
            colour = states[0] if states[0] else b-1
            row[5*q+b] = row[5*a-5*q-b] = colour
    assert all(0 <= c < m['colours'] for c in row[1:])
    return row[1:]


def word_pins(m, word):
    assert len(word) == 5*m['a']-1
    row = [-1, *word]
    pins = [[m['E'][u, row[5*u]]] for u in range(1, m['h']+1)]
    for b in (1, 2):
        for q in range(m['a']):
            c = row[5*q+b]
            assert c == b-1 or c in m['common']
            pins.append([m['Q'][b, q, 0 if c == b-1 else c]])
    return pins


def dimacs(m, clauses):
    return ('p cnf %d %d\n' % (m['variables'], len(clauses)) +
            ''.join(' '.join(map(str, cl))+' 0\n' for cl in clauses)).encode()


def run(a, colours, budget, output, fixed=None, pin_word=None, symmetry=True,
        normalize_axis=False):
    from pysat.solvers import Solver
    from verify import verify_word
    start = time.monotonic()
    m, cnf = encoding(a, colours, symmetry, fixed, normalize_axis)
    if pin_word is not None:
        cnf.extend(word_pins(m, pin_word))
    cnf_bytes = dimacs(m, cnf)
    report = dict(axis_factor=a, short_factor=5, colours=colours, modulus=5*a,
                  variables=m['variables'], clauses=len(cnf),
                  schur_clauses=m['schur_clauses'], budget=budget,
                  solver='cadical195', symmetry='common palette' if symmetry else 'none',
                  distinguished_colours=m['distinguished'],
                  axis_normalized=normalize_axis,
                  cnf_sha256=hashlib.sha256(cnf_bytes).hexdigest(),
                  cnf_bytes=len(cnf_bytes), fixed_class=fixed,
                  whole_word_pinned=pin_word is not None)
    with Solver(name='cadical195', bootstrap_with=cnf) as solver:
        solver.conf_budget(budget)
        answer = solver.solve_limited()
        report.update(status={True: 'SAT', False: 'UNSAT_UNCERTIFIED', None: 'UNKNOWN'}[answer],
                      stats=solver.accum_stats())
        if answer:
            report['word'] = decode(m, set(solver.get_model()))
            report['check'] = verify_word(report)
            if pin_word is not None:
                assert report['word'] == pin_word
    report['seconds'] = time.monotonic()-start
    Path(output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('word', 'fixed_class')}), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--axis-factor', type=int, default=109)
    parser.add_argument('--colours', type=int, default=6)
    parser.add_argument('--budget', type=int, default=100000)
    parser.add_argument('--fixed-scaffold', action='store_true')
    parser.add_argument('--pin-word')
    parser.add_argument('--no-symmetry', action='store_true')
    parser.add_argument('--normalize-axis', action='store_true')
    parser.add_argument('--output')
    parser.add_argument('--export-cnf')
    args = parser.parse_args()
    fixed = None
    if args.fixed_scaffold:
        seed = json.loads((Path(__file__).resolve().parent/'scaffold.json').read_text())
        assert args.axis_factor == seed['axis_factor'] and args.colours == 6
        fixed = dict(colour=2, **{k: seed[k] for k in ('first_column', 'second_column', 'axis_class')})
    pin = json.loads(Path(args.pin_word).read_text())['word'] if args.pin_word else None
    if args.export_cnf:
        m, cnf = encoding(args.axis_factor, args.colours, not args.no_symmetry, fixed, args.normalize_axis)
        if pin is not None:
            cnf.extend(word_pins(m, pin))
        payload = dimacs(m, cnf)
        Path(args.export_cnf).write_bytes(payload)
        print(json.dumps(dict(variables=m['variables'], clauses=len(cnf), bytes=len(payload),
                              sha256=hashlib.sha256(payload).hexdigest())))
    elif args.output:
        run(args.axis_factor, args.colours, args.budget, args.output, fixed, pin,
            not args.no_symmetry, args.normalize_axis)
    else:
        parser.error('provide --output for a bounded solve or --export-cnf for a solver-free export')
