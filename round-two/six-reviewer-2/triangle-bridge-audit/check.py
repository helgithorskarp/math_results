#!/usr/bin/env python3
"""Independent set-incidence / integer Gram / rational Euclid audit of LEMMA9878.
No producer imports, source, certificate, numerical coordinates, or external input.
"""
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import hashlib, json, sys, time

A = ((0,5,11),(0,6,11),(0,5,7),(5,9,11))
B = ((1,2,4),(2,4,8),(1,2,10),(1,10,12))
AS, BS = frozenset(sum(A,())), frozenset(sum(B,()))
FRESH = 3
J = (Q(28,39),Q(1186,1593))
WIDE = (Q(7,10),Q(3,4))
ZERO, ONE, R = (0,), (1,), (0,1)

def need(condition, message):
    if not condition: raise ValueError(message)

def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return tuple(p) if p else ZERO

def add(a,b):
    return trim(tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))))

def scale(a,s):return trim(tuple(s*x for x in a))
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    v=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):v[i+j]+=x*y
    return trim(v)

def divrem(a,b):
    need(b!=ZERO,'zero polynomial divisor')
    a=trim(tuple(Q(x) for x in a));b=trim(tuple(Q(x) for x in b))
    q=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=ZERO and len(a)>=len(b):
        k=len(a)-len(b); v=a[-1]/b[-1]; q[k]+=v
        a=sub(a,(Q(0),)*k+scale(b,v))
    return trim(q),a

def bezout(f,g):
    need(f!=ZERO or g!=ZERO,'both gaps vanish identically')
    p,q=f,g;u,v=ONE,ZERO;s,t=ZERO,ONE
    while q!=ZERO:
        d,z=divrem(p,q);p,q=q,z;u,s=s,sub(u,mul(d,s));v,t=t,sub(v,mul(d,t))
    k=Q(1)/p[-1];h=scale(p,k);u=scale(u,k);v=scale(v,k)
    need(add(mul(u,f),mul(v,g))==h,'whole Bezout identity')
    return h,u,v

def bernstein(p,band):
    a,b=band;need(a<b,'ordered band');d=len(p)-1
    power=[sum(Q(p[j])*comb(j,k)*a**(j-k)*(b-a)**k for j in range(k,d+1)) for k in range(d+1)]
    return tuple(sum(power[k]*Q(comb(i,k),comb(d,k)) for k in range(i+1)) for i in range(d+1))

def strict_sign(coeff):return all(x>0 for x in coeff) or all(x<0 for x in coeff)

def numerator(v,w):
    diag=ZERO
    for x,y in zip(v,w):diag=add(diag,mul(x,y))
    sv=ZERO;sw=ZERO
    for x in v:sv=add(sv,x)
    for x in w:sw=add(sw,x)
    return add(mul((2,-2),diag),mul(R,mul(sv,sw)))

def face(t):return tuple(sorted(t))
def edges(t):return set(combinations(face(t),2))
def boundary(patch):
    cnt=Counter(e for t in patch for e in edges(t))
    need(set(cnt.values())=={1,2},'patch edge multiplicity')
    return tuple(sorted(e for e in cnt if cnt[e]==1))
AE,BE=boundary(A),boundary(B)
AC=set().union(*(edges(t) for t in A));BC=set().union(*(edges(t) for t in B))
CORES=tuple(sorted(face(t) for t in A+B))

def adjacencies(faces):
    return tuple((i,j) for i,j in combinations(range(len(faces)),2) if len(set(faces[i])&set(faces[j]))==2)

def tree(faces):
    if len(set(faces))!=len(faces):return False
    adj=adjacencies(faces)
    if len(adj)!=len(faces)-1:return False
    seen={0}
    for _ in faces:
        for i,j in adj:
            if i in seen or j in seen:seen.update((i,j))
    return len(seen)==len(faces)

def admissible(bridges):
    fs=tuple(sorted(CORES+tuple(face(t) for t in bridges)))
    if len(set(fs))!=len(fs):return False
    for t in bridges:
        for e in edges(t):
            if set(e)<=AS and e not in AC:return False
            if set(e)<=BS and e not in BC:return False
    if max(Counter(e for t in fs for e in edges(t)).values())>2:return False
    return tree(fs)

