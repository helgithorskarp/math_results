"""Independent exact clause audit and signed-set positive-RUP verifier.

Reviewer: six-reviewer-5. No author Python module is imported. Immutable
signed-literal sets represent clauses, and two sets represent true/false
literals. The author checker scans tuples using a dictionary of Booleans.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


class Invalid(ValueError):
    pass


def need(condition, explanation):
    if not condition:
        raise Invalid(explanation)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def clauses(path):
    with Path(path).open() as stream:
        fields = next(stream, '').split()
        need(len(fields) == 4 and fields[:2] == ['p', 'cnf'], 'CNF header')
        nv, nc = map(int, fields[2:])
        need(nv > 0 and nc > 0, 'CNF dimensions')
        rows = []
        for line in stream:
            values = list(map(int, line.split()))
            need(values and values[-1] == 0 and 0 not in values[:-1], 'CNF termination')
            row = values[:-1]
            need(all(0 < abs(x) <= nv for x in row), 'CNF variable domain')
            need(len(set(row)) == len(row), 'Duplicate CNF literal')
            need(not any(-x in row for x in row), 'Tautological CNF clause')
            rows.append(tuple(row))
        need(len(rows) == nc, 'CNF row coverage')
    return nv, rows


def reconstruct(source, cnf, runs):
    """Regroup the mathematical implications; compare every clause as a multiset."""
    nv, actual = clauses(cnf)
    word_bytes = (source / 'base3704.bits').read_bytes()
    n = 3704
    need(word_bytes.endswith(b'\n') and len(word_bytes) == n + 1, 'Word framing')
    # Squaring every nonzero field element is independent of Euler's criterion.
    residues = {x * x % 617 for x in range(1, 617)}
    base = [int((t - 1) % 617 not in residues and (t - 1) % 617 != 0)
            for t in range(1, n + 1)]
    base[3702] = 1
    need(word_bytes == ''.join(map(str, base)).encode() + b'\n', 'Literal QR617 word')
    pool = json.loads((source / 'AP-pool.json').read_text())
    need(set(pool) == {'length', 'term_count', 'base_bits_sha256', 'APs'}, 'Pool schema')
    need(type(pool['length']) is int and pool['length'] == n, 'Pool length')
    need(type(pool['term_count']) is int and pool['term_count'] == 7, 'AP length')
    need(pool['base_bits_sha256'] == hashlib.sha256(word_bytes[:-1]).hexdigest(), 'Pool base')
    aps = pool['APs']
    need(type(aps) is list and len(aps) > 0, 'AP pool')
    need(all(type(ap) is list and len(ap) == 2 and
             all(type(x) is int for x in ap) and ap[0] >= 1 and ap[1] >= 1 and
             ap[0] + 6 * ap[1] <= n for ap in aps), 'Actual nonconstant AP domain')
    need(aps == sorted(aps) and len(set(map(tuple, aps))) == len(aps), 'AP uniqueness')
    expected = []

    def implication(antecedents, consequent=None):
        expected.append(tuple([-x for x in antecedents] +
                              ([] if consequent is None else [consequent])))

    # Define starts by three separate implications, with the virtual preceding
    # edit bit false at t=1. No candidate endpoint is silently discarded.
    for t in range(1, n + 1):
        start = n + t
        implication([start], t)
        if t > 1:
            implication([start], -(t - 1))
            implication([t, -(t - 1)], start)
        else:
            implication([t], start)
    if runs == 3:
        expected.append((-1,))
        threshold = lambda i, j: 2 * n + 3 * (i - 1) + j
        for j in range(1, 4):
            if j > 1:
                expected.append((-threshold(1, j),))
            for i in range(1, n):
                if j == 1:
                    implication([n + i], threshold(i, j))
                elif i > 1:
                    implication([n + i, threshold(i - 1, j - 1)], threshold(i, j))
                if i > 1:
                    implication([threshold(i - 1, j)], threshold(i, j))
        for t in range(2, n + 1):
            implication([n + t, threshold(t - 1, 3)])
        need(nv == 5 * n - 3, 'Three-run identifier boundary')
    elif runs == 2:
        def first(i):
            return 2 * n + i if i <= 2 else 2 * n + 2 * i - 1

        def second(i):
            return 2 * n + 3 if i == 2 else 2 * n + 2 * i - 2

        for t in range(1, n - 1):
            implication([n + t], first(t))
        for t in range(1, n - 2):
            implication([first(t)], first(t + 1))
        for t in range(2, n):
            implication([n + t, first(t - 1)], second(t))
        for t in range(2, n - 1):
            implication([second(t)], second(t + 1))
        for t in range(3, n + 1):
            implication([n + t, second(t - 1)])
        need(nv == 4 * n - 4, 'Two-run identifier boundary')
    else:
        raise Invalid('Unsupported run bound')
    for a, d in aps:
        positions = [a + k * d for k in range(7)]
        # Enumerate both forbidden actual f colors, translating f=b XOR e.
        for color in [0, 1]:
            expected.append(tuple(p if base[p - 1] == color else -p for p in positions))
    canon = lambda row: tuple(sorted(row))
    need(Counter(map(canon, actual)) == Counter(map(canon, expected)),
         'Complete clause multiset mismatch')
    need({abs(x) for row in expected for x in row} == set(range(1, nv + 1)),
         'Exact fresh identifier coverage')
    return {'status': 'ALL_LITERAL_CLAUSES_MATCH_INDEPENDENT_DEFINITIONS',
            'runs': runs, 'APs': len(aps), 'variables': nv, 'clauses': len(actual),
            'literals': sum(map(len, actual)), 'CNF_sha256': sha(cnf),
            'word_sha256': sha(source / 'base3704.bits'),
            'pool_sha256': sha(source / 'AP-pool.json')}


def literal_set(row, nv):
    need(len(set(row)) == len(row), 'Duplicate proof literal')
    for x in row:
        need(0 < abs(x) <= nv, 'Proof variable domain')
    need(not any(-x in row for x in row), 'Tautological proof clause')
    return frozenset(row)


def verify(cnf, proof):
    nv, initial = clauses(cnf)
    db = {i: literal_set(row, nv) for i, row in enumerate(initial, 1)}
    count = len(initial)
    last = count
    additions = deletions = hint_reads = lines = 0
    finished = False
    with Path(proof).open() as stream:
        for line in stream:
            need(not finished, 'Content after empty clause')
            tokens = line.split()
            need(len(tokens) >= 3, 'Proof grammar')
            ident = int(tokens[0])
            lines += 1
            if tokens[1] == 'd':
                ids = list(map(int, tokens[2:]))
                need(ids and ids[-1] == 0 and all(x > 0 for x in ids[:-1]), 'Deletion grammar')
                need(0 < ident <= last and len(set(ids[:-1])) == len(ids) - 1, 'Deletion identifiers')
                for i in ids[:-1]:
                    need(i in db, 'Unavailable deletion')
                    del db[i]
                deletions += len(ids) - 1
                continue
            need(ident > last, 'Fresh proof identifier')
            nums = list(map(int, tokens[1:]))
            need(nums.count(0) == 2 and nums[-1] == 0, 'Proof terminators')
            split = nums.index(0)
            proposed = nums[:split]
            hints = nums[split + 1:-1]
            need(hints and all(h > 0 for h in hints), 'Positive RUP hints required')
            new_clause = literal_set(proposed, nv)
            # All literals of the proposed clause are initially false.
            false = set(new_clause)
            true = {-x for x in new_clause}
            conflict = False
            for offset, h in enumerate(hints):
                need(h in db, 'Unavailable proof hint')
                row = db[h]
                hint_reads += 1
                need(row.isdisjoint(true), 'Satisfied hint')
                pending = row.difference(false)
                need(len(pending) <= 1, 'Nonunit hint')
                if not pending:
                    need(offset == len(hints) - 1, 'Hints after conflict')
                    conflict = True
                else:
                    unit = next(iter(pending))
                    true.add(unit)
                    false.add(-unit)
            need(conflict, 'No RUP conflict')
            db[ident] = new_clause
            last = ident
            additions += 1
            finished = not proposed
    need(finished, 'No terminal empty clause')
    return {'status': 'SIGNED_SET_RUP_EMPTY_CLAUSE_VERIFIED',
            'variables': nv, 'input_clauses': count, 'proof_lines': lines,
            'RUP_additions': additions, 'deletions': deletions,
            'hint_reads': hint_reads, 'last_clause_id': last,
            'CNF_sha256': sha(cnf), 'LRAT_sha256': sha(proof)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path)
    p.add_argument('--CNF', type=Path, required=True)
    p.add_argument('--LRAT', type=Path)
    p.add_argument('--runs', type=int, choices=[2, 3])
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    began = time.monotonic()
    result = {}
    if args.source is not None:
        need(args.runs is not None, 'Run bound required')
        result['encoding'] = reconstruct(args.source, args.CNF, args.runs)
    if args.LRAT is not None:
        result['proof'] = verify(args.CNF, args.LRAT)
    need(result, 'No verification requested')
    result.update(agent='six-reviewer-5', role='independent reviewer',
                  python=sys.version.split()[0], optimization=sys.flags.optimize,
                  seconds=time.monotonic() - began,
                  maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  checker_sha256=sha(__file__))
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
