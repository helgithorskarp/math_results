#!/usr/bin/env python3
"""Solver-free union-cut verification, including every labeled core transport.

The pinned upstream checker certifies the input universe. New root cuts are
reconstructed using ternary assignments and literal set intersections.
"""
import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'ramsey_r55_coupled_signature_counts'
PINS={'CERTIFICATE.tsv':'3903b439068cd87a37fc716541a365894fd2498afdbaee8bcfa7edc3ac0916e9',
      'verify_certificate.py':'585ef332f3e07c7eae1a349a942ea2cce07c68f2d594f36c937864f517e91d76',
      'SUMMARY.tsv':'cce4476cf875ff5d086a2f4fe3a830ddd6ba74e119cb4f9e049f14bfd2f3c511'}
FIELDS=('counts_18_to_24','M','input_cores','orbits','primal_cores','dual_cores','split_cores','removed_splits')
RAMSEY=((1,1,1,1,1),(1,2,3,4,5),(1,3,6,9,14),(1,4,9,18,31),(1,5,14,31,62))

def require(test, detail):
    if not test: raise ValueError(detail)

def check_ramsey_table():
    for a in range(1,6):
        for b in range(1,6):
            if min(a,b)==1: expected=1
            else:
                left,right=RAMSEY[a-2][b-1],RAMSEY[a-1][b-2]
                expected=left+right
                if left%2==right%2==0: expected-=1
            require(RAMSEY[a-1][b-1]==expected,'recurrence/parity upper table')

def vertices(mask,k): return {v for v in range(k) if mask>>v&1}

def root_bound(a,b,near):
    k=len(near)
    require(type(a) is int and type(b) is int and 0<=a<1<<k and 0<=b<1<<k,'root masks')
    require(not a&b and a|b,'disjoint nonempty root pair')
    red,blue=vertices(a,k),vertices(b,k)
    require(len(red)<=4 and len(blue)<=4,'root size')
    require(all(j in near[i] for i,j in combinations(red,2)),'root is not a red clique')
    require(all(j not in near[i] for i,j in combinations(blue,2)),'root is not a blue clique')
    fixed=set(range(k))-red-blue
    for v in red: fixed&=near[v]
    for v in blue: fixed-=near[v]
    return RAMSEY[4-len(red)][4-len(blue)]-1-len(fixed)

def all_roots(near):
    k=len(near)
    for word in product(range(3),repeat=k):
        red={i for i,c in enumerate(word) if c==1}
        blue={i for i,c in enumerate(word) if c==2}
        if not red and not blue: continue
        if any(j not in near[i] for i,j in combinations(red,2)): continue
        if any(j in near[i] for i,j in combinations(blue,2)): continue
        a=sum(1<<v for v in red);b=sum(1<<v for v in blue)
        yield a,b,root_bound(a,b,near)

def read_values(payload):
    pairs=payload['values']
    require(type(pairs) is list and all(type(p) is list and len(p)==2 for p in pairs),'primal format')
    require(all(type(x) is int and type(v) is int and v>0 for x,v in pairs),'primal integer numerators')
    require(pairs==sorted(pairs) and len({x for x,v in pairs})==len(pairs),'primal order/uniqueness')
    return dict(pairs)

def check_primal(payload,caps,b,near,denominator=1):
    y=read_values(payload)
    require(type(denominator) is int and denominator>0,'denominator')
    require(set(y)<=set(caps),'forbidden signature')
    require(all(v<=denominator*caps[x] for x,v in y.items()),'signature capacity')
    require(sum(y.values())==denominator*b[0],'central total')
    for i,target in enumerate(b[1:]):
        require(sum(v for x,v in y.items() if x>>i&1)==denominator*target,'incidence equality')
    for a,bb,cap in all_roots(near):
        mass=sum(v for x,v in y.items() if x&a==a and not x&bb)
        require(mass<=denominator*cap,('union capacity',a,bb,mass,denominator*cap))

