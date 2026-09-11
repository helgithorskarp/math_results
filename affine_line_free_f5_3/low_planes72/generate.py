"""Complete four-case CNF cover of 72-point line-free sets.

Each formula also requires two further planes of size <=9, as guaranteed
by the exact incidence certificate. A solver UNKNOWN proves nothing.
"""
import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from model import CASES, PROFILES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, choices=range(4), required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    points = list(product(range(5), repeat=3))
    index = {p: i+1 for i, p in enumerate(points)}
    directions = [v for v in points if any(v) and next(x for x in v if x) == 1]
    lines = sorted({tuple(sorted(index[tuple((x+t*d) % 5 for x, d in zip(p, v))]
                                for t in range(5))) for p in points for v in directions})
    planes = [(normal, b, [i+1 for i, p in enumerate(points)
                          if sum(x*y for x, y in zip(p, normal)) % 5 == b])
              for normal in directions for b in range(5)]
    assert len(lines) == 775 and len(planes) == 155
    cnf, pool = CNF(), IDPool(start_from=126)

    def card(kind, literals, bound, gate=None):
        clauses = getattr(CardEnc, kind)(lits=literals, bound=bound,
                    vpool=pool, encoding=EncType.seqcounter).clauses
        cnf.extend(clauses if gate is None else [[-gate]+clause for clause in clauses])

    for line in lines:
        cnf.append([-v for v in line])
    card('equals', list(range(1, 126)), 72)
    for _, _, plane in planes:
        card('atmost', plane, 16)
    case = CASES[args.case]
    for axis, kind in enumerate(case):
        for value, size in enumerate(PROFILES[kind]):
            card('equals', [i+1 for i, p in enumerate(points) if p[axis] == value], size)
    for line in lines:
        axes = [k for k in range(3) if all(points[i-1][k] == 0 for i in line)]
        if not axes:
            continue
        bound = 3
        if len(axes) == 2:
            # Pencil sum is 72+5*k; four other planes have size at most16.
            bound = (sum(PROFILES[case[k]][0] for k in axes)+64-72)//5
        for subset in combinations(line, bound+1):
            cnf.append([-v for v in subset])

    extra_low = []
    for normal, _, plane in planes:
        if sum(x != 0 for x in normal) == 1:
            continue  # The only low coordinate planes are already fixed.
        indicator = pool.id()
        extra_low.append(indicator)
        card('atmost', plane, 9, gate=indicator)
        plane_set = set(plane)
        for line in lines:
            if set(line) <= plane_set:
                for four in combinations(line, 4):
                    cnf.append([-indicator]+[-v for v in four])
    assert len(extra_low) == 140
    card('atleast', extra_low, 2)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.out))
    metadata = {'case': args.case, 'profile_names': ''.join('AB'[i] for i in case),
        'coordinate_profiles': [PROFILES[i] for i in case],
        'variables': cnf.nv, 'clauses': len(cnf.clauses),
        'sha256': hashlib.sha256(args.out.read_bytes()).hexdigest(),
        'status': 'GENERATED', '72_point_decision': 'OPEN'}
    args.out.with_suffix('.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
