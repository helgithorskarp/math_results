#!/usr/bin/env python3
"""Exact bounded-depth hat profile obstruction. Standard library only.

six-heesch-3, researcher, 2026-10-01. No upstream code or solver imports.
"""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNIT = ((-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0))
IDENTITY = (1,0,0,0,1,0)

def require(ok, message):
    if not ok: raise ValueError(message)
def add(p,q): return p[0]+q[0],p[1]+q[1]
def sub(p,q): return p[0]-q[0],p[1]-q[1]
def cross(p,q): return p[0]*q[1]-p[1]*q[0]
def point(m,p): return m[0]*p[0]+m[1]*p[1]+m[2],m[3]*p[0]+m[4]*p[1]+m[5]
def compose(m,n):
    a,b,c,d,e,f=m;g,h,i,j,k,l=n
    return a*g+b*j,a*h+b*k,a*i+b*l+c,d*g+e*j,d*h+e*k,d*i+e*l+f
def digest(value): return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
def centre_lattice(p): return p[1]%2==0 and (p[0]-p[1])%6==0
def cell_direction(p):
    choices=[v for v in UNIT if centre_lattice(sub(p,v))]
    require(len(choices)==1,'invalid kite cell label')
    return choices[0]
def is_cell(p): return sum(centre_lattice(sub(p,v)) for v in UNIT)==1
def face(p):
    v=cell_direction(p);c=sub(p,v)
    left=(-v[1],v[0]+v[1]);right=(v[0]+v[1],-v[0])
    return c,add(p,right),add(p,v),add(p,left)
def oriented_edges(poly):
    return [(a,poly[(i+1)%len(poly)]) for i,a in enumerate(poly)]

def cell_neighbour_tables():
    """Derive the stars from actual face vertices, with a finite distance bound."""
    vertex={};edge={}
    for p in UNIT:
        pv=set(face(p));pe={tuple(sorted(e)) for e in oriented_edges(face(p))}
        vv=set();ee=set()
        # Every face vertex has Euclidean distance 1 from its cell label.
        # Thus cells sharing a vertex have centre distance <=2, so both
        # integer axial coordinate differences have absolute value <=2.
        for dx in range(-3,4):
            for dy in range(-3,4):
                q=add(p,(dx,dy))
                if q==p or not is_cell(q):continue
                qv=set(face(q));qe={tuple(sorted(e)) for e in oriented_edges(face(q))}
                if pv&qv:vv.add((dx,dy))
                if pe&qe:ee.add((dx,dy))
        require(len(vv)==9 and len(ee)==4,'kite star cardinalities')
        vertex[p]=frozenset(vv);edge[p]=frozenset(ee)
    return vertex,edge

VERTEX_STAR,EDGE_STAR=cell_neighbour_tables()
def neighbours(p,edges_only=False):
    table=EDGE_STAR if edges_only else VERTEX_STAR
    return {add(p,v) for v in table[cell_direction(p)]}
def halo(cells): return set().union(*(neighbours(p) for p in cells))-set(cells)
def orientations():
    result=[]
    for a,d in UNIT:
        for b,e in UNIT:
            if 2*a*b+a*e+d*b+2*d*e==1:result.append((a,b,0,d,e,0))
    require(len(result)==12,'orientation cardinality')
    return sorted(result)

def validate_model(data):
    cells=frozenset(tuple(p) for p in data['cells'])
    vertices=tuple(tuple(p) for p in data['vertices'])
    require(len(cells)==8 and len(vertices)==14,'hat cardinalities')
    require(all(len(p)==2 and all(type(x)is int for x in p) for p in cells|set(vertices)),
            'integer input coordinates')
    boundary=Counter()
    for p in cells:
        polygon=face(p)
        require(sum(cross(a,b) for a,b in oriented_edges(polygon))==4,'kite area')
        for a,b in oriented_edges(polygon):
            if boundary[b,a]:boundary[b,a]-=1
            else:boundary[a,b]+=1
    boundary=Counter({e:n for e,n in boundary.items() if n})
    require(boundary==Counter(oriented_edges(vertices)),'cell decomposition does not give ports')
    require(sum(cross(a,b) for a,b in oriented_edges(vertices))==32,'hat area')
    require(sorted((sub(b,a)[0]**2+sub(b,a)[0]*sub(b,a)[1]+sub(b,a)[1]**2)
                   for a,b in oriented_edges(vertices))==[1]*8+[3]*6,'port lengths')
    for m in orientations():
        require(all(centre_lattice(point(m,p)) for p in ((0,0),(6,0),(2,2))),
                'orientation does not preserve centre lattice')
        require(all(is_cell(point(m,p)) for p in cells),'orientation does not preserve cell labels')
    return cells,vertices