def typed_cases():
    out={}
    for ae,be in product(AE,BE):
        for a,b in product(ae,be):
            ap=next(v for v in ae if v!=a);bp=next(v for v in be if v!=b)
            forms={
                'S':((a,ap,b),(a,b,bp)),
                'UV':((a,ap,FRESH),(a,b,FRESH),(a,b,bp)),
                'VW':((a,ap,b),(a,b,FRESH),(b,bp,FRESH)),
                'UVW':((a,ap,FRESH),(a,b,FRESH),(b,bp,FRESH)),
            }
            for kind,raw in forms.items():
                bs=tuple(sorted(face(t) for t in raw))
                need(admissible(bs),'typed placement must retain ALL adjacencies')
                need(bs not in out,'literal placement duplicate')
                out[bs]=dict(kind=kind,a_edge=ae,b_edge=be,a=a,b=b)
    need(Counter(v['kind'] for v in out.values())==Counter(dict(S=144,UV=144,VW=144,UVW=144)),'typed coverage')
    return out

def exhaustive_long():
    candidates=set();kept=set();reasons=Counter()
    for ae,be in product(AE,BE):
        for u3,w3 in product(sorted(BS|{FRESH}),sorted(AS|{FRESH})):
            u=frozenset(ae+(u3,));w=frozenset(be+(w3,))
            if len(u&w)!=1:continue
            z=next(iter(u&w))
            for otheru,otherw in product(sorted(u-{z}),sorted(w-{z})):
                v=frozenset((z,otheru,otherw))
                need(len(v)==3,'middle distinct corners')
                bs=tuple(sorted(face(t) for t in (u,v,w)))
                need(bs not in candidates,'exhaustive literal duplicate')
                candidates.add(bs)
                if admissible(bs):kept.add(bs)
                else:reasons['rejected']=reasons['rejected']+1
    need(len(candidates)==3024,'whole candidate coverage')
    need(len(kept)==432,'whole admissible coverage')
    return candidates,kept,reasons

def construct(bridges):
    fs=tuple(sorted(CORES+bridges));need(tree(fs),'full selected tree')
    vertices=set().union(*(set(t) for t in fs));need(len(vertices)==len(fs)+2,'saturated support')
    root=fs.index(face(A[0]));seen={root};queue=deque([root]);ad=adjacencies(fs)
    p={0:(ONE,ZERO,ZERO),5:(ZERO,ONE,ZERO),11:(ZERO,ZERO,ONE)}
    while queue:
        i=queue.popleft()
        for ii,jj in ad:
            if i not in (ii,jj):continue
            j=jj if i==ii else ii
            if j in seen:continue
            share=set(fs[i])&set(fs[j]);z=next(iter(set(fs[i])-share));w=next(iter(set(fs[j])-share))
            need(w not in p,'fresh child corner required by saturation')
            x,y=sorted(share)
            p[w]=tuple(sub(mul(R,add(p[x][k],p[y][k])),p[z][k]) for k in range(3))
            seen.add(j);queue.append(j)
    need(set(p)==vertices and len(seen)==len(fs),'complete BFS image')
    contacts=tuple(sorted(set().union(*(edges(t) for t in fs))))
    need(len(contacts)==(21 if len(bridges)==2 else 23),'literal patch contacts')
    for v in sorted(p):need(numerator(p[v],p[v])==(2,-1),'unit norm numerator')
    for v,w in contacts:need(numerator(p[v],p[w])==R,'entire patch contact numerator')
    f=sub(numerator(p[7],p[12]),R);g=sub(numerator(p[9],p[10]),R)
    return fs,p,contacts,f,g

def rational(x):return str(Q(x))
def packed(p):return [rational(x) for x in p]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()

def core_noncontacts():
    # Each core is independently anchored at its own named root triple.
    out=[]
    for patch,root in ((A,A[0]),(B,B[0])):
        fs=tuple(face(t) for t in patch);idx=fs.index(face(root));seen={idx};q=deque([idx])
        p={v:tuple(ONE if j==i else ZERO for j in range(3)) for i,v in enumerate(root)}
        ad=adjacencies(fs)
        while q:
            i=q.popleft()
            for aa,bb in ad:
                if i not in (aa,bb):continue
                j=bb if i==aa else aa
                if j in seen:continue
                xy=set(fs[i])&set(fs[j]);x,y=sorted(xy)
                z=next(iter(set(fs[i])-xy));w=next(iter(set(fs[j])-xy))
                need(w not in p,'core disk fresh corner')
                p[w]=tuple(sub(mul(R,add(p[x][k],p[y][k])),p[z][k]) for k in range(3))
                seen.add(j);q.append(j)
        ce=set().union(*(edges(t) for t in fs))
        need(len(seen)==4 and len(p)==6 and len(ce)==9,'entire core')
        actual=set()
        for x,y in combinations(sorted(p),2):
            gap=sub(numerator(p[x],p[y]),R)
            if (x,y) in ce:need(gap==ZERO,'core contact');actual.add((x,y))
            else:
                # The three factored forms are checked as full integer polynomial identities.
                forms=(scale(mul((-1,1),(1,1)),2),scale(mul(mul(R,(-1,1)),(2,1)),2),scale(mul(mul(mul(R,(-1,1)),(1,1)),(2,1)),2))
                need(gap in forms,'strict all-0<r<1 factored core gap')
                out.append(dict(pair=[x,y],gap=packed(gap),factor=1+forms.index(gap)))
        triangles={t for t in combinations(sorted(p),3) if edges(t)<=actual}
        need(triangles==set(fs),'no extra entirely-core triangle')
    need(len(out)==12,'complete core noncontact set')
    return out


