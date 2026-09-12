"""Independent graph6 degree extraction and corewise certificate reconstruction."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations
import hashlib
import json
from check_pair import need
HERE = Path(__file__).resolve().parent


def multiset(domain, length):
    result = 1
    for i in range(1, length+1):
        result, rem = divmod(result*(domain+i-1), i)
        need(rem == 0, 'root recurrence integer')
    return result


def verify(data, residual, certificate):
    keys = json.loads((HERE/'KEYS.json').read_text())
    counts = [list(map(int, row.split())) for row in (HERE/'COUNTS.tsv').read_text().splitlines()]
    lookup = {tuple(k['degrees']): row[1:] for k, row in zip(keys, counts)}
    hist = Counter(); class_sums = {}; count_pins = []
    old = json.loads((HERE.parent/'ramsey_r55_maximal_residual_domains/EXPECTED.json').read_text())
    pins = json.loads((HERE.parent/'ramsey_r55_maximal_residual_domains/INPUTS.json').read_text())
    contacts = [list(map(int, row.split())) for row in (HERE.parent/'ramsey_r55_q9_core_contact_domains/COUNTS.tsv').read_text().splitlines()]
    for pin in pins:
        n = pin['order']; q = (43-n)//4
        raw = (Path(data)/pin['file']).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'input pin')
        Braw = (Path(residual)/f'{n}.tsv').read_bytes()
        Bpin = next(x for x in old['census']['catalogues'] if x['order'] == n)
        need(hashlib.sha256(Braw).hexdigest() == Bpin['count_sha256'], 'residual pin')
        lines, Brows = raw.splitlines(), Braw.splitlines()
        need(len(lines) == len(Brows) == pin['count'], 'complete core scope')
        sums = [[0, 0, 0] for _ in range(5, q+1)]
        for i, (line, Brow) in enumerate(zip(lines, Brows)):
            cells = Brow.split(); need(int(cells[0]) == i and cells[1] == line, 'core alignment')
            # Expand the payload to a bit string; independent from census adjacency matrix.
            payload = ''.join(format(c-63, '06b') for c in line[1:])
            d = [0]*n
            for bit, (v, u) in zip(payload, ((v,u) for v in range(n) for u in range(v))):
                if bit == '1': d[v] += 1; d[u] += 1
            key = tuple(sorted(d)); hist[key] += 1; nr, nb = lookup[key]
            pr = 15**n
            if q == 8: pr = 2433780807*15**3
            pb = int(cells[3])
            if q == 9:
                pr = contacts[i][2]; pb = min(pb, contacts[contacts[i][3]][1])
            nr, nb = min(nr, pr), min(nb, pb)
            # Repeated multiplication, directly core by core, no histogram aggregation.
            for j, r in enumerate(range(5, q+1)):
                prior = 1; after = 1
                for b in range(q):
                    prior *= pr if b < r else pb; after *= nr if b < r else nb
                sums[j][0] += prior; sums[j][1] += after; sums[j][2] += after < prior
        for r, sums_r in zip(range(5, q+1), sums): class_sums[(q,r)] = sums_r
        count_pins.append(dict(order=n, count_sha256=Bpin['count_sha256'], records=len(lines)))
    need(hist == Counter({tuple(k['degrees']): k['multiplicity'] for k in keys}), 'all histogram multiplicities')
    entropy = json.loads((HERE.parent/'ramsey_r55_three_block_entropy/EXPECTED.json').read_text())['global_bound']['classes']
    before_total = F(); after_total = F(); strict = 0
    need(len(certificate['classes']) == 18, 'all macro strata')
    for cl, parent in zip(certificate['classes'], old['global_bound']['classes']):
        q, r = cl['q'], cl['r']; need((q,r) == (parent['q'],parent['r']), 'macro order')
        matrix = multiset(1998, r-1)*multiset(1931, q-r)
        for u,v in combinations(range(1,q),2): matrix *= 37823 if (u<r)==(v<r) else 35714
        beta = F(**next(x for x in entropy if (x['q'],x['r']) == (q,r))['probability_upper'])
        # Validate the imported upward entropy rounding from its three exact probabilities.
        pS=F(50076756774655,54108801960767);pM=F(42206573324092,48242850554108);pN=F(38488830004364,48242850554108)
        product = F(1)
        for T in combinations(range(1,q),3):
            colors = [v<r for v in T]
            for v in T:
                same = sum((w<r)==(v<r) for w in T)
                product *= pS if same==3 else pM if same==2 else pN
        need(beta**(3*(q-3)) >= product, 'entropy bound')
        prior, new, affected = class_sums[(q,r)]
        before, after = prior*matrix*beta, new*matrix*beta
        need(F(**cl['before_upper']) == F(**parent['after_upper']) == before, 'old class')
        need(F(**cl['after_upper']) == after and cl['prior_contact_sum']==prior and cl['new_contact_sum']==new, 'new class')
        need(F(**cl['ratio_to_previous_upper']) == after/before, 'class ratio')
        need(cl['strictly_improved_tasks'] == affected, 'affected task count')
        before_total += before; after_total += after; strict += affected
    need(F(**certificate['before_upper']) == before_total and F(**certificate['after_upper']) == after_total, 'global sum')
    need(F(**certificate['ratio_to_previous_upper']) == after_total/before_total, 'global ratio')
    need(certificate['strict_task_bounds'] == strict == 2188482, 'strict total')
    need(certificate['core_graphs'] == sum(hist.values()) == 547362, 'core total')
    need(certificate['original_tasks'] == 2189178 and certificate['histogram_keys'] == len(hist) == 824, 'coverage totals')
    need(certificate['imported_residual_counts'] == count_pins, 'record pins')
    need(3*after_total < before_total, 'more than factor-three improvement')
    return dict(status='INDEPENDENT_COREWISE_GLOBAL_ARITHMETIC_VERIFIED', cores=sum(hist.values()),
                exact_degree_incidences=sum(len(d)*m for d,m in hist.items()), macro_strata=18,
                strict_task_bounds=strict, original_task_decisions=0,
                trust='Same author, independent arithmetic and parsing; not an external review')

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('residual');p.add_argument('out');a=p.parse_args()
    result=verify(a.data,a.residual,json.loads((HERE/'EXPECTED.json').read_text()))
    Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