def placements_at_targets(cells,targets,occupied):
    """All aligned hats meeting targets, by every cell-to-target alignment."""
    result={}
    for m in orientations():
        rotated={point(m,p) for p in cells}
        for p in rotated:
            for q in targets:
                t=sub(q,p)
                if not centre_lattice(t):continue
                shifted=frozenset(add(x,t) for x in rotated)
                if shifted&occupied:continue
                a,b,_,d,e,_=m;result[(a,b,t[0],d,e,t[1])]=shifted
    return dict(sorted(result.items()))

def boxed_neighbours(cells,targets):
    """Control: broad translation boxes; no cell-to-target anchor generation."""
    result={}
    for m in orientations():
        rotated={point(m,p) for p in cells}
        lows=[min(q[k] for q in targets)-max(p[k] for p in rotated) for k in (0,1)]
        highs=[max(q[k] for q in targets)-min(p[k] for p in rotated) for k in (0,1)]
        for x in range(lows[0],highs[0]+1):
            for y in range(lows[1],highs[1]+1):
                if not centre_lattice((x,y)):continue
                shifted=frozenset(add(p,(x,y)) for p in rotated)
                if shifted&cells or not shifted&targets:continue
                a,b,_,d,e,_=m;result[(a,b,x,d,e,y)]=shifted
    return dict(sorted(result.items()))

def transported_candidates(cells,patch,relative):
    occupied=set().union(*({point(t,p) for p in cells} for t in patch));result={}
    for t in patch:
        for n in relative:
            m=compose(t,n);shifted=frozenset(point(m,p) for p in cells)
            if not shifted&occupied:result[m]=shifted
    return occupied,dict(sorted(result.items()))

def covers_bit(candidates,targets,occupied):
    """MRV exact cover; collisions checked on full tile footprints."""
    poses=list(candidates);universe=sorted(set(occupied)|set(targets)|set().union(*candidates.values()))
    index={p:i for i,p in enumerate(universe)}
    def mask(s):return sum(1<<index[p] for p in s)
    masks=[mask(candidates[t]) for t in poses];goal=mask(targets)
    users={index[p]:[i for i,m in enumerate(masks) if m&(1<<index[p])] for p in targets}
    answers=[];nodes=0
    def visit(taken,chosen):
        nonlocal nodes
        nodes+=1;remaining=goal&~taken
        if not remaining:answers.append(tuple(sorted(poses[i] for i in chosen)));return
        choices=None
        while remaining:
            bit=remaining&-remaining;k=bit.bit_length()-1;remaining-=bit
            allowed=[i for i in users[k] if not masks[i]&taken]
            if not allowed:return
            if choices is None or len(allowed)<len(choices):choices=allowed
        for i in choices:visit(taken|masks[i],chosen+(i,))
    visit(mask(occupied),())
    require(len(answers)==len(set(answers)),'duplicate bit cover')
    return sorted(answers),nodes

def covers_sets(candidates,targets,occupied):
    """Independent control: sets, reverse fixed cell order, no MRV."""
    users={p:[t for t,c in candidates.items() if p in c] for p in targets}
    target_order=sorted(targets,reverse=True);answers=[];nodes=0
    def visit(taken,chosen):
        nonlocal nodes
        nodes+=1;missing=[p for p in target_order if p not in taken]
        if not missing:answers.append(tuple(sorted(chosen)));return
        # Sound dead-cell prune only; no topology or profile pruning.
        if any(not any(candidates[t].isdisjoint(taken) for t in users[p]) for p in missing):return
        for t in reversed(users[missing[0]]):
            if candidates[t].isdisjoint(taken):visit(taken|candidates[t],chosen+(t,))
    visit(set(occupied),())
    require(len(answers)==len(set(answers)),'duplicate set cover')
    return sorted(answers),nodes

def profile_graph(vertices,patch):
    edges=defaultdict(list)
    for n,m in enumerate(patch):
        polygon=[point(m,p) for p in vertices]
        for i,(a,b) in enumerate(oriented_edges(polygon)):
            edges[tuple(sorted((a,b)))].append((n,i,a,b))
    graph=[set() for _ in range(28)];relations=set()
    for inc in edges.values():
        require(len(inc)<=2,'three tiles share a port')
        if len(inc)!=2:continue
        a,b=inc;reverse=int(a[2]==b[3])
        require(reverse or a[2]==b[2],'bad endpoint order')
        det_a=patch[a[0]][0]*patch[a[0]][4]-patch[a[0]][1]*patch[a[0]][3]
        det_b=patch[b[0]][0]*patch[b[0]][4]-patch[b[0]][1]*patch[b[0]][3]
        require(det_a==(-1)**(reverse+1)*det_b,'shared ports have wrong interior sides')
        relations.add(tuple(sorted((a[1],b[1])))+(reverse,))
        for r in (0,1):
            i=2*a[1]+r;j=2*b[1]+(r^reverse)
            graph[i].add(j);graph[j].add(i)
    return graph,sorted(relations)

