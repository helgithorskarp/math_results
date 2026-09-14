"""Complete sqrt(3)-pair attachment gate on the existing H421 support.

This auxiliary gate imports one hash-pinned exact geometry file from the
parent contribution. The 16-point theorem does not depend on this host.
"""
from pathlib import Path
from itertools import combinations
import hashlib,importlib.util,json

HERE=Path(__file__).resolve().parent
DEPENDENCY=HERE.parent/'hadwiger_nelson_heptagon_difference_lifts'/'geometry.py'
SHA='67599414c9cabc9e1e9f0100907c3c039200deea4ffd935cb6ba09d67c57ef07'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def run():
    need(hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest()==SHA,'parent geometry bytes')
    spec=importlib.util.spec_from_file_location('hn_host_geometry',DEPENDENCY)
    G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
    h,d=G.integerize(G.host());p=sorted({G.sub(x,y) for x in h for y in h})
    need(d==7 and len(h)==21 and len(p)==421,'source identity')
    scaled=[G.scale(x,6) for x in p];where={x:i for i,x in enumerate(scaled)}
    alpha=G.sub(G.scale(G.POW[7],2),G.ONE) # i sqrt3
    need(G.mul(alpha,alpha)==G.scale(G.ONE,-3),'sqrt(-3) identity')
    records=[];new=set();edges=[]
    for i,j in combinations(range(421),2):
        distance=G.norm(G.sub(p[j],p[i]))
        if distance==G.scale(G.ONE,d*d):edges.append((i,j))
        if distance!=G.scale(G.ONE,3*d*d):continue
        roots=[]
        for sign in (-1,1):
            root=G.add(G.scale(G.add(p[i],p[j]),3),G.scale(G.mul(alpha,G.sub(p[j],p[i])),sign))
            for v in (i,j):need(G.norm(G.sub(root,scaled[v]))==G.scale(G.ONE,(6*d)**2),'unit intersection')
            if root not in where:new.add(root)
            roots.append(where.get(root))
        need(roots[0]!=roots[1],'two different intersections')
        records.append([i,j,*roots])
    need(len(edges)==1848 and len(records)==126 and not new,'complete attachment gate')
    return {'status':'NO_NEW_PHYSICAL_POINT','source_points':421,'source_edges':1848,
            'all_pair_checks':421*420//2,'sqrt3_pairs':126,'distinct_intersections_per_pair':2,
            'unit_root_checks':504,'new_points':0,'physical_union_points':421,
            'root_index_table_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
            'dependency_sha256':SHA}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
