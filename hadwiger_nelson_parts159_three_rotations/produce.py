"""Optional discovery replay. Verification never imports a SAT solver."""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import json
from pysat.solvers import Solver
import geometry as G
import verify as V

def x(v, c):
    return 4*v+c+1

def solve(n, edges, equal=(), fixed=()):
    clauses = [[x(v, c) for c in range(4)] for v in range(n)]
    clauses += [[-x(a, c), -x(b, c)] for a, b in edges for c in range(4)]
    clauses += [[x(v, c)] for v, c in fixed]
    for a, b in equal:
        for c in range(4):
            clauses.extend([[-x(a, c), x(b, c)], [-x(b, c), x(a, c)]])
    with Solver(name='cadical195', bootstrap_with=clauses) as s:
        s.conf_budget(500000)
        result = s.solve_limited()
        G.require(result is True, 'discovery replay did not return SAT; no theorem inferred')
        positive = {v for v in s.get_model() if v > 0}
    colors = [next(c for c in range(4) if x(v, c) in positive) for v in range(n)]
    G.require(all(colors[a] != colors[b] for a, b in edges)
              and all(colors[a] == colors[b] for a, b in equal)
              and all(colors[v] == c for v, c in fixed), 'solver witness')
    return colors

def produce():
    data = G.build(); data['group_map'] = dict(data['groups'])
    lib, words = G.library(); internal = data['internal']; fixed = lib[0]
    texts, text_index = [], {}
    def add_word(w):
        G.require(V.word_ok(w, internal), 'generated component coloring')
        text = ''.join(map(str, w))
        if text not in text_index:
            text_index[text] = len(texts); texts.append(text)
        return text_index[text]
    def label(k, v):
        return 0 if v == 0 else 158*k+v
    base = [(label(k, a), label(k, b)) for k in range(3) for a, b in internal]
    extension_rows, cycle_rows, masks = [], [], []
    for gi, (_, es) in enumerate(data['groups']):
        masks.append([sum(1 << j for j, b in enumerate(words) if V.bridge_ok(a, b, es))
                      for a in lib])
        if any(V.bridge_ok(fixed, w, es) for w in words):
            continue
        # The central copy is fixed to the exact field coloring.
        all_edges = [(a, b) for a, b in internal]
        clauses = [[x(v, c) for c in range(4)] for v in range(159)]
        clauses += [[-x(a, c), -x(b, c)] for a, b in all_edges for c in range(4)]
        clauses += [[x(0, 0)]]+[[-x(b, fixed[a])] for a, b in es]
        with Solver(name='cadical195', bootstrap_with=clauses) as s:
            s.conf_budget(500000)
            G.require(s.solve_limited() is True, 'extension replay failed')
            pos = {v for v in s.get_model() if v > 0}
        w = tuple(next(c for c in range(4) if x(v, c) in pos) for v in range(159))
        G.require(V.bridge_ok(fixed, w, es), 'extension witness')
        extension_rows.append([gi, add_word(w)])
    by_field, cache, residual = defaultdict(list), {}, []
    for i, (g, f, z) in enumerate(data['roots']):
        by_field[f].append(i)
    for f, ids in by_field.items():
        for i, j in combinations(ids, 2):
            gi, _, u = data['roots'][i]; gj, _, v = data['roots'][j]
            es, same, _ = G.relative_contacts(data, u, v, data['fields'][f])
            if not es:
                continue
            key = tuple(es), tuple(same)
            if key not in cache:
                cache[key] = [sum(1 << k for k, b in enumerate(words)
                                  if V.bridge_ok(a, b, es, same)) for a in words]
            comp = cache[key]
            covered = any(comp[b] & masks[gj][a] for a in range(4) for b in range(24)
                          if masks[gi][a] >> b & 1)
            if not covered:
                residual.append((i, j, es, same))
    for i, j, es, same in sorted(residual):
        gi, _, _ = data['roots'][i]; gj, _, _ = data['roots'][j]
        ee = base+[(a, label(1, b)) for a, b in data['groups'][gi][1]]
        ee += [(a, label(2, b)) for a, b in data['groups'][gj][1]]
        ee += [(label(1, a), label(2, b)) for a, b in es]
        equal = [(label(1, a), label(2, b)) for a, b in same]
        colors = solve(475, ee, equal, [(0, 0)])
        indices = [add_word(tuple([colors[0]]+colors[158*k+1:158*(k+1)+1])) for k in range(3)]
        cycle_rows.append([i, j, *indices])
    return {'words': texts, 'extensions': extension_rows, 'cycles': cycle_rows}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    G.require(not args.output.exists(), 'choose a new output file')
    cert = produce()
    args.output.write_text(json.dumps(cert, separators=(',', ':'))+'\n')
    print(json.dumps({'words': len(cert['words']), 'extensions': len(cert['extensions']),
                      'cycles': len(cert['cycles'])}, sort_keys=True))
