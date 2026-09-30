"""Literal geometry and fraction-free determinant for one incidence pattern."""
from pathlib import Path
from collections import Counter, deque
import argparse
import copy
import hashlib
import itertools
import json
import math

BASE=Path(__file__).resolve().parent
POLYGON=[(1,0),(4,0),(4,3),(5,3),(5,4),(6,4),(6,5),
         (3,5),(3,4),(2,4),(2,3),(0,3),(0,1),(1,1)]
TILE={(x,y) for y,left,right in [(0,1,4),(1,0,4),(2,0,4),(3,2,5),(4,3,6)] for x in range(left,right)}
VERTICAL=list(range(1,14,2));HORIZONTAL=list(range(0,14,2))
COORDINATES=[(VERTICAL.index(j if j%2 else (j-1)%14),
              7+HORIZONTAL.index(j if not j%2 else j-1)) for j in range(14)]
FIXTURE_PATH='heesch_polyomino_star_b_obstruction/positive_comparison.json'
FIXTURE_SHA='f352747cf676d96f005e2c06c2d3b3997af2dab032f9d06c250838587607d5eb'


def require(condition,message):
    if not condition: raise ValueError(message)


def transformed(M,p):
    return tuple(sum(M[a][b]*p[b] for b in [0,1]) for a in [0,1])


def image_cells(M):
    cells=set()
    for x,y in TILE:
        corners=[transformed(M,(x+u,y+v)) for u,v in itertools.product([0,1],repeat=2)]
        cells.add((min(a for a,b in corners),min(b for a,b in corners)))
    return cells


def normalize(cells):
    x0,y0=min(x for x,y in cells),min(y for x,y in cells)
    return tuple(sorted((x-x0,y-y0) for x,y in cells))


def disc(cells):
    def flood(start,domain):
        seen={start};todo=deque([start])
        while todo:
            x,y=todo.popleft()
            for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if p in domain and p not in seen: seen.add(p);todo.append(p)
        return seen
    require(flood(min(cells),cells)==cells,'packing union is not edge connected')
    x0,x1=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    y0,y1=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    empty={(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)}-cells
    require(flood((x0,y0),empty)==empty,'packing union has a hole')
    for x,y in {(x+u,y+v) for x,y in cells for u,v in itertools.product([0,1],repeat=2)}:
        occupied={i for i,p in enumerate([(x,y),(x-1,y),(x,y-1),(x-1,y-1)]) if p in cells}
        require(occupied not in [{0,3},{1,2}],'packing union has a vertex pinch')


