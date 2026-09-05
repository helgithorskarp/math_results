#!/usr/bin/env python3
"""Direct plane coordinates for a former library residual; no census imports."""
from pathlib import Path
from hashlib import sha256
from itertools import permutations
import json

HERE=Path(__file__).resolve().parent
ZERO=(0,)*8
FACTORS=tuple((3 if i&1 else 1)*(11 if i&2 else 1)*(13 if i&4 else 1) for i in range(8))

def require(ok,msg):
    if not ok:raise ValueError(msg)

def basis(**entries):
    out=[0]*8
    for k,v in entries.items():out[int(k[1:])]=v
    return tuple(out)

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,n):return tuple(n*x for x in a)
def mul(a,b):
    out=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i^j]+=x*y*FACTORS[i&j]
    return tuple(out)
def cmul(z,w):
    x,y=z;X,Y=w
    return add(mul(x,X),scale(mul(y,Y),-1)),add(mul(x,Y),mul(y,X))
def norm(z):return add(mul(z[0],z[0]),mul(z[1],z[1]))
def point(a):
    x,b,c,d=a
    return basis(k0=x,k3=b),basis(k1=c,k2=d)

def read_points(n):
    pins={159:'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',214:'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}
    raw=(HERE.parent/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes()
    require(sha256(raw).hexdigest()==pins[n],'wrong point source')
    require(raw.decode().splitlines()[0]=='# scale 12','wrong coordinate scale')
    rows=[]
    for line in raw.decode().splitlines():
        if not line or line.startswith('#'):continue
        a=tuple(map(int,line.split()))
        require(len(a)==16 and not any(a[i] for i in range(16) if i not in (0,5,9,12)),'unexpected source basis')
        rows.append(tuple(a[i] for i in (0,5,9,12)))
    require(len(rows)==len(set(rows))==n,'wrong point count')
    return rows

def read_colors(path,n):
    out=[tuple(map(int,s)) for s in path.read_text().splitlines()]
    require(all(len(c)==n and c[0]==0 and set(c)<=set(range(4)) for c in out),'invalid color labels')
    return out

def main():
    A=read_points(159);V=read_points(214)
    t=(basis(k0=5),basis(k2=1))
    original=[tuple(scale(x,6) for x in point(a)) for a in A]
    B=list(dict.fromkeys(original+[cmul(t,point(a)) for a in A]))
    require(len(B)==292 and B[0]==(ZERO,ZERO),'incorrect inner union')
    example=json.loads((HERE/'first_repair_example.json').read_text())
    p,q=example['B_anchor'],example['anchor']
    require((p,q)==(28,46) and B[p]==(ZERO,basis(k1=24)),'incorrect attachment')
    require(example['T']==['7/8','0','7/24','0'] and example['W']==['1/2','0','1/2','0'],'wrong polynomial')
    order=[p]+[i for i in range(292) if i!=p]
    BP=[tuple(scale(add(z,scale(w,-1)),8) for z,w in zip(B[i],B[p])) for i in order]
    H=[point(tuple(x-y for x,y in zip(v,V[q]))) for v in V]
    labels=[i for i in range(214) if i!=q]
    libB=read_colors(HERE.parent/'hadwiger_nelson_nonmono159_moser_triple/colors_B.txt',292)+read_colors(HERE/'new_B.txt',292)
    libV=read_colors(HERE.parent/'hadwiger_nelson_mixed505_anchor0/colors_H.txt',214)+read_colors(HERE/'new_V.txt',214)
    require((len(libB),len(libV))==(8,7),'wrong repaired libraries')
    perms=[(0,)+a for a in permutations((1,2,3))]
    results=[]
    for epsilon in (-1,1):
        u=(basis(k0=21,k7=-epsilon),basis(k1=7,k6=3*epsilon))
        require(norm(u)==basis(k0=48**2),'multiplier is not unit')
        T=(basis(k0=42),basis(k1=14));W=(basis(k0=24),basis(k1=24))
        uu,Tu=cmul(u,u),cmul(T,u)
        require(all(add(add(uu[k],scale(Tu[k],-1)),scale(W[k],48))==ZERO for k in [0,1]),'quadratic identity failed')
        image=[cmul(u,h) for h in H]
        require(image[q]==(ZERO,ZERO),'misplaced right anchor')
        points=BP+[image[i] for i in labels]
        require(len(points)==len(set(points))==505,'unexpected overlap')
        edges=[];cross=[];left=right=0
        for i,(x,y) in enumerate(points):
            for j in range(i+1,len(points)):
                X,Y=points[j]
                delta=(add(x,scale(X,-1)),add(y,scale(Y,-1)))
                if norm(delta)!=basis(k0=576**2):continue
                edges.append((i,j))
                if j<292:left+=1
                elif i==0 or i>=292:right+=1
                else:cross.append((i,labels[j-292]))
        require((len(edges),left,right,len(cross))==(2232,1251,977,4),'wrong strict graph')
        require(cross==[tuple(e) for e in example['cross_edges']],'wrong residual cross edges')
        def coloring(ib,iv,ip):
            cb,cv,perm=libB[ib],libV[iv],perms[ip]
            return tuple(cb[i]^cb[p] for i in order)+tuple(perm[cv[j]^cv[q]] for j in labels)
        baseline_success=0
        for ib in range(3):
            for iv in range(2):
                for ip in range(6):
                    c=coloring(ib,iv,ip)
                    baseline_success+=all(c[i]!=c[j] for i,j in edges)
        require(baseline_success==0,'example did not defeat the original library')
        witness=None
        for ib in range(8):
            for iv in range(7):
                for ip in range(6):
                    c=coloring(ib,iv,ip)
                    if all(c[i]!=c[j] for i,j in edges):
                        witness=(ib,iv,ip);break
                if witness is not None:break
            if witness is not None:break
        require(witness is not None,'repaired library failed direct graph')
        results.append({'epsilon':epsilon,'vertices':505,'strict_unit_edges':len(edges),'new_cross_edges':len(cross),
                        'old_library_successes':baseline_success,'new_library_witness':witness,
                        'edge_sha256':sha256(json.dumps(edges).encode()).hexdigest(),
                        'color_sha256':sha256(bytes(c)).hexdigest()})
    print(json.dumps({'real_radicals':[3,11,13],'coordinate_scale':576,'all_pairs_per_realization':127260,
                      'unit_and_quadratic_checked':True,'realizations':results},indent=2))

if __name__=='__main__':main()
