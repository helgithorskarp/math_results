#!/usr/bin/env python3
"""Independent finite cover reconstruction and exact multiplier verification."""
import argparse
from collections import Counter
from itertools import combinations,product
import importlib.util
import json
from pathlib import Path
import exact as X

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reviewer_rows',HERE.parent/'hadwiger_nelson_radix_four_active_closure_review1/independent_check.py')
V=importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)


def fmul(a,b):
    # Polynomial product in F2[t]/(t^2+t+1), without a table.
    p=0
    for bit in range(2):
        if b & (1<<bit):p^=a<<bit
    if p&4:p^=7
    return p


def signature(row):
    values=[(a%2)+2*(b%2) for a,b in row]
    pivot=next(v for v in values[1:] if v)
    inv=next(x for x in (1,2,3) if fmul(x,pivot)==1)
    return tuple(fmul(inv,v) for v in values[1:]),fmul(inv,values[0])


def plane_pencils():
    normals=((1,0),(0,1),(1,1),(1,2),(1,3))
    points=tuple(product(range(4),repeat=2))
    types=[(n,c) for n in normals for c in range(4) if not(c==0 and n in normals[:2])]
    masks={s:sum(1<<k for k,p in enumerate(points) if fmul(s[0][0],p[0])^fmul(s[0][1],p[1])==s[1]) for s in types}
    pencils=[]
    for choice in combinations(types,5):
        if len({n for n,c in choice})!=5:continue
        mask=0
        for s in choice:mask|=masks[s]
        if mask==(1<<16)-1:pencils.append(tuple(sorted(choice)))
    X.need(len(pencils)==9,'nine realized two-dimensional five-direction covers')
    return sorted(pencils)


def inventory():
    rows,factors,circle,monos,rowids=V.reconstruct_inventory()
    byid={c:r for r,c in rowids.items()}
    buckets={}
    for row,c in rowids.items():buckets.setdefault(signature(row),[]).append(c)
    for bucket in buckets.values():bucket.sort()
    patterns=[];quintets=[];counts=Counter();trace=[]
    small=plane_pencils()
    for i,j in combinations(range(1,5),2):
        ei=tuple(int(k==i-1) for k in range(4));ej=tuple(int(k==j-1) for k in range(4))
        for pen in small:
            full=[]
            for (a,b),c in pen:
                normal=tuple(a if k==i-1 else b if k==j-1 else 0 for k in range(4))
                full.append((normal,c))
            full=tuple(sorted(full));patterns.append(full)
            ai=next(k for k,s in enumerate(full) if s[0]==ei)
            aj=next(k for k,s in enumerate(full) if s[0]==ej)
            for lift in product(*(buckets[s] for s in full)):
                first,second=byid[lift[ai]],byid[lift[aj]]
                alpha=X.mul(first[i],X.conj(first[0]));beta=X.mul(second[j],X.conj(second[0]))
                X.need(alpha in X.UNITS and beta in X.UNITS,'unit anchor phases')
                normalized=[]
                for curve in lift:
                    row=byid[curve]
                    X.need(all(d==(0,0) for k,d in enumerate(row) if k not in (0,i,j)),'exact two-coordinate support')
                    normalized.append(X.canonical((row[0],X.mul(row[i],X.conj(alpha)),X.mul(row[j],X.conj(beta)))))
                key=tuple(sorted(normalized));q=tuple(sorted(lift));quintets.append(q);counts[key]+=1
                trace.append((q,key))
    patterns=sorted(patterns);quintets.sort();trace.sort()
    X.need(len(patterns)==len(set(patterns))==54,'all 54 pencils distinct')
    X.need(len(quintets)==len(set(quintets))==6912,'all 6912 quintets distinct')
    X.need(len(counts)==32 and set(counts.values())=={216},'normal-form census')
    keys=sorted(counts)
    expected_anchors={((-1,0),(-1,0),(0,0)),((-1,0),(0,0),(-1,0))}
    X.need(all(expected_anchors<=set(key) for key in keys),'normalized singleton anchors')
    return factors,patterns,quintets,keys,trace


def run(certificate_path,export=None):
    cert=json.loads(Path(certificate_path).read_text())
    factors,patterns,quintets,keys,trace=inventory()
    checked=X.check_identities(cert,keys)
    if export:
        with Path(export).open('x') as f:
            json.dump({'schema':'hn-radix-two-coordinate-exclusions-v1','forbidden_quintets':quintets},f,sort_keys=True,separators=(',',':'));f.write('\n')
    return {'verified':True,'coordinate_pairs':6,'realized_pencils':54,'lifted_quintets':6912,
            'normal_forms':32,'lifts_per_normal_form':216,'polynomial_identities_checked':checked,
            'direct_denominator_contradiction_forms':31,'power_compatibility_contradiction_forms':1,
            'curve_inventory_sha256':X.digest(factors),'patterns_sha256':X.digest(patterns),
            'quintets_sha256':X.digest(quintets),'normal_forms_sha256':X.digest(keys),
            'normalization_transcript_sha256':X.digest(trace),
            'complex_affine_concurrences':0,'valid_inside_larger_active_sets':True,
            'record_improvement':False,'complete_A5_architecture_closed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
    parser.add_argument('--export-interface',type=Path)
    parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args();result=run(args.certificate,args.export_interface)
    if args.check_expected:X.need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected exact census')
    print(json.dumps(result,indent=2,sort_keys=True))
