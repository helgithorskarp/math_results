"""Independent circumradius census and a shared positive colouring for36 exterior placements."""
import argparse,copy,hashlib,json,math,time
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,permutations,product
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)


# Sparse squarefree radical arithmetic. Keys are squarefree radicands.
def clean(x):
    return {r:F(v) for r,v in x.items() if v}


def plus(x, y):
    z = dict(x)
    for r,v in y.items():
        z[r] = z.get(r,F(0))+v
    return clean(z)


def neg(x):
    return {r:-v for r,v in x.items()}


def times(x, y):
    z = {}
    for r,a in x.items():
        for s,b in y.items():
            g = math.gcd(r,s)
            t = r*s//(g*g)
            z[t] = z.get(t,F(0))+g*a*b
    return clean(z)


def cadd(z, w):
    return (plus(z[0],w[0]),plus(z[1],w[1]))


def csub(z, w):
    return (plus(z[0],neg(w[0])),plus(z[1],neg(w[1])))


def cmul(z, w):
    return (plus(times(z[0],w[0]),neg(times(z[1],w[1]))),
            plus(times(z[0],w[1]),times(z[1],w[0])))


def squared(z, w):
    a,b = csub(z,w)
    return plus(times(a,a),times(b,b))


def point(a=0,b=0,c=0,d=0):
    return (clean({1:a,3:b}),clean({1:c,3:d}))


def key(z):
    return tuple(tuple(sorted(v.items())) for v in z)


def ordered(z):
    return tuple(v.get(r,F(0)) for v in z for r in (1,3,11,33))


def decode(z):
    require(len(z)==8 and all(type(v) is int for v in z),'coordinate shape')
    return tuple(clean({r:F(v,12) for r,v in zip((1,3,11,33),z[offset:offset+4])}) for offset in (0,4))


def cross(a,b):
    return plus(times(a[0],b[1]),neg(times(a[1],b[0])))


def dot(a,b):
    return plus(times(a[0],b[0]),times(a[1],b[1]))


def scale(x,t):
    return times(x,{1:F(t)})


ZERO=point()
UNIT={1:F(1)}
ROOTS=[point(a=F(c,2),d=F(s,2)) for c,s in [(2,0),(1,1),(-1,1),(-2,0),(-1,-1),(1,-1)]]
CENTRES=[ZERO,point(a=1),ROOTS[1]]


def orbit(z):
    return [cmul(z,r) for r in ROOTS]


def canonical(z):
    return min(orbit(z),key=ordered)

