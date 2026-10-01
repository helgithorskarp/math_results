"""Independent literal reconstruction; Python standard library only."""
import argparse
import hashlib
import itertools
import json
import math
import pathlib
from fractions import Fraction

N, Q = 10080, 1680
PREFIX = ((8,0),(9,0),(10,0),(14,1),(12,10),(16,4))
JOINT = (15,32,288,1440,2016,10080)

def need(ok, message):
    if not ok:
        raise ValueError(message)

def integer(x):
    return type(x) is int

def components(actions, size):
    parent=list(range(size))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]
            a=parent[a]
        return a
    for g in actions:
        for a,b in enumerate(g):
            x,y=find(a),find(b)
            if x!=y:
                parent[max(x,y)]=min(x,y)
    buckets={}
    for a in range(size):
        buckets.setdefault(find(a),[]).append(a)
    return sorted(buckets.values(),key=lambda x:x[0])

def tree_generators():
    result=[]
    for p,exponent in [(2,5),(3,2),(5,1),(7,1)]:
        modulus=p**exponent
        constraints=[]
        for n,a in PREFIX:
            k=0
            while n%(p**(k+1))==0:
                k+=1
            if k:
                constraints.append((k,a%(p**k)))
        unit=(N//modulus)*pow(N//modulus,-1,modulus)
        for depth in range(exponent):
            step=p**depth
            for node in range(step):
                frozen={a//step%p for k,a in constraints
                        if k>depth and a%step==node}
                free=[c for c in range(p) if c not in frozen]
                for left,right in itertools.combinations(free,2):
                    action=[]
                    for x in range(N):
                        residue=x%modulus
                        digit=residue//step%p
                        move=0
                        if residue%step==node:
                            if digit==left:move=(right-left)*step
                            if digit==right:move=(left-right)*step
                        action.append((x+unit*move)%N)
                    result.append(action)
    return result

def block(y):
    q,z=y%48,y%35
    return [(q+48*j)+288*((z-q-48*j)*pow(288,-1,35)%35)
            for j in range(6)]

def local_mass(mask):
    rows=[{j%3 for j in range(6) if j%2==r and mask>>j&1}
          for r in range(2)]
    return min(2*len(rows[0]|rows[1]),3+2*len(rows[0]),
               3+2*len(rows[1]),6)

def vertex_mass(mask):
    return max(sum(1+(-1)**j*h[j%3] for j in range(6) if mask>>j&1)
               for h in itertools.permutations((-1,0,1)))

def reconstruct(cert):
    need(cert['fixture']['period']==N,'period')
    need(cert['fixture']['anchors']==[list(x) for x in PREFIX],'literal prefix')
    need(cert['coupled_resources']==list(JOINT),'joint resource identities')
    need(integer(cert['denominator']) and cert['denominator']>0,'probability denominator')
    S=cert['denominator']
    divisors=[d for d in range(1,N+1) if N%d==0]
    available=[d for d in divisors if d>=8 and d not in dict(PREFIX)]
    outside=[d for d in available if d not in JOINT]
    need(cert['fixture']['available_moduli']==available,'unused divisors')
    need(cert['beta']==[501,500] and cert['maximum_outside_group_size']==5,'target parameters')
    residual=[all(x%n!=a for n,a in PREFIX) for x in range(N)]
    need(cert['fixture']['residual_count']==sum(residual),'residual cardinality')
    need(int(cert['fixture']['residual_hex'],16)==sum(1<<x for x in range(N) if residual[x]),'residual word')
    cells=[block(y) for y in range(Q)]
    need(sorted(x for c in cells for x in c)==list(range(N)),'physical block partition')
    need(all(x%Q==y for y,c in enumerate(cells) for x in c),'periodic physical labels')
    masks=[sum(1<<j for j,x in enumerate(c) if residual[x]) for c in cells]
    masses=[local_mass(m) for m in range(64)]
    need(all(masses[m]==vertex_mass(m) for m in range(64)),'row-cover/vertex dual agreement')

    # Independent global construction from frozen paths, not author helper code.
    generators=tree_generators()
    class_actions={d:[] for d in divisors}
    grid_checks=0
    for g in generators:
        need(sorted(g)==list(range(N)),'physical bijection')
        need(all(g[g[x]]==x for x in range(N)),'involution')
        need(all((x%n==a)==(g[x]%n==a) for n,a in PREFIX for x in range(N)),
             'prescribed class preservation')
        for d in divisors:
            action=[g[a]%d for a in range(d)]
            need(sorted(action)==list(range(d)),'congruence phase bijection')
            need(all(g[x]%d==action[x%d] for x in range(N)),
                 'all physical congruence partitions')
            class_actions[d].append(action)
        qaction=[g[y]%Q for y in range(Q)]
        need(all(g[x]%Q==qaction[x%Q] for x in range(N)),'periodic reduction')
        for y,c in enumerate(cells):
            target=cells[qaction[y]]
            index={x:j for j,x in enumerate(target)}
            image=[index[g[x]] for x in c]
            need(len({(j%2,k%2) for j,k in enumerate(image)})==2,
                 'independent binary row action')
            need(len({(j%3,k%3) for j,k in enumerate(image)})==3,
                 'independent ternary column action')
            grid_checks+=1
    physical=components(generators,N)
    ordinary=[o for o in physical if residual[o[0]]]
    need(all(all(residual[x] for x in o) for o in ordinary),'residual orbit')
    periodic=components([[g[y]%Q for y in range(Q)] for g in generators],Q)
    phase_orbits={d:components(class_actions[d],d) for d in outside}
    L=math.lcm(*(len(o) for orbits in phase_orbits.values() for o in orbits))
    W=S*L
    scale=W*W
    records=cert['resource_marginals']
    need([r['resource'] for r in records]==outside,'complete distinct marginal inventory')
    credit=[0]*N
    nonzero=0
    for record in records:
        d=record['resource']
        lookup={o[0]:o for o in phase_orbits[d]}
        probability=[0]*d
        seen=set()
        for entry in record['entries']:
            a,number=entry['phase_representative'],entry['numerator']
            need(integer(a) and a in lookup and a not in seen,'phase orbit representative')
            need(integer(number) and number>=0,'nonnegative integer probability')
            o=lookup[a]
            need(entry['orbit_size']==len(o),'phase orbit size')
            for b in o:probability[b]=number*(L//len(o))
            seen.add(a)
            nonzero+=number>0
        need(sum(probability)==W,'unit resource probability')
        for x in range(N):
            m=probability[x%d]
            credit[x]+=W*m-2*m*m
    need(all(len({credit[x] for x in o})==1 for o in physical),'invariant outside credit')

    joint_u=[0]*N
    joint_v=[0]*Q
    joint_phases=[]
    need(sum(e['numerator'] for e in cert['joint_mixture'])==S,'unit joint mixture')
    for entry in cert['joint_mixture']:
        alpha=entry['numerator']
        need(integer(alpha) and alpha>=0,'joint probability')
        phases=entry['phases']
        need(len(phases['outside'])==2 and len(phases['top'])==4,'joint tuple dimension')
        decoded=[]
        for d,a in zip(JOINT[:2],phases['outside']):
            need(integer(a) and 0<=a<d,'outside actual phase')
            decoded.append((d,a))
        for wanted,triple in zip((1,5,7,35),phases['top']):
            d,t,r=triple
            need(all(integer(v) for v in triple) and d==wanted and 0<=t<288 and 0<=r<d,
                 'labelled TOP actual phase')
            a=t if d==1 else t+288*((r-t)*pow(288,-1,d)%d)
            decoded.append((288*d,a))
        hit=[any(x%d==a for d,a in decoded) for x in range(N)]
        for x in range(N):joint_u[x]+=alpha*hit[x]
        for y,c in enumerate(cells):
            remaining=sum(1<<j for j,x in enumerate(c) if residual[x] and not hit[x])
            joint_v[y]+=alpha*(masses[masks[y]]-masses[remaining])
        joint_phases.append({'numerator':alpha,'actual_phases':[list(x) for x in decoded]})

    # Uniformly transport the legal joint tuple through the finite generated
    # group. Transitivity gives coefficient averages on each orbit, without
    # enumerating group elements or making any restriction on the weights.
    multiplier=scale//S
    need(multiplier*S==scale,'integer joint scale')
    coeff=[]
    for o in ordinary:
        a=sum(credit[x]+multiplier*joint_u[x] for x in o)
        demand=len(o)
        need(500*a>=501*scale*demand,'ordinary coefficient domination')
        coeff.append(['ordinary',o[0],len(o),a,demand])
    periodic_credit=[sum(credit[x] for x in c) for c in cells]
    periodic_demand=[masses[m] for m in masks]
    for o in periodic:
        need(len({periodic_demand[y] for y in o})==1,'invariant balanced demand')
        a=sum(periodic_credit[y]+multiplier*joint_v[y] for y in o)
        demand=sum(periodic_demand[y] for y in o)
        need(500*a>=501*scale*demand,'periodic coefficient domination including zero demand')
        coeff.append(['periodic',o[0],len(o),a,demand])
    ratios=[Fraction(a,scale*d) for _,_,_,a,d in coeff if d]
    minimum=min(ratios)
    margin=min(500*a-501*scale*d for _,_,_,a,d in coeff if d)
    digest=hashlib.sha256(json.dumps(coeff,separators=(',',':')).encode()).hexdigest()
    return {'agent':'six-reviewer-2','role':'independent mathematical reviewer',
            'residual':sum(residual),'generators':len(generators),'divisors':len(divisors),
            'congruence_point_checks':len(generators)*len(divisors)*N,
            'physical_grid_actions':grid_checks,'ordinary_orbits':len(ordinary),
            'periodic_orbits':len(periodic),
            'positive_periodic_orbits':sum(sum(periodic_demand[y] for y in o)>0 for o in periodic),
            'outside_resources':len(outside),'phase_orbits':sum(map(len,phase_orbits.values())),
            'nonzero_marginal_entries':nonzero,'orbit_size_lcm':L,
            'probability_scale':W,'coefficient_scale':scale,
            'minimum_ratio':[minimum.numerator,minimum.denominator],
            'minimum_positive_margin':margin,'coefficients_sha256':digest,
            'joint_actual_phases':joint_phases,
            'ordinary_and_all_periodic_coefficients':coeff,
            'proof_scope':'fixed prefix, free20; all weights; grouping generalization needs resource incidence1 and weighted co-occurrence<=4; no covering verdict'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate',default=str(pathlib.Path(__file__).with_name('CERTIFICATE.json')))
    args=parser.parse_args()
    cert=json.loads(pathlib.Path(args.certificate).read_text())
    print(json.dumps(reconstruct(cert),sort_keys=True,indent=2))

if __name__=='__main__':main()
