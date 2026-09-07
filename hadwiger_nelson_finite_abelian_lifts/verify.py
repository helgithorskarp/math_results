#!/usr/bin/env python3
"""Independent stdlib checker: fields, rhombus identities, exact drawing, RUP.

Does not import producer, solver, numerical geometry or a computer algebra system.
All validation uses explicit exceptions and works under python -O.
"""
import argparse
import collections
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x, lo, hi):
    return type(x) is int and lo <= x <= hi


class Ring:
    def __init__(self,p,modulus):
        self.p=p;self.m=tuple(modulus);self.d=len(modulus)-1
        self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
        self.elements=list(itertools.product(range(p),repeat=self.d))

    def decode(self,x):
        v=[]
        for _ in range(self.d):
            x,a=divmod(x,self.p);v.append(a)
        require(x==0,'field address range')
        return tuple(v)

    def plus(self,a,b):
        return tuple((x+y)%self.p for x,y in zip(a,b))

    def neg(self,a):
        return tuple(-x%self.p for x in a)

    def times(self,a,b):
        v=[0]*(2*self.d-1)
        for i in range(self.d):
            for j in range(self.d):
                v[i+j]+=a[i]*b[j]
        for k in range(2*self.d-2,self.d-1,-1):
            c=v[k]%self.p
            for j in range(self.d):
                v[k-self.d+j]-=c*self.m[j]
        return tuple(x%self.p for x in v[:self.d])

    def power(self,a,n):
        result=self.one
        for bit in bin(n)[2:]:
            result=self.times(result,result)
            if bit=='1':result=self.times(result,a)
        return result


def rhombus_identity(R,S,edges,rel):
    n=R.p**R.d
    require(type(rel) is dict and set(rel)=={'target','terms'},'relation shape')
    require(integer(rel['target'],1,n-1),'relation target type')
    s=R.decode(rel['target']);require(s in S,'relation target generator')
    require(type(rel['terms']) is list and rel['terms'],'nonempty relation')
    path=[];seen=set()
    for term in rel['terms']:
        require(type(term) is list and len(term)==2,'relation term shape')
        t,c=term
        require(integer(t,1,n-1) and integer(c,1,R.p-1),'relation term range')
        t=R.decode(t)
        require(t in S and t not in (s,R.neg(s)),'relation transverse generator')
        require(t not in seen,'duplicate relation generator');seen.add(t)
        path.extend([t]*c)
    endpoint=R.zero
    for t in path:endpoint=R.plus(endpoint,t)
    require(endpoint==s,'relation sum')
    # A literal integer combination of genuine graph four-cycle rows.
    # Sum_{k=0}^{p-2}(p-1-k)[Delta_s((k+1)s)-Delta_s(ks)]
    # equals p*(e_0-e_s). This must vanish for any injective unit drawing.
    total=collections.Counter();x=R.zero;squares=0
    for k in range(R.p-1):
        y=x;weight=R.p-1-k
        for t in path:
            ys=R.plus(y,s);yt=R.plus(y,t);yst=R.plus(ys,t)
            square=(y,ys,yst,yt)
            require(len(set(square))==4,'four distinct rhombus vertices')
            for a,b in zip(square,square[1:]+square[:1]):
                require(frozenset((a,b)) in edges,'rhombus edge')
            for v,c in ((y,1),(yst,1),(ys,-1),(yt,-1)):
                total[v]+=weight*c
            y=yt;squares+=1
        require(y==R.plus(x,s),'rhombus path endpoint')
        x=R.plus(x,s)
    total={v:c for v,c in total.items() if c}
    require(total=={R.zero:R.p,s:-R.p},'integer rhombus row certificate')
    return squares


def qadd(a,b):return a[0]+b[0],a[1]+b[1]
def qneg(a):return -a[0],-a[1]
def qmul(a,b):return a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def qscale(a,c):return a[0]*c,a[1]*c


def drawing_q3(edges):
    z=(Q(0),Q(0));one=(Q(1),Q(0))
    T=[(z,z),(one,z),((Q(1,2),Q(0)),(Q(0),Q(1,2)))]
    points={}
    for a,b in itertools.product(range(3),repeat=2):
        x,y=T[b]
        ux=qadd(qscale(x,Q(3,5)),qscale(y,Q(-4,5)))
        uy=qadd(qscale(x,Q(4,5)),qscale(y,Q(3,5)))
        points[(a,b)]=(qadd(T[a][0],ux),qadd(T[a][1],uy))
    require(len(set(points.values()))==9,'q3 drawing injective')
    pairs=0
    for a,b in itertools.combinations(points,2):
        dx=qadd(points[a][0],qneg(points[b][0]));dy=qadd(points[a][1],qneg(points[b][1]))
        norm=qadd(qmul(dx,dx),qmul(dy,dy))
        require((norm==one)==(frozenset((a,b)) in edges),'q3 full distance graph')
        if norm==one:require(sum(a)%3!=sum(b)%3,'q3 colouring')
        pairs+=1
    require(all(frozenset(((a,0),(b,0))) in edges for a,b in itertools.combinations(range(3),2)),
            'q3 triangle lower bound')
    return pairs


def four_cnf(n,edges):
    # Independently reconstructed exactly-one encoding and first-edge pins.
    V=lambda v,c:1+4*v+c
    cnf=[]
    for v in range(n):
        cnf.append([V(v,c) for c in range(4)])
        for c,d in itertools.combinations(range(4),2):
            cnf.append([-V(v,c),-V(v,d)])
    for u,v in sorted(edges):
        cnf.extend([[-V(u,c),-V(v,c)] for c in range(4)])
    u,v=min(edges);cnf.extend([[V(u,0)],[V(v,1)]])
    return cnf


