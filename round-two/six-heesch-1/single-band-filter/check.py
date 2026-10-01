"""Solver-free checks of a bounded integral P192 band-stretch classification."""
from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path
import time

from upper import Geometry, Cover, require, flood

HERE=Path(__file__).resolve().parent


def normalize(cs):
    cs=list(map(tuple,cs));require(cs and len(cs)==len(set(cs)),'empty/duplicate prototype')
    require(all(len(p)==2 and all(type(z) is int for z in p) for p in cs),'noninteger prototype')
    x=min(p[0] for p in cs);y=min(p[1] for p in cs)
    return tuple(sorted((a-x,b-y) for a,b in cs))


def images(cs):
    # Definition-level signed permutation images, distinct from upper.image.
    return tuple(sorted({normalize([(sx*(y if swap else x),sy*(x if swap else y)) for x,y in cs])
                         for swap,sx,sy in product((False,True),(-1,1),(-1,1))}))


def pixels(shapes,p):
    require(len(p)==3 and all(type(z) is int for z in p),'malformed positive pose')
    o,x,y=p;require(0<=o<len(shapes),'positive orientation outside domain')
    return {(a+x,b+y) for a,b in shapes[o]}


def halo(cs):
    return {(x+dx,y+dy) for x,y in cs for dx,dy in product((-1,0,1),repeat=2)}-set(cs)


def disc(cs):
    if not cs or flood(cs,min(cs))!=cs:return False
    vertices={(x-dx,y-dy) for x,y in cs for dx,dy in product((0,1),repeat=2)}
    for x,y in vertices:
        bits=[q in cs for q in ((x,y),(x+1,y),(x,y+1),(x+1,y+1))]
        if bits in ([True,False,False,True],[False,True,True,False]):return False
    xmin=min(x for x,y in cs)-1;xmax=max(x for x,y in cs)+1
    ymin=min(y for x,y in cs)-1;ymax=max(y for x,y in cs)+1
    empty={(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)}-cs
    return flood(empty,(xmin,ymin))==empty


def coronas(cs,levels):
    shapes=images(cs);occupied=set();stats=[];count=0
    require(len(levels)==4 and len(levels[0])==1 and pixels(shapes,levels[0][0])==set(cs),'wrong three-corona root')
    for k,ps in enumerate(levels):
        old=set(occupied)
        for p in ps:
            fp=pixels(shapes,p);require(not occupied&fp,'positive whole-copy overlap')
            if k:require(bool(fp&halo(old)),'positive copy misses preceding prefix')
            occupied.update(fp);count+=1
        if k:require(halo(old)<=occupied,'incomplete positive halo')
        require(disc(occupied),'positive prefix is not a closed disc')
        stats.append(dict(level=k,copies=count,cells=len(occupied)))
    return stats


def periodic(cs,record):
    shapes=images(cs);a,b=record['periods']
    require(all(len(p)==2 and all(type(z) is int for z in p) for p in (a,b)),'noninteger period')
    d=a[0]*b[1]-a[1]*b[0];require(d>0,'nonpositive determinant')
    poses=record['fundamental_poses'];require(len(poses)*len(cs)==d,'periodic area mismatch')
    def residue(p):
        x,y=p;return (b[1]*x-b[0]*y)%d,(-a[1]*x+a[0]*y)%d
    seen=set()
    for p in poses:
        for q in pixels(shapes,p):
            r=residue(q);require(r not in seen,'periodic cell collision');seen.add(r)
    reps=[];xs=(0,a[0],b[0],a[0]+b[0]);ys=(0,a[1],b[1],a[1]+b[1])
    for x in range(min(xs),max(xs)+1):
        for y in range(min(ys),max(ys)+1):
            u=b[1]*x-b[0]*y;v=-a[1]*x+a[0]*y
            if 0<=u<d and 0<=v<d:reps.append((x,y))
    require(len(reps)==d and set(map(residue,reps))==seen,'fundamental parallelogram coverage failed')
    for lev in record['levels']:
        for o,x,y in lev:
            require(any(o==ro and residue((x-tx,y-ty))==(0,0) for ro,tx,ty in poses),'positive copy outside periodic orbit')
    return dict(fundamental_copies=len(poses),determinant=d,distinct_residues=len(seen))


def family(base):
    out=[];seen=set()
    for axis in (0,1):
        for band in range(max(p[axis] for p in base)+1):
            for extra in range(1,5):
                cells=set()
                for p in base:
                    if p[axis]==band:
                        for n in range(extra+1):q=list(p);q[axis]+=n;cells.add(tuple(q))
                    else:q=list(p);q[axis]+=extra*(p[axis]>band);cells.add(tuple(q))
                cs=normalize(cells)
                if len(cs)<=19:continue
                key=min(images(cs))
                if key in seen:continue
                seen.add(key);out.append(dict(index=len(out),axis=axis,band=band,extra=extra,cells=cs))
    require(len(out)==37,'family coverage changed')
    return out


def catalog(data,certificate,items):
    lower=[r['index'] for r in data['tilers']];upper=[r['index'] for r in certificate['records']]
    require(lower==[2,9,22] and len(upper)==len(set(upper))==34 and set(lower).isdisjoint(upper), 'invalid classification catalogs')
    require(set(lower)|set(upper)==set(range(len(items))),'incomplete classification coverage')


