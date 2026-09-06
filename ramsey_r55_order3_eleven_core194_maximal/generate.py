#!/usr/bin/env python3
"""Canonical local24 classification and a complete fixed-neighborhood43 test."""
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SEED = ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24/c194.edges'
SEED_SHA = '41d4c7939f74d60ff1716787923afca5349829cc90fd5c79be95f8c1e82b1178'
BITS = '100110110110110100'


def need(ok, message):
    if not ok: raise ValueError(message)


def info(path):
    return dict(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def seed():
    need(info(SEED)['sha256']==SEED_SHA,'seed identity')
    lines=SEED.read_text().splitlines();need(lines[0]=='24 156','seed header')
    return {tuple(map(int,line.split())) for line in lines[1:]}


def local():
    ids={(i,j,d):k+1 for k,(i,j,d) in enumerate((i,j,d) for i,j in combinations(range(8),2) for d in range(3))}
    def edge(a,b):
        a,b=sorted((a,b));i,s=divmod(a,3);j,t=divmod(b,3)
        return i<4 if i==j else ids[i,j,(t-s)%3]
    return ids,edge


def forbid(n,edge,sizes):
    rows=set()
    for order,color in sizes:
        for vertices in combinations(range(n),order):
            literals=set()
            for a,b in combinations(vertices,2):
                e=edge(a,b)
                if type(e)is bool:
                    if e!=color:break
                else:literals.add(-e if color else e)
            else:rows.add(tuple(sorted(literals)))
    return sorted(rows)


def columns():
    ids,_=local()
    return [[ids[i,j,d] for i in range(4) for d in range(3)] for j in range(4,8)]


def rotate(word,s):return tuple(word[3*i+(d+s)%3] for i in range(4) for d in range(3))


def phase_rows():
    bad=[w for w in product((0,1),repeat=12) if w!=min(rotate(w,s) for s in range(3))]
    return [tuple(-v if b else v for v,b in zip(c,w)) for c in columns() for w in bad]


def order_rows():
    rows=[];top=84
    for a,b in zip(columns(),columns()[1:]):
        previous=None
        for k,(x,y) in enumerate(zip(a,b)):
            rows.append(tuple(([-previous] if previous else [])+[-x,y]))
            if k==11:continue
            top+=1;q=top
            if previous:rows.append((-q,previous))
            rows.extend([(-q,-x,y),(-q,x,-y),
                tuple(([-previous] if previous else [])+[-x,-y,q]),
                tuple(([-previous] if previous else [])+[x,y,q])])
            previous=q
    return rows,top


def representatives():
    red=seed();has=lambda a,b:tuple(sorted((a,b))) in red
    ids,_=local();records={};stabilizer=0
    for p in permutations(range(4)):
        for phases in product(range(3),repeat=4):
            f=[3*p[i]+(s+phases[i])%3 for i in range(4) for s in range(3)]
            if any(has(f[3*i],f[3*j+d])!=(BITS[k]=='1') for k,(i,j,d) in enumerate((i,j,d) for i,j in combinations(range(4),2) for d in range(3))):continue
            stabilizer+=1;contacts=[]
            for j in range(4,8):
                w,s=min((tuple(int(has(f[3*i],3*j+(d+s)%3)) for i in range(4) for d in range(3)),s) for s in range(3))
                contacts.append((w,j,s))
            for w,j,s in sorted(contacts):f.extend(3*j+(d+s)%3 for d in range(3))
            word=sum(int(has(f[3*i],f[3*j+d]))<<(v-1) for (i,j,d),v in ids.items())
            h=f'{word:021x}'
            if h not in records or f<records[h]:records[h]=f
    need(stabilizer==24 and len(records)==4,'expected witness images')
    return dict(red_stabilizer=stabilizer,representatives=[dict(word=h,pullback_permutation=records[h]) for h in sorted(records)])


def local_rows():
    ids,edge=local();rows=forbid(24,edge,((5,True),(4,False)))
    core=[ids[i,j,d] for i,j in combinations(range(4),2) for d in range(3)]
    rows.extend((v if b=='1' else -v,) for v,b in zip(core,BITS))
    base=len(rows);phase=phase_rows();ordering,top=order_rows();reps=representatives()
    blockers=[tuple(-(i+1) if int(r['word'],16)>>i&1 else i+1 for i in range(84)) for r in reps['representatives']]
    return top,rows+phase+ordering+blockers,dict(base_clauses=base,phase_clauses=len(phase),order_clauses=len(ordering),blockers=len(blockers))


def full():
    red=seed();constants={};keys={}
    for a,b in combinations(range(43),2):
        if b<24:constants[a,b]=(a,b) in red
        elif a==33 or b==33:constants[a,b]=(a if b==33 else b)>=24
        elif b<33 and a//3==b//3:constants[a,b]=False
        elif b<33:
            i,s=divmod(a,3);j,t=divmod(b,3);keys[a,b]=(3*i,3*j+(t-s)%3)
        elif a<33:keys[a,b]=(3*(a//3),b)
        else:keys[a,b]=(a,b)
    ids={key:i+1 for i,key in enumerate(sorted(set(keys.values())))}
    edges=dict(constants);edges.update({e:ids[k] for e,k in keys.items()})
    return ids,lambda a,b:edges[min(a,b),max(a,b)]


def write(path,kind):
    if kind=='classification':top,rows,extra=local_rows()
    elif kind=='extension':
        ids,edge=full();top=len(ids);rows=forbid(43,edge,((5,True),(5,False)));extra={}
    else:raise ValueError('unknown formula role')
    path.write_text(f'p cnf {top} {len(rows)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in rows))
    return dict(**info(path),variables=top,clauses=len(rows),**extra)


def boundary():
    path=ROOT.parent/'ramsey_r55_order3_eleven_local_bound_propagation/boundary.json'
    need(info(path)['sha256']=='9195e8c27426bd7829814c5e085fdd03fa623753faa6153a9654219576bfedd4','prior full boundary')
    old=json.loads(path.read_text());need(old['remaining_maximal_full_branches']==[194],'sole remaining maximal branch')
    return dict(remaining_full_cores=old['remaining_full_cores'],remaining_full_classes=old['remaining_full_classes'],
        remaining_full_labeled=old['remaining_full_labeled'],cumulative_full_classes_excluded=old['cumulative_full_classes_excluded'],
        cumulative_full_labeled_excluded=old['cumulative_full_labeled_excluded'],new_whole_core_exclusions=[],
        new_maximal_branch_exclusions=[194],new_labeled_maximal_exclusions=81,remaining_maximal_full_branches=[],
        first_empty_blue_bound_at_most_three_in=old['remaining_full_cores'],target_graph=False,
        scope='Core194 maximal attachment only; whole-core boundary unchanged')
