"""Check the motivating odd-distance graph, not its unit-distance graph."""
import json
from itertools import combinations
from pathlib import Path
from verify import points, row, plus, times, F, digest


def colour(n, edges, k, unequal=None):
    adj=[set() for _ in range(n)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    if unequal is not None:
        u,v=unequal;adj[u].add(v);adj[v].add(u)
    col=[-1]*n;nodes=0
    def visit():
        nonlocal nodes
        nodes+=1
        left=[v for v in range(n) if col[v]<0]
        if not left:return tuple(col)
        v=max(left,key=lambda v:(len({col[u] for u in adj[v] if col[u]>=0}),len(adj[v]),-v))
        used={col[u] for u in adj[v] if col[u]>=0}
        # Only one unused colour need be tried: names are interchangeable.
        for c in range(min(k,max(col,default=-1)+2)):
            if c in used:continue
            col[v]=c
            found=visit()
            if found is not None:return found
        col[v]=-1
        return None
    result=visit()
    if result is not None and any(result[u]==result[v] for u in range(n) for v in adj[u]):
        raise ValueError('invalid source colouring')
    return result,nodes


def check():
    p=points();es=[];hist={1:0,3:0,5:0,7:0}
    for i,j in combinations(range(21),2):
        r=row(p[i],p[j]);d=plus(r[0],times((F(3),F(0)),r[2]))
        for length in hist:
            if d==(F(65536*length*length),F(0)):
                es.append((i,j));hist[length]+=1
    half=[(i,j) for i,j in es if j<11]
    sep,half_nodes=colour(11,half,4,(0,1))
    if sep is not None:raise ValueError('half does not force equality')
    c4,n4=colour(21,es,4)
    c5,n5=colour(21,es,5)
    if c4 is not None or c5 is None:raise ValueError('source chromatic number mismatch')
    if (1,11) not in es:raise ValueError('missing spindle bridge')
    return {'source_vertices':21,'source_odd_edges':len(es),
            'half_odd_edges':len(half),'edge_length_histogram':hist,
            'four_colouring_exists':False,'five_colouring':list(c5),
            'source_edges_sha256':digest(es),
            'search_nodes':{'half_separating_four':half_nodes,'full_four':n4,'full_five':n5}}


if __name__=='__main__':
    result=check()
    expected=json.loads(Path(__file__).with_name('source_expected.json').read_text())
    if json.loads(json.dumps(result))!=expected:raise ValueError('source expected mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))
