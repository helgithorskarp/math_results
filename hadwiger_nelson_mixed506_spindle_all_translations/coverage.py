"""Explicit positive four-colouring cover of disjoint placements."""
from itertools import permutations
from collections import Counter
from hashlib import sha256
import json
import geometry as G
PERMS=list(permutations(range(4)))
BAD=[[sum(1<<i for i,p in enumerate(PERMS) if p[b]==a) for b in range(4)] for a in range(4)]

def libraries(B,V,EB,EV):
    libs=G.C.libraries(B,V,EB,EV)
    for side,lib,pts,ee in zip(('B','V'),libs,(B,V),(EB,EV)):
        rows=[tuple(map(int,s)) for s in (G.HERE/f'new_{side}.txt').read_text().splitlines()]
        G.require(len(rows)==1,'one new row expected')
        for c in rows:
            G.require(len(c)==len(pts) and set(c)<=set(range(4)) and all(c[i]!=c[j] for i,j in ee),'invalid added colouring')
            lib.append(c)
    return libs

def witness(ee,libs):
    for ib,cb in enumerate(libs[0]):
        for iv,cv in enumerate(libs[1]):
            mask=(1<<24)-1
            for e in ee:
                i,j=divmod(e,214);mask &= ~BAD[cb[i]][cv[j]]
                if not mask:break
            if mask:return ib,iv,(mask&-mask).bit_length()-1
    return None

def cover(rows,libs,path):
    hist=Counter();used=Counter();stream=sha256();geometry_hash=sha256()
    with path.open('w') as f:
        for key,ee in rows:
            w=witness(ee,libs);G.require(w is not None,'uncovered disjoint placement '+str(key))
            ib,iv,ip=w;pi=PERMS[ip]
            G.require(all(libs[0][ib][e//214]!=pi[libs[1][iv][e%214]] for e in ee),'selected colouring failed')
            line=json.dumps([key,ee,w],separators=(',',':'))+'\n';f.write(line);stream.update(line.encode())
            geometry_hash.update((json.dumps([key,ee],separators=(',',':'))+'\n').encode())
            hist[len(ee)]+=1;used[w]+=1
    return {'disjoint_translations':len(rows),'cross_edge_histogram':sorted(hist.items()),
            'library_sizes':list(map(len,libs)),'used_witnesses':len(used),
            'geometry_stream_sha256':geometry_hash.hexdigest(),'coverage_stream_sha256':stream.hexdigest(),'uncovered':0}
