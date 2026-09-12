"""Complete core census and safe intersection upper bound, all 18 strata."""
from collections import Counter
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
from catalog import obtain, adjacency
from exchange import need
HERE = Path(__file__).resolve().parent


def rat(x):
    return dict(numerator=x.numerator, denominator=x.denominator)


def inputs(data):
    lines = obtain(data)
    hist = Counter()
    keys_by_core = {}
    for n, rows in lines.items():
        degrees = [tuple(sorted(map(sum, adjacency(raw)))) for raw in rows]
        keys_by_core[n] = degrees
        hist.update(degrees)
    keys = [dict(n=len(d), degrees=list(d), multiplicity=m) for d, m in sorted(hist.items(), key=lambda x: (len(x[0]), x[0]))]
    return lines, keys_by_core, keys


def global_bound(data, residual, keys, counts):
    lines, per_core, expected_keys = inputs(data)
    need(keys == expected_keys, 'complete histogram identity')
    need(len(counts) == len(keys), 'local count coverage')
    local = {}
    for i, (key, row) in enumerate(zip(keys, counts)):
        need(row[0] == i and all(0 <= v <= 15**key['n'] for v in row[1:]) and len(row) == 3, 'local count bounds')
        local[tuple(key['degrees'])] = row[1:]
    inherited = json.loads((HERE.parent/'ramsey_r55_maximal_residual_domains/EXPECTED.json').read_text())
    entropy = json.loads((HERE.parent/'ramsey_r55_three_block_entropy/EXPECTED.json').read_text())['global_bound']['classes']
    contacts = [list(map(int, s.split())) for s in (HERE.parent/'ramsey_r55_q9_core_contact_domains/COUNTS.tsv').read_text().splitlines()]
    compressed = {}; imported_pins = []
    for pin in inherited['census']['catalogues']:
        n = pin['order']; path = Path(residual)/f'{n}.tsv'; raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        need(digest == pin['count_sha256'], 'reviewed residual counts hash')
        rows = raw.splitlines(); need(len(rows) == len(lines[n]), 'residual coverage')
        c = Counter()
        for i, row in enumerate(rows):
            label, graph, free, cover = row.split()
            need(int(label) == i and graph == lines[n][i], 'residual graph identity/order')
            nr, nb = local[per_core[n][i]]
            pr = 2433780807*15**3 if n == 11 else 15**n
            pb = int(cover)
            if n == 7:
                pr = contacts[i][2]; pb = min(pb, contacts[contacts[i][3]][1])
            c[(pr, pb, min(pr, nr), min(pb, nb))] += 1
        compressed[n] = c
        imported_pins.append(dict(order=n, count_sha256=digest, records=len(rows)))
    classes = []; before_total = F(); after_total = F(); improved = 0
    for cl in inherited['global_bound']['classes']:
        q, r = cl['q'], cl['r']; n = 43-4*q; a = r-1; b = q-r
        M = comb(1998+a-1, a)*comb(1931+b-1, b)*37823**(comb(a, 2)+comb(b, 2))*35714**(a*b)
        beta = F(**next(x for x in entropy if (x['q'], x['r']) == (q, r))['probability_upper'])
        prior_contacts = sum(m*pr**r*pb**b for (pr,pb,nr,nb), m in compressed[n].items())
        new_contacts = sum(m*nr**r*nb**b for (pr,pb,nr,nb), m in compressed[n].items())
        strict = sum(m for (pr,pb,nr,nb), m in compressed[n].items() if nr**r*nb**b < pr**r*pb**b)
        before = M*beta*prior_contacts; after = M*beta*new_contacts
        need(before == F(**cl['after_upper']) and 0 < after <= before, 'parent reconstruction/bound')
        classes.append(dict(q=q, r=r, core_count=len(lines[n]), prior_contact_sum=prior_contacts,
                            new_contact_sum=new_contacts, before_upper=rat(before), after_upper=rat(after),
                            ratio_to_previous_upper=rat(after/before), strictly_improved_tasks=strict))
        before_total += before; after_total += after; improved += strict
    need(before_total == F(**inherited['global_bound']['after_upper']), 'whole parent reconstruction')
    return dict(status='COMPLETE_CORE_EXCHANGE_GLOBAL_UPPER', classes=classes,
                before_upper=rat(before_total), after_upper=rat(after_total),
                ratio_to_previous_upper=rat(after_total/before_total),
                strict_task_bounds=improved, original_tasks=sum(x['core_count'] for x in classes),
                core_graphs=sum(len(x) for x in lines.values()), histogram_keys=len(keys),
                imported_residual_counts=imported_pins, new_original_task_decisions=0,
                target_found=False, symmetry_assumptions=False,
                interpretation='Ratio of upper certificates; no solver speedup or original-task UNSAT claim')
