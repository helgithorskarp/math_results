#!/usr/bin/env python3
"""six-reviewer-4: independent degree98 two-root Book audit.

Border completion enumerates every 4x4 nonnegative margin-two matrix.
A written orthogonal decomposition reduces det(H) and its 21-kernel to
six dimensions. Determinants use subset expansion, ranks use minors.
Author data is an optional passive comparison, never enumeration input.
"""
from collections import Counter
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import argparse
import hashlib
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def transpose(a):
    return list(map(list,zip(*a)))

def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def identity(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def determinant(a):
    """Signed expansion over selected columns; exact integer additions/products."""
    n=len(a)
    need(all(len(row)==n and all(type(x) is int for x in row) for row in a),
         'integer square determinant input')
    dp=[0]*(1<<n);dp[0]=1
    for mask in range(1<<n):
        k=mask.bit_count()
        if k==n:
            continue
        for j in range(n):
            if not(mask>>j&1):
                sign=-1 if (mask>>(j+1)).bit_count()%2 else 1
                dp[mask|1<<j]+=sign*dp[mask]*a[k][j]
    return dp[-1]

def rank_by_minors(a):
    """Complete nonzero-minor criterion; only used on reduced 6x6 matrices."""
    n=len(a)
    for k in range(n,0,-1):
        for rows in combinations(range(n),k):
            for cols in combinations(range(n),k):
                minor=[[a[i][j] for j in cols] for i in rows]
                if determinant(minor):
                    return k
    return 0

def margins():
    """Every top-left ternary 3x3 determines its border uniquely."""
    visits=0
    matrices=[]
    for interior in product(range(3),repeat=9):
        visits+=1
        m=[list(interior[3*i:3*i+3])+[2-sum(interior[3*i:3*i+3])]
           for i in range(3)]
        last=[2-sum(m[i][j] for i in range(3)) for j in range(3)]
        last.append(2-sum(last))
        m.append(last)
        if min(x for row in m for x in row)<0 or max(x for row in m for x in row)>2:
            continue
        need(all(sum(row)==2 for row in m) and
             all(sum(m[i][j] for i in range(4))==2 for j in range(4)),
             'border margins')
        matrices.append(tuple(x for row in m for x in row))
    need(visits==3**9 and len(matrices)==len(set(matrices)), 'complete distinct border domain')
    return sorted(matrices),visits

def small_operator(flat):
    a=[[0]*8 for _ in range(8)]
    for i in range(8):
        a[i][i^1]=1
    for i in range(4):
        for j in range(4):
            a[i][4+j]=a[4+j][i]=flat[4*i+j]
    need(all(sum(row)==3 for row in a), 'weighted cross block degree three')
    basis=[[int(i==j)-int(i==3) for i in range(4)]+[0]*4 for j in range(3)]
    basis += [[0]*4+[int(i==j)-int(i==3) for i in range(4)] for j in range(3)]
    q=transpose(basis)
    aq=multiply(a,q)
    selectors=[0,1,2,4,5,6]
    t=[aq[i] for i in selectors]
    need(aq==multiply(q,t), 'complete side-zero-sum restriction')
    return a,t

def forced(flat):
    a,t=small_operator(flat)
    f=[[0]*22 for _ in range(22)]
    for i in range(8):
        for j in range(8):
            f[5+i][5+j]=a[i][j]
    for i,j in combinations(range(3),2):
        f[2+i][2+j]=f[2+j][2+i]=1
    for center in range(3):
        for leaf in range(13+3*center,16+3*center):
            f[2+center][leaf]=f[leaf][2+center]=1
    degrees=[8]*2+[9]*20
    h=[[(2*degrees[i]-17)**2+4*degrees[i] if i==j else
         4*(degrees[i]+degrees[j]-14)-4*f[i][j]
         for j in range(22)] for i in range(22)]
    need([sum(row) for row in f]==[0]*2+[5]*3+[3]*8+[1]*9,
         'full prescribed defect degrees')
    return f,h,a,t

def basis_and_blocks():
    columns=[]
    blocks=[]
    def add(vectors):
        start=len(columns);columns.extend(vectors);blocks.append((start,len(columns)))
    add([[1,-1]+[0]*20])
    leaves=[]
    for start in (13,16,19):
        for i in (0,1):
            v=[0]*22;v[start+i]=1;v[start+2]=-1;leaves.append(v)
    add(leaves)
    contrasts=[]
    for t in ((1,-1,0),(0,1,-1)):
        c=[0]*22;l=[0]*22
        for i in range(3):
            c[2+i]=t[i]
            for j in range(3):l[13+3*i+j]=t[i]
        contrasts.extend([c,l])
    add(contrasts)
    side=[]
    for first in (5,9):
        for i in range(3):
            v=[0]*22;v[first+i]=1;v[first+3]=-1;side.append(v)
    add(side)
    add([[0]*5+[1]*4+[-1]*4+[0]*9])
    add([[1]*22,[1]*2+[0]*20,[1]*2+[2]*3+[1]*8+[0]*9])
    add([[0]*2+[12]*3+[-9]*8+[4]*9])
    need(len(columns)==22, 'complete basis dimension')
    q=transpose(columns)
    gram=multiply(columns,q)
    owner={i:k for k,(lo,hi) in enumerate(blocks) for i in range(lo,hi)}
    need(all(gram[i][j]==0 for i in range(22) for j in range(22) if owner[i]!=owner[j]),
         'orthogonal invariant-subspace decomposition')
    determinants=[]
    for lo,hi in blocks:
        value=determinant([row[lo:hi] for row in gram[lo:hi]])
        need(value>0, 'full rank of every actual Gram block')
        determinants.append(value)
    k3=[[19,0,12],[-4,-1,8],[0,2,1]]
    h3=multiply(k3,k3)
    need(determinant(k3)==-419 and determinant(
        [[h3[i][j]-21*int(i==j) for j in range(3)] for i in range(3)])==64,
        'cyclic block determinant and exclusion of eigenvalue21')
    return q,blocks,determinants,h3

def action_matrix(t,h3):
    sizes=(1,6,4,6,1,3,1)
    actions=[[[25]],[[21*int(i==j) for j in range(6)] for i in range(6)],
             [[25,-12,0,0],[-4,21,0,0],[0,0,25,-12],[0,0,-4,21]],
             [[21*int(i==j)-4*t[i][j] for j in range(6)] for i in range(6)],
             [[25]],h3,[[9]]]
    out=[[0]*22 for _ in range(22)]
    offset=0
    for size,block in zip(sizes,actions):
        for i in range(size):
            for j in range(size):out[offset+i][offset+j]=block[i][j]
        offset+=size
    return out,actions[3]

def orbits(domain):
    unseen=set(domain);answer=[]
    swaps=((1,0,2,3),(0,1,3,2),(2,3,0,1))
    while unseen:
        representative=min(unseen);orbit={representative};todo=[representative]
        while todo:
            m=todo.pop()
            for p in swaps:
                for row_action in (True,False):
                    v=tuple(m[4*(p[i] if row_action else i)+(j if row_action else p[j])]
                            for i in range(4) for j in range(4))
                    need(v in unseen, 'matching-group orbit remains in its disjoint domain')
                    if v not in orbit:orbit.add(v);todo.append(v)
        unseen-=orbit;answer.append({'flat_M':list(representative),'size':len(orbit)})
    return answer

def lattice():
    # An alternative leaf basis, with a direct integer coordinate inverse.
    vectors=[]
    for start in (13,16,19):
        for pair in ((0,1),(1,2)):
            v=[0]*22;v[start+pair[0]]=1;v[start+pair[1]]=-1;vectors.append(v)
    gram=multiply(vectors,transpose(vectors))
    need(gram==[[2 if i==j else -1 if i//2==j//2 else 0 for j in range(6)]
                for i in range(6)] and determinant(gram)==27, 'full integral leaf lattice Gram')
    # In each leaf triple (x,y,z) with x+y+z=0, coefficients are (x,-z).
    for xy in product(range(-2,3),repeat=2):
        x,y=xy;z=-x-y
        need([x,-x-z,z]==[x,y,z], 'integer coordinate recovery')
    return {'rank':6,'Gram_determinant':27,'basis_type':'successive differences in each leaf triple',
            'quadratic_polynomial':[1,1,-5],'nonsquare_discriminant':21,'forced_trace':-3,
            'self_adjoint_integral_trace_parity':0}

def run(compare=None):
    domain,visits=margins()
    q,blocks,gram_dets,h3=basis_and_blocks()
    certificate=lattice()
    source=json.loads(compare.read_text()) if compare else None
    source_records={tuple(r[0]):r for r in source['records']} if source else None
    if source:
        need(set(source_records)==set(domain) and len(source['records'])==len(domain),
             'independent complete domain equals passive source domain')
    groups=orbits(domain)
    whole=hashlib.sha256();full=hashlib.sha256()
    stats=Counter();classes=Counter();square=[];ranks=Counter();det_a=Counter()
    factor=419*75*21**3*477
    for flat in domain:
        f,h,a,t=forced(flat)
        action,p6=action_matrix(t,h3)
        need(multiply(h,q)==multiply(q,action), 'all literal invariant-basis entries')
        d6=determinant(p6);need(d6>0,'positive reduced determinant')
        dh=factor**2*d6;root=isqrt(dh);is_square=root*root==dh
        need(is_square==(isqrt(d6)**2==d6), 'square factor preserves square status')
        dt=determinant(t)
        ra=rank_by_minors(t) if dt==0 else 6
        ranks[12-ra]+=1
        need(determinant(a)==-3*dt, 'constant and contrast restriction determinants')
        det_a[dt]+=1;classes[d6]+=1
        if is_square:
            need(dt!=0 and ra==6,'entire21eigenspace equals six leaf differences')
            square.append({'flat_M':list(flat),'det_reduced':d6,'det_T':dt,
                           'rank_H_minus21I':16,'trace_parity_contradiction':True})
            stats['square_forms']+=1
        else:
            need(root*root<dh<(root+1)*(root+1), 'strict nonsquare interval')
            stats['nonsquare_forms']+=1
        if source:
            r=source_records[flat]
            need(r[1]==dh and r[2]==root and r[3]==hashlib.sha256(encoded(f)).hexdigest()
                 and r[4]==hashlib.sha256(encoded(h)).hexdigest() and r[5]==is_square,
                 'all literal source determinant/root/full-matrix records')
        whole.update(encoded([flat,p6,d6,t,dt,ra,dh])+b'\n')
        full.update(encoded([flat,f,h])+b'\n')
    need(len(domain)==282 and stats['square_forms']==18 and stats['nonsquare_forms']==264
         and len(groups)==16, 'complete finite census')
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer','complete':True,
            'border_interiors_visited':visits,'forms':len(domain),**stats,'orbits':groups,
            'Gram_block_dimensions':[hi-lo for lo,hi in blocks],'Gram_block_determinants':gram_dets,
            'uniform_determinant_square_factor':factor,'uniform_kernel_formula':'nullity(H-21I)=12-rank(T)',
            'full_kernel_dimension_counts':dict(sorted(ranks.items())),
            'det_T_counts':dict(sorted(det_a.items())),
            'reduced_determinant_counts':dict(sorted(classes.items())),
            'square_forms_records':square,'square_full_kernel_dimensions':[6],
            'invariant_basis_entries_checked':282*22*22,'lattice_certificate':certificate,
            'reduced_record_stream_sha256':whole.hexdigest(),
            'full_F_H_stream_sha256':full.hexdigest(),'adjacency_survivors':0}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--compare-author',type=Path,help='optional passive source summary')
    parser.add_argument('--expected',type=Path,help='compare complete output with frozen reviewer result')
    args=parser.parse_args()
    data=(json.dumps(run(args.compare_author),indent=2,sort_keys=True)+'\n').encode()
    if args.expected:
        need(data==args.expected.read_bytes(),'full reviewer output agrees')
    print(data.decode(),end='')
