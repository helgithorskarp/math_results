"""Dense exact producer for QQ endpoint cases, HCP control and size profiles.

This proves the arithmetic/enumeration statements of PROOF.md. The spherical
and Jordan-curve bridges are ordinary proofs, not certified by this program.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import argparse, hashlib, json
from poly import Rat, bernstein

ROOT = Path(__file__).resolve().parent
LO, HI = F(1, 2), F(5, 7)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode_poly(p):
    return [str(x) for x in p]


def cases():
    one, c, h = Rat([1]), Rat([0, 1]), Rat([1, 2])
    b = {1:one, 2:c/h, 3:(c-one)/Rat([1, 3])}
    rows = []
    for t in range(1, 4):
        for s in range(t, 4):
            sigma = (one-c*c)/(h*(b[t]+c*b[s]))
            p = one-h*b[t]*sigma
            delta = h*sigma*sigma-Rat([4])*p
            lower = c*c/h-c*sigma+p
            upper = h-h*sigma+p
            require((p+h*b[t]*sigma-one).n == [], 'first star equation')
            require((p-c*c-c*h*b[s]*sigma).n == [], 'second star equation')
            if t == 1:
                obstruction = {'kind':'negative_discriminant',
                    'rational':delta.encode(),
                    'Bernstein_numerator':encode_poly(bernstein(delta.n, LO, HI))}
                require(all(x<0 for x in bernstein(delta.n, LO, HI)), 'case1 sign')
            elif (t,s) == (2,2):
                target = -(Rat([-1,2])*(one+c)*(one+c)/(c*c))
                require((delta-target).n == [], 'case22 factor')
                obstruction = {'kind':'strict_above_lower_endpoint',
                    'rational':delta.encode(),
                    'factor':'-(2c-1)(1+c)^2/c^2',
                    'exception_c':'1/2','exception_P':'1/2',
                    'exception_S_over_A':'1','exception_x_equals_y_squared':'1/2'}
            elif (t,s) == (2,3):
                n = lower*c*h
                require(n.d == [F(1)] and n.n == list(map(F,[-1,-3,1,7])),
                        'lower-gap numerator')
                signs = bernstein(n.n, LO, HI)
                require(all(x<0 for x in signs), 'case23 closed sign')
                obstruction = {'kind':'negative_lower_gap_product',
                    'rational':lower.encode(),'numerator':n.encode(),
                    'Bernstein_numerator':encode_poly(signs)}
            else:
                target = -Rat([1,3])/h
                require((sigma-target).n == [], 'case33 negative sum')
                obstruction = {'kind':'negative_sum',
                    'rational':sigma.encode(),
                    'Bernstein_numerator':encode_poly(bernstein(sigma.n, LO, HI))}
                require(all(x<0 for x in bernstein(sigma.n, LO, HI)), 'case33 sign')
            for rational in (sigma,p,delta,lower,upper,b[t],b[s]):
                require(all(x>=0 for x in rational.d) and any(x>0 for x in rational.d),
                        'canonical denominator positive at c>0')
            rows.append({'t':t,'s':s,'B_t_over_A':b[t].encode(),
                'B_s_over_A':b[s].encode(),'S_over_A':sigma.encode(),
                'P':p.encode(),'discriminant':delta.encode(),
                'lower_gap_product':lower.encode(),'upper_gap_product':upper.encode(),
                'obstruction':obstruction})
    require(len(rows)==6, 'complete six-case domain')
    return rows


def components(adjacency):
    todo = set(adjacency)
    out = []
    while todo:
        stack = [min(todo)]; reached = set()
        while stack:
            v=stack.pop()
            if v in reached:continue
            reached.add(v);stack.extend(adjacency[v]-reached)
        todo-=reached;out.append(sorted(reached))
    return out


def calibration():
    equator=[(1,0,0),(F(1,2),F(1,2),0),(-F(1,2),F(1,2),0),
        (-1,0,0),(-F(1,2),-F(1,2),0),(F(1,2),-F(1,2),0)]
    top=[(F(1,2),F(1,6),F(1,3)),(-F(1,2),F(1,6),F(1,3)),
        (0,-F(1,3),F(1,3))]
    points=[tuple(map(F,p)) for p in equator+top+[(x,y,-z) for x,y,z in top]]
    labels=['E'+str(i) for i in range(6)]+['U'+str(i) for i in range(3)]+['L'+str(i) for i in range(3)]
    metric=(1,3,6)
    def dot(a,b):return sum(w*x*y for w,x,y in zip(metric,a,b))
    def linear(a,b):return sum(x*y for x,y in zip(a,b))
    def sub(a,b):return tuple(x-y for x,y in zip(a,b))
    def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    gram=[[dot(a,b) for b in points] for a in points]
    require(all(gram[i][i]==1 for i in range(12)), 'unit coordinates')
    require(all(gram[i][j]<=LO for i,j in combinations(range(12),2)), 'packing')
    require(all(sum(p[j] for p in points)==0 for j in range(3)), 'positive barycenter')
    require(any(linear(points[a],cross(points[b],points[c]))!=0
        for a,b,c in combinations(range(12),3)), 'full span')
    edges={frozenset((a,b)) for a,b in combinations(range(12),2) if gram[a][b]==LO}
    require(len(edges)==24, 'all24 contacts')
    facets={}
    for a,b,c in combinations(range(12),3):
        n=cross(sub(points[b],points[a]),sub(points[c],points[a]))
        if n==(0,0,0):continue
        k=linear(n,points[a]);values=[linear(n,p)-k for p in points]
        if all(v<=0 for v in values):pass
        elif all(v>=0 for v in values):n=tuple(-v for v in n);k=-k
        else:continue
        require(k>0, 'strictly positive facet height')
        vertices=tuple(i for i,p in enumerate(points) if linear(n,p)==k)
        require(len(vertices) in (3,4), 'only T/Q facets')
        facets[vertices]=tuple(v/k for v in n)
    require(len(facets)==14 and sum(len(f)==3 for f in facets)==8, 'HCP8T6Q')
    cycles=[]
    for vertices in sorted(facets):
        adjacency={v:{w for w in vertices if frozenset((v,w)) in edges} for v in vertices}
        require(all(len(ns)==2 for ns in adjacency.values()), 'facet contact degrees2')
        start=min(vertices);last=None;v=start;cycle=[]
        while v not in cycle:
            cycle.append(v);w=min(adjacency[v]-({last} if last is not None else set()));last,v=v,w
        require(v==start and set(cycle)==set(vertices), 'whole facet cycle')
        cycles.append(cycle)
    face_edges=[{frozenset((f[i],f[(i+1)%len(f)])) for i in range(len(f))} for f in cycles]
    require(set().union(*face_edges)==edges, 'contacts exactly all hull edges')
    qq=[];tt=[];nn=[]
    for edge in sorted(edges,key=lambda e:sorted(e)):
        incident=[i for i,es in enumerate(face_edges) if edge in es]
        require(len(incident)==2, 'edge has two actual incident faces')
        if all(len(cycles[i])==4 for i in incident):
            stars=[sorted(len(cy) for cy in cycles if v in cy) for v in sorted(edge)]
            require(stars==[[3,3,4,4],[3,3,4,4]], 'TTQQ exceptional stars')
            for i in incident:
                opposite=[e for e in combinations(cycles[i],2) if frozenset(e) not in edges]
                require(len(opposite)==2 and all(gram[a][b]==0 for a,b in opposite), 'spherical squares')
            qq.append({'edge':[labels[v] for v in sorted(edge)],'endpoint_face_sizes':stars})
            nn.append(edge)
        if all(len(cycles[i])==3 for i in incident):tt.append(incident)
    require(len(qq)==3 and len(tt)==3, 'HCP QQ/TT seams')
    tids=[i for i,f in enumerate(cycles) if len(f)==3]
    t_adj={i:set() for i in tids}
    for a,b in tt:t_adj[a].add(b);t_adj[b].add(a)
    t_components=[]
    for group in components(t_adj):
        vertices=set().union(*(set(cycles[i]) for i in group))
        edge_count=sum(len(t_adj[i]) for i in group)//2
        require(edge_count==len(group)-1 and len(vertices)<=len(group)+2, 'calibration triangle trees')
        t_components.append({'triangles':sorted(sorted(labels[v] for v in cycles[i]) for i in group),
            'vertices':sorted(labels[v] for v in vertices),'faces':len(group),'TT_edges':edge_count})
    qids=[i for i,f in enumerate(cycles) if len(f)==4]
    q_adj={i:{j for j in qids if j!=i and set(cycles[i])&set(cycles[j])} for i in qids}
    require(len(components(q_adj))==1, 'connected nontriangle union control')
    require(set().union(*(set(cycles[i]) for i in qids))==set(range(12)), 'all points on nontriangles')
    return {'name':'classical HCP triangular orthobicupola J27',
        'c':'1/2','coordinate_metric':list(metric),'labels':labels,
        'scaled_points':[[str(x) for x in p] for p in points],
        'Gram':[[str(x) for x in row] for row in gram],
        'faces':[[labels[v] for v in cy] for cy in cycles],
        'supporting_planes':[{'vertices':[labels[v] for v in f],
            'normal':[str(x) for x in facets[f]],'constant':'1'} for f in sorted(facets)],
        'QQ_edges':qq,'triangle_components':t_components,
        'contacts':24,'strict_noncontacts':42,'T_Q_counts':[8,6],
        'NN_edges':len(nn),'TT_edges':len(tt)}


def partitions(n,least=1):
    if n==0:
        yield [];return
    for x in range(least,n+1):
        for tail in partitions(n-x,x):yield [x]+tail


def motif_profiles():
    blocks=[[(0,5,11),(0,6,11),(0,5,7),(5,9,11)],
            [(1,2,4),(2,4,8),(1,2,10),(1,10,12)]]
    edge_sets=[]; support=[]
    for block in blocks:
        es=[{frozenset(p) for p in combinations(tri,2)} for tri in block]
        adjacent={i:{j for j in range(4) if i!=j and es[i]&es[j]} for i in range(4)}
        require(len(components(adjacent))==1, 'connected four-face cluster')
        edge_sets.append(set().union(*es));support.append(set().union(*(set(t) for t in block)))
    require(len(set().union(*edge_sets))==18 and len(set().union(*support))==12 and not(support[0]&support[1]), 'injective18-edge motif interface')
    all_parts=list(partitions(11));rows=[]
    for sizes in all_parts:
        if len(sizes)>8:continue
        compatible=max(sizes)>=10 or sum(x>=4 for x in sizes)>=2
        rows.append({'component_sizes':sizes,'NN_edges':8-len(sizes),
            'TT_edges':11-len(sizes),'motif_size_condition':compatible})
    require(len(all_parts)==56 and len(rows)==52, 'complete size domain')
    eligible=[r['component_sizes'] for r in rows if r['motif_size_condition']]
    require(len(eligible)==11, 'eleven necessary compatible profiles')
    return {'triangles':[[list(t) for t in b] for b in blocks],
        'cluster_supports':[sorted(s) for s in support],
        'prescribed_edges':[sorted(e) for e in sorted(set().union(*edge_sets),key=lambda e:sorted(e))],
        'all_partitions_11':56,'cohort_profile_count':52,'rows':rows,
        'motif_compatible_profiles':eligible,'motif_incompatible_profiles':41,
        'not_sufficient_for_occurrence':True,'no_profile_excludes_packings':True}


def produce():
    return {'schema':'tammes-connected-map-filters-v1',
        'actual_agent':'six-tammes-1','role':'researcher',
        'algebraic_closed_band':['1/2','5/7'],
        'local_conclusion_lower_strict':True,'local_upper_included':True,
        'QQ_cases':cases(),'endpoint_calibration':calibration(),
        'triangle_forest_profiles':motif_profiles()}


def canonical(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',type=Path)
    args=parser.parse_args();obj=produce();data=canonical(obj)
    if args.emit:
        args.emit.write_bytes(data)
    else:
        require((ROOT/'CERTIFICATE.json').read_bytes()==data, 'whole certificate bytes mismatch')
    print(json.dumps({'verified':True,'whole_comparison':not bool(args.emit),
        'QQ_cases':6,'calibration_contacts':24,'calibration_QQ_edges':3,
        'forest_profiles':52,'motif_compatible':11,'motif_incompatible':41,
        'sha256':hashlib.sha256(data).hexdigest()},sort_keys=True))


if __name__=='__main__':main()
