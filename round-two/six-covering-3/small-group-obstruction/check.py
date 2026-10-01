"""Literal exact check of a covering-budget barrier for every small outside grouping.

Actual author six-covering-3, researcher. Standard library only; no solver,
discovery code, imported orbit tables, tensor rows or optimizer. The explicit
swap helpers credit peer7174 and the published8857 implementation.
"""
from collections import Counter,defaultdict
from fractions import Fraction
from itertools import combinations,permutations
import argparse
import json
from math import lcm
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
        groups=defaultdict(list)
        for x in range(len(self.parent)):groups[self.root(x)].append(x)
        return list(groups.values())


def p_part(n,p):
    result=1
    while n%p==0:result*=p;n//=p
    return result


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
    p,power,prefix,a,b=generator;pp=p_part(modulus,p)
    if pp<=power or x%power!=prefix:return x
    digit=x//power%p;new=b if digit==a else a if digit==b else digit
    target=(x%pp)+(new-digit)*power;other=modulus//pp
    return (x+other*(((target-x)*pow(other,-1,pp))%pp))%modulus


def balanced_mass(mask):
    return max(sum(1+(1 if j%2==0 else -1)*h[j%3]
                   for j in range(6) if mask&(1<<j)) for h in permutations((-1,0,1)))


def check(data):
    f=data['fixture'];N,B,T,C,Q=10080,288,48,35,1680
    P=[tuple(pair) for pair in f['anchors']]
    need(f['period']==N and P==[(8,0),(9,0),(10,0),(14,1),(12,10),(16,4)],'wrong forced-six-class domain')
    need(f['minimum']==8 and len({n for n,a in P})==6,'wrong minimum or distinctness')
    need(all(type(n)is int and type(a)is int and N%n==0 and 0<=a<n for n,a in P),'invalid known phase')
    residual=[all(x%n!=a for n,a in P) for x in range(N)]
    need(sum(residual)==f['residual_count']==5408,'wrong physical residual count')
    need(int(f['residual_hex'],16)==sum(int(r)<<x for x,r in enumerate(residual)),'wrong physical support')
    available=[n for n in range(8,N+1) if N%n==0 and n not in dict(P)]
    tops=[288,1440,2016,10080];joint_ns=[15,32,*tops]
    need(available==f['available_moduli'] and len(available)==59,'incomplete available resources')
    need(f['four_top_resources']==tops and f['prescribed_top_phases'] in ({},[]),'TOP family changed')
    outside=sorted(set(available)-set(joint_ns));need(len(outside)==53,'wrong outside resource pool')
    S=data['denominator'];num,den=data['beta'];group_size=data['maximum_outside_group_size']
    need(type(S)is int and S==1000000 and (num,den)==(501,500) and group_size==5,'wrong claimed rational parameters')
    need(data['outside_credit']=='mu - (group_size-1)*mu^2/2' and data['partition_scope']=='all nonnegative group coefficients, group size at most five, each outside resource incidence exactly one',
         'wrong credit or partition convention')
    need(data['coupled_resources']==joint_ns and data['joint_periodic_mode']=='known_delta','wrong joint capacity')
    marginals=data['resource_marginals']
    need(Counter(g['resource'] for g in marginals)==Counter(outside),'missing or duplicate resource marginal')
    for group in marginals:
        n=group['resource'];entries=group['entries']
        need(type(n)is int and entries and sum(e['numerator'] for e in entries)==S,'marginal mass is not one')
        for e in entries:
            a,size,alpha=e['phase_representative'],e['orbit_size'],e['numerator']
            need(type(a)is int and 0<=a<n and type(size)is int and 1<=size<=n and type(alpha)is int and 0<alpha<=S,
                 'invalid marginal phase/size/probability')
    joint=data['joint_mixture'];need(joint and sum(e['numerator'] for e in joint)==S,'joint probability mass is not one')
    decoded=[]
    for e in joint:
        alpha=e['numerator'];a=e['phases']['outside'];triples=e['phases']['top']
        need(type(alpha)is int and 0<alpha<=S,'invalid joint probability')
        need(len(a)==2 and all(type(v)is int and 0<=v<n for n,v in zip((15,32),a)),'invalid joint outside phase')
        need(len(triples)==4,'incomplete actual TOP assignment')
        phases=list(a)
        for d,(dd,t,r) in zip((1,5,7,35),triples):
            need(dd==d and type(t)is int and type(r)is int and 0<=t<B and 0<=r<d,'invalid labelled TOP phase')
            phases.append(t+B*(((r-t)*pow(B,-1,d))%d) if d>1 else t)
        need(all(0<=a<n for n,a in zip(joint_ns,phases)),'invalid decoded actual phase')
        decoded.append((alpha,phases))
    mass=[balanced_mass(mask) for mask in range(64)]
    need(all(mass[a]<=mass[a|(1<<j)] for a in range(64) for j in range(6)),'balanced mass is not monotone')
    grid_checks=0
    for row in permutations((0,1)):
        for col in permutations((0,1,2)):
            mapping=[next(k for k in range(6) if k%2==row[j%2] and k%3==col[j%3]) for j in range(6)]
            for mask in range(64):
                target=sum(1<<mapping[j] for j in range(6) if mask&(1<<j))
                need(mass[mask]==mass[target],'balanced grid invariance fails');grid_checks+=1
    U=[[0]*C for _ in range(T)]
    for x,r in enumerate(residual):
        if r:U[x%T][x%C]|=1<<((x%B)//T)
    vd=[mass[U[y%T][y%C]] for y in range(Q)]
    du,dv=DSU(N),DSU(Q);phase_dsu={n:DSU(n) for n in outside}
    generators=swaps(N,P);divisors=[n for n in range(1,N+1) if N%n==0]
    for gen in generators:
        perm=[image(x,N,gen) for x in range(N)]
        need(len(set(perm))==N,'swap is not a bijection')
        maps={n:[perm[a]%n for a in range(n)] for n in divisors}
        for n,mapping in maps.items():
            need(len(set(mapping))==n and all(perm[x]%n==mapping[x%n] for x in range(N)),
                 'swap changes a divisor congruence partition')
            if n in phase_dsu:
                for a,b in enumerate(mapping):phase_dsu[n].join(a,b)
        blocks={}
        for x,y in enumerate(perm):
            need(all((x%n==a)==(y%n==a) for n,a in P),'swap changes a known class');du.join(x,y)
            key,target=(x%T,x%C),(y%T,y%C);j,jj=(x%B)//T,(y%B)//T
            if key not in blocks:blocks[key]=(target,{}, {})
            to,row,col=blocks[key]
            need(to==target,'primitive block split')
            need(j%2 not in row or row[j%2]==jj%2,'row action depends on column')
            need(j%3 not in col or col[j%3]==jj%3,'column action depends on row')
            row[j%2],col[j%3]=jj%2,jj%3
        need(len({v[0] for v in blocks.values()})==Q,'block action not bijective')
        for target,row,col in blocks.values():
            need(set(row.values())=={0,1} and set(col.values())=={0,1,2},'invalid grid action')
        for y in range(Q):
            z=maps[Q][y];need(vd[y]==vd[z],'periodic demand changes');dv.join(y,z)
    u_orbits=[o for o in du.orbits() if residual[o[0]]];v_orbits=dv.orbits()
    need(len(generators)==55 and len(u_orbits)==16 and len(v_orbits)==60,'wrong stabilizer quotient')
    need(sum(any(vd[y] for y in o) for o in v_orbits)==16,'wrong positive periodic quotient')
    phase_orbits={n:{o[0]:o for o in d.orbits()} for n,d in phase_dsu.items()}
    entries_count=0;L=1
    for group in marginals:
        n=group['resource'];seen=set()
        for e in group['entries']:
            a=e['phase_representative'];need(a in phase_orbits[n] and a not in seen,'invalid or duplicate canonical phase orbit')
            seen.add(a);orbit=phase_orbits[n][a]
            need(len(orbit)==e['orbit_size'],'declared marginal orbit size is false')
            L=lcm(L,len(orbit));entries_count+=1
    W=S*L;scale=2*W*W
    credits=[0]*N;quadratic=[0]*N
    for group in marginals:
        n=group['resource'];phase_credit=[0]*n;phase_square=[0]*n;probability_check=Fraction(0)
        for e in group['entries']:
            orbit=phase_orbits[n][e['phase_representative']]
            mu=e['numerator']*(L//len(orbit))
            need(0<=mu<=W,'marginal point probability exceeds one')
            value=2*W*mu-(group_size-1)*mu*mu
            for a in orbit:phase_credit[a]=value;phase_square[a]=mu*mu
            probability_check+=Fraction(e['numerator'],S)
        need(probability_check==1,'legal phase distribution does not sum to one')
        for x in range(N):credits[x]+=phase_credit[x%n];quadratic[x]+=phase_square[x%n]
    cu=credits[:];cv=[sum(credits[x] for x in range(y,N,Q)) for y in range(Q)]
    need(scale%S==0,'joint mixture scale mismatch')
    for alpha,phases in decoded:
        multiplier=(scale//S)*alpha;H=[[0]*C for _ in range(T)]
        for x in range(N):
            if any(x%n==a for n,a in zip(joint_ns,phases)):
                cu[x]+=multiplier;H[x%T][x%C]|=1<<((x%B)//T)
        for y in range(Q):
            u,h=U[y%T][y%C],H[y%T][y%C]
            cv[y]+=multiplier*(mass[u]-mass[u&~h])
    ratios=[];min_margin=None;worst=None;cardinality_ratios={k:[] for k in range(2,7)}
    vquadratic=[sum(quadratic[x] for x in range(y,N,Q)) for y in range(Q)]
    for kind,orbits,coef,dem in [('u',u_orbits,cu,[int(r) for r in residual]),('v',v_orbits,cv,vd)]:
        for orbit in orbits:
            a=sum(coef[x] for x in orbit);d=sum(dem[x] for x in orbit);margin=den*a-num*scale*d
            need(margin>=0,'small-group credit does not dominate claimed demand on an orbit')
            if d:
                ratio=Fraction(a,scale*d);ratios.append(ratio)
                q=sum((quadratic if kind=='u' else vquadratic)[x] for x in orbit)
                for k in cardinality_ratios:cardinality_ratios[k].append(Fraction(a+(group_size-k)*q,scale*d))
                min_margin=margin if min_margin is None else min(min_margin,margin)
                if worst is None or ratio<worst[0]:worst=(ratio,kind,orbit[0],len(orbit))
    minimum=min(ratios)
    return {'agent':'six-covering-3','role':'researcher','status':'EXACT INDEPENDENT LITERAL CHECK PASSED',
       'period':N,'minimum_modulus_exactly':8,'anchors':[list(pair) for pair in P],'residual':sum(residual),
       'unused_resources':len(available),'outside_resources':len(outside),'coupled_resources':joint_ns,
       'beta':[num,den],'denominator':S,'maximum_outside_group_size':group_size,
       'marginal_phase_orbit_entries':entries_count,'joint_entries':len(joint),
       'generators':len(generators),'checked_divisor_class_families':len(divisors),'balanced_grid_mask_controls':grid_checks,
       'outside_phase_orbits':sum(len(v) for v in phase_orbits.values()),'ordinary_orbits':len(u_orbits),
       'periodic_orbits':len(v_orbits),'positive_periodic_orbits':16,'clearing_orbit_lcm':L,
       'minimum_verified_ratio':[minimum.numerator,minimum.denominator],'minimum_integer_margin':min_margin,
       'worst_positive_orbit':{'kind':worst[1],'representative':worst[2],'size':worst[3]},
       'same_certificate_cardinality_credit_ratios':{str(k):[min(rs).numerator,min(rs).denominator]
            for k,rs in cardinality_ratios.items()},
       'scope':'All-weight obstruction for EVERY fractional outside grouping with size at most five, incidence one, and joint15/32/four-TOP budget; not a covering exclusion or numerical LCM bound.'}


if __name__=='__main__':
    import time,resource
    parser=argparse.ArgumentParser();parser.add_argument('certificate',type=Path,nargs='?',default=Path(__file__).with_name('certificate.json'))
    args=parser.parse_args();start=time.monotonic();result=check(json.loads(args.certificate.read_text()))
    print(json.dumps(result))
    print(json.dumps({'seconds':round(time.monotonic()-start,3),'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
