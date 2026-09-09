"""Narrow resolution/unit-substitution checker, independent of the RUP code."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_SHA = 'ba96586572a831dbc6a12329515cad3d11779a1ea01b3242e981a2c1f539c2d1'


def check(directory, cert):
    nc, nv = 1502521, 946
    if (set(cert) != {'format','r','base_sha256','assumptions','proof','vertex',
                     'blue_neighbors','ramsey_subset','premise','conclusion','implied_unit'}
        or cert['format'] != 'q8-r8-rup-ramsey-branch-v1'
        or cert['r'] != 8 or type(cert['r']) is not int
        or cert['base_sha256'] != BASE_SHA or cert['assumptions'] != [-119]
        or cert['vertex'] != 3 or cert['blue_neighbors'] != list(range(4,32))
        or cert['ramsey_subset'] != list(range(4,29)) or cert['implied_unit'] != 119
        or cert['conclusion'] != 'UNSAT_NEGATIVE_PHYSICAL_BRANCH'):
        raise ValueError('Independent fixed theorem scope')
    premise = cert['premise']
    if premise != dict(red_clique=5, blue_clique=4, order=25,
        source='https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf',
        citation='B. D. McKay and S. P. Radziszowski, R(4,5)=25, Journal of Graph Theory 19 (1995), 309-322'):
        raise ValueError('Independent external premise')
    needed = {h for step in cert['proof'] for h in step['hints'] if 0<h<=nc}
    digest = hashlib.sha256()
    db = {nc+1: frozenset([-119])}
    with (Path(directory)/'q8-r8.cnf').open('rb') as f:
        header = f.readline(); digest.update(header)
        if header != b'p cnf 946 1502521\n':
            raise ValueError('Independent header')
        count = 0
        for count, line in enumerate(f,1):
            digest.update(line)
            if count in needed:
                a = [int(x) for x in line.split()]
                if a[-1] != 0:
                    raise ValueError('Independent DIMACS')
                db[count] = frozenset(a[:-1])
    if count != nc or digest.hexdigest() != BASE_SHA:
        raise ValueError('Independent full base checksum')
    resolution, substitution = 0, 0
    for ident, step in enumerate(cert['proof'], nc+2):
        if not isinstance(step,dict) or set(step) != {'clause','hints'}:
            raise ValueError('Independent step format')
        c, hints = step['clause'], step['hints']
        if (not isinstance(c,list) or len(set(c)) != len(c)
            or any(type(x) is not int or not 1<=abs(x)<=nv for x in c)
            or not isinstance(hints,list) or not hints
            or any(type(h) is not int or h not in db for h in hints)):
            raise ValueError('Independent literals or backward references')
        conclusion = frozenset(c)
        passed = False
        if len(hints) == 2:
            a,b = [db[h] for h in hints]
            pivots = a & frozenset(-x for x in b)
            if len(pivots) == 1:
                x = next(iter(pivots))
                if (a-{x}) | (b-{-x}) == conclusion:
                    passed = True
                    resolution += 1
        if not passed:
            if any(len(db[h]) != 1 for h in hints[:-1]):
                raise ValueError('Independent unit premises')
            units = {next(iter(db[h])) for h in hints[:-1]}
            if any(-x in units for x in units):
                raise ValueError('Independent inconsistent units')
            reason = db[hints[-1]]
            if reason & units or reason-{-x for x in units} != conclusion or len(conclusion) != 1:
                raise ValueError('Independent unit substitution')
            substitution += 1
        db[ident] = conclusion
    established = {next(iter(c)) for c in db.values() if len(c)==1}
    # For vertex 3, the physical edge numbers are 119..157 in vertex order.
    if not all(-v in established for v in range(119,147)):
        raise ValueError('Independent 28-neighbor conclusion')
    # Direct exhaustive normalization check, without any CNF or producer import.
    ordered = negative = 0
    for matrix in range(1<<16):
        signatures = [sum(((matrix>>(4*u+v))&1)<<u for u in range(4)) for v in range(4)]
        if signatures != sorted(signatures,reverse=True):
            continue
        ordered += 1
        if not matrix >> 12 & 1:
            negative += 1
            if matrix >= 4096:
                raise ValueError('Independent highest-row implication')
    return dict(status='VERIFIED_RELATIVE_TO_PUBLISHED_RAMSEY_BOUND',
                resolution_steps=resolution, unit_substitution_steps=substitution,
                normalized_matrices=ordered, negative_first_top_bit_matrices=negative,
                forced_blue_neighbors=28, selected_ramsey_vertices=25,
                full_ramsey_proof_checked=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('directory'); p.add_argument('certificate')
    a = p.parse_args()
    print(json.dumps(check(a.directory, json.loads(Path(a.certificate).read_text())), indent=2))