def check_dual(payload,caps,b,near,branch=None):
    lam=payload['lambda'];roots=payload['roots']
    require(type(lam) is list and len(lam)==len(b) and all(type(v) is int for v in lam),'lambda dimension/domain')
    require(type(roots) is list and all(type(r) is list and len(r)==3 for r in roots),'dual root format')
    require(roots==sorted(roots) and len({(a,bb) for a,bb,v in roots})==len(roots),'dual roots order/uniqueness')
    require(all(type(v) is int and v>0 for a,bb,v in roots),'root weights')
    lhs=sum(v*t for v,t in zip(lam,b))
    rhs=sum(v*root_bound(a,bb,near) for a,bb,v in roots)
    bw=payload.get('branch_weight',0)
    require(type(bw) is int and bw>=0,'branch weight')
    if branch is None: require(bw==0,'unspecified branch')
    else:
        sig,sign,bound=branch
        require(sig in caps and sign in (-1,1),'split variable/domain')
        rhs+=bw*bound
    for x,cap in caps.items():
        coefficient=lam[0]+sum(v for i,v in enumerate(lam[1:]) if x>>i&1)
        coefficient-=sum(v for a,bb,v in roots if x&a==a and not x&bb)
        if branch is not None and x==sig: coefficient-=bw*sign
        rhs+=cap*max(0,coefficient)
    require(lhs>rhs,('strict exact dual inequality',lhs,rhs))

def verify(kind,payload,caps,b,near):
    if kind=='primal': check_primal(payload,caps,b,near)
    elif kind=='dual': check_dual(payload,caps,b,near)
    else:
        require(kind=='split','certificate kind')
        x,t=payload['signature'],payload['threshold']
        require(type(t) is int,'integral split threshold')
        # Every integer y_x lies in exactly one of these two halfspaces.
        check_dual(payload['left'],caps,b,near,(x,1,t))
        check_dual(payload['right'],caps,b,near,(x,-1,-t-1))
        real=payload['real_primal']
        require(real['denominator']>1,'proper fractional witness')
        check_primal(real,caps,b,near,real['denominator'])

def move(kind,payload,p):
    def mask(x): return sum(1<<p[i] for i in range(len(p)) if x>>i&1)
    def primal(y):
        return {**y,'values':sorted([mask(x),v] for x,v in y['values'])}
    def dual(y):
        lam=[y['lambda'][0]]+[0]*len(p)
        for i in range(len(p)): lam[p[i]+1]=y['lambda'][i+1]
        return {**y,'lambda':lam,'roots':sorted([mask(a),mask(b),v] for a,b,v in y['roots'])}
    if kind=='primal': return primal(payload)
    if kind=='dual': return dual(payload)
    return {**payload,'signature':mask(payload['signature']),
            'left':dual(payload['left']),'right':dual(payload['right']),
            'real_primal':primal(payload['real_primal'])}