def verify_rup(cnf,proof,nvars):
    db=[];occ=collections.defaultdict(list);units=[]
    def insert(c):
        i=len(db);c=tuple(set(c));db.append(c)
        for lit in c:occ[lit].append(i)
        if len(c)==1:units.append(c[0])
    for c in cnf:insert(c)
    def conflict(assumptions):
        assigned={};queue=list(units)+list(assumptions)
        while queue:
            lit=queue.pop();v=abs(lit);b=lit>0
            if v in assigned:
                if assigned[v]!=b:return True
                continue
            assigned[v]=b
            for i in occ[-lit]:
                unassigned=[];satisfied=False
                for a in db[i]:
                    av=assigned.get(abs(a))
                    if av is None:unassigned.append(a)
                    elif av==(a>0):satisfied=True;break
                if satisfied:continue
                if not unassigned:return True
                if len(unassigned)==1:queue.append(unassigned[0])
        return False
    additions=deletions=0;ended=False
    for line in proof.splitlines():
        require(not ended,'proof data after empty clause')
        tokens=line.split();require(tokens,'empty proof line')
        deletion=tokens[0]=='d'
        if deletion:tokens=tokens[1:]
        try:c=list(map(int,tokens))
        except ValueError:raise ValueError('proof syntax') from None
        require(c and c[-1]==0 and all(1<=abs(l)<=nvars for l in c[:-1]),'proof literal range')
        c=c[:-1]
        if deletion:
            # Ignoring deletions is sound for pure RUP: every addition was
            # already established as a consequence of the original clauses.
            deletions+=1;continue
        require(conflict([-a for a in c]),'addition not RUP')
        insert(c);additions+=1
        if not c:ended=True
    require(ended,'proof has no final empty clause')
    return {'rup_additions':additions,'ignored_deletions':deletions}


def verify(directory,certificate=None,proof=None,colouring=None):
    if certificate is None:certificate=json.loads((directory/'certificate.json').read_text())
    require(type(certificate) is dict and set(certificate)=={'version','limit','cases'},'certificate shape')
    require(integer(certificate['version'],1,1) and integer(certificate['limit'],508,508),'certificate version/limit')
    # Independent complete parameter enumeration by factoring all q<=floor(sqrt(508)).
    expected=[]
    for q in range(2,23):
        divisors=[p for p in range(2,q+1) if q%p==0 and all(p%d for d in range(2,p))]
        if len(divisors)==1:
            p=divisors[0];f=0;x=q
            while x%p==0:x//=p;f+=1
            require(x==1,'prime power factorization');expected.append((q,p,f))
    rows=certificate['cases'];require(type(rows) is list and len(rows)==len(expected),'complete case count')
    totals={'verified':True,'cases':len(rows),'nonrealizable':0,'field_nonzero_elements':0,
            'norm_tests':0,'pair_tests':0,'rhombus_rows':0,'q3_drawing_pairs':0}
    for row,(q,p,f) in zip(rows,expected):
        require(type(row) is dict and set(row)=={'q','p','f','modulus','generators','vertices','edges','redundancy'},'case shape')
        require(all(integer(row[k],v,v) for k,v in [('q',q),('p',p),('f',f),('vertices',q*q)]),'complete ordered parameter coverage')
        m=row['modulus'];require(type(m) is list and len(m)==2*f+1 and m[-1]==1 and all(integer(x,0,p-1) for x in m),'modulus shape')
        R=Ring(p,m)
        # Every nonzero quotient-ring element is invertible, certifying this is
        # a field independently of the producer's trial-factor irreducibility.
        for a in R.elements:
            if a!=R.zero:
                require(R.power(a,q*q-1)==R.one,'quotient is not a field')
                totals['field_nonzero_elements']+=1
        S=set()
        for a in R.elements:
            power=R.one
            for _ in range(q+1):power=R.times(power,a)
            if power==R.one:S.add(a)
            totals['norm_tests']+=1
        g=row['generators'];require(type(g) is list and all(integer(x,1,q*q-1) for x in g) and g==sorted(set(g)),'generator addresses')
        require(len(S)==q+1 and {R.decode(x) for x in g}==S,'full norm-one generator set')
        E=set();integer_edges=[]
        for x,y in itertools.combinations(range(q*q),2):
            a,b=R.decode(x),R.decode(y)
            if R.plus(a,R.neg(b)) in S:
                E.add(frozenset((a,b)));integer_edges.append((x,y))
            totals['pair_tests']+=1
        require(integer(row['edges'],len(E),len(E)) and 2*len(E)==q*q*(q+1),'full graph edge count')
        if q==3:
            require(row['redundancy'] is None,'q3 exceptional case')
            totals['q3_drawing_pairs']=drawing_q3(E)
        else:
            totals['rhombus_rows']+=rhombus_identity(R,S,E,row['redundancy'])
            totals['nonrealizable']+=1
        if q==11:
            w=colouring if colouring is not None else json.loads((directory/'q11_five_colouring.json').read_text())
            require(type(w) is list and len(w)==121 and all(integer(c,0,4) for c in w),'five-colouring shape')
            require(all(w[x]!=w[y] for x,y in integer_edges),'five-colouring edge')
            pr=proof if proof is not None else (directory/'q11_four_unsat.drat').read_text()
            totals.update(verify_rup(four_cnf(121,integer_edges),pr,484))
            totals['q11_chromatic_number']=5
    totals['record_improvement']=False
    return totals


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    args=ap.parse_args();print(json.dumps(verify(args.directory),sort_keys=True))


if __name__=='__main__':main()