def finite_audit(data):
    require(data['denominator']==12,'fixed denominator')
    rho=(clean({1:F(5,6)}),clean({11:F(1,6)}))
    sigma=(clean({1:F(-1,4),33:F(-1,12)}),clean({3:F(-1,12),11:F(1,4)}))
    require([decode(x) for x in data['shifts']]==[rho,sigma],'fixed shifts')
    require(all(squared(x,ZERO)==UNIT for x in (rho,sigma)),'unit shifts')
    # Reconstruct the patch by lattice membership, independently of rim union.
    P=[]
    for a,b in product(range(-2,4),repeat=2):
        z=point(a=F(a)+F(b,2),d=F(b,2))
        if any(squared(z,d)==UNIT for d in CENTRES):P.append(z)
    P.sort(key=ordered)
    require(len(P)==12,'patch size')
    B=[p for p in P if p not in CENTRES]
    placements=[];normals={};exterior={}
    for a,b in product(range(6),repeat=2):
        W=[cadd(p,cmul(z,ROOTS[j])) for z,j in ((rho,a),(sigma,b)) for p in B]
        require(len({key(w) for w in W})==18,'distinct exterior pair')
        require(all(squared(w,d) not in ({},UNIT) for w in W for d in CENTRES),'outside X')
        ns=[canonical(csub(w,d)) for w in W for d in CENTRES]
        counts=Counter(key(n) for n in ns)
        require(sorted(counts.values())==[1]*18+[2]*18,'per-placement normal multiplicities')
        for n in ns:normals[ordered(n)]=n
        for w in W:exterior[ordered(w)]=w
        placements.append((a,b,W,counts))
    N=[normals[k] for k in sorted(normals)]
    require(len(N)==36 and [decode(x) for x in data['normal_representatives']]==N,'normal representative census')
    require(len(exterior)==108,'global exterior union')
    directions=[decode(x) for x in data['directions']]
    require(directions==sorted(directions,key=ordered),'direction order')
    require(len({key(canonical(z)) for z in directions})==len(directions),'distinct direction orbits')
    require(all(canonical(z)==z and squared(z,ZERO)==UNIT for z in directions),'canonical unit directions')
    require(directions==[point(a=-1),cmul(rho,point(a=-1)),sigma],'only three direction orbits')
    witness={tuple(row[:3]):row[3:] for row in data['unit_rows']}
    require(len(witness)==len(data['unit_rows']),'unique census witnesses')
    outcomes=Counter();hits=[];used=set()
    # Independent unit-circumradius criterion, with no field inversion:
    # |a|² |b|² |a-b|² = 4 det(a,b)², for nonparallel a,b.
    for i,j in combinations_with_replacement(range(len(N)),2):
        a=N[i];A=squared(a,ZERO)
        for k,r in enumerate(ROOTS):
            b=cmul(N[j],r);Bnorm=squared(b,ZERO);delta=cross(a,b);case=(i,j,k)
            if not delta:
                outcomes['identical' if a==b else 'parallel_incompatible']+=1
                require(case not in witness,'spurious parallel witness')
                continue
            if times(times(A,Bnorm),squared(a,b))!=scale(times(delta,delta),4):
                outcomes['nonunit']+=1
                require(case not in witness,'spurious unit circumcentre')
                continue
            outcomes['unit']+=1
            require(case in witness,'missing unit circumcentre')
            label,step=witness[case]
            require(type(label) is int and label in range(len(directions)) and type(step) is int and step in range(6),'solution labels')
            z=cmul(directions[label],ROOTS[step])
            require(scale(dot(z,a),2)==A and scale(dot(z,b),2)==Bnorm,'unique line-intersection witness')
            hits.append(case);used.add(label)
    require(set(hits)==set(witness) and used==set(range(len(directions))),'complete unit witnesses')
    require(sum(outcomes.values())==3996 and dict(outcomes)==data['outcomes'],'all pair outcomes')
    Q={h:[cadd(d,z) for d in CENTRES for z in orbit(u)] for h,u in enumerate(directions) if u not in ROOTS}
    require(list(Q)==[1,2],'two generic candidates')
    vertices=P+list(exterior.values())+sum(Q.values(),[])
    require(len({key(z) for z in vertices})==156,'156 distinct union vertices')
    V=sorted(vertices,key=ordered)
    require([decode(x) for x in data['vertices']]==V,'shared finite graph reconstruction')
    idx={key(z):i for i,z in enumerate(V)}
    E=[list(e) for e in combinations(range(len(V)),2) if squared(V[e[0]],V[e[1]])==UNIT]
    require(E==data['edges'] and len(E)==690,'complete shared edge list')
    adjacency=[set() for _ in V]
    for a,b in E:adjacency[a].add(b);adjacency[b].add(a)
    c=data['colouring']
    require(len(c)==156 and all(type(x) is int and x in range(4) for x in c),'shared four-colour dimensions')
    require([c[idx[key(d)]] for d in CENTRES]==[0,1,2],'prescribed centre colours')
    require(all(c[a]!=c[b] for a,b in E),'shared positive colouring')
    case_rows=[];edge_hist=Counter();cross_hist=Counter();incidence_hist=Counter();checks=0
    for a,b,W,counts in placements:
        contacts={h:sum(idx[key(q)] in adjacency[idx[key(w)]] for w in W for q in qq) for h,qq in Q.items()}
        heavy=[h for h in Q if contacts[h]>=3]
        require(heavy==[1,2],'two important components in every placement')
        ids={idx[key(z)] for z in P+W+sum((Q[h] for h in heavy),[])}
        edges=[(i,j) for i,j in E if i in ids and j in ids]
        require(len(ids)==66 and all(c[i]!=c[j] for i,j in edges),'positive complete core restriction')
        cross_count=sum(idx[key(w)] in adjacency[idx[key(v)]] for w in W[:9] for v in W[9:])
        for block in (W[:9],W[9:]):
            block_ids={idx[key(z)] for z in block}
            require(all(len(adjacency[i]&block_ids)==2 for i in block_ids),'two exterior cycles')
            seen=set();stack=[next(iter(block_ids))]
            while stack:
                v=stack.pop()
                if v in seen:continue
                seen.add(v);stack.extend((adjacency[v]&block_ids)-seen)
            require(seen==block_ids,'connected nine-cycle')
        case_rows.append({'orientation':[a,b],'normal_class_sizes':sorted(counts.values()),
                          'heavy':heavy,'incidences':[contacts[h] for h in heavy],
                          'vertices':len(ids),'edges':len(edges),'cross_edges':cross_count})
        edge_hist[len(edges)]+=1;cross_hist[cross_count]+=1;incidence_hist[tuple(contacts[h] for h in heavy)]+=1
        checks+=len(edges)
    require(case_rows==data['cases'] and len(case_rows)==36,'all36 case rows')
    return {'placements':36,'exterior_points_per_placement':18,'normal_classes_per_placement':36,
            'maximum_normal_multiplicity_per_placement':2,'shared_normal_classes':36,
            'pair_rotation_cases':3996,'pair_outcomes':dict(outcomes),'unit_circumcentre_witnesses':len(hits),
            'candidate_direction_orbits':3,'important_components_per_placement':2,
            'core_vertices_per_placement':66,'core_edge_histogram':{str(k):v for k,v in sorted(edge_hist.items())},
            'cross_cycle_edge_histogram':{str(k):v for k,v in sorted(cross_hist.items())},
            'incidence_histogram':{','.join(map(str,k)):v for k,v in sorted(incidence_hist.items())},
            'exterior_union_vertices':108,'shared_certificate_vertices':156,'shared_pair_norms':12090,
            'shared_unit_edges':690,'shared_colour_edge_checks':690,'restricted_core_edge_checks':checks,
            'full_infinite_graphs_four_colourable':36,'simultaneous_108_exterior_closure_claimed':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--discover',action='store_true')
    args=p.parse_args();work=Path(args.work);start=time.monotonic()
    raw=(work/'certificate.json').read_bytes()
    require(raw==(HERE/'certificate.json').read_bytes(),'published certificate bytes')
    data=json.loads(raw);report=finite_audit(data)
    mutants=[]
    b=copy.deepcopy(data);b['normal_representatives'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['unit_rows'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['cases'][0]['heavy'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['edges'].pop();mutants.append(b)
    b=copy.deepcopy(data);u,v=b['edges'][0];b['colouring'][u]=b['colouring'][v];mutants.append(b)
    rejected=0
    for bad in mutants:
        try:finite_audit(bad)
        except ValueError:rejected+=1
        else:raise ValueError('malformed certificate accepted')
    report.update(status='PASS',malformed_certificate_rejections=rejected,certificate_bytes=len(raw),
                  certificate_sha256=hashlib.sha256(raw).hexdigest(),native_solver_calls=0)
    if not args.discover:require(report==json.loads((HERE/'expected.json').read_text()),'expected result')
    (work/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (work/'timing.json').write_text(json.dumps({'seconds':time.monotonic()-start},indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