def mutation_tests(examples):
    kind,payload,caps,b,near=examples['primal']
    bad=json.loads(json.dumps(payload));bad['values'][0][1]+=1
    tests=[lambda:verify(kind,bad,caps,b,near)]
    _,dp,dc,db,dn=examples['dual']
    zero={'lambda':[0]*len(db),'roots':[]}
    tests.append(lambda:check_dual(zero,dc,db,dn))
    overlap={'lambda':dp['lambda'],'roots':[[1,1,1]]}
    tests.append(lambda:check_dual(overlap,dc,db,dn))
    _,sp,sc,sb,sn=examples['split']
    broken=json.loads(json.dumps(sp));broken['right']['lambda']=[0]*len(sb)
    broken['right']['roots']=[];broken['right']['branch_weight']=0
    tests.append(lambda:verify('split',broken,sc,sb,sn))
    for test in tests:
        try: test()
        except ValueError: continue
        raise ValueError('altered certificate accepted')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.tsv')
    parser.add_argument('--emit-summary',action='store_true')
    args=parser.parse_args()
    check_ramsey_table()
    for name,digest in PINS.items(): require(sha256((PRIOR/name).read_bytes()).hexdigest()==digest,name)
    replay=subprocess.run([sys.executable,'-O',str(PRIOR/'verify_certificate.py')],check=True,capture_output=True,text=True)
    require('PASS 374 degree-preserving orbits' in replay.stdout,'prior verification')
    spec=importlib.util.spec_from_file_location('prior_checker',PRIOR/'verify_certificate.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    previous,globals_=old.load_inputs()
    with (PRIOR/'CERTIFICATE.tsv').open() as stream:
        source=[r for r in csv.DictReader(stream,delimiter='\t') if r['kind']=='primal']
    with args.certificate.open() as stream: records=list(csv.DictReader(stream,delimiter='\t'))
    require(len(records)==len(source)==332,'orbit record count')
    metadata=('counts_18_to_24','M','red_mask','orbit_size')
    require([tuple(r[f] for f in metadata) for r in records]==[tuple(r[f] for f in metadata) for r in source],'exact ordered input orbit coverage')
    grouped=defaultdict(list)
    for row in records: grouped[row['counts_18_to_24']].append(row)
    summary=[];totals=Counter();orbit_counts=Counter();examples={};excluded=set();legacy_tests=0
    source_by_key={(r['counts_18_to_24'],r['red_mask']):r for r in source}
    for counts,rows in grouped.items():
        cs=tuple(map(int,counts.split(',')))
        ds=tuple(d for d,n in zip(range(18,25),cs) if d!=21 for _ in range(n))
        require(sum(cs)==43 and len(ds)<=6,'small exceptional scope')
        M=int(rows[0]['M']);_,universe=old.universe(ds,M);seen=set();tally=Counter()
        for row in rows:
            mask=int(row['red_mask']);kind=row['kind'];payload=json.loads(row['payload'])
            orbit=old.orbit_with_maps(mask,ds)
            require(len(orbit)==int(row['orbit_size']) and min(orbit)==mask,'orbit metadata')
            require(not seen&orbit.keys(),'overlap');seen.update(orbit)
            for image,p in orbit.items():
                caps,b,near=universe[image]
                verify(kind,move(kind,payload,p),caps,b,near)
            caps,b,near=universe[mask]
            examples.setdefault(kind,(kind,payload,caps,b,near))
            if kind!='primal':
                legacy=source_by_key[(counts,row['red_mask'])]
                old_values=[list(map(int,part.split(':'))) for part in legacy['payload'].split(',')]
                try: check_primal({'values':old_values},caps,b,near)
                except ValueError as error:
                    require(type(error.args[0]) is tuple and error.args[0][0]=='union capacity',
                            'legacy witness must fail specifically a new union cut')
                    legacy_tests+=1
                else: raise ValueError('legacy witness survived a proved union exclusion')
            tally[kind]+=len(orbit);orbit_counts[kind]+=1
        totals.update(tally)
        previous_row=next(r for r in previous if r['counts_18_to_24']==counts)
        removed=int(previous_row['split_count']) if not tally['primal'] else 0
        if not tally['primal']: excluded.add(counts)
        if tally['primal']: require(cs[0]==cs[5]==cs[6]==0,'small-core degree range')
        summary.append([counts,M,len(seen),len(rows),tally['primal'],tally['dual'],tally['split'],removed])
    require(sum(totals.values())==4800 and len(summary)==17,'complete input totals')
    mutation_tests(examples)
    old_excluded={r['counts_18_to_24'] for r in previous if not int(r['pass'])}
    with (PRIOR/'SUMMARY.tsv').open() as stream:
        old_excluded|={r['counts_18_to_24'] for r in csv.DictReader(stream,delimiter='\t') if not int(r['primal_cores'])}
    inherited=[r for r in globals_ if r['status']=='feasible' and r['counts_18_to_24'] not in old_excluded]
    require(len(inherited)==73 and sum(int(r['split_count']) for r in inherited)==290,'inherited global totals')
    remaining=[r for r in inherited if r['counts_18_to_24'] not in excluded]
    global_M=Counter();split_M=Counter()
    for r in remaining:
        global_M[int(r['M'])]+=1;split_M[int(r['M'])]+=int(r['split_count'])
    text='\t'.join(FIELDS)+'\n'+''.join('\t'.join(map(str,row))+'\n' for row in summary)
    if args.emit_summary: print(text,end='');return
    require((HERE/'SUMMARY.tsv').read_text()==text,'entry-level summary match')
    print('PASS pinned upstream exact census replay and 332 ordered input orbits')
    print('PASS parity-refined Ramsey recurrence and literal root-union constraints')
    print('PASS exact certificates at all 4800 labeled input cores')
    print('orbit_counts='+json.dumps(dict(sorted(orbit_counts.items())),sort_keys=True))
    print('labeled_counts='+json.dumps(dict(sorted(totals.items())),sort_keys=True))
    print(f'PASS {len(excluded)} global and {sum(row[-1] for row in summary)} anchored split exclusions')
    print(f'remaining_candidates={len(remaining)} globals, {sum(int(r["split_count"]) for r in remaining)} splits')
    print('global_M214_to_M220='+','.join(str(global_M[m]) for m in range(214,221)))
    print('split_M214_to_M220='+','.join(str(split_M[m]) for m in range(214,221)))
    print('PASS split certificate and real witness establish a genuine integrality gap')
    print(f'PASS {legacy_tests} legacy primal witnesses fail specifically a new union cut')
    print('PASS altered primal, zero dual, overlapping roots, and broken split rejected')
    print('SCOPE union-count relaxations only; 56 larger profiles unclassified; no target graph')
    print('certificate_sha256='+sha256(args.certificate.read_bytes()).hexdigest())

if __name__=='__main__': main()
