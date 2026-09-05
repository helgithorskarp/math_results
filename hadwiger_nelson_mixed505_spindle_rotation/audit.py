"""Independent all-difference-pair distance scan; no slope or local arithmetic."""
from pathlib import Path
from hashlib import sha256
from itertools import permutations,combinations
from collections import Counter
import importlib.util,json
HERE=Path(__file__).resolve().parent
PRIMES=(1321,5281)
ROOTS=((321,416,501),(1302,325,1874))

def require(ok,msg):
    if not ok:raise ValueError(msg)

def source():
    p=HERE.parent/'hadwiger_nelson_mixed506_fixed_rotation/audit.py'
    require(sha256(p.read_bytes()).hexdigest()=='2f16055d2986bc9b5810757cf77403414c4a990acbed46d2b7378c4d67981e41','independent source pin failed')
    s=importlib.util.spec_from_file_location('radical_source',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m.source() # Both integer arrays have denominator72; V is translated.

def delta(x,y):return tuple(a-b for a,b in zip(x,y))

def source_edges(G):
    # Cartesian norm in Q(sqrt(33)); all source labels, no imported edges.
    ee=[]
    for i,j in combinations(range(len(G)),2):
        a,b,c,d=delta(G[i],G[j])
        if a*a+33*b*b+3*c*c+11*d*d==5184 and a*b+c*d==0:ee.append((i,j))
    return ee

def modular(G,p,roots,rotate):
    from math import isqrt
    require(all(p%d for d in range(2,isqrt(p)+1)),'nonprime modulus')
    r3,r5,r11=roots
    require(all(r*r%p==d for r,d in zip(roots,(3,5,11))),'invalid radical image')
    inv72,inv8=pow(72,-1,p),pow(8,-1,p);out=[]
    for a,b,c,d in G:
        x=(a+b*r3*r11)*inv72%p;y=(c*r3+d*r11)*inv72%p
        if rotate:x,y=(7*x-r3*r5*y)*inv8%p,(r3*r5*x+7*y)*inv8%p
        out.append((x,y))
    return out

# Generic eight-dimensional real radical ring Q[sqrt3,sqrt5,sqrt11].
RAD=(3,5,11)
FACT=[1]*8
for mask in range(8):
    for bit,p in enumerate(RAD):
        if mask>>bit&1:FACT[mask]*=p

def add(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(x,c):return tuple(c*a for a in x)
def mul(x,y):
    z=[0]*8
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[i^j]+=a*b*FACT[i&j]
    return tuple(z)

def cartesian(x):
    a,b,c,d=x;re=[0]*8;im=[0]*8
    re[0]=a;re[5]=b;im[1]=c;im[4]=d
    return tuple(re),tuple(im)

SQ15=(0,0,0,1,0,0,0,0)
def exact_contact(x,y):
    xr,xi=cartesian(x);yr,yi=cartesian(y)
    wr=add(add(scale(xr,8),scale(yr,-7)),mul(SQ15,yi))
    wi=add(add(scale(xi,8),scale(yi,-7)),scale(mul(SQ15,yr),-1))
    return add(mul(wr,wr),mul(wi,wi))==(576**2,0,0,0,0,0,0,0)

def digest(obj):return sha256((json.dumps(obj,separators=(',',':'))+'\n').encode()).hexdigest()

def library(G,ee,side):
    paths=([HERE.parent/'hadwiger_nelson_nonmono159_moser_triple/colors_B.txt'] if side=='B' else
           [HERE.parent/'hadwiger_nelson_mixed505_anchor0/colors_H.txt'])
    paths += [HERE.parent/f'hadwiger_nelson_mixed505_high_degree_attachments/new_{side}.txt',HERE/f'new_{side}.txt']
    rows=[]
    for path in paths:
        for line in path.read_text().splitlines():
            row=[int(c) for c in line]
            require(len(row)==len(G) and all(0<=c<4 for c in row),'invalid colour domain')
            require(all(row[i]!=row[j] for i,j in ee),'improper component colouring')
            rows.append(row)
    return rows

def run(expected):
    B,V=source();EB,EV=source_edges(B),source_edges(V)
    require([len(B),len(V),len(EB),len(EV)]==[292,214,1251,977],'source graph differs')
    # Build differences as sets, then reconstruct incidences by endpoint lookup.
    diffs=[sorted({delta(x,y) for x in G for y in G if x!=y}) for G in (B,V)]
    X,Y=diffs;require([len(X),len(Y)]==expected['nonzero_difference_counts'],'difference sets differ')
    px=[modular(X,p,r,False) for p,r in zip(PRIMES,ROOTS)]
    py=[modular(Y,p,r,True) for p,r in zip(PRIMES,ROOTS)]
    p,p2=PRIMES;first=second=0;pairs=[];first_hash=sha256();second_hash=sha256()
    for i,(x,y) in enumerate(px[0]):
        for j,(a,b) in enumerate(py[0]):
            if ((x-a)**2+(y-b)**2-1)%p:continue
            first+=1;first_hash.update(f'{i},{j}\n'.encode())
            xx,yy=px[1][i];aa,bb=py[1][j]
            if ((xx-aa)**2+(yy-bb)**2-1)%p2:continue
            second+=1;second_hash.update(f'{i},{j}\n'.encode())
            if exact_contact(X[i],Y[j]):pairs.append((X[i],Y[j]))
    require(len(pairs)==expected['exact_contact_difference_pairs'] and digest(pairs)==expected['contact_pairs_sha256'],'complete exact contact stream differs')
    lookup=[{x:i for i,x in enumerate(G)} for G in (B,V)]
    ee=[[] for _ in range(292*214)]
    for x,y in pairs:
        ix=[(m,lookup[0][add4(a,x)]) for m,a in enumerate(B) if add4(a,x) in lookup[0]]
        iy=[(n,lookup[1][add4(a,y)]) for n,a in enumerate(V) if add4(a,y) in lookup[1]]
        for m,i in ix:
            for n,j in iy:ee[214*m+n].append((i,j))
    for e in ee:e.sort();require(len(e)==len(set(e)),'duplicate edge')
    require(digest(ee)==expected['complete_placement_edges_sha256'],'all placement edges differ')
    cb,cv=library(B,EB,'B'),library(V,EV,'V');perms=list(permutations(range(4)))
    stream=sha256();hist=Counter();used=Counter()
    for label,edges in enumerate(ee):
        m,n=divmod(label,214);selected=None
        # Build forbidden colour pairs once for each choice of source rows.
        for ib,left in enumerate(cb):
            for iv,right in enumerate(cv):
                banned={(left[i],right[j]) for i,j in edges}
                for ip,pi in enumerate(perms):
                    if pi[right[n]]!=left[m]:continue
                    if not any(pi[b]==a for a,b in banned):selected=(ib,iv,ip);break
                if selected is not None:break
            if selected is not None:break
        require(selected is not None,'uncovered placement')
        stream.update((json.dumps([m,n,edges,selected],separators=(',',':'))+'\n').encode())
        hist[len(edges)]+=1;used[selected]+=1
    require(stream.hexdigest()==expected['complete_colour_coverage_sha256'],'full colouring stream differs')
    require([list(x) for x in sorted(hist.items())]==expected['new_cross_edge_histogram'],'histogram differs')
    require([[list(w),c] for w,c in sorted(used.items())]==expected['selected_witnesses'],'selected witnesses differ')
    return {'all_difference_pairs_tested':len(X)*len(Y),'first_modulus_survivors':first,'both_moduli_survivors':second,
            'first_survivor_stream_sha256':first_hash.hexdigest(),'second_survivor_stream_sha256':second_hash.hexdigest(),
            'exact_contact_pairs':len(pairs),'independent_contact_and_placement_streams_match':True,
            'every_overlap_colouring_checked':len(ee),'complete_colouring_stream_matches':True,
            'solver_required':False,'slope_partition_used':False}

def add4(x,y):return tuple(a+b for a,b in zip(x,y))
if __name__=='__main__':print(json.dumps(run(json.loads((HERE/'expected.json').read_text())),indent=2))