def upper_case(item,record):
    g=Geometry(item['cells']);bad=set();steps=0
    require(record['excluded_integer_depth']==(3 if item['index']==5 else 2),'unexpected upper depth')
    for c in record['corner_certificates']:
        p=tuple(c['type']);require(p in g.integer_contacts,'corner support is not a whole-copy contact')
        steps+=g.corner([g.root,p],c['certificate'])
        # Reverse the same unordered support, then apply the inverse D4 isometry.
        bad.update((p,g.relative(p,g.root)))
    cover=Cover(g,[g.root],bad);stars=sorted(cover.enumerate())
    recorded=sorted(tuple(map(tuple,ps)) for ps in record['root_stars'])
    require(stars==recorded,'complete first-surround catalog differs')
    nodes=cover.nodes
    if item['index']==5:
        require(len(stars)==1,'special case has more than one first surround')
        c=Cover(g,[g.root]+list(stars[0]),bad)
        require(not c.enumerate(),'third-corona necessary second surround exists')
        nodes+=c.nodes
    else:require(not stars,'second-corona necessary first surround exists')
    return dict(index=item['index'],area=len(g.cells),excluded_integer_depth=record['excluded_integer_depth'],
                corner_certificates=len(record['corner_certificates']),forced_steps=steps,cover_nodes=nodes)


def validate(data,certificate):
    require(data['agent']=='six-heesch-1' and data['role']=='researcher','wrong provenance')
    base=normalize(data['base_cells']);require(len(base)==17 and data['primary_index']==192,'wrong primary seed')
    items=family(base);catalog(data,certificate,items);results=[];tilers=[]
    for r in certificate['records']:results.append(upper_case(items[r['index']],r))
    for r in data['tilers']:
        item=items[r['index']]
        require((item['axis'],item['band'],item['extra'])==tuple(r['stretch']),'wrong tiling case')
        cs=item['cells'];checks=coronas(cs,r['levels']);q=periodic(cs,r)
        # Positive control: the necessary cover engine admits these exact copies.
        g=Geometry(cs);fixed=[g.root]
        for level in r['levels'][1:]:
            c=Cover(g,fixed,set());require(c.accepts(list(map(tuple,level))),'released-domain positive control failed')
            fixed+=list(map(tuple,level))
        tilers.append(dict(index=r['index'],area=len(cs),coronas=checks,periodic=q))
    return dict(agent='six-heesch-1',role='researcher',family_size=len(items),integer_non_tilers=results,
                plane_tilers=tilers,corner_certificates=sum(r['corner_certificates'] for r in results),
                forced_steps=sum(r['forced_steps'] for r in results),cover_nodes=sum(r['cover_nodes'] for r in results),
                scope='Exactly three integer-grid plane tilers and three-corona disc cases in the specified37-shape family. Other34 have integer-prefix upper obstructions, not arbitrary-motion upper bounds. Finite-five remains open.')


def controls(data,certificate):
    rejected=[];items=family(normalize(data['base_cells']))
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name)
        else:raise ValueError('malformed control accepted: '+name)
    broken=deepcopy(certificate);broken['records'].pop()
    reject('missing_case',lambda:catalog(data,broken,items))
    row=next(r for r in certificate['records'] if r['corner_certificates']);g=Geometry(items[row['index']]['cells'])
    c=deepcopy(row['corner_certificates'][0]);c['certificate']['empty'][0]+=100000
    reject('new_vertex_improperly_required',lambda:g.corner([g.root,tuple(c['type'])],c['certificate']))
    c=deepcopy(row['corner_certificates'][0]);c['certificate']['empty'][2]=4
    reject('invalid_quadrant',lambda:g.corner([g.root,tuple(c['type'])],c['certificate']))
    special=deepcopy(next(r for r in certificate['records'] if r['index']==5));special['root_stars'][0].pop()
    reject('wrong_complete_first_catalog',lambda:upper_case(items[5],special))
    r=deepcopy(data['tilers'][0]);r['levels'][3].pop()
    reject('missing_outer_copy',lambda:coronas(items[r['index']]['cells'],r['levels']))
    r=deepcopy(data['tilers'][0]);r['fundamental_poses'].append(r['fundamental_poses'][0])
    reject('duplicate_periodic_copy',lambda:periodic(items[r['index']]['cells'],r))
    r=deepcopy(data['tilers'][0]);r['periods'][1][1]+=1
    reject('wrong_period',lambda:periodic(items[r['index']]['cells'],r))
    return rejected


def main():
    start=time.monotonic();data=json.loads((HERE/'input.json').read_text());certificate=json.loads((HERE/'certificate.json').read_text())
    require(hashlib.sha256((HERE/'upper.py').read_bytes()).hexdigest()==data['upper_source']['sha256'],'vendored geometry changed')
    result=validate(data,certificate);result['rejected_controls']=controls(data,certificate)
    require(time.monotonic()-start<90,'reader wall guard; incomplete')
    expected=HERE/'expected.json'
    if expected.exists():require(result==json.loads(expected.read_text()),'expected result changed')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
