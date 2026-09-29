"""Check a 30-dimensional closed metric box and a three-pair mass rule.

Python 3.11+, standard library only. No solver or discovery code is used.
Shortestness is certified by six integer Lipschitz potential vectors.
"""
from itertools import combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent


def components(adj,removed):
    left=set(adj)-set(removed);out=[]
    while left:
        part={left.pop()};todo=list(part)
        while todo:
            v=todo.pop();new=adj[v]&left;left-=new;part|=new;todo.extend(new)
        out.append(part)
    return sorted(out,key=lambda K:(-len(K),sorted(K)))


def fixture():
    rows=[(1,2,3,4,5),(0,2,5,6,10),(0,1,3,6,7),(0,2,4,7,8),
          (0,3,5,8,9),(0,1,4,9,10),(1,2,7,10,11),(2,3,6,8,11),
          (3,4,7,9,11),(4,5,8,10,11),(1,5,6,9,11),(6,7,8,9,10)]
    core={v:set(row) for v,row in enumerate(rows)}
    assert all(v in core[u] for v in core for u in core[v])
    faces=[q for q in combinations(range(12),3) if all(b in core[a] for a,b in combinations(q,2))]
    assert len(faces)==20
    adj={v:set(row) for v,row in core.items()};triangles=[]
    for i,face in enumerate(faces):
        z=12+i;adj[z]=set(face)
        for v in face:adj[v].add(z)
        triangles.extend(tuple(sorted((a,b,z))) for a,b in combinations(face,2))
    edges=sorted((a,b) for a in adj for b in adj[a] if a<b)
    assert len(edges)==90 and len(triangles)==60 and len(adj)-len(edges)+len(triangles)==2
    assert all(sum(a in F and b in F for F in triangles)==2 for a,b in edges)
    for v in adj:
        link={u:set() for u in adj[v]}
        for F in triangles:
            if v in F:
                a,b=[u for u in F if u!=v];link[a].add(b);link[b].add(a)
        assert all(len(row)==2 for row in link.values())
        assert len(components(link,[]))==1
    assert len(components(adj,[]))==1
    return adj,core,faces


def check_potential(core,center,path,potential):
    assert path and len(path)==len(set(path))
    assert all(v in core[u] for u,v in zip(path,path[1:]))
    chosen={tuple(sorted((u,v))) for u,v in zip(path,path[1:])}
    critical={e:(158 if e in chosen else 144)*c for e,c in center.items()}
    assert len(potential)==12 and all(type(x) is int for x in potential)
    assert potential[path[0]]==0
    assert potential[path[-1]]==sum(critical[e] for e in chosen)
    assert all(abs(potential[v]-potential[u])<=w for (u,v),w in critical.items())


def main():
    data=json.loads((HERE/'certificate.json').read_text())
    adj,core,faces=fixture()
    assert data['vertices']==32 and data['faces']==[list(F) for F in faces]
    assert (data['lower_multiplier'],data['center_multiplier'],data['upper_multiplier'])==(144,151,158)
    center={(u,v):c for u,v,c in data['core_edges']}
    assert len(data['core_edges'])==len(center)==30
    assert set(center)=={(u,v) for u in core for v in core[u] if u<v}
    assert all(type(c) is int and c>0 for c in center.values())
    pairs=data['candidate_pairs'];paths=[p for pair in pairs for p in pair]
    assert len(pairs)==3 and all(len(pair)==2 for pair in pairs)
    assert len(data['critical_corner_potentials'])==6
    for path,potential in zip(paths,data['critical_corner_potentials']):
        check_potential(core,center,path,potential)
    parts=[components(adj,set(pair[0])|set(pair[1])) for pair in pairs]
    large=[[K for K in row if len(K)>1] for row in parts]
    assert [list(map(len,row)) for row in large]==[[13],[21],[13,6]]
    H1,H2=large[0][0],large[1][0];C,D=large[2]
    assert not H1&C and not H2&D
    # Every other component is a singleton, so the displayed implications
    # handle all nonnegative masses once no single vertex carries half.
    assert [sum(len(K)==1 for K in row) for row in parts]==[10,5,5]
    # No four-vertex guard can put every large residual into the current
    # deletion-stable internal two-path-cover class. After deleting k core
    # vertices, keep a core spanning tree and attach every surviving mark
    # meeting it as a leaf. Even after 4-k further mark deletions there
    # remain at least sixteen such leaves.
    core_deletions=0;minimum_leaves=20
    for k in range(5):
        for deleted in combinations(range(12),k):
            assert len(components(core,deleted))==1
            attached=sum(bool(set(F)-set(deleted)) for F in faces)
            leaves=attached-(4-k)
            assert leaves>=16
            minimum_leaves=min(minimum_leaves,leaves);core_deletions+=1
    # The radius is tight for this path library: 5-9-10 ties the direct
    # edge 5-10 at its adverse corner. A larger symmetric radius breaks
    # shortestness of this path; it need not break the separator theorem.
    assert center[5,9]+center[9,10]==144 and center[5,10]==158
    assert 158*(center[5,9]+center[9,10])==144*center[5,10]
    assert 17*(center[5,9]+center[9,10])>15*center[5,10]
    forged=list(data['critical_corner_potentials'][0]);forged[paths[0][-1]]+=1
    try:check_potential(core,center,paths[0],forged)
    except AssertionError:pass
    else:raise AssertionError('forged shortest-path potential accepted')
    output={'status':'PASS','vertices':32,'edges':90,'faces':60,'core_price_dimensions':30,
            'relative_closed_radius':'7/151','shortest_path_potentials':6,
            'lipschitz_edge_checks':180,'candidate_pairs':3,
            'nonsingleton_component_sizes':[[13],[21],[13,6]],
            'disjoint_heavy_implications':2,'rejected_forged_potentials':1,
            'core_deletions_checked':core_deletions,'minimum_guard_tree_leaves':minimum_leaves,
            'larger_radius_control':'1/16 breaks path 5-9-10 only; no separator-failure claim',
            'mass_scope':'all 32 vertices; arbitrary nonnegative real masses',
            'ambient_condition':'core is isometric, equivalently each face-star two-edge route dominates the core endpoint distance',
            'problem31_resolution':False}
    print(json.dumps(output,sort_keys=True))


if __name__=='__main__':main()