def classify_graph(graph):
    done=set();freedom=0;certificates=[]
    for root in range(28):
        if root in done:continue
        parent={root:None};colour={root:0};queue=deque([root]);conflict=None
        while queue:
            a=queue.popleft()
            for b in sorted(graph[a]):
                if b not in colour:parent[b]=a;colour[b]=1-colour[a];queue.append(b)
                elif colour[a]==colour[b] and conflict is None:conflict=a,b
        done.update(colour)
        if conflict is None:freedom+=1;continue
        def route(a):
            result=[a]
            while parent[a] is not None:a=parent[a];result.append(a)
            return result
        a,b=conflict
        certificates.append((sorted(colour),list(reversed(route(a)))+route(b)))
    return freedom,certificates

def read_odd_walks(graph,certificates):
    """Check literal walks and connectivity without using the colouring routine."""
    covered=set()
    for nodes,walk in certificates:
        nodes=set(nodes)
        require(nodes and not nodes&covered,'component partition')
        require(all(graph[a]<=nodes for a in nodes),'component not closed')
        require(walk[0]==walk[-1] and (len(walk)-1)%2==1,'not an odd closed walk')
        require(all(a in nodes for a in walk),'walk leaves component')
        require(all(b in graph[a] for a,b in zip(walk,walk[1:])),'absent odd-walk edge')
        reached={walk[0]};stack=[walk[0]]
        while stack:
            for b in graph[stack.pop()]:
                if b not in reached:reached.add(b);stack.append(b)
        require(reached==nodes,'nodes do not connect to odd walk')
        covered.update(nodes)
    require(covered==set(range(28)),'not all functions forced')

def profile_test(vertices,patch):
    graph,relations=profile_graph(vertices,patch);freedom,certificates=classify_graph(graph)
    if not freedom:read_odd_walks(graph,certificates)
    return freedom

def read_disk_boundary(cells):
    boundary=Counter()
    for p in cells:
        for a,b in oriented_edges(face(p)):
            if boundary[b,a]:boundary[b,a]-=1
            else:boundary[a,b]+=1
    edges=[e for e,n in boundary.items() if n]
    require(all(boundary[e]==1 for e in edges),'repeated boundary edge')
    successors=defaultdict(list);predecessors=defaultdict(list)
    for a,b in edges:successors[a].append(b);predecessors[b].append(a)
    require(set(successors)==set(predecessors),'open boundary')
    require(all(len(successors[p])==len(predecessors[p])==1 for p in successors),
            'pinched boundary')
    start=min(successors);walk=[start];p=successors[start][0]
    while p!=start:
        require(p not in walk,'multiple boundary loops')
        walk.append(p);p=successors[p][0]
    require(len(walk)==len(edges),'more than one boundary component')
    require(sum(cross(a,b) for a,b in oriented_edges(walk))==4*len(cells),'boundary area')
    return len(edges)

def read_sharp_witness(data,cells,vertices,first,exceptions):
    # The paired states count graph components, not independent functions.
    # This explicit symmetric polynomial demonstrates actual nonzero functions.
    signs=data['sharp_profile_signs'];require(len(signs)==14 and any(signs),'zero sharp witness')
    require(all(type(s)is int and s in (-1,0,1) for s in signs),'profile signs')
    first_index=exceptions[0]['first_index'];patch=(IDENTITY,)+first[first_index]
    taken=set().union(*({point(t,p) for p in cells} for t in patch))
    boundary_edges=read_disk_boundary(taken)
    for pp in [patch]+[r['poses'] for r in exceptions]:
        graph,relations=profile_graph(vertices,pp)
        require(all(signs[i]+signs[j]==0 for i,j,reverse in relations),
                'symmetric polynomial profiles do not match')
    # f(t)=t^2(1-t)^2; direct integer coefficient substitution verifies reversal.
    from math import comb
    coefficients=(0,0,1,-2,1)
    reflected=tuple(sum(coefficients[k]*comb(k,j)*(-1)**j for k in range(j,5))
                    for j in range(5))
    require(reflected==coefficients,'profile reversal identity')
    require(coefficients[0]==sum(coefficients)==0 and
            coefficients[1]==sum(k*coefficients[k] for k in range(5))==0,
            'profile endpoint value or tangent')
    return {'first_index':first_index,'disk_first_tiles':len(patch),
            'disk_first_boundary_edges':boundary_edges,'hollow_second_tiles':len(exceptions[0]['poses']),
            'symmetric_polynomial_coefficients':coefficients,'profile_signs':signs}

