from paths import INPUTS, WORK
"""Explore a literal one-cap trade in the classical68-block Steiner plane.

Delete the ten old blocks meeting a fixed five-cap in three points;
replace each by a new-point word omitting one cap point, and add the cap.
All g-respecting omission choices in this narrowly specified family are tested.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time
import carrier as C
from quotient import encoded

HERE=Path(__file__).resolve().parent


def main():
    import steiner
    S=steiner.code();old=set(S);G=C.STANDARD_G;started=time.monotonic()
    caps=tuple(sorted((1<<16)|C.mask((2*a,2*a+1,2*b,2*b+1))
                      for a,b in combinations(range(8),2) if
                      ((1<<16)|C.mask((2*a,2*a+1,2*b,2*b+1))) not in old))
    records=[];positive=[]
    for cap in caps:
        C.require(C.image(cap,G)==cap and max((cap&w).bit_count() for w in S)<=3,'fixed five-cap')
        removed=tuple(w for w in S if (cap&w).bit_count()==3)
        C.require(len(removed)==10,'ten distinct triple parents')
        fixed=tuple(w for w in removed if C.image(w,G)==w)
        pairs=tuple((w,C.image(w,G)) for w in removed if w<C.image(w,G))
        C.require(len(fixed)==2 and len(pairs)==4,'parent orbit decomposition')
        choices=tuple(C.points(w&cap) for w,z in pairs)
        raw=pair_patterns=valid=0
        for omissions in product(*choices):
            raw+=1
            omit={w:16 for w in fixed}
            for (w,z),v in zip(pairs,omissions):omit[w]=v;omit[z]=G[v]
            tails=tuple(w^(1<<omit[w]) for w in removed)
            kept=tuple(tuple(C.points(t&cap)) for t in tails)
            C.require(all(len(p)==2 for p in kept),'two retained cap points')
            if len(set(kept))!=10:continue
            pair_patterns+=1
            if any((a&b).bit_count()>1 for a,b in combinations(tails,2)):continue
            words=tuple(sorted((old-set(removed))|{cap}|{t|(1<<17) for t in tails}))
            degrees=C.check_code(words,G)
            C.require(len(words)==69,'one-cap trade size69')
            center=next(v for v in range(0,16,2) if not cap>>v&1)
            C.require(degrees[center]==degrees[center+1]==20 and
                      sum(w>>center&1 and w>>(center+1)&1 for w in words)==5,'swapped saturated pair')
            record={'cap':cap,'omissions':sorted(omit.items()),'words':words,
                    'centers':[center,center+1],'replications':degrees}
            positive.append(record);valid+=1
        records.append({'cap':cap,'raw_g_respecting_choices':raw,'cap_pair_patterns':pair_patterns,
                        'valid69_trades':valid})
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_SPECIFIED_ONE_CAP_TRADE_FAMILY',
            'steiner_blocks':68,'caps':len(caps),'raw_choices':sum(r['raw_g_respecting_choices'] for r in records),
            'cap_pair_patterns':sum(r['cap_pair_patterns'] for r in records),
            'valid69_trades':len(positive),'distinct69_codes':len({tuple(p['words']) for p in positive}),
            'records':records,'positive':positive,'seconds':time.monotonic()-started,
            'scope':'one classical plane, g-fixed nonblock five-caps containing fixedX, contained tails and g-respecting omissions; not all69 codes/trades'}
    (WORK/'swapped-steiner-one-cap-trades.json').write_bytes(encoded(result))
    if positive:
        first=positive[0]
        witness={'agent':'six-code-2','role':'researcher','words':first['words'],'involution':G,
                 'centers':first['centers'],'replications':first['replications'],'construction':{'cap':first['cap'],
                 'omissions':first['omissions']},'claim':'69-word one-cap Steiner trade; no unrestricted record'}
        (WORK/'swapped-steiner-witness69.json').write_bytes(encoded(witness))
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','positive')},sort_keys=True))
    print(json.dumps({'per_cap':[{'cap_pair_patterns':a,'valid69_trades':b,'caps':n}
          for (a,b),n in sorted(Counter((r['cap_pair_patterns'],r['valid69_trades']) for r in records).items())]}))


if __name__=='__main__':main()
