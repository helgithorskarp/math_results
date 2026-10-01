"""One capped exact AP-support hypergraph and SAT matching instance.

Discovery only: even an UNSAT answer is not an independently proved
negative result. Positive claims require the separate actual-term checker.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import time


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def negate(value):
    return not value if type(value) is bool else -value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    require(0 <= args.index < 625 and not args.output_dir.exists(), 'Fresh canonical-case output required')
    began = time.monotonic()
    args.output_dir.mkdir(parents=True)
    if args.index < 3:
        B, A = (0, 1, 11)[args.index], 0
    elif args.index < 314:
        B, A = args.index - 3, 1
    else:
        B, A = args.index - 314, 11
    squares = {x * x % 311 for x in range(1, 311)}
    values = []
    for x in range(311):
        y = (pow(x, 4, 311) + A * x * x + B) % 311
        values.append(None if y == 0 else int(y in squares))
    edges, choices = {}, 0
    for a in range(311):
        for d in range(1, 311):
            choices += 1
            residues = [(a + j * d) % 311 for j in range(7)]
            if any(x == 0 or values[x] is None for x in residues):
                continue
            orbits = tuple(sorted({min(x, 311 - x) for x in residues}))
            if len(orbits) != 7:
                continue
            if len({((a + j * d) % 2) ^ values[x] for j, x in enumerate(residues)}) != 1:
                continue
            edges.setdefault(orbits, [[a + 1, d], [(-(a + 6 * d) % 622) % 311 + 1, d]])
    require(choices == 96410, 'Exact canonical AP scan domain')
    ordered = [{'orbits': list(support), 'pair': pair} for support, pair in sorted(edges.items())]
    hypergraph = {'modulus': 311, 'index': args.index, 'coefficients': [B, 0, A, 0, 1],
                  'vertices': list(range(1, 156)), 'edges': ordered,
                  'coverage': 'All a=0..310,d=1..310; root-free supports disjoint from their negatives; duplicate orbit supports merged.'}
    hg_path = args.output_dir / 'hypergraph.json'
    hg_path.write_text(json.dumps(hypergraph, separators=(',', ':')) + '\n')
    n = len(ordered)
    # At most7*n incidence checks,21*n point-at-most-one rows,48*n
    # truncated exact prefix-counter rows. This is a conservative preflight.
    preflight = choices + 622 + 76 * n + 1
    base = {'agent': 'six-vdw-1', 'role': 'researcher',
            'checked_at': datetime.now(timezone.utc).isoformat(), 'index': args.index,
            'AP_choices_checked': choices, 'distinct_orbit_edges': n, 'target_matching_size': 12,
            'hypergraph': str(hg_path.resolve()), 'hypergraph_sha256': hashlib.sha256(hg_path.read_bytes()).hexdigest(),
            'conservative_preflight_cases': preflight,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'mathematical_exclusion': False, 'new_W_bound': None, 'threads': 1}
    if preflight > 200000:
        base.update(status='MATCHING_MODEL_PREFLIGHT_OVER_CAP_PAUSED_NO_EXCLUSION',
                    seconds=time.monotonic() - began, maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (args.output_dir / 'metadata.json').write_text(json.dumps(base, indent=2) + '\n')
        print(json.dumps(base), flush=True)
        return
    clauses, top = [], n

    def variable():
        nonlocal top
        top += 1
        return top

    def clause(values):
        if any(v is True for v in values):
            return
        row = [v for v in values if v is not False]
        require(all(type(v) is int and v != 0 for v in row), 'Literal types')
        clauses.append(row)

    incidence = [[] for _ in range(156)]
    for edge_id, edge in enumerate(ordered, 1):
        for orbit in edge['orbits']:
            incidence[orbit].append(edge_id)
    for orbit in range(1, 156):
        xs = incidence[orbit]
        if len(xs) < 2:
            continue
        if len(xs) == 2:
            clause([-xs[0], -xs[1]])
            continue
        previous = variable()
        clause([-xs[0], previous])
        for x in xs[1:-1]:
            current = variable()
            clause([-x, current])
            clause([-previous, current])
            clause([-x, -previous])
            previous = current
        clause([-xs[-1], -previous])
    point_rows = len(clauses)
    previous = [True] + [False] * 12
    for i, x in enumerate(range(1, n + 1), 1):
        current = [True] + [False] * 12
        for j in range(1, min(i, 12) + 1):
            z = variable()
            p, q = previous[j], previous[j - 1]
            # z <=> p OR(x AND q), where p/q include exact boundary constants.
            clause([negate(p), z])
            clause([-x, negate(q), z])
            clause([-z, p, x])
            clause([-z, p, q])
            current[j] = z
        previous = current
    clause([previous[12]])
    combined = choices + 622 + 7 * n + len(clauses)
    require(combined <= preflight <= 200000, 'Actual model case cap')
    cnf_path = args.output_dir / 'matching.cnf'
    cnf_path.write_text('p cnf ' + str(top) + ' ' + str(len(clauses)) + '\n' +
                        ''.join(' '.join(map(str, row)) + ' 0\n' for row in clauses))
    base.update(status='MATCHING_CNF_READY_PENDING_SOLVER_AND_DEFINITION_CHECK',
                CNF=str(cnf_path.resolve()), CNF_sha256=hashlib.sha256(cnf_path.read_bytes()).hexdigest(),
                variables=top, clauses=len(clauses), point_at_most_one_rows=point_rows,
                exact_prefix_threshold_rows=len(clauses) - point_rows,
                conservative_combined_cases=combined, seconds=time.monotonic() - began,
                maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(base['seconds'] < 30, 'Unchanged30s child guard')
    (args.output_dir / 'metadata.json').write_text(json.dumps(base, indent=2) + '\n')
    print(json.dumps(base, indent=2), flush=True)


if __name__ == '__main__':
    main()