def run(data):
    cells,vertices=validate_model(data);target=halo(cells)
    relative=placements_at_targets(cells,target,cells)
    require(relative==boxed_neighbours(cells,target),'neighbour generation controls differ')
    first,nodes1=covers_bit(relative,target,cells)
    control,nodes1control=covers_sets(relative,target,cells)
    require(first==control,'first-surround controls differ')
    histogram1=Counter();histogram2=Counter();exceptions=[];free_first=[]
    second_records=[];nodes2=0;nodes2control=0;second_count=0
    for index,chosen in enumerate(first):
        patch=(IDENTITY,)+chosen;freedom=profile_test(vertices,patch);histogram1[freedom]+=1
        if not freedom:continue
        free_first.append(index)
        occupied,candidates=transported_candidates(cells,patch,relative);target2=halo(occupied)
        control_candidates=placements_at_targets(cells,target2,occupied)
        require(candidates==control_candidates,'second candidate controls differ')
        second,n=covers_bit(candidates,target2,occupied)
        second_control,nc=covers_sets(control_candidates,target2,occupied)
        require(second==second_control,'second-surround controls differ')
        nodes2+=n;nodes2control+=nc;second_count+=len(second)
        second_records.append((index,second))
        for selected in second:
            full=patch+selected;freedom=profile_test(vertices,full);histogram2[freedom]+=1
            if not freedom:continue
            taken=set().union(*({point(t,p) for p in cells} for t in full));goal3=halo(taken)
            candidates3=placements_at_targets(cells,goal3,taken)
            isolated=sorted(p for p in goal3 if neighbours(p,True)<=taken)
            blocked=sorted(p for p in goal3 if not any(p in c for c in candidates3.values()))
            require(isolated and set(isolated)<=set(blocked),'exception is not sealed and unfillable')
            exceptions.append({'first_index':index,'poses':full,'freedom':freedom,
                               'isolated_gaps':isolated,'zero_user_halo_cells':blocked})
    require(histogram1[0]+len(free_first)==len(first),'classification incomplete')
    require(len(exceptions)==histogram2[2] and all(r['freedom']==2 for r in exceptions),
            'unclassified nonflat second surround')
    sharp=read_sharp_witness(data,cells,vertices,first,exceptions)
    exception_data=json.loads((HERE/'exceptions.json').read_text())
    require(json.loads(json.dumps(exceptions))==exception_data,'exception fixtures differ')
    return {
        'agent':'six-heesch-3','role':'researcher',
        'model':'aligned hat reference patches; 14 complete normal-graph ports',
        'neighbours':len(relative),'root_halo_cells':len(target),
        'first_surrounds':len(first),'first_bipartite_component_histogram':sorted(histogram1.items()),
        'first_search_nodes_bit':nodes1,'first_search_nodes_sets':nodes1control,
        'first_surrounds_sha256':digest(first),
        'free_first_indices':free_first,'second_surrounds_examined':second_count,
        'second_bipartite_component_histogram':sorted(histogram2.items()),
        'second_search_nodes_bit':nodes2,'second_search_nodes_sets':nodes2control,
        'second_surrounds_sha256':digest(second_records),
        'exceptional_second_surrounds':len(exceptions),'exceptions_sha256':digest(exceptions),
        'every_exception_sealed_and_unfillable':True,
        'all_aligned_disk_two_surround_profiles_flat':True,
        'all_aligned_three_surround_profiles_flat':True,
        'sharpness_in_the_reference_profile_equations':sharp,
        'seven_corona_construction_found':False,
    }

def controls(data):
    """Geometry and odd-walk reader rejection controls, not theorem evidence."""
    malformed=json.loads(json.dumps(data));malformed['cells'][0][0]+=1
    rejected=0
    try:validate_model(malformed)
    except ValueError:rejected+=1
    malformed=json.loads(json.dumps(data));malformed['vertices'][0][0]+=1
    try:validate_model(malformed)
    except ValueError:rejected+=1
    graph=[set() for _ in range(28)]
    for i in range(28):graph[i].add(i)
    certificates=[([i],[i,i]) for i in range(28)]
    read_odd_walks(graph,certificates)
    bad=[([i],[i,i,i]) if i==0 else c for i,c in enumerate(certificates)]
    try:read_odd_walks(graph,bad)
    except ValueError:rejected+=1
    bad=certificates[:-1]
    try:read_odd_walks(graph,bad)
    except ValueError:rejected+=1
    graph[0].clear()
    try:read_odd_walks(graph,certificates)
    except ValueError:rejected+=1
    require(rejected==5,'malformed control did not reject')
    return rejected

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',action='store_true')
    args=parser.parse_args();data=json.loads((HERE/'input.json').read_text())
    result=run(data);result['malformed_controls_rejected']=controls(data)
    result=json.loads(json.dumps(result))
    if args.expected:require(result==json.loads((HERE/'expected.json').read_text()),'expected output differs')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
