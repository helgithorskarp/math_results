"""Independent circumradius census, complete core audit and cycle-state controls."""
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
    require(len(z)==2 and all(len(v)==4 for v in z),'coordinate shape')
    return tuple(clean({r:F(*v) for r,v in zip((1,3,11,33),axis)}) for axis in z)


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
    rho=(clean({1:F(5,6)}),clean({11:F(1,6)}))
    require(decode(data['rho'])==rho and squared(rho,ZERO)==UNIT,'rho')
    # Lattice reconstruction differs from the producer's translated rim union.
    candidates=[]
    for a,b in product(range(-2,4),repeat=2):
        z=point(a=F(a)+F(b,2),d=F(b,2))
        if any(squared(z,d)==UNIT for d in CENTRES):candidates.append(z)
    P=sorted(candidates,key=ordered)
    require(len(P)==12 and [decode(x) for x in data['patch']]==P,'patch')
    exterior_base=[p for p in P if p not in CENTRES]
    W=[cadd(p,rho) for p in exterior_base]
    require([decode(x) for x in data['exterior']]==W,'translated exterior')
    require(len({key(w) for w in W})==9,'distinct exterior')
    normals=[csub(w,d) for w in W for d in CENTRES]
    require(all(squared(a,ZERO) not in ({},UNIT) for a in normals),'W outside X')
    classes=Counter(ordered(canonical(a)) for a in normals)
    require(sorted(classes.values())==data['constraint_classes'],'rotated normal classes')
    require(max(classes.values())==2 and len(classes)==18,'normal multiplicity bound')
    directions=[decode(row['direction']) for row in data['orbits']]
    require(directions==sorted(directions,key=ordered),'orbit order')
    require(len({ordered(canonical(u)) for u in directions})==len(directions),'distinct orbits')
    require(all(canonical(u)==u and squared(u,ZERO)==UNIT for u in directions),'unit canonical directions')
    # Determine all possible nonparallel coincidences without field division.
    # The unit-circumradius identity is A*B*C=4*det(a,b)^2.
    witness={tuple(row[:3]):row[3:] for row in data['unit_rows']}
    require(len(witness)==len(data['unit_rows']),'unique positive pair rows')
    outcomes=Counter();hits=[];used=set()
    for i,j in combinations_with_replacement(range(27),2):
        a=normals[i];A=squared(a,ZERO)
        for step,r in enumerate(ROOTS):
            b=cmul(normals[j],r);B=squared(b,ZERO);delta=cross(a,b)
            case=(i,j,step)
            if not delta:
                outcomes['identical' if a==b else 'parallel_incompatible']+=1
                require(case not in witness,'spurious parallel solution')
                continue
            C=squared(a,b)
            if times(times(A,B),C)!=scale(times(delta,delta),4):
                outcomes['nonunit_circumcentre']+=1
                require(case not in witness,'spurious circumradius solution')
                continue
            outcomes['unit_circumcentre']+=1
            require(case in witness,'missing unit circumcentre')
            index,jj=witness[case]
            require(type(index) is int and index in range(len(directions)) and jj in range(6),'solution labels')
            z=cmul(directions[index],ROOTS[jj])
            require(scale(dot(z,a),2)==A and scale(dot(z,b),2)==B,'unique circumcentre witness')
            hits.append(case);used.add(index)
    require(sum(outcomes.values())==2268 and dict(outcomes)==data['outcomes'],'complete pair outcomes')
    require(set(hits)==set(witness) and used==set(range(len(directions))),'all solutions accounted for')
    heavy=[];contact_counts=[]
    for index,(u,row) in enumerate(zip(directions,data['orbits'])):
        special=u in ROOTS
        require(row['exceptional']==special,'exceptional classification')
        if special:continue
        Q=[cadd(d,z) for d in CENTRES for z in orbit(u)]
        require(len({key(z) for z in Q})==18,'generic component distinctness')
        contacts=[[i,j] for i,w in enumerate(W) for j,z in enumerate(Q) if squared(w,z)==UNIT]
        require(contacts==row['contacts'],'complete orbit/exterior incidences')
        contact_counts.append(len(contacts))
        if len(contacts)>=3:heavy.append(index)
    require(heavy==data['heavy_orbit_indices'],'all important components')
    V=P+W+[cadd(d,z) for index in heavy for d in CENTRES for z in orbit(directions[index])]
    require([decode(x) for x in data['vertices']]==V and len({key(z) for z in V})==len(V),'whole core reconstruction')
    E=[list(e) for e in combinations(range(len(V)),2) if squared(V[e[0]],V[e[1]])==UNIT]
    require(E==data['edges'],'complete core edge list')
    require(data['centres']==[V.index(d) for d in CENTRES],'centre labels')
    row=data['colouring']
    require(len(row)==len(V) and all(type(v) is int and v in range(4) for v in row),'four-colour dimensions')
    require([row[v] for v in data['centres']]==[0,1,2],'pinned centres')
    require(all(row[a]!=row[b] for a,b in E),'positive core colouring')
    permutation_checks=0
    for perm in permutations(range(4)):
        c=[perm[x] for x in row]
        require(all(c[a]!=c[b] for a,b in E),'renamed positive colouring')
        permutation_checks+=len(E)
    # Check that the geometric kernel has the inherited component structure.
    for h in range(len(heavy)):
        start=21+18*h
        internal={tuple(e) for e in E if start<=e[0]<e[1]<start+18}
        predicted=set()
        for i,j in product(range(3),range(6)):
            x=start+6*i+j
            predicted.add(tuple(sorted((x,start+6*i+(j+1)%6))))
            for k in range(i+1,3):predicted.add((x,start+6*k+j))
        require(internal==predicted,'generic Cartesian edges')
        for i,j in product(range(3),range(6)):
            x=start+6*i+j
            require([c for c,d in enumerate(CENTRES) if squared(V[x],d)==UNIT]==[i],'owner centre')
    patchcol=[]
    for x,y in P:
        b=2*y.get(3,F(0));a=x.get(1,F(0))-b/2
        require(a.denominator==b.denominator==1,'patch lattice recovery')
        patchcol.append(int(a+2*b)%3)
    three=[]
    for phases in product((1,-1),repeat=len(heavy)):
        c=patchcol+[None]*9+[(i+ph*(-1)**j)%3 for ph in phases for i in range(3) for j in range(6)]
        require(all(c[a]!=c[b] for a,b in E if c[a] is not None and c[b] is not None),'pinned shell three-colouring')
        masks=[]
        for w in range(12,21):
            seen={c[b if a==w else a] for a,b in E if w in (a,b) and c[b if a==w else a] is not None}
            masks.append([i for i in range(3) if i not in seen])
        empty=[i for i,m in enumerate(masks) if not m]
        require(empty,'three-colour contradiction')
        three.append({'phases':list(phases),'lists':masks,'empty_exterior_index':empty[0]})
    require(three==data['three_colour_obstructions'],'all inherited three-colour states refuted')
    return {'pair_rotation_cases':2268,'pair_outcomes':dict(outcomes),'unit_circumcentre_witnesses':len(hits),
            'normal_orbit_classes':len(classes),'maximum_normal_class_size':2,'candidate_direction_orbits':len(directions),
            'important_components':len(heavy),'important_component_exterior_incidences':contact_counts,
            'core_vertices':len(V),'core_pair_norms':len(V)*(len(V)-1)//2,'core_unit_edges':len(E),
            'four_colouring_edge_checks':len(E),'renamed_four_colouring_edge_checks':permutation_checks,
            'three_colour_shell_states_refuted':len(three),'whole_infinite_construction_chromatic_number':4}


