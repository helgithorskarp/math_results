"""Complete incoming270/90 atlas and the necessary charge selector for P17."""
from pathlib import Path
import itertools
import json
import hashlib
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'heesch_polyomino_corner_obstruction'
PINS={'corners.py': '45a035a10e4b881ca3bb26750f2947b382a6b66e65f87d403cade6ba04d29409', 'patterns.py': 'f497a2590f2311bbd31bff9fed4f16db47cf64f6b4ca071798943ccc7742d925', 'pairs.json': '52395c73e83ff3a1b023a1c50ebc43472caded160e4b0645c8fcbbbf905d4033', 'extension.py': 'e2fb72bb58423106ac50720f7019676ef2cc3b84803c79f9d0cc6ab0a33c388f'}
for name,digest in PINS.items():
    if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('changed dependency: '+name)
sys.path.insert(0,str(BASE))
from corners import QUADRANTS,choices,footprint,image_cell,normalize,variants,vertices
from patterns import pattern_classes
for name in ('corners','patterns'):
    if Path(sys.modules[name].__file__).resolve()!=BASE/(name+'.py'):
        raise ValueError('dependency imported from an unexpected path')

def bits(shape,v):
    return tuple((v[0]+dx,v[1]+dy) in shape for dx,dy in QUADRANTS)


def corner_inventory(shape,amount):
    return sorted((v,bits(shape,v).index(amount==1)) for v in vertices(shape)
                  if sum(bits(shape,v))==amount)


def matrix_records(tile,shapes):
    records={}
    for swap,sx,sy in itertools.product((False,True),(-1,1),(-1,1)):
        raw=tuple(image_cell(p,swap,sx,sy) for p in tile)
        g=min(x for x,y in raw),min(y for x,y in raw)
        shape=normalize(raw)
        matrix=((0,sx),(sy,0)) if swap else ((sx,0),(0,sy))
        records[shapes.index(shape)]={'matrix':matrix,'minimum':g,'shape':shape}
    if len(records)!=8:raise ValueError('this inversion audit requires asymmetric P17')
    return records


def mv(matrix,p):
    return tuple(sum(a*b for a,b in zip(row,p)) for row in matrix)


def inversion(code,records,shapes,tile):
    index,x,y=code;record=records[index];matrix=record['matrix']
    inverse=tuple(zip(*matrix));b=x-record['minimum'][0],y-record['minimum'][1]
    inv_record=next(r for r in records.values() if r['matrix']==inverse)
    ax,ay=mv(inverse,b)
    translation=inv_record['minimum'][0]-ax,inv_record['minimum'][1]-ay
    result=(shapes.index(inv_record['shape']),*translation)
    # Transform the actual neighbor footprint back to the canonical root.
    swap=bool(inverse[0][1]);sx=sum(inverse[0]);sy=sum(inverse[1])
    mapped={(u-ax,v-ay) for u,v in
            (image_cell(p,swap,sx,sy) for p in footprint(shapes[index],(x,y)))}
    if mapped!=set(tile):raise ValueError('affine inverse round trip failed')
    return result


def pool(data):
    tile=normalize(data['tile']);shapes=variants(tile);root=set(tile)
    tips=corner_inventory(root,1);reentrant=corner_inventory(root,3)
    records=matrix_records(tile,shapes);out=set();per_corner=[]
    for vertex,quadrant in reentrant:
        dx,dy=QUADRANTS[quadrant]
        possible=choices(shapes,(vertex[0]+dx,vertex[1]+dy),root)
        per_corner.append((vertex,quadrant,len(possible)))
        out.update((shapes.index(shape),*translation) for shape,translation,_ in possible)
    inverse={inversion(q,records,shapes,tile) for q in out}
    # Independent construction: anchor reentrant vertices of a provider on root tips.
    direct=set()
    for vertex,quadrant in tips:
        for index,shape in enumerate(shapes):
            for anchor,missing in corner_inventory(set(shape),3):
                if missing!=quadrant:continue
                translation=vertex[0]-anchor[0],vertex[1]-anchor[1]
                if not footprint(shape,translation)&root:direct.add((index,*translation))
    if direct!=inverse:raise ValueError('vertex and affine-inverse atlases differ')
    for code in inverse:
        if inversion(code,records,shapes,tile) not in out:raise ValueError('inverse atlas is not involutive')
    codes=sorted(inverse);squares=[footprint(shapes[i],(x,y)) for i,x,y in codes]
    receives=[];source_labels=[]
    for (index,x,y),square in zip(codes,squares):
        receives.append([i for i,(v,q) in enumerate(tips)
                         if sum(bits(square,v))==3 and not bits(square,v)[q]])
        if not receives[-1]:raise ValueError('provider has no charge')
        labels=[]
        matrix=records[index]['matrix'];inverse=tuple(zip(*matrix));g=records[index]['minimum']
        for j in receives[-1]:
            vertex=tips[j][0]
            original=mv(inverse,(vertex[0]-x+g[0],vertex[1]-y+g[1]))
            labels.append(next(k for k,(v,q) in enumerate(reentrant) if v==original))
        source_labels.append(labels)
    classes=set(pattern_classes(data));root_index=shapes.index(tile)
    excluded=[i for i,(index,x,y) in enumerate(codes)
              if (tile,shapes[index],x,y) in classes]
    conflicts={}
    for a,b in itertools.combinations(range(len(codes)),2):
        ia,xa,ya=codes[a];ib,xb,yb=codes[b]
        reason=[]
        if squares[a]&squares[b]:reason.append('overlap')
        if (shapes[ia],shapes[ib],xb-xa,yb-ya) in classes:reason.append('interior_pair')
        if reason:conflicts[(a,b)]=reason
    return {'tile':tile,'shapes':shapes,'root_orientation':root_index,'tips':tips,
            'reentrant':reentrant,'outgoing_count':len(out),'incoming_codes':codes,
            'per_corner':per_corner,'receives':receives,'source_labels':source_labels,'root_excluded':excluded,
            'conflicts':[(a,b,reason) for (a,b),reason in sorted(conflicts.items())]}


def formula(atlas,threshold):
    n=len(atlas['incoming_codes']);tips=atlas['tips'];flags=list(range(n+1,n+1+len(tips)))
    clauses=[[-i-1] for i in atlas['root_excluded']]
    clauses += [[-a-1,-b-1] for a,b,_ in atlas['conflicts']]
    for j,flag in enumerate(flags):
        owners=[i+1 for i,r in enumerate(atlas['receives']) if j in r]
        clauses.append([-flag,*owners])
        clauses.extend([[-owner,flag] for owner in owners])
    if not 0<=threshold<=len(flags):raise ValueError('invalid threshold')
    if threshold:
        clauses.extend(map(list,itertools.combinations(flags,len(flags)-threshold+1)))
    return n+len(flags),clauses
