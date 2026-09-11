#!/usr/bin/env python3
"""Check a rational fractional cover supported on canonical eleven-pairs."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,json

def check(path,weights_path,orbit_path=None):
    data=json.loads(path.read_text());weights=list(map(int,weights_path.read_text().split()))
    assert data['n']==82 and data['reflection_average']is False
    assert len(weights)==82 and weights==weights[::-1]and sum(weights)==30884468
    coverage=[Fraction(0)]*82;counts=Counter();rows=Counter();pair_values=[];pairs=[]
    mask=lambda a:sum(1<<x for x in a)
    for row in data['rows']:
        kind=row['kind'];classes=row['classes'];assert kind in ['ten','pair']
        assert len(classes)==(1 if kind=='ten'else 2)
        union=[]
        for a in classes:
            assert a==sorted(set(a))and len(a)==(10 if kind=='ten'else 11)and all(0<=x<82 for x in a)
            sums=[x+y for i,x in enumerate(a)for y in a[i:]];assert len(sums)==len(set(sums));union+=a
        assert len(union)==len(set(union))
        if kind=='pair':
            a,b=classes;wa,wb=[sum(weights[x]for x in c)for c in classes]
            assert wa+wb>=6884468 and wa>=3943985 and wa>=wb
            # A is the canonical representative of the earlier orbit.
            ma,mb=mask(a),mask(b);ra=mask([81-x for x in a]);rb=mask([81-x for x in b])
            assert ma<ra
            if wa==wb:assert ma<=min(mb,rb)
            if ma==min(mb,rb):assert mb==ra
            pair_values.append((wa,wb));pairs.append((a,b))
        value=Fraction(row['numerator'],row['denominator']);assert value>0
        counts[kind]+=value;rows[kind]+=1
        for x in union:coverage[x]+=value
    assert coverage==[1]*82
    assert counts=={'ten':6,'pair':1}and data['ten_multiplicity']==6 and data['pair_multiplicity']==1
    result=dict(verified=True,positive_rows=dict(rows),point_equalities=82,ten_multiplicity=6,pair_multiplicity=1,canonical_orientation_checked=True,minimum_old_pair_weight=min(sum(v)for v in pair_values),minimum_heavier_eleven_weight=min(v[0]for v in pair_values),minimum_lighter_eleven_weight=min(v[1]for v in pair_values))
    if orbit_path:
        orbit=[tuple(map(int,l.split()))for l in orbit_path.read_text().splitlines()];assert len(orbit)==8214;index={a:i for i,a in enumerate(orbit)};indices=[]
        for a,b in pairs:
            i,j=index[tuple(a)],index[tuple(b)];assert i%2==0 and i<j and i//2<=data['maximum_anchor_orbit'];indices.append(i//2)
        result['maximum_anchor_orbit']=max(indices)
    return result
if __name__=='__main__':
    if not __debug__:raise SystemExit('Assertions required.')
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True);p.add_argument('--weights',type=Path,required=True);p.add_argument('--orbit',type=Path);a=p.parse_args();print(json.dumps(check(a.certificate,a.weights,a.orbit),indent=2))
