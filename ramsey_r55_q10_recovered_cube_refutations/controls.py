"""Small exhaustive propagation controls and negative certificate controls."""
from itertools import product
from pathlib import Path
import json
import subprocess
import verify


def naive(rows, assumptions=()):
    values = {}
    for x in assumptions:
        if abs(x) in values and values[abs(x)] != (x > 0):
            return True
        values[abs(x)] = x > 0
    changed = True
    while changed:
        changed = False
        for clause in rows:
            if any(values.get(abs(x)) == (x > 0) for x in clause
                   if abs(x) in values):
                continue
            live = [x for x in clause if abs(x) not in values]
            if not live:
                return True
            if len(live) == 1:
                values[abs(live[0])] = live[0] > 0
                changed = True
    return False


def run(propagator, checker, scratch, fixedpoint_checker):
    scratch = Path(scratch)
    choices = [[x for x in (a, 2*b) if x]
               for a, b in product((-1, 0, 1), repeat=2)]
    query = scratch/'small-queries.txt'
    query.write_text(''.join(' '.join(map(str, c))+' 0\n' for c in choices))
    count = rejected = 0
    for word in range(512):
        rows = [c for i, c in enumerate(choices) if word >> i & 1]
        cnf = scratch/'small.cnf'
        cnf.write_text(f'p cnf 2 {len(rows)}\n' +
                       ''.join(' '.join(map(str, c))+' 0\n' for c in rows))
        result = subprocess.run([str(propagator), str(cnf), str(query)],
                                capture_output=True, text=True)
        if naive(rows):
            verify.need(result.returncode != 0, 'initial contradiction accepted')
            rejected += 1
            continue
        verify.need(result.returncode == 0, 'propagator rejected consistent base')
        actual = json.loads(result.stdout)['tests']
        for c, row in zip(choices, actual):
            verify.need(row['rup'] == naive(rows, [-x for x in c]),
                        'watched propagation disagrees with naive fixed point')
            count += 1
    negative = 0
    inputs = json.loads((verify.ROOT/'INPUTS.json').read_text())
    for claim in inputs['certificates']:
        lines = (verify.ROOT/(claim['id']+'-core.cnf')).read_text().splitlines()
        for literal in claim['clause']:
            body = lines[1:]
            body.remove(f'{-literal} 0')
            bad = scratch/'missing-assumption.cnf'
            bad.write_text(f'p cnf 40351 {len(body)}\n'+'\n'.join(body)+'\n')
            result = subprocess.run([str(checker), str(bad),
                str(verify.ROOT/(claim['id']+'-core.drat'))], capture_output=True)
            verify.need(result.returncode != 0, 'missing assumption not rejected')
            negative += 1
    # An incomplete proof must not be turned into a certificate.
    empty = scratch/'empty-proof.drat'; empty.write_text('')
    result = subprocess.run([str(checker), str(verify.ROOT/'d22-20-core.cnf'),
                             str(empty)], capture_output=True)
    verify.need(result.returncode != 0, 'incomplete proof accepted'); negative += 1
    fixtures = [('1 2 0', '0', '0', True),
                ('1 1 0', '0', '0', False),
                ('1 2 0', '0', '-1 0', False),
                ('1 2 0', '1 0', '1 0', False),
                ('1 2 0', '0', '1 1 0', False)]
    for body, query_text, assignment, expected in fixtures:
        cnf = scratch/'fixedpoint-small.cnf'; cnf.write_text('p cnf 2 1\n'+body+'\n')
        q = scratch/'fixedpoint-query.txt'; q.write_text(query_text+'\n')
        a = scratch/'fixedpoint-assignment.txt'; a.write_text(assignment+'\n')
        result = subprocess.run([str(fixedpoint_checker), str(cnf), str(q), str(a)],
                                capture_output=True)
        verify.need((result.returncode == 0) == expected, 'fixedpoint control')
    return {'small_formulas': 512, 'initial_conflicts': rejected,
            'fixed_point_comparisons': count, 'negative_proofs': negative,
            'fixedpoint_controls': len(fixtures)}
