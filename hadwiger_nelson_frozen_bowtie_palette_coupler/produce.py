#!/usr/bin/env python3
"""Independent reconstruction and DSATUR census; no verifier imports."""
from pathlib import Path
from itertools import combinations, product
import argparse, hashlib, json
BASE = Path(__file__).resolve().parent
N = [4,5,6,7,9,10,12,14,15,17,18,22,25,28]

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()

def mul(a, b):
    # Index bits represent sqrt(3), sqrt(11); repeated bits square out.
    out = [0]*4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            repeat = i & j
            out[i ^ j] += x*y*(3 if repeat & 1 else 1)*(11 if repeat & 2 else 1)
    return out

def reconstruct():
    rows = [list(map(int, l.split())) for l in (BASE/'source29.tsv').read_text().splitlines() if l and not l.startswith('#')]
    points = [(5*a,0,0,5*b,0,5*c,5*d,0) for _,a,b,c,d in rows]
    centre = (0,0,0,0,60,0,0,0)
    directions = [(36,0,0,0,48,0,0,0),(18,-24,0,0,24,18,0,0)]
    points += [centre] + [tuple(c+s*x for c,x in zip(centre,u)) for s in (1,-1) for u in directions]
    if len(set(points)) != 34:
        raise ValueError('geometry collisions')
    edges = []; stream = hashlib.sha256()
    for i,j in combinations(range(34),2):
        d = [a-b for a,b in zip(points[i],points[j])]
        n = [a+b for a,b in zip(mul(d[:4],d[:4]),mul(d[4:],d[4:]))]
        stream.update((','.join(map(str,n))+'\n').encode())
        if n == [3600,0,0,0]:
            edges.append([i,j])
    adj = [set() for _ in range(29)]
    for a,b in edges:
        if b < 29:
            adj[a].add(b);adj[b].add(a)
    return points,edges,adj,stream.hexdigest()

def census(adj):
    ni = {v:i for i,v in enumerate(N)}
    patterns = []; a = []
    def enum(i,m):
        if i == 14:
            patterns.append(tuple(a));return
        previous = [ni[u] for u in adj[N[i]] if u in ni and ni[u] < i]
        for c in range(min(2,m+1)+1):
            if all(a[j] != c for j in previous):
                a.append(c);enum(i+1,max(m,c));a.pop()
    enum(0,-1)
    nodes = 0
    def solve(pat):
        col = [-1]*29;col[0] = 3
        for i,c in zip(N,pat):col[i] = c
        def go():
            nonlocal nodes
            nodes += 1
            remaining = [v for v in range(29) if col[v] < 0]
            if not remaining:return list(col)
            used = {v:{col[u] for u in adj[v] if col[u] >= 0} for v in remaining}
            v = max(remaining,key=lambda x:(len(used[x]),len(adj[x]),-x))
            for c in range(4):
                if c not in used[v]:
                    col[v] = c;answer = go()
                    if answer is not None:return answer
            col[v] = -1;return None
        return go()
    allowed = []; denied = []
    for pat in patterns:
        word = solve(pat);key = ''.join(map(str,pat))
        if word is None:denied.append(key)
        else:
            if not all(word[u] != word[v] for u in range(29) for v in adj[u]):
                raise ValueError('source witness')
            allowed.append((key,''.join(map(str,word))))
    if not all(set(w) == set('012') for w,_ in allowed):
        raise ValueError('frozen palette')
    return patterns,allowed,denied,nodes

def main():
    ap = argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--table',type=Path);ap.add_argument('--compare',type=Path)
    a = ap.parse_args();P,E,adj,dist = reconstruct();pat,allowed,denied,nodes = census(adj)
    counts = [0,0,0]
    local = [[0,1],[0,2],[0,3],[0,4],[1,2],[3,4]]
    for leaves in product(range(4),repeat=4):
        possible = []
        for c in range(4):
            word = (c,)+leaves
            if all(word[i] != word[j] for i,j in local):possible.append(c)
        before = bool(possible);after = any(c != 3 for c in possible)
        counts[0] += before;counts[1] += after;counts[2] += before and not after
    M = len(allowed)
    result = {'points':len(P),'unit_edges':len(E),'point_hash':digest(P),'edge_hash':digest(E),'distance_hash':dist,
              'bare_at_most_three_colour_patterns':len(pat),'source_canonical_patterns':M,'source_rejected_patterns':len(denied),
              'source_pattern_hash':hashlib.sha256(''.join(w+'\n' for w,_ in allowed).encode()).hexdigest(),
              'input_joint_canonical_patterns':M*counts[0],'composite_joint_canonical_patterns':M*counts[1],
              'lost_joint_canonical_patterns':M*counts[2]}
    if a.compare:
        expected = json.loads(a.compare.read_text())
        for k,v in result.items():
            if expected[k] != v:raise ValueError('producer/checker disagreement: '+k)
    result['dsatur_nodes'] = nodes
    if a.table:a.table.write_text(''.join(w+'\t'+c+'\n' for w,c in allowed))
    text = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')
if __name__ == '__main__':main()
