"""All 62488 single-overlap placements for u=(7+i sqrt(15))/8."""
from pathlib import Path
from hashlib import sha256
from collections import defaultdict,Counter
from itertools import permutations
from math import gcd
import importlib.util,json
HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def load(name,path,pin):
    path=HERE.parent/path
    require(sha256(path.read_bytes()).hexdigest()==pin,'input pin mismatch: '+str(path))
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m

F=load('source_integer','hadwiger_nelson_mixed505_all_gadget_anchors/verify.py','526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38')

def sources():
    B,V,_,_,EB,EV=F.construction()
    return B,[tuple(6*a for a in x) for x in V],EB,EV

def differences(G):
    inc=defaultdict(list)
    for a,x in enumerate(G):
        for b,y in enumerate(G):
            if a!=b:inc[F.subtract(y,x)].append((a,b))
    return inc

def slope(x):
    a,b,c,d=x
    if a==b==0:return (0,)
    nums=(3*(a*a-33*b*b),3*a*c-33*b*d,a*d-3*b*c)
    g=gcd(*nums)
    if nums[0]<0:g=-g
    return tuple(v//g for v in nums)

def contact_pairs(I,J):
    buckets=defaultdict(list)
    for y in sorted(J):buckets[slope(y)].append(y)
    pairs=[];tested=0
    for x in sorted(I):
        a,b,c,d=x;nx=F.norm(x)
        for y in buckets.get(slope(x),[]):
            tested+=1;A,B,C,D=y;ny=F.norm(y)
            cr=(a*A+33*b*B+3*c*C+11*d*D,a*B+b*A+c*D+d*C)
            require(a*C+11*b*D-c*A-11*d*B==0 and a*D+3*b*C-d*A-3*c*B==0,'parallel classification failed')
            if (4*(nx[0]+ny[0])-7*cr[0],4*(nx[1]+ny[1])-7*cr[1])==(4*72**2,0):pairs.append((x,y))
    return pairs,tested

def project(I,J,pairs):
    edges=[[] for _ in range(292*214)]
    for x,y in pairs:
        for m,i in I[x]:
            for n,j in J[y]:edges[214*m+n].append((i,j))
    for e in edges:
        e.sort();require(len(e)==len(set(e)),'duplicate cross edge')
    return edges

def libraries(B,V,EB,EV,new=True):
    libs=F.libraries(B,V,EB,EV)
    for side,lib,G,ee in zip(('B','V'),libs,(B,V),(EB,EV)):
        paths=[HERE.parent/f'hadwiger_nelson_mixed505_high_degree_attachments/new_{side}.txt']
        if new:paths.append(HERE/f'new_{side}.txt')
        for path in paths:
            for line in path.read_text().splitlines():
                c=tuple(map(int,line))
                require(len(c)==len(G) and set(c)<=set(range(4)) and all(c[i]!=c[j] for i,j in ee),'invalid component colouring')
                lib.append(c)
    return libs

PERMS=list(permutations(range(4)))
def witness(m,n,ee,libs):
    for ib,cb in enumerate(libs[0]):
        for iv,cv in enumerate(libs[1]):
            for ip,pi in enumerate(PERMS):
                if cb[m]==pi[cv[n]] and all(cb[i]!=pi[cv[j]] for i,j in ee):return ib,iv,ip
    return None

def digest(obj):return sha256((json.dumps(obj,separators=(',',':'))+'\n').encode()).hexdigest()

def run():
    B,V,EB,EV=sources();I,J=differences(B),differences(V)
    pairs,tested=contact_pairs(I,J);edges=project(I,J,pairs);libs=libraries(B,V,EB,EV)
    certificate=[tuple(map(int,line.split())) for line in (HERE/'contacts.tsv').read_text().splitlines() if line and not line.startswith('#')]
    require(certificate==[x+y for x,y in pairs],'compact contact certificate differs')
    stream=sha256();hist=Counter();used=Counter()
    for label,ee in enumerate(edges):
        m,n=divmod(label,214);w=witness(m,n,ee,libs)
        require(w is not None,'uncovered placement '+str((m,n)))
        ib,iv,ip=w;cb,cv=libs[0][ib],libs[1][iv];pi=PERMS[ip]
        require(cb[m]==pi[cv[n]] and all(cb[i]!=pi[cv[j]] for i,j in ee),'selected colouring failed')
        stream.update((json.dumps([m,n,ee,w],separators=(',',':'))+'\n').encode())
        hist[len(ee)]+=1;used[w]+=1
    return {'rotation':'(7+i sqrt(15))/8','source_sizes':[292,214], 'source_edges':[len(EB),len(EV)],
            'source_integer_denominator':72,'nonzero_difference_counts':[len(I),len(J)],
            'difference_product':len(I)*len(J),'parallel_pairs':tested,'exact_contact_difference_pairs':len(pairs),
            'contact_pairs_sha256':digest(pairs),'complete_placement_edges_sha256':digest(edges),
            'placements':len(edges),'strict_graph_order':505,'new_cross_edge_histogram':sorted(hist.items()),
            'library_sizes':list(map(len,libs)),'selected_witnesses':[[list(w),c] for w,c in sorted(used.items())],
            'complete_colour_coverage_sha256':stream.hexdigest(),'uncovered':0}
if __name__=='__main__':print(json.dumps(run(),indent=2))
