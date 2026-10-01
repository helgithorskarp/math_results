"""Check the rational obstruction by literal residues and explicit digit swaps.

No solver, optimizer, or orbit-helper import. All coefficient arithmetic is
integer. Author: six-covering-3, researcher. The stabilizer mechanism is the
published six-covering-2 result7174, not an original orbit construction here.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
import json
from math import gcd, isqrt, lcm
from pathlib import Path


def need(test,message):
    if not test:raise ValueError(message)


class DSU:
    def __init__(self,n):self.parent=list(range(n))
    def root(self,x):
        while self.parent[x]!=x:
            self.parent[x]=self.parent[self.parent[x]];x=self.parent[x]
        return x
    def join(self,x,y):
        x,y=self.root(x),self.root(y)
        if x!=y:self.parent[max(x,y)]=min(x,y)
    def orbits(self):
        d=defaultdict(list)
        for x in range(len(self.parent)):d[self.root(x)].append(x)
        return list(d.values())


def p_part(n,p):
    r=1
    while n%p==0:r*=p;n//=p
    return r


def swaps(N,P):
    generators=[]
    for p in (2,3,5,7):
        power=1;pp=p_part(N,p)
        while power<pp:
            for prefix in range(power):
                visited={a//power%p for n,a in P if p_part(n,p)>power and a%power==prefix}
                free=[digit for digit in range(p) if digit not in visited]
                for a,b in combinations(free,2):generators.append((p,power,prefix,a,b))
            power*=p
    return generators


def image(x,modulus,generator):
    p,power,prefix,a,b=generator
    pp=p_part(modulus,p)
    if pp<=power or x%power!=prefix:return x
    digit=x//power%p
    new=b if digit==a else a if digit==b else digit
    target=(x%pp)+(new-digit)*power
    other=modulus//pp
    return (x+other*(((target-x)*pow(other,-1,pp))%pp))%modulus


def balanced_mass(mask):
    return max(sum(1+(1 if j%2==0 else -1)*h[j%3]
                   for j in range(6) if mask&(1<<j))
               for h in permutations((-1,0,1)))


def check(data):
    f=data['fixture'];N=f['period'];B=N//35;T=B//6;C=35;Q=T*C
    need((N,B,T,Q)==(10080,288,48,1680),'wrong assigned domain')
    P=[tuple(pair) for pair in f['anchors']]
    need(P==[(8,0),(9,0),(10,0),(14,1),(12,10),(16,1),(15,2),(32,2)],'wrong frozen prefix')
    need(len({n for n,a in P})==len(P) and all(N%n==0 and 0<=a<n for n,a in P),'invalid classes')
    need(f['minimum']==8 and min(n for n,a in P)==8,'minimum mismatch')
    residual=[all(x%n!=a for n,a in P) for x in range(N)]
    need(sum(residual)==f['residual_count']==4753,'literal support count mismatch')
    need(int(f['residual_hex'],16)==sum(int(hit)<<x for x,hit in enumerate(residual)),'literal support bitset mismatch')
    available=[n for n in range(8,N+1) if N%n==0 and n not in dict(P)]
    need(available==f['available_moduli'] and len(available)==57,'incomplete unused resources')
    tops=[B*d for d in (1,5,7,35)]
    need(tops==f['four_top_resources'] and not f['prescribed_top_phases'],'top resources not all free')
    outside=[n for n in available if n not in tops]
    known_outside=[(n,a) for n,a in P if n not in tops]
    U=[[0]*C for q in range(T)]
    for x in range(N):
        if all(x%n!=a for n,a in known_outside):U[x%T][x%C]|=1<<((x%B)//T)
    mass=[balanced_mass(mask) for mask in range(64)]
    need(all(0<=v<=6 for v in mass),'mass outside range')
    need(all(mass[a]<=mass[a|(1<<j)] for a in range(64) for j in range(6)),'mass not monotone')
    vd=[mass[U[y%T][y%C]] for y in range(Q)]
    du,dv=DSU(N),DSU(Q)
    generators=swaps(N,P)
    # Check each concrete congruence class, not just the union of known classes.
    for gen in generators:
        for x in range(N):
            y=image(x,N,gen)
            need(all((x%n==a)==(y%n==a) for n,a in P),'swap changes a prescribed class')
            du.join(x,y)
        for x in range(Q):
            y=image(x,Q,gen)
            need(vd[x]==vd[y],'swap changes primitive demand')
            dv.join(x,y)
    u_orbits=[o for o in du.orbits() if residual[o[0]]]
    v_orbits=dv.orbits()
    need(all(all(residual[x] for x in o) for o in u_orbits),'support orbit crosses known union')
    need(len(u_orbits)==data['u_orbits']==52,'u orbit count mismatch')
    need(sum(any(vd[y] for y in o) for o in v_orbits)==data['v_orbits']==52,'v orbit count mismatch')
    S=data['denominator'];beta_num,beta_den=data['beta']
    need(type(S)is int and S>0 and type(beta_num)is int and type(beta_den)is int
         and beta_num>beta_den>0,'invalid rational parameters')
    counts=Counter();top_count=0;entries=0
    cu=[0]*N;cv=[0]*Q
    for group in data['mixtures']:
        ns=group['resources'];need(all(type(n)is int for n in ns),'noninteger resource')
        need(len(set(ns))==len(ns),'repeated resource in group')
        is_top=group['kind']=='top_union'
        if is_top:
            top_count+=1;need(ns==tops and group['periodic_mode']=='delta','wrong TOP group')
        else:
            need(group['kind']=='outside' and all(n in outside for n in ns),'wrong outside group')
            counts.update(ns)
            proper=lcm(*(gcd(n,B) for n in ns))<B
            need(group['periodic_mode']==('union' if proper else 'individual_sum'),'wrong periodic group mode')
        need(sum(entry['numerator'] for entry in group['entries'])==S,'mixture load is not one')
        for entry in group['entries']:
            alpha=entry['numerator'];need(type(alpha)is int and 0<alpha<=S,'invalid numerator')
            if is_top:
                triples=entry['phases'];need(len(triples)==4,'incomplete TOP phase tuple')
                phases=[]
                for d,(dd,t,r) in zip((1,5,7,35),triples):
                    need(dd==d and type(t)is int and type(r)is int and 0<=t<B and 0<=r<d,'invalid TOP phase')
                    a=t+B*(((r-t)*pow(B,-1,d))%d) if d>1 else t
                    phases.append(a)
            else:
                phases=entry['phases'];need(len(phases)==len(ns),'outside phase count mismatch')
                need(all(type(a)is int and 0<=a<n for n,a in zip(ns,phases)),'invalid outside phase')
            H=[[0]*C for q in range(T)] if is_top else None
            for x in range(N):
                hits=sum(x%n==a for n,a in zip(ns,phases))
                cu[x]+=alpha*int(hits>0)
                if is_top:
                    if hits:H[x%T][x%C]|=1<<((x%B)//T)
                else:
                    cv[x%Q]+=alpha*(int(hits>0) if group['periodic_mode']=='union' else hits)
            if is_top:
                for y in range(Q):
                    q,z=y%T,y%C
                    cv[y]+=alpha*(mass[U[q][z]]-mass[U[q][z]&~H[q][z]])
            entries+=1
    need(top_count==1 and counts==Counter(outside),'groups do not partition every outside resource once')
    ratios=[];min_integer_margin=None
    for orbits,covered,demand in ((u_orbits,cu,[int(hit) for hit in residual]),(v_orbits,cv,vd)):
        for orbit in orbits:
            rhs=sum(covered[x] for x in orbit);lhs=sum(demand[x] for x in orbit)
            margin=beta_den*rhs-beta_num*S*lhs
            need(margin>=0,'orbit coefficient does not dominate beta demand')
            if lhs:
                ratios.append(Fraction(rhs,S*lhs))
                min_integer_margin=margin if min_integer_margin is None else min(min_integer_margin,margin)
    minimum=min(ratios)
    return {'agent':'six-covering-3','role':'researcher','status':'EXACT CHECK PASSED',
        'period':N,'minimum_modulus_exactly':8,'known_classes':len(P),'residual':sum(residual),
        'unused_resources':len(available),'outside_resources':len(outside),'groups_including_top':len(data['mixtures']),
        'phase_mixture_entries':entries,'denominator':S,'beta':[beta_num,beta_den],
        'explicit_swap_generators':len(generators),'u_orbits':len(u_orbits),
        'positive_v_orbits':sum(any(vd[y] for y in o) for o in v_orbits),
        'all_v_orbits_including_zero_demand':len(v_orbits),
        'minimum_verified_ratio':[minimum.numerator,minimum.denominator],
        'minimum_integer_margin':min_integer_margin,
        'claim':f'Displayed fixed mixed budget >={beta_num}/{beta_den} times demand for every admissible u,v',
        'scope':'No covering existence, subtree exclusion, optimality or global LCM improvement'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--out',type=Path)
    args=p.parse_args();result=check(json.loads(args.certificate.read_text()))
    if args.out:args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
