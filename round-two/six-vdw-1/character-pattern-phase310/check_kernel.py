"""Independent Gauss-symbol physical-AP binding plus strict positive RUP replay."""
import argparse
import hashlib
import json
from pathlib import Path
from strict_rup import verify


def need(ok, message):
    if not ok:
        raise ValueError(message)


def symbol(x):
    need(type(x) is int and 1 <= x < 31, 'undefined or malformed character argument')
    return sum((k * x) % 31 > 15 for k in range(1, 16)) % 2


def derive(certificate):
    need(certificate['schema'] == 'CHARACTER_PHASE310_AP_KERNEL_V1' and certificate['q'] == 31
         and certificate['period'] == 310 and certificate['roots'] == [1,2,4]
         and certificate['pole'] == 0 and certificate['variables'] == 55, 'exact original obstruction family')
    roots = [1,2,4]
    bits = {r: tuple(symbol((r - a) % 31) for a in roots)
            for r in range(1,31) if r not in roots}
    keys = sorted(set(bits.values()))
    need(keys == [tuple((t >> j) & 1 for j in [2,1,0]) for t in range(8)], 'all eight actual character patterns')
    labels = {}
    for r in range(1,31):
        row = 8 + roots.index(r) if r in roots else keys.index(bits[r])
        for s in range(10):
            v = 5 * row + s % 5 + 1
            labels[r, s] = v if s < 5 else -v
    physical = [None if x % 31 == 0 else labels[x % 31, x % 10] for x in range(310)]
    need(set(v for v in physical if v is not None) == set(range(1,56)) | set(range(-55,0)),
         'every original input occurs with both physical polarities')
    root_points = 0
    for x, value in enumerate(physical):
        if value is not None:
            need(physical[(x + 155) % 310] == -value, 'all original antipodal point identities')
            root_points += x % 31 in roots
    need(root_points == 30, 'all three actual roots are retained, only pole0 omitted')
    clauses = []
    leaf_terms = 0
    for record in certificate['ap_records']:
        need(type(record) is list and len(record) == 3 and all(type(x) is int for x in record), 'literal AP record')
        a, d, common = record
        need(0 <= a < 310 and 1 <= d < 310 and common in [0,1], 'actual cyclic AP and palette domains')
        points = [(a + j * d) % 310 for j in range(7)]
        need(all(x % 31 != 0 for x in points), 'original AP leaf hits omitted pole')
        demand = {}
        for x in points:
            tag = labels[x % 31, x % 10]
            expected = common if tag > 0 else 1 - common
            need(abs(tag) not in demand or demand[abs(tag)] == expected, 'tautological leaf cannot be a premise')
            demand[abs(tag)] = expected
            leaf_terms += 1
        clauses.append(tuple(-v if demand[v] else v for v in sorted(demand)))
    need(len(clauses) == 1758 and len(set(clauses)) == len(clauses), 'entire unique original AP kernel')
    cnf = (f'p cnf 55 {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode()
    return cnf, {'actual_AP_leaves': len(clauses), 'original_terms_checked': leaf_terms,
                 'whole_physical_points': 310, 'regular_points': 300, 'root_points_retained': root_points,
                 'clause_sha256': hashlib.sha256(json.dumps(clauses, separators=(',', ':')).encode()).hexdigest()}


def check(certificate_path, proof_path, output):
    need(not output.exists(), 'fresh generated original-AP CNF')
    raw = certificate_path.read_bytes()
    cnf, stats = derive(json.loads(raw))
    output.write_bytes(cnf)
    checked = verify(output, proof_path)
    checked.update({'author': 'six-vdw-1', 'role': 'researcher', 'AP_certificate_sha256': hashlib.sha256(raw).hexdigest(),
                    'actual_physical_bindings': stats,
                    'status': 'COMPLETE_ORIGINAL_AP_KERNEL_AND_STRICT_RUP_CHECKED',
                    'scope': 'One fixed character-root triple, all independent10-phase functions after forced antipodality. No numerical W claim.'})
    return checked


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('certificate', type=Path)
    p.add_argument('proof', type=Path)
    p.add_argument('--cnf-out', type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(check(a.certificate, a.proof, a.cnf_out), sort_keys=True))
