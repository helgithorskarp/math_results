#!/usr/bin/env python3
"""Independent exact incidence and entrywise triple-coverage audit.

No producer module or field arithmetic is imported. All centres are treated
as untrusted rational coordinate certificates. Multiplication expands
monomial exponents, and no inversion or circumcentre formula is used.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
POWERS=[(i&1,(i>>1)&1,(i>>2)&1) for i in range(8)]
INDEX={p:i for i,p in enumerate(POWERS)}
PRIMES=(3,5,11)


def require(ok,detail):
    if not ok:raise ValueError(detail)


def multiply(a,b):
    result=[0]*8
    for powers,x in zip(POWERS,a):
        if not x:continue
        for other,y in zip(POWERS,b):
            if not y:continue
            exponents=[u+v for u,v in zip(powers,other)]
            coefficient=x*y
            for prime,e in zip(PRIMES,exponents):coefficient*=prime**(e//2)
            result[INDEX[tuple(e%2 for e in exponents)]]+=coefficient
    return tuple(result)


def distance(a,b):
    d=[tuple(x-y for x,y in zip(a[axis],b[axis])) for axis in (0,1)]
    return tuple(x+y for x,y in zip(multiply(d[0],d[0]),multiply(d[1],d[1])))


def parse(row):
    require(len(row)==2 and all(len(axis)==8 for axis in row),'coordinate shape')
    return tuple(tuple(Fraction(c) for c in axis) for axis in row)


def integer_point(p,D):
    axes=[]
    for axis in p:
        cs=[D*c for c in axis]
        require(all(c.denominator==1 for c in cs),'integer scaling')
        axes.append(tuple(c.numerator for c in cs))
    return tuple(axes)


def exact_unit_triple(a,b,c,D):
    s,t,u=distance(a,b),distance(a,c),distance(b,c)
    st=multiply(s,t); stu=multiply(st,u)
    w=tuple(x+y-z for x,y,z in zip(s,t,u)); square=multiply(w,w)
    return all(x==D*D*(4*y-z) for x,y,z in zip(stu,st,square))


def source_data():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input identity',name))
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    points={int(v):parse(row) for v,row in old['coordinates'].items()}
    require(sorted(points)==list(range(553)) and len(set(points.values()))==553,'union source')
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    H=[points[v] for v in labels]
    require(len(H)==len(set(H))==510,'Heule source')
    aligned=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json').read_text())
    require(set(H)=={parse(row) for row in aligned['aligned_H']},'second Heule table')
    # The independent ambient definition uses the previously published A976
    # certificate's actual labels, rather than filtering neighbour metadata.
    ac=json.loads((REPO/'hadwiger_nelson_parts509_A976_colourability/certificate.json').read_text())
    pool=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    ambient=set(points[v] for v in range(374,509))
    for v in ac['vertices']:
        ambient.add(points[v] if v<374 else parse([pool[v-509]['x'],pool[v-509]['y']]))
    require(len(ambient)==1111,'independent parked ambient')
    return H,labels,set(points.values()),ambient,points


def audit(work):
    start=time.monotonic();H,labels,union,ambient,original=source_data()
    native_lines=(work/'points.txt').read_text().splitlines()
    require(native_lines[0]=='510 96' and len(native_lines)==511,'filter input header')
    H96=[integer_point(p,96) for p in H]
    require([[int(x) for axis in p for x in axis] for p in H96]==[list(map(int,line.split())) for line in native_lines[1:]],'entrywise native coordinates')
    require(json.loads((work/'H_labels.json').read_text())==labels,'native index interpretation')
    require(all(abs(x)<=144 for p in H96 for axis in p for x in axis),'native coefficient range')
    edges=[(i,j) for i,j in combinations(range(510),2) if distance(H96[i],H96[j])==(96**2,)+(0,)*7]
    require(len(edges)==2504,'complete Heule unit graph')
    rows=json.loads((work/'centres.json').read_text()); centres=[parse(row['coordinates']) for row in rows]
    require(centres==sorted(set(centres)),'distinct ordered centres')
    scaled_H={96:H96};cover=set();fresh=[];hist=Counter();external=Counter();outside=Counter();new=Counter()
    Hset=set(H);neighbour_sets=[];denominators=Counter();strong=[]
    for index,(q,row) in enumerate(zip(centres,rows)):
        D=lcm(96,*(c.denominator for axis in q for c in axis));denominators[D]+=1
        if D not in scaled_H:scaled_H[D]=[integer_point(p,D) for p in H]
        qi=integer_point(q,D);unit=(D*D,)+(0,)*7
        neighbours=[i for i,p in enumerate(scaled_H[D]) if distance(p,qi)==unit]
        require(neighbours==row['neighbors'] and len(neighbours)>=3,('centre incidences',index))
        require(len(row['witness'])==3 and row['witness']==sorted(set(row['witness'])) and set(row['witness'])<=set(neighbours),'witness triple')
        neighbour_sets.append(neighbours)
        for triple in combinations(neighbours,3):
            require(triple not in cover,'one triple assigned to multiple centres')
            cover.add(triple)
        degree=len(neighbours);hist[degree]+=1
        if q not in Hset:external[degree]+=1
        if q not in union:outside[degree]+=1
        if q not in ambient and q not in union:
            new[degree]+=1
            if degree>=4:
                fresh.append({'centre_index':index,**row,'degree':degree})
                if degree>=7:
                    Pscaled=[integer_point(original[v],D) for v in range(509)]
                    pns=[v for v,p in enumerate(Pscaled) if distance(p,qi)==unit]
                    strong.append({'centre_index':index,'degree_Heule':degree,'degree_Parts':len(pns),'coordinates':row['coordinates'],
                                   'Heule_neighbours_in_union_labels':[labels[v] for v in neighbours],'Parts_neighbours':pns,
                                   'no_sqrt5':all(q[a][i]==0 for a in (0,1) for i in (2,3,6,7))})
    survivors=[tuple(map(int,line.split())) for line in (work/'survivors.tsv').read_text().splitlines()]
    require(survivors==sorted(set(survivors)) and all(len(t)==3 and 0<=t[0]<t[1]<t[2]<510 for t in survivors),'survivor stream domain and order')
    missing=cover-set(survivors);require(not missing,'valid centre triple omitted by native filter')
    false=sorted(set(survivors)-cover)
    for i,j,k in false:require(not exact_unit_triple(H96[i],H96[j],H96[k],96),'unaccounted exact unit triple')
    require([list(t) for t in false]==json.loads((work/'rejected.json').read_text()),'entrywise rejected triples')
    require(fresh==json.loads((work/'fresh_candidates.json').read_text()),'entrywise fresh frontier')
    if (HERE/'fresh_candidates.json').exists():require(fresh==json.loads((HERE/'fresh_candidates.json').read_text()),'public frontier certificate')
    filtering=json.loads((work/'filter.json').read_text())
    require(filtering['vertices']==510 and filtering['triples']==comb(510,3) and filtering['second_survivors']==len(survivors),'native exhaustive count')
    summary=json.loads((work/'summary.json').read_text())
    checked={'vertices':510,'unit_edges':len(edges),'centres':len(rows),'full_degree_histogram':dict(sorted(hist.items())),
             'external_degree_histogram':dict(sorted(external.items())),'outside_closed553_histogram':dict(sorted(outside.items())),
             'outside_both553_and1111_histogram':dict(sorted(new.items())),'fresh_degree_at_least_four':len(fresh),
             'unit_circle_triples':len(cover),'modular_rejections':len(false),'filter':filtering,
             'centres_sha256':sha256((work/'centres.json').read_bytes()).hexdigest(),
             'survivors_sha256':sha256((work/'survivors.tsv').read_bytes()).hexdigest()}
    for key,value in checked.items():require(json.loads(json.dumps(value))==summary[key],('producer summary',key))
    expected=HERE/'expected.json'
    if expected.exists():require(json.loads(json.dumps(checked))==json.loads(expected.read_text()),'stable expected result')
    result={'status':'EXACT HEULE510 CENTRE CENSUS AND NEW FRONTIER VERIFIED','checked':checked,'full_incidence_pairs':len(rows)*510,
            'Heule_pair_checks':comb(510,2),'complete_survivor_triples_compared_entrywise':len(survivors),
            'centres_by_common_denominator':dict(sorted(denominators.items())),'strong_fresh_candidates':strong,
            'extra_Parts_incidence_checks':len(strong)*509,'seconds':time.monotonic()-start,
            'independent_author_review_claimed':False,'native_colour_queries':0,'record_improvement':False}
    (work/'audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();audit(args.work)
