#!/usr/bin/env python3
"""Complete two-circle enumeration and a conservative integer triangle screen."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, product
from collections import defaultdict
from math import isqrt
import argparse, json
from reproduce import HERE, SEED, g, seed_check, require, sha
k=g.k
encode=g.encode
strict_edges=g.strict_edges

T=1<<100;GRID=1<<32
RAD=(1,3,5,15,11,33,55,165)

def ceildiv(a,b):return -((-a)//b)
def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivsub(a,b):return a[0]-b[1],a[1]-b[0]
def ivmul(a,b):
    z=[x*y for x in a for y in b];return min(z)//T,ceildiv(max(z),T)
def ivsquare(a):
    lo=0 if a[0]<=0<=a[1] else min(a[0]*a[0],a[1]*a[1]);hi=max(a[0]*a[0],a[1]*a[1]);return lo//T,ceildiv(hi,T)
def ivroot(a):
    if a[0]<0:raise ValueError('negative interval root')
    lo=isqrt(a[0]*T);hi=isqrt(a[1]*T);return lo,hi+(hi*hi<a[1]*T)
def coord(row):
    lo=hi=0
    for c,d in zip(row,RAD):
        r=isqrt(d*T*T);rr=r+(r*r<d*T*T)
        lo+=c*(r if c>=0 else rr);hi+=c*(rr if c>=0 else r)
    return lo//96,ceildiv(hi,96)
def squared_coeff(row):
    out=[0]*8
    for block in (row[:8],row[8:]):
        for i in range(8):
            for j in range(i,8):out[i^j]+=(1 if i==j else 2)*block[i]*block[j]*RAD[i&j]
    return tuple(out)


def enumerate_centres(rows, moved, make_nonk):
    intervals=[(coord(r[:8]),coord(r[8:])) for r in rows]
    exact=[(tuple(Q(v,96) for v in r[:8]),tuple(Q(v,96) for v in r[8:])) for r in rows]
    cache={};centres={};nonk=[];maxwidth=0
    stats={'pairs':0,'inside_pairs':0,'K_pairs':0,'nonK_pairs':0,'tangent_pairs':0}
    for i,j in combinations(range(len(rows)),2):
        stats['pairs']+=1
        dx=ivsub(intervals[j][0],intervals[i][0]);dy=ivsub(intervals[j][1],intervals[i][1])
        s=ivadd(ivsquare(dx),ivsquare(dy))
        if s[0]>4*T:continue
        coefficient=squared_coeff([b-a for a,b in zip(rows[i],rows[j])])
        if coefficient==(4*96*96,)+(0,)*7:
            stats['tangent_pairs']+=1;root=k.zero(3)
        else:
            require(0<s[0]<=s[1]<4*T,'unseparated squared distance')
            stats['inside_pairs']+=1
            if coefficient not in cache:
                field_s=tuple(Q(v,96*96) for v in coefficient)
                rho=k.sub(k.inv(field_s,3),k.const(3,Q(1,4)))
                cache[coefficient]=k.field_sqrt(rho,3)
            root=cache[coefficient]
        if root is not None:
            if coefficient!=(4*96*96,)+(0,)*7:stats['K_pairs']+=1
            middle=g.scale(g.add(exact[i],exact[j]),Q(1,2));d=g.sub(exact[j],exact[i])
            offset=(k.neg(k.mul(d[1],root,3)),k.mul(d[0],root,3))
            for point in set([g.add(middle,offset),g.sub(middle,offset)]):
                centres.setdefault(point,set()).update((i,j))
            continue
        stats['nonK_pairs']+=1
        if not make_nonk:continue
        rho=(T*T//s[1]-T//4,ceildiv(T*T,s[0])-T//4);rt=ivroot(rho)
        mx0=ivadd(intervals[i][0],intervals[j][0]);my0=ivadd(intervals[i][1],intervals[j][1])
        mx=(mx0[0]//2,ceildiv(mx0[1],2));my=(my0[0]//2,ceildiv(my0[1],2))
        wx=ivmul((-dy[1],-dy[0]),rt);wy=ivmul(dx,rt)
        for sign in (-1,1):
            x=ivadd(mx,wx) if sign==1 else ivsub(mx,wx)
            y=ivadd(my,wy) if sign==1 else ivsub(my,wy)
            width=max(x[1]-x[0],y[1]-y[0]);maxwidth=max(maxwidth,width)
            require(width<=T//(1<<40) and max(map(abs,x+y))<16*T,'enclosure width or range')
            gx=((x[0]+x[1])*GRID)//(2*T);gy=((y[0]+y[1])*GRID)//(2*T)
            require(max(abs(gx*T-x[0]*GRID),abs(gx*T-x[1]*GRID),
                        abs(gy*T-y[0]*GRID),abs(gy*T-y[1]*GRID))<=2*T,'grid error bound')
            nonk.append([i,j,sign,gx,gy,int(i in moved or j in moved)])
    stats.update(K_points=len(centres),max_interval_width_scaled=maxwidth)
    return centres,nonk,stats


def screen(points):
    S=1<<32;H=1<<28;MARGIN=1<<40;LOW=S*S-MARGIN;HIGH=S*S+MARGIN
    cells=defaultdict(list)
    for i,p in enumerate(points):cells[p[3]//H,p[4]//H].append(i)
    offsets=[]
    for x,y in product(range(-18,19),repeat=2):
        a=max(0,abs(x)-1)*H;b=max(0,abs(y)-1)*H;c=(abs(x)+1)*H;d=(abs(y)+1)*H
        if a*a+b*b<=HIGH and c*c+d*d>=LOW:offsets.append((x,y))
    triangles=set();tests=0;annulus=0
    for i,p in enumerate(points):
        if not p[5]:continue
        x,y=p[3],p[4];cx,cy=x//H,y//H;nb=[]
        for ox,oy in offsets:
            for j in cells.get((cx+ox,cy+oy),()):
                if i==j:continue
                tests+=1;dx=x-points[j][3];dy=y-points[j][4];z=dx*dx+dy*dy
                if LOW<=z<=HIGH:nb.append(j)
        annulus+=len(nb)
        for j,l in combinations(nb,2):
            dx=points[j][3]-points[l][3];dy=points[j][4]-points[l][4];z=dx*dx+dy*dy
            if LOW<=z<=HIGH:triangles.add(tuple(sorted((i,j,l))))
    return sorted(triangles),{'grid_offsets':len(offsets),'coordinate_pair_tests':tests,'directed_annulus_pairs':annulus}


def generate(output):
    construction=json.loads((HERE/'construction.json').read_text());data=(SEED/'certificate.json').read_bytes()
    require(sha(data)==construction['seed_certificate_sha256'],'seed certificate hash')
    cert=json.loads(data);inputs=seed_check.load_inputs(cert)
    labels,rows,_=seed_check.construct(cert,inputs)
    coordinate_input=inputs['hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json']['coordinates']
    original=[]
    for i in range(509):
        row=[96*Q(c) for axis in coordinate_input[str(i)] for c in axis]
        require(all(c.denominator==1 for c in row),'original coordinate scale')
        original.append(tuple(map(int,row)))
    old,_,oldstats=enumerate_centres(original,set(),False)
    current,nonk,currentstats=enumerate_centres(rows,{i for i,u in enumerate(labels) if u>=509},True)
    seed={(tuple(Q(c,96) for c in r[:8]),tuple(Q(c,96) for c in r[8:])) for r in rows}
    require(seed<=set(current),'seed not regenerated by its unit neighbours')
    ordered=sorted(set(current)-seed)
    records=[{'point':encode(p),'neighbours':sorted(current[p]),'fresh':p not in old} for p in ordered]
    pairs,_=strict_edges(ordered);ns=[set() for _ in ordered]
    for a,b in pairs:ns[a].add(b);ns[b].add(a)
    triangles=sorted((a,b,c) for a,b in pairs for c in ns[a]&ns[b] if b<c and
                     (records[a]['fresh'] or records[b]['fresh'] or records[c]['fresh']))
    nonk_tri,screenstats=screen(nonk)
    result={'original_census':oldstats,'seed_census':currentstats,'external_K_points':len(records),
            'fresh_K_points':sum(r['fresh'] for r in records),'K_triangles':len(triangles),
            'nonK_points':len(nonk),'fresh_nonK_points':sum(p[5] for p in nonk),
            'nonK_triangle_candidates':len(nonk_tri),'screen':screenstats}
    expected=json.loads((HERE/'gate_certificate.json').read_text())['geometry_summary']
    require(result==expected,'geometry census mismatch')
    output.mkdir(parents=True,exist_ok=True)
    (output/'gate_geometry.json').write_text(json.dumps({'K_points':records,'K_triangles':triangles,
        'nonK_points':nonk,'nonK_triangles':nonk_tri,'summary':result},separators=(',',':'))+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();print(json.dumps(generate(args.output),sort_keys=True))
