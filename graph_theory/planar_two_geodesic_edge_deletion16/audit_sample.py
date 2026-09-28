"""Cross-language sample audit of the edge-deletion induction.

Input is the hard graph6 stream from plantri -g 16 0/1000, passed through
filter_hard.cpp. This script
uses the earlier independent Python graph routines for distances, cuts, and
components, then implements the witness-edge induction separately from the
C++ full-census verifier.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SHA256 = "a1ee18fc00018b938e76cf40925df78f5b69d86f41788babceb04af139e69c92"

def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

v=load('v',ROOT/'graph_theory/planar_two_geodesic_triangulation14/verify.py')
c=load('c',ROOT/'graph_theory/planar_two_geodesic_finite/check.py')
memo={}
stats={'states':0,'maxdepth':0,'term_diameter':0,'term_cut':0,'internal':0}

def paths_with_edges(adj, dist):
    n=len(adj); paths=[]
    for u in range(n): paths.append((1<<u,()))
    def visit(source,target,cur,nodes,edges):
        if cur==target:
            paths.append((nodes,tuple(sorted(edges))))
            return
        for nxt in range(n):
            if ((adj[cur]>>nxt)&1 and dist[source][nxt]==dist[source][cur]+1
                and dist[source][nxt]+dist[nxt][target]==dist[source][target]):
                edge=(min(cur,nxt),max(cur,nxt))
                visit(source,target,nxt,nodes|(1<<nxt),edges+(edge,))
    for u in range(n):
        for w in range(u+1,n):
            visit(u,w,u,1<<u,())
    return paths

def witness_edges(adj, dist, easy):
    paths=paths_with_edges(adj,dist)
    best=None;best_score=(100,100)
    for i,(mask1,edges1) in enumerate(paths):
        for mask2,edges2 in paths[i:]:
            together=tuple(sorted(set(edges1+edges2)))
            score=(sum(edge not in easy for edge in together),len(together))
            if score>=best_score:
                continue
            if c.largest_component(adj,mask1|mask2)<=len(adj)//2:
                best=together;best_score=score
                if score[0]==0:return best
    return best

def certify(adj,depth=0,limit=5000):
    key=tuple(adj)
    if key in memo:return memo[key]
    stats['states']+=1;stats['maxdepth']=max(stats['maxdepth'],depth)
    if stats['states']>limit:raise RuntimeError('state limit')
    dist=c.distances(adj)
    if any(x<0 or x>3 for row in dist for x in row):
        stats['term_diameter']+=1;memo[key]=True;return True
    if v.has_half_cut(adj,4):
        stats['term_cut']+=1;memo[key]=True;return True
    easy=set()
    for u in range(len(adj)):
        for w in range(u+1,len(adj)):
            if not (adj[u]>>w&1):continue
            child=adj.copy();child[u]&=~(1<<w);child[w]&=~(1<<u)
            childdist=c.distances(child)
            if any(x<0 or x>3 for row in childdist for x in row) or v.has_half_cut(child,4):
                easy.add((u,w))
    edges=witness_edges(adj,dist,easy)
    if edges is None:
        print('COUNTEREXAMPLE',key)
        memo[key]=False;return False
    stats['internal']+=1
    for u,w in edges:
        if (u,w) in easy:continue
        child=adj.copy();child[u]&=~(1<<w);child[w]&=~(1<<u)
        if not certify(child,depth+1,limit):
            memo[key]=False;return False
    memo[key]=True;return True

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('hard_graph6',type=Path)
    args=parser.parse_args()
    raw=args.hard_graph6.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA256:
        raise AssertionError('hard-stream SHA256 mismatch')
    lines=raw.splitlines()
    if len(lines)!=399:
        raise AssertionError('wrong hard-stream record count')
    indices=sorted(set(range(20))|set(range(0,len(lines),50)))
    for i in indices:
        adj=v.decode_graph6(lines[i],16)
        if not certify(adj,limit=200000):
            raise AssertionError(f'failed sample index {i}')
    print(json.dumps({'sampled_roots':len(indices),'states':stats['states'],
                      'max_depth':stats['maxdepth'],'failures':0},sort_keys=True))