def canonical(row):
    nonzero=[abs(a) for a in row if a]
    require(nonzero,'vacuous incidence constraint')
    divisor=math.gcd(*nonzero)
    if next(a for a in row if a)<0: divisor=-divisor
    return [a//divisor for a in row]


def determinant(matrix):
    a=[list(row) for row in matrix];n=len(a);sign=1;previous=1
    require(n>0 and all(len(r)==n for r in a),'minor is not square')
    for k in range(n-1):
        if not a[k][k]:
            pivot=next((r for r in range(k+1,n) if a[r][k]),None)
            if pivot is None: return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        pivot=a[k][k]
        for r in range(k+1,n):
            for c in range(k+1,n):
                numerator=a[r][c]*pivot-a[r][k]*a[k][c]
                require(numerator%previous==0,'nonexact Bareiss division')
                a[r][c]=numerator//previous
            a[r][k]=0
        previous=pivot
    return sign*a[-1][-1]


def verify(data):
    require(data['agent']=='six-heesch-1' and data['role']=='researcher','wrong author metadata')
    require(data['prototype_vertices']==[list(p) for p in POLYGON],'wrong prototype vertex labels')
    require(data['coordinate_variables']==[list(p) for p in COORDINATES],'wrong edge variable map')
    require(data['variables']==26 and data['scale_variable']==6,'wrong coordinate dimensions')
    require(data['fixture_path']==FIXTURE_PATH and data['fixture_sha256']==FIXTURE_SHA,'wrong fixture pin')
    fixture_path=BASE.parent/FIXTURE_PATH
    fixture_bytes=fixture_path.read_bytes()
    require(hashlib.sha256(fixture_bytes).hexdigest()==FIXTURE_SHA,'positive fixture bytes changed')
    fixture=json.loads(fixture_bytes)
    first=[r for r in fixture['poses'] if r['level']<=1]
    require(len(first)==7 and len(data['copies'])==7,'wrong seven-copy template')
    baseline=[POLYGON[j][0] for j in VERTICAL]+[POLYGON[j][1] for j in HORIZONTAL]
    require(baseline[5]==0 and baseline[7]==0 and baseline[6]==1,'wrong translation/scale gauges')
    D4=[]
    for swap in [False,True]:
        for sx,sy in itertools.product([-1,1],repeat=2):
            D4.append(((0,sx),(sy,0)) if swap else ((sx,0),(0,sy)))
    images=sorted({normalize(image_cells(M)) for M in D4})
    points=[];expressions=[];footprints=[]
    for c,entry in enumerate(data['copies']):
        require(entry['code']==first[c]['code'] and entry['level']==first[c]['level'],'wrong fixture copy')
        M=tuple(map(tuple,entry['matrix']))
        require(M in D4 and all(type(v) is int for row in M for v in row),'matrix is not D4')
        i,tx,ty=entry['code']
        raw=image_cells(M)
        require(normalize(raw)==images[i],'matrix disagrees with canonical image code')
        shift=(tx-min(x for x,y in raw),ty-min(y for x,y in raw))
        require(entry['baseline_translation']==list(shift),'wrong baseline affine translation')
        if c==0:
            require(M==((1,0),(0,1)) and shift==(0,0),'root is not fixed')
        else: baseline.extend(shift)
        points.append([tuple(v[a]+shift[a] for a in [0,1]) for v in map(lambda p:transformed(M,p),POLYGON)])
        footprints.append({(x+shift[0],y+shift[1]) for x,y in raw})
        expr=[]
        for xvar,yvar in COORDINATES:
            axes=[]
            for a in [0,1]:
                row=[0]*26
                row[xvar]=M[a][0];row[yvar]=M[a][1]
                if c: row[14+2*(c-1)+a]=1
                axes.append(row)
            expr.append(axes)
        expressions.append(expr)
    require(data['baseline']==baseline and all(type(z) is int for z in baseline),'wrong baseline null vector')
    for c,ps in enumerate(points):
        for j,p in enumerate(ps):
            require(tuple(sum(a*b for a,b in zip(row,baseline)) for row in expressions[c][j])==p,'wrong coordinate expression')
    require(not any(a&b for a,b in itertools.combinations(footprints,2)),'positive first template overlaps')
    whole=set().union(*footprints)
    halo={(x+u,y+v) for x,y in footprints[0] for u,v in itertools.product([-1,0,1],repeat=2)}-footprints[0]
    require(halo<=whole,'positive root is not strictly interior')
    root_vertices={(x+u,y+v) for x,y in footprints[0] for u,v in itertools.product([0,1],repeat=2)}
    for cells in footprints[1:]:
        require(any((x+u,y+v) in root_vertices for x,y in cells for u,v in itertools.product([0,1],repeat=2)), 'positive copy misses root contact')
    disc(whole)
    constraints=data['constraints']
    require(len(constraints)==25,'missing or additional certificate row')
    def location(value):
        require(type(value) is list and len(value)==2 and all(type(v) is int for v in value),'malformed corner address')
        c,j=value
        require(0<=c<7 and 0<=j<14,'corner address out of range')
        return c,j
    rows=[];kinds=Counter()
    for constraint in constraints:
        reason=constraint['reason'];kind=reason['kind'];kinds[kind]+=1
        if kind=='prototype_gauge':
            require(reason['value']==0 and reason['axis'] in ['x','y'],'wrong prototype gauge')
            row=[0]*26;row[5 if reason['axis']=='x' else 7]=1
        elif kind=='vertex_equality':
            c,j=location(reason['first']);d,k=location(reason['second']);axis=reason['axis']
            require(type(axis) is int and axis in [0,1],'wrong coordinate axis')
            require(c!=d and points[c][j]==points[d][k]==tuple(reason['point']),'false baseline vertex equality')
            row=[a-b for a,b in zip(expressions[c][j][axis],expressions[d][k][axis])]
        elif kind=='corner_on_edge':
            c,j=location(reason['corner']);edge=reason['edge']
            require(type(edge) is list and len(edge)==3 and all(type(v) is int for v in edge),'malformed edge address')
            d,k,nextk=edge
            require(0<=d<7 and 0<=k<14 and nextk==(k+1)%14,'wrong edge address')
            p=points[c][j];q=points[d][k];r=points[d][nextk]
            axis=0 if q[0]==r[0] else 1
            require(c!=d and q[axis]==r[axis] and reason['normal_axis']==axis,'wrong normal axis')
            require(p==tuple(reason['point']) and p[axis]==q[axis] and min(q[1-axis],r[1-axis])<p[1-axis]<max(q[1-axis],r[1-axis]),'false baseline corner-on-edge incidence')
            row=[a-b for a,b in zip(expressions[c][j][axis],expressions[d][k][axis])]
        else: raise ValueError('unknown geometric constraint kind')
        row=canonical(row)
        pairs=constraint['coefficients']
        require(type(pairs) is list and all(type(p) is list and len(p)==2 and all(type(x) is int for x in p) for p in pairs),'malformed sparse coefficients')
        require(pairs==[[i,a] for i,a in enumerate(row) if a],'stored row differs from literal incidence')
        require(sum(a*b for a,b in zip(row,baseline))==0,'baseline is not a null vector')
        rows.append(row)
    require(len({tuple(r) for r in rows})==25,'duplicate certificate rows')
    require(dict(kinds)=={'vertex_equality':19,'corner_on_edge':4,'prototype_gauge':2},'wrong incidence counts')
    minor=[[a for j,a in enumerate(row) if j!=6] for row in rows]
    value=determinant(minor)
    require(value==2 and data['minor_determinant']==value,'false nonsingular minor')
    return {'agent':'six-heesch-1','role':'researcher','status':'literal incidences and exact determinant verified',
            'prototype_vertices':14,'prototype_edge_coordinates':14,'copy_translations':12,'variables':26,
            'copies':7,'first_packing_cells':len(whole),'constraints':25,'constraint_kinds':dict(kinds),
            'minor_dimension':25,'minor_determinant':value,'scale_coordinate':6,
            'kernel_conclusion':'all shape coordinates and all copy translations are uniform multiples of the baseline',
            'fixture_sha256':FIXTURE_SHA}


def controls(data):
    tests=[]
    bad=copy.deepcopy(data);bad['constraints'].pop();tests.append(('deleted constraint',bad))
    bad=copy.deepcopy(data);bad['constraints'][0]['coefficients'][0][1]*=-1;tests.append(('altered coefficient',bad))
    bad=copy.deepcopy(data);bad['constraints'][0]['reason']['point'][0]+=1;tests.append(('false incidence point',bad))
    bad=copy.deepcopy(data);bad['copies'][1]['matrix'][0][0]+=2;tests.append(('invalid orientation',bad))
    bad=copy.deepcopy(data);bad['copies'][1]['baseline_translation'][0]+=1;tests.append(('shifted baseline copy',bad))
    bad=copy.deepcopy(data);bad['prototype_vertices'][0][0]+=1;tests.append(('changed prototype vertex',bad))
    rejected=[]
    for label,bad in tests:
        try: verify(bad)
        except ValueError: rejected.append(label)
        else: raise ValueError('malformed control accepted: '+label)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    certificate=BASE/'certificate.json'
    data=json.loads(certificate.read_text())
    result=verify(data)
    result['certificate_sha256']=hashlib.sha256(certificate.read_bytes()).hexdigest()
    if args.controls: result['rejected_controls']=controls(data)
    if args.expected:
        require(not args.controls,'expected output is for the plain reader')
        require(result==json.loads(args.expected.read_text()),'expected result differs')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