def profiles():
    # Literal cut masks enumerate all ordered compositions, then sort into partitions.
    parts=set()
    for mask in range(1<<10):
        cuts=[0]+[i+1 for i in range(10) if mask&(1<<i)]+[11]
        parts.add(tuple(sorted(b-a for a,b in zip(cuts,cuts[1:]))))
    screen=sorted(t for t in parts if len(t)<=8)
    old=[t for t in screen if sum(x>=4 for x in t)>=2 or max(t)>=10]
    new=[t for t in screen if sum(x>=4 for x in t)>=2]
    need(len(parts)==56 and len(screen)==52 and len(old)==11 and len(new)==9,'profile sets')
    return dict(all=56,screen=52,old=[list(t) for t in old],new=[dict(e=8-len(t),sizes=list(t)) for t in new],removed=[list(t) for t in old if t not in new])

def run():
    began=time.monotonic();cases=typed_cases();candidates,kept,reasons=exhaustive_long()
    need(kept=={bs for bs in cases if len(bs)==3},'ENTIRE typed/exhaustive case sets agree')
    hset={};bindings=[];degree=Counter();image=hashlib.sha256();norms=contacts_count=grams=0;maxgap=0
    for bs,meta in sorted(cases.items()):
        need(time.monotonic()-began<55,'original 55-second primary guard')
        fs,p,ce,f,g=construct(bs);h,u,v=bezout(f,g)
        b=bernstein(h,J);need(strict_sign(b),'closed original band strict sign')
        key=digest(packed(h));hset[key]=dict(h=packed(h),bernstein_original=packed(b),bernstein_wider=packed(bernstein(h,WIDE)))
        wide=strict_sign(bernstein(h,WIDE))
        bindings.append(dict(bridges=[list(t) for t in bs],type=meta['kind'],h=key,f=packed(f),g=packed(g),u=packed(u),v=packed(v)))
        gram=[[packed(numerator(p[x],p[y])) for y in sorted(p)] for x in sorted(p)]
        image.update(canonical(dict(faces=fs,vertices=sorted(p),vectors={k:[packed(q) for q in vec] for k,vec in sorted(p.items())},contacts=ce,gram=gram,f=packed(f),g=packed(g)))+b'\n')
        norms+=len(p);contacts_count+=len(ce);grams+=len(p)**2;maxgap=max(maxgap,len(f)-1,len(g)-1);degree[len(h)-1]+=1
    need(len(hset)==38,'distinct monic witnesses')
    need(dict(sorted(degree.items()))=={1:111,2:117,3:119,4:128,5:37,6:37,7:17,8:10},'witness degree image')
    result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',target_height=9878,fresh_label=FRESH,
        method='set-based full face incidence; generic saturated-support BFS; integer Gram numerator; fresh rational Euclid Bezout; affine-power Bernstein',
        original_r_band=packed(J),wider_r_band=packed(WIDE),wider_band_pass=all(strict_sign(tuple(Q(v) for v in x['bernstein_wider'])) for x in hset.values()),
        typed_cases=dict(Counter(v['kind'] for v in cases.values())),exhaustive_candidates=len(candidates),exhaustive_kept=len(kept),candidate_set_sha256=digest(sorted(candidates)),whole_case_set_sha256=digest(sorted(cases)),
        core_faces=[list(t) for t in CORES],a_boundary=[list(e) for e in AE],b_boundary=[list(e) for e in BE],distinct_h=len(hset),h_degree_cases=dict(sorted(degree.items())),distinct_h_degree_sum=sum(len(v['h'])-1 for v in hset.values()),
        maximum_gap_degree=maxgap,maximum_h_degree=max(len(v['h'])-1 for v in hset.values()),norm_identities=norms,contact_identities=contacts_count,gram_numerators=grams,cross_gap_polynomials=2*len(cases),whole_geometry_sha256=image.hexdigest(),
        core_noncontacts=core_noncontacts(),profiles=profiles(),witnesses={k:hset[k] for k in sorted(hset)},bindings=bindings)
    result['whole_bindings_sha256']=digest(bindings)
    if '--full' not in sys.argv:
        indices={key:i for i,key in enumerate(sorted(hset))}
        result['bindings']=[[x['type'],x['bridges'],indices[x['h']]] for x in bindings]
    return result

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,separators=(',',':')))