STATES=[p for p in permutations(range(4),3) if all(p[i]!=i for i in range(3))]
COMPAT=[[all(a[i]!=b[i] for i in range(3)) for b in STATES] for a in STATES]


def cycle_oracle(forbidden):
    masks=[set(range(4))-{i} for i in range(3) for _ in range(6)]
    for v,c in forbidden:masks[v].discard(c)
    allowed=[[s for s,p in enumerate(STATES) if all(p[i] in masks[6*i+j] for i in range(3))] for j in range(6)]
    for start in allowed[0]:
        paths={start:[start]}
        for j in range(1,6):
            new={}
            for t in allowed[j]:
                for prev,path in paths.items():
                    if COMPAT[prev][t]:new[t]=path+[t];break
            paths=new
        for last,path in paths.items():
            if COMPAT[last][start]:return [STATES[path[j]][i] for i in range(3) for j in range(6)]
    return None


def repair(forbidden):
    for sign in (1,-1):
        row=[(i+sign*(-1)**j)%3 for i in range(3) for j in range(6)]
        bad={v for v,c in forbidden if row[v]==c}
        if not bad:return row
        if len(bad)==1:
            v=next(iter(bad))
            if (v,3) not in forbidden:
                row[v]=3
                return row
    raise ValueError('two-incidence repair failed')


def interface_controls():
    require(len(STATES)==11,'eleven column states')
    edges=[]
    for i,j in product(range(3),range(6)):
        edges.append((6*i+j,6*i+(j+1)%6))
        for k in range(i+1,3):edges.append((6*i+j,6*k+j))
    events=list(product(range(18),range(4)))
    cases=[()]+[(e,) for e in events]+list(combinations_with_replacement(events,2))
    stream=hashlib.sha256()
    for constraints in cases:
        for row in (repair(constraints),cycle_oracle(constraints)):
            require(row is not None and all(row[6*i+j]!=i for i in range(3) for j in range(6)),'centre extension')
            require(all(row[a]!=row[b] for a,b in edges),'interface edge')
            require(all(row[v]!=c for v,c in constraints),'interface restriction')
        stream.update((''.join(map(str,repair(constraints)))+'\n').encode())
    require(cycle_oracle([(0,1),(0,2),(0,3)]) is None,'empty-list blocking control')
    require(cycle_oracle([(0,1),(0,2),(6,0),(6,2)]) is None,'adjacent fourth-colour singleton control')
    return {'column_states':len(STATES),'compatible_ordered_state_pairs':sum(map(sum,COMPAT)),
            'two_incidence_cases':len(cases),'repair_and_oracle_positive_checks':2*len(cases),
            'repair_stream_sha256':stream.hexdigest(),'blocking_controls':2}


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--discover',action='store_true')
    args=p.parse_args();work=Path(args.work);start=time.monotonic()
    raw=(work/'certificate.json').read_bytes()
    require(raw==(HERE/'certificate.json').read_bytes(),'published certificate bytes')
    data=json.loads(raw)
    report=finite_audit(data);report.update(interface_controls())
    mutants=[]
    b=copy.deepcopy(data);b['constraint_classes'].append(1);mutants.append(b)
    b=copy.deepcopy(data);b['unit_rows'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['heavy_orbit_indices'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['edges'].pop();mutants.append(b)
    b=copy.deepcopy(data);b['colouring'][0]=b['colouring'][1];mutants.append(b)
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
