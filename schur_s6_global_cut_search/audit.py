"""Audit generated global-cut formulas and small cardinality controls."""
import argparse
import hashlib
import itertools
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


ROOT = Path(__file__).resolve().parent.parent
BASE_SHA = {
    'plain': 'fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2',
    'rgs': '332e4b211a672836c68320f9403b0454462a96df2071aefcc2a72f809820eb7c',
}


def x(v, c):
    return 6 * (v - 1) + c


def card_controls():
    for n in range(2, 7):
        for bound in range(1, n + 1):
            cardinality = CardEnc.atleast(lits=[-i for i in range(1, n + 1)],
                                           bound=bound, top_id=n,
                                           encoding=EncType.totalizer)
            with Solver(name='cadical195', bootstrap_with=cardinality.clauses) as solver:
                for bits in itertools.product((False, True), repeat=n):
                    assumptions = [i if bit else -i for i, bit in enumerate(bits, 1)]
                    assert solver.solve(assumptions=assumptions) == (bits.count(False) >= bound)


def audit(base_path, target_path, mode, branch, distance, splitting, first_use):
    assert hashlib.sha256(base_path.read_bytes()).hexdigest() == BASE_SHA[mode]
    base = CNF(from_file=str(base_path))
    target = CNF(from_file=str(target_path))
    at = 0
    assert target.clauses[:len(base.clauses)] == base.clauses
    at += len(base.clauses)
    top = base.nv
    if mode == 'rgs':
        assert not branch and not first_use
    if branch:
        assert mode == 'plain' and branch in (1, 2, 3)
        assert target.clauses[at:at+2] == [[x(2, 2)], [x(537, branch)]]
        at += 2
    if distance:
        fs_file = ROOT / 'schur_s6_fredricksen_sweet_distance/baseline.txt'
        assert hashlib.sha256(fs_file.read_bytes()).hexdigest() == '2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d'
        fs = fs_file.read_text().strip()
        assert len(fs) == 536
        mismatch = [-x(v, int(c)) for v, c in enumerate(fs, 1)]
        card = CardEnc.atleast(lits=mismatch, bound=54, top_id=top,
                               encoding=EncType.totalizer)
        assert target.clauses[at:at+len(card.clauses)] == card.clauses
        at += len(card.clauses)
        top = card.nv
    if splitting:
        seed_file = ROOT / 'schur_s6_external_class_trade/seed537.txt'
        assert hashlib.sha256(seed_file.read_bytes()).hexdigest() == '58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3'
        seed = seed_file.read_text().strip()
        assert len(seed) == 537
        selectors = []
        for old in '123456':
            members = [v for v in range(1, 538) if seed[v - 1] == old]
            top += 1
            selectors.append(top)
            for new in range(1, 7):
                expected = [-top] + [-x(v, new) for v in members]
                assert target.clauses[at] == expected
                at += 1
        for triple in itertools.combinations(selectors, 3):
            assert target.clauses[at] == list(triple)
            at += 1
    if first_use:
        assert branch in (1, 2, 3)
        first = 4 if branch == 3 else 3
        seen = {}
        for colour in range(first, 6):
            for v in range(1, 538):
                top += 1
                seen[colour, v] = top
                before = seen.get((colour, v-1))
                expected = ([[-x(v, colour), top], [-top, x(v, colour)]]
                            if before is None else
                            [[-before, top], [-x(v, colour), top],
                             [-top, before, x(v, colour)]])
                assert target.clauses[at:at+len(expected)] == expected
                at += len(expected)
        for colour in range(first+1, 7):
            for v in range(1, 538):
                before = seen.get((colour-1, v-1))
                assert target.clauses[at] == ([-x(v, colour), before] if before else [-x(v, colour)])
                at += 1
    assert at == len(target.clauses)
    assert top == target.nv
    print('PASS', mode, branch, 'vars', top, 'clauses', at,
          'sha256', hashlib.sha256(target_path.read_bytes()).hexdigest())


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--base', type=Path, required=True)
    p.add_argument('--target', type=Path, required=True)
    p.add_argument('--mode', choices=('plain', 'rgs'), required=True)
    p.add_argument('--branch', type=int, choices=(0, 1, 2, 3), default=0)
    p.add_argument('--distance', action='store_true')
    p.add_argument('--splitting', action='store_true')
    p.add_argument('--first-use', action='store_true')
    args = p.parse_args()
    card_controls()
    audit(args.base, args.target, args.mode, args.branch,
          args.distance, args.splitting, args.first_use)
