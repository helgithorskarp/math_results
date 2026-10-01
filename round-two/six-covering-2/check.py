"""Literal exact replay of complete conditional covering-exclusion trees.

No solver, discovery orbit constructor, or reported capacity is trusted.
Python >= 3.10, standard library only. See proof.md for the reduction.
"""
import argparse
from collections import Counter
from hashlib import sha256
from functools import lru_cache
import json
from math import gcd, isqrt
from pathlib import Path


def divisors(n):
    result=set()
    for d in range(1,isqrt(n)+1):
        if n%d==0:result.update((d,n//d))
    return sorted(result)


def axes(n):
    result=[];p=2
    while p*p<=n:
        if n%p==0:
            power=1
            while n%p==0:n//=p;power*=p
            result.append((p,power))
        p+=1
    if n>1:result.append((n,n))
    return result


def axis_part(m,p):
    q=1
    while m%p==0:m//=p;q*=p
    return q


def coordinate_transport(p,P,A,m,a,b):
    """Construct and check a literal rooted-tree permutation for one axis."""
    maps={}
    constraints=[(axis_part(n,p),c,c) for n,c in A]
    constraints.append((axis_part(m,p),a,b))
    for q,s,t in constraints:
        power=1
        while power<q:
            table=maps.setdefault((power,s%power),{})
            left=s//power%p;right=t//power%p
            if left in table and table[left]!=right:return None
            if right in table.values() and table.get(left)!=right:return None
            table[left]=right;power*=p
    for table in maps.values():
        unused_left=[c for c in range(p) if c not in table]
        unused_right=[c for c in range(p) if c not in table.values()]
        table.update(zip(unused_left,unused_right))
    perm=[]
    for x in range(P):
        power=1;y=0
        while power<P:
            digit=x//power%p;table=maps.get((power,x%power))
            y+=(table[digit] if table is not None else digit)*power;power*=p
        perm.append(y)
    if set(perm)!=set(range(P)):return None
    q=p
    while q<=P:
        images={r:set() for r in range(q)}
        for x,y in enumerate(perm):images[x%q].add(y%q)
        if any(len(v)!=1 for v in images.values()):return None
        if len({next(iter(v)) for v in images.values()})!=q:return None
        q*=p
    for q,s,t in constraints:
        if any((x%q==s%q)!=(perm[x]%q==t%q) for x in range(P)):return None
    return perm


def transport(L,A,m,a,b):
    result=[]
    for p,P in axes(L):
        perm=coordinate_transport(p,P,A,m,a,b)
        if perm is None:return None
        result.append(perm)
    return result


@lru_cache(maxsize=512)
def literal_mask_points(L,P,mask):
    return frozenset(x for x in range(L) if mask>>(x%P)&1)


def decode(L,boxes,U):
    periods=[P for p,P in axes(L)];W=[0]*L
    for box in boxes:
        if len(box)!=len(periods)+1 or type(box[-1]) is not int or box[-1]<=0:
            raise ValueError('Malformed positive integer weight')
        if any(type(mask) is not int or not 0<mask<1<<P for mask,P in zip(box[:-1],periods)):
            raise ValueError('Malformed coordinate mask')
        sets=[literal_mask_points(L,P,mask) for mask,P in zip(box[:-1],periods)]
        ordered=sorted(sets,key=len);points=set(ordered[0])
        for other in ordered[1:]:points.intersection_update(other)
        for x in points:
            if W[x] or x not in U:raise ValueError('Overlapping or covered weight')
            W[x]=box[-1]
    if not any(W):raise ValueError('Zero weight')
    return W


def capacities(W,B,pairs2):
    """All actual progressions and every selected phase-pair union."""
    singles={m:max(sum(W[a::m]) for a in range(m)) for m in B}
    degree=Counter();joint=[];digest=sha256();phase_pairs=0
    for edge,coef in pairs2:
        if len(edge)!=2 or edge[0]>=edge[1] or any(m not in B for m in edge):
            raise ValueError('Invalid paired resources')
        if type(coef) is not int or coef not in (1,2):raise ValueError('Invalid half coefficient')
        m,n=edge;degree[m]+=coef;degree[n]+=coef
        if degree[m]>2 or degree[n]>2:raise ValueError('Resource overcharge')
        largest=0
        for a in range(m):
            left=sum(W[a::m])
            for b in range(n):
                value=left+sum(W[x] for x in range(b,len(W),n) if x%m!=a)
                largest=max(largest,value);phase_pairs+=1
                digest.update(f'{value},'.encode())
        joint.append([m,n,coef,largest])
    cap2=sum((2-degree[m])*singles[m] for m in B)+sum(c*v for m,n,c,v in joint)
    return cap2,2*sum(singles.values()),joint,digest.hexdigest(),phase_pairs


def check_tree(tree):
    if not tree.get('complete'):raise ValueError('An incomplete search is not a certificate')
    L=tree['L'];minimum=tree['minimum'];A=tuple(tuple(v) for v in tree['root_anchors'])
    if type(L) is not int or L<1 or type(minimum) is not int or minimum<2:raise ValueError('Invalid period or minimum')
    if len(dict(A))!=len(A) or any(m<minimum or L%m or not 0<=a<m for m,a in A):raise ValueError('Invalid root classes')
    D=[m for m in divisors(L) if m>=minimum];nodes=tree['nodes'];vectors=tree['vectors']
    visited=set();used_vectors=set();events=[];counts=Counter();raw_phases=positive_phases=pair_phases=0
    permutation_digest=sha256();pair_digest=sha256()

    def visit(i,A,U):
        nonlocal raw_phases,positive_phases,pair_phases
        if type(i) is not int or not 0<=i<len(nodes) or i in visited:raise ValueError('Missing, cyclic or shared proof node')
        visited.add(i)
        if not U:raise ValueError('A covering prefix cannot be excluded')
        node=nodes[i];B=[m for m in D if m not in dict(A)]
        kind=node.get('type')
        if kind=='branch':
            m=node['modulus'];children=node['children']
            if node.get('complete') is not True or m not in B or not children:raise ValueError('Incomplete or invalid branch')
            if any(len(c)!=2 or type(c[0]) is not int or not 0<=c[0]<m for c in children):raise ValueError('Malformed branch phase')
            if len({c[0] for c in children})!=len(children):raise ValueError('Duplicate branch phase')
            representatives=[a for a,j in children]
            if any(not any(x%m==a for x in U) for a in representatives):raise ValueError('Zero-gain child')
            for a in range(m):
                raw_phases+=1
                if not any(x%m==a for x in U):continue
                positive_phases+=1
                for b in representatives:
                    perm=transport(L,A,m,a,b)
                    if perm is not None:
                        permutation_digest.update(json.dumps([i,a,b,perm],separators=(',',':')).encode());break
                else:raise ValueError('Unrepresented actual positive-gain phase')
            counts['expanded']+=1;events.append([i,'branch',m,representatives])
            for a,j in children:visit(j,A+((m,a),),{x for x in U if x%m!=a})
        elif kind=='uniform':
            W=[int(x in U) for x in range(L)];demand=len(U);capacity=sum(max(sum(W[a::m]) for a in range(m)) for m in B)
            if demand<=capacity:raise ValueError('False or nonstrict uniform exclusion')
            if (demand,capacity)!=(node['demand'],node['capacity']):raise ValueError('Uniform total mismatch')
            counts['uniform']+=1;events.append([i,'uniform',demand,capacity])
        elif kind=='weighted':
            v=node['vector']
            if type(v) is not int or not 0<=v<len(vectors) or v in used_vectors:raise ValueError('Invalid or reused vector')
            used_vectors.add(v);data=vectors[v]
            if (data['L'],data['minimum'],tuple(tuple(t) for t in data['anchors']))!=(L,minimum,A):raise ValueError('Weight prefix mismatch')
            W=decode(L,data['boxes'],U);demand2=2*sum(W)
            cap2,single2,joint,pd,npairs=capacities(W,B,data['pairs2']);pair_phases+=npairs
            pair_digest.update(pd.encode())
            if demand2<=cap2 or demand2-cap2!=data['gap2']:raise ValueError('False, nonstrict or mismatched weighted exclusion')
            label='fractional' if any(c==1 for e,c in data['pairs2']) else ('paired' if data['pairs2'] else 'single')
            counts[label]+=1;events.append([i,label,demand2,cap2,single2,joint])
        else:raise ValueError('Open or unknown proof node')

    U={x for x in range(L) if all(x%m!=a for m,a in A)}
    visit(0,A,U)
    if visited!=set(range(len(nodes))) or used_vectors!=set(range(len(vectors))):raise ValueError('Unused proof evidence')
    return {'period':L,'root':A,'nodes':len(nodes),'vectors':len(vectors),'boxes':sum(len(v['boxes']) for v in vectors),
            'cuts':dict(counts),'raw_branch_phases':raw_phases,'positive_transports':positive_phases,'pair_phase_entries':pair_phases,
            'events_sha256':sha256(json.dumps(events,separators=(',',':')).encode()).hexdigest(),
            'permutations_sha256':permutation_digest.hexdigest(),'pair_tables_sha256':pair_digest.hexdigest()}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('certificate',type=Path)
    ap.add_argument('--expected',type=Path);args=ap.parse_args()
    result=check_tree(json.loads(args.certificate.read_text()))
    # JSON normalization converts tuple-valued mathematical data to reader-visible lists.
    result=json.loads(json.dumps(result))
    if args.expected and result!=json.loads(args.expected.read_text()):raise ValueError('Manifest mismatch')
    print(json.dumps(result,sort_keys=True))
