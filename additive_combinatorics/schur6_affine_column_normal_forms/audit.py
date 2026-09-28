"""Literal modular-equation audit of the independent-column criterion.

The symbolic table is filled from reflected point pairs. Sums are enumerated
by output and first summand, independently of the reduced criterion loops.
"""
import argparse
import itertools
import json
import time
from pathlib import Path

from model import variable_maps, criterion_clauses, encoding, decode
from verify import verify_word


def literal_clauses(a, colours=6):
    n = 5*a
    table = {}
    next_var = 0
    for u in range(1, (a+1)//2):
        for c in range(colours):
            next_var += 1
            table[5*u, c] = table[n-5*u, c] = next_var
    for b in (1, 2):
        for q in range(a):
            for state in (0, *range(2, colours)):
                next_var += 1
                colour = state if state else b-1
                table[5*q+b, colour] = table[n-5*q-b, colour] = next_var
    result = set()
    pairs = 0
    for z in range(1, n):
        for x in range(1, n):
            y = (z-x) % n
            if not y or y < x:
                continue
            pairs += 1
            for c in range(colours):
                if all((v, c) in table for v in (x, y, z)):
                    result.add(tuple(sorted({-table[v, c] for v in (x, y, z)})))
    return result, pairs, table


def clause_audit(a, colours=6):
    m = variable_maps(a, colours)
    reduced = criterion_clauses(m)
    literal, pairs, table = literal_clauses(a, colours)
    assert reduced == literal, (a, colours, len(reduced-literal), len(literal-reduced),
                                list(reduced-literal)[:3], list(literal-reduced)[:3])
    assert set(table.values()) == set(range(1, m['variables']+1))
    return dict(axis_factor=a, colours=colours, variables=m['variables'],
                modular_pairs=pairs, schur_clauses=len(literal), status='EXACT_CLAUSE_EQUALITY')


def truth_from_states(m, e, q1, q2):
    return {m['E'][u, e[u-1]] for u in range(1, m['h']+1)} | {
        m['Q'][b, q, values[q]] for b, values in ((1, q1), (2, q2)) for q in range(m['a'])}


def small_audit(a=5, colours=4):
    m, normalized = encoding(a, colours, symmetry=True)
    forbidden = criterion_clauses(m)
    masks = [sum(1 << (-v-1) for v in cl) for cl in forbidden]
    _, plain = encoding(a, colours, symmetry=False)
    checked = valid = 0
    counts = {}
    q_states = list(itertools.product(m['labels'], repeat=a))
    # Bit masks are only an efficient evaluator of explicit, already audited
    # clauses. Independent full modular checking is applied to every survivor.
    q_masks = {}
    for b in (1, 2):
        q_masks[b] = [sum(1 << (m['Q'][b, q, row[q]]-1) for q in range(a)) for row in q_states]
    def accepts(cnf, truth):
        return all(any(v in truth if v > 0 else -v not in truth for v in cl) for cl in cnf)
    for e in itertools.product(range(colours), repeat=m['h']):
        axis = sum(1 << (m['E'][u, e[u-1]]-1) for u in range(1, m['h']+1))
        for i, q1 in enumerate(q_states):
            left = axis | q_masks[1][i]
            for j, q2 in enumerate(q_states):
                checked += 1
                occupied = left | q_masks[2][j]
                if any(occupied & forbidden_mask == forbidden_mask for forbidden_mask in masks):
                    continue
                valid += 1
                truth = truth_from_states(m, e, q1, q2)
                assert accepts(plain, truth)
                data = dict(axis_factor=a, colours=colours, word=decode(m, truth))
                check = verify_word(data)
                counts[check['columns_equal']] = counts.get(check['columns_equal'], 0)+1
                palette = {}
                for c in (*q1, *q2, *e):
                    if c >= 2 and c not in palette:
                        palette[c] = len(palette)+2
                ee = [palette.get(c, c) for c in e]
                qq1 = [palette.get(c, c) for c in q1]
                qq2 = [palette.get(c, c) for c in q2]
                image = truth_from_states(m, ee, qq1, qq2)
                assert accepts(normalized, image)
                verify_word(dict(axis_factor=a, colours=colours, word=decode(m, image)))
    return dict(axis_factor=a, colours=colours, complete_assignments=checked,
                valid=valid, diagonal=counts.get(True, 0), nondiagonal=counts.get(False, 0),
                every_valid_word_checked=True, common_palette_complete=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--skip-small', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    audits = []
    for a, k in ((1, 6), (3, 6), (5, 4), (5, 6), (13, 6), (61, 6), (109, 6)):
        record = clause_audit(a, k)
        audits.append(record)
        print(json.dumps(record), flush=True)
    data = dict(clause_audits=audits)
    if not args.skip_small:
        data['assignment_audits'] = [small_audit(1, 6), small_audit(5, 4)]
        print(json.dumps(data['assignment_audits']), flush=True)
    from affine import clause_audit as affine_clause_audit
    data['affine_clause_audits'] = [affine_clause_audit(a, lam, delta) for a, lam, delta in
        [(13,5,7),(13,5,12),(13,8,3),(13,8,8),(109,33,13),(109,33,100),(109,76,52),(109,76,30),(43,22,0)]]
    print(json.dumps(dict(status='PASS', affine_clause_audits=data['affine_clause_audits'])), flush=True)
    Path(args.output).write_text(json.dumps(data, indent=2)+'\n')


if __name__ == '__main__':
    main()
