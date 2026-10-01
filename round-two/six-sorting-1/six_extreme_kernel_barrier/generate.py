"""Produce selected six-extreme witnesses using exact Boolean columns.

Enumerates one complete original family, then chooses a witness at every
realized output configuration. The proof needs only the selected lower sum;
the standalone scalar checker does not import this producer.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent


def mask(xs):
    return sum(1 << p for p in xs)


def record(gates, lows, highs):
    free = [p for p in range(13) if p not in lows + highs]
    if len(free) != 7:
        raise ValueError('wrong original cube')
    tags = [-1 if p in lows else 1 if p in highs else 0 for p in range(13)]
    columns = [0] * 13
    for assignment in range(128):
        for j,p in enumerate(free):
            columns[p] |= ((assignment >> j) & 1) << assignment
    touched = redundant = 0
    for t,(a,b) in enumerate(gates):
        if tags[a] or tags[b]:
            touched |= 1 << t
            if tags[a] > tags[b]:
                tags[a],tags[b] = tags[b],tags[a]
                columns[a],columns[b] = columns[b],columns[a]
        else:
            x,y = columns[a],columns[b]
            if not x & ~y:
                redundant |= 1 << t
            columns[a],columns[b] = x & y,x | y
    return {'original_low_mask':mask(lows),'original_high_mask':mask(highs),
            'current_low_mask':mask([p for p in range(13) if tags[p]<0]),
            'current_high_mask':mask([p for p in range(13) if tags[p]>0]),
            'marked_touch_mask':touched,'redundancy_mask':redundant,
            'D':touched.bit_count(),'R':redundant.bit_count(),
            'C':touched.bit_count()+redundant.bit_count()}


def main():
    begin = time.monotonic()
    fixture = json.loads((ROOT/'fixture.json').read_text())
    gates = fixture['prefix']
    if len(gates)!=32 or any(not 0<=a<b<13 for a,b in gates):
        raise ValueError('invalid literal prefix')
    # Integer-mask order matches the compact C++ exploratory census, but that
    # census is not a dependency of this producer or of the scalar checker.
    threes = sorted(mask(xs) for xs in combinations(range(13),3))
    selected = {}
    count = 0
    for low in threes:
        lows = [p for p in range(13) if low >> p & 1]
        for high in threes:
            if low & high:
                continue
            highs = [p for p in range(13) if high >> p & 1]
            row = record(gates,lows,highs)
            key = (row['current_low_mask'],row['current_high_mask'])
            if key not in selected or row['C']>selected[key]['C']:
                selected[key] = row
            count += 1
    if count!=34320 or len(selected)!=18:
        raise ValueError('unexpected producer census')
    witnesses = [selected[key] for key in sorted(selected)]
    mass = sum(2**r['C'] for r in witnesses)
    if mass!=281018368 or mass<=2**28:
        raise ValueError('expected strict obstruction absent')
    certificate = {'schema':'native-kernel-zero-six-extreme-lower-witnesses-v1',
                   'agent':'six-sorting-1','role':'researcher',
                   'fixture_sha256':hashlib.sha256((ROOT/'fixture.json').read_bytes()).hexdigest(),
                   'n':13,'kernel_id':0,'prefix_size':32,'l':3,'h':3,
                   'free_inputs':7,'small_size_lower_bound':16,'size_budget':44,
                   'witnesses':witnesses,'witness_lower_mass':mass,
                   'cap':2**28,'minimum_sorter_total':45,
                   'remaining_nine_wire_ids':fixture['remaining_nine_wire_ids']}
    data=(json.dumps(certificate,indent=2)+'\n').encode()
    (ROOT/'certificate.json').write_bytes(data)
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'SIX_EXTREME_KERNEL_CERTIFICATE_REGENERATED',
                      'producer_original_domains':count,'selected_witnesses':len(witnesses),
                      'witness_lower_mass':mass,'certificate_sha256':hashlib.sha256(data).hexdigest(),
                      'seconds':time.monotonic()-begin,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
