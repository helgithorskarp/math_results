"""Independent centered-square, rectangle, and bounding-box audits."""
from fractions import Fraction
from pathlib import Path
import itertools
import json


def require(condition,message):
    if not condition:raise ValueError(message)


def image_point(point,turns,mirror):
    x,y=point
    if mirror:x=-x
    for _ in range(turns):x,y=-y,x
    return x,y


def image_squares(squares,turns,mirror):
    result=[]
    for x,y in squares:
        u,v=image_point((2*x+1,2*y+1),turns,mirror)
        require(u%2==v%2==1,'square centers left the odd mesh')
        result.append(((u-1)//2,(v-1)//2))
    return tuple(sorted(result))


def normalized(squares):
    ox=min(x for x,y in squares);oy=min(y for x,y in squares)
    return tuple(sorted((x-ox,y-oy) for x,y in squares))


def orientations(tile):
    return tuple(sorted({normalized(image_squares(tile,k,m)) for k in range(4) for m in (False,True)}))


def translated(shape,x,y):
    return tuple((a+x,b+y) for a,b in shape)


def overlap(a,b):
    return any(max(x,u)<min(x+1,u+1) and max(y,v)<min(y+1,v+1)
               for x,y in a for u,v in b)


SIGNS=((1,1),(-1,1),(-1,-1),(1,-1))
LOWERS=((0,0),(-1,0),(-1,-1),(0,-1))


def quadrants(squares,vertex):
    return tuple(any(x<=Fraction(4*vertex[0]+sx,4)<x+1
                         and y<=Fraction(4*vertex[1]+sy,4)<y+1 for x,y in squares)
                 for sx,sy in SIGNS)


def mesh_vertices(squares):
    return sorted({(x+dx,y+dy) for x,y in squares for dx in (0,1) for dy in (0,1)})


def types(squares,count):
    result=[]
    for vertex in mesh_vertices(squares):
        qs=quadrants(squares,vertex)
        if sum(qs)==count:result.append((vertex,qs.index(count==1)))
    return result


def direct_pool(tile,shapes,tips):
    result=set()
    for vertex,missing in tips:
        for i,shape in enumerate(shapes):
            for x in range(vertex[0]-max(a for a,b in shape)-1,vertex[0]+1):
                for y in range(vertex[1]-max(b for a,b in shape)-1,vertex[1]+1):
                    moved=translated(shape,x,y);qs=quadrants(moved,vertex)
                    if sum(qs)==3 and not qs[missing] and not overlap(moved,tile):
                        result.add((i,x,y))
    return sorted(result)


def map_to_tile(squares,tile):
    results=[]
    for k in range(4):
        for mirror in (False,True):
            moved=image_squares(squares,k,mirror)
            if normalized(moved)==tile:
                results.append((k,mirror,(min(x for x,y in moved),min(y for x,y in moved))))
    require(len(results)==1,'P17 must have a unique orientation inverse')
    return results[0]


def relative(first,second,tile,shapes):
    k,mirror,(ox,oy)=map_to_tile(first,tile)
    moved=image_squares(second,k,mirror)
    return shapes.index(normalized(moved)),min(x for x,y in moved)-ox,min(y for x,y in moved)-oy


def forbidden(first,second,tile,shapes,library):
    return relative(first,second,tile,shapes) in library or relative(second,first,tile,shapes) in library


def boundary_disc(squares):
    """One simple directed boundary cycle plus edge-connected cells."""
    shape=set(squares);require(bool(shape),'empty disc input')
    reached={next(iter(shape))};pending=list(reached)
    while pending:
        x,y=pending.pop()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            p=x+dx,y+dy
            if p in shape and p not in reached:reached.add(p);pending.append(p)
    if reached!=shape:return False
    directed=[]
    for x,y in shape:
        if (x,y-1) not in shape:directed.append(((x,y),(x+1,y)))
        if (x+1,y) not in shape:directed.append(((x+1,y),(x+1,y+1)))
        if (x,y+1) not in shape:directed.append(((x+1,y+1),(x,y+1)))
        if (x-1,y) not in shape:directed.append(((x,y+1),(x,y)))
    links={a:b for a,b in directed}
    if len(links)!=len(directed) or len({b for a,b in directed})!=len(directed):return False
    start=next(iter(links));current=start;visited=set()
    while current not in visited:
        visited.add(current);current=links[current]
    return current==start and len(visited)==len(directed)


def audit_atlas(atlas,data):
    tile=tuple(map(tuple,data['tile']));shapes=orientations(tile);tips=types(tile,1)
    require(shapes==atlas['shapes'],'centered and signed-permutation shapes disagree')
    require(tips==atlas['tips'],'rectangle and cell tip inventories disagree')
    require(types(tile,3)==atlas['reentrant'],'reentrant inventories disagree')
    require(boundary_disc(tile),'P17 is not a disc')
    codes=direct_pool(tile,shapes,tips)
    require(codes==atlas['incoming_codes'],'bounding and inversion incoming atlases differ')
    squares=[translated(shapes[i],x,y) for i,x,y in codes]
    receives=[];labels=[]
    for square in squares:
        row=[j for j,(v,q) in enumerate(tips) if sum(quadrants(square,v))==3 and not quadrants(square,v)[q]]
        receives.append(row);k,mirror,origin=map_to_tile(square,tile);source=[]
        for j in row:
            u,v=image_point(tips[j][0],k,mirror);point=u-origin[0],v-origin[1]
            source.append(next(i for i,(p,q) in enumerate(types(tile,3)) if p==point))
        labels.append(source)
    require(receives==atlas['receives'],'rectangle received-tip incidence disagrees')
    require(labels==atlas['source_labels'],'intrinsic source-corner labels disagree')
    library=set(map(tuple,data['forbidden_poses']))
    excluded=[i for i,square in enumerate(squares) if forbidden(tile,square,tile,shapes,library)]
    require(excluded==atlas['root_excluded'],'inverse rectangle root exclusions disagree')
    conflicts=[]
    for a,b in itertools.combinations(range(len(codes)),2):
        reason=[]
        if overlap(squares[a],squares[b]):reason.append('overlap')
        if forbidden(squares[a],squares[b],tile,shapes,library):reason.append('interior_pair')
        if reason:conflicts.append((a,b,reason))
    require(conflicts==atlas['conflicts'],'rectangle full-overlap or relative pair clause disagrees')
    return {'incoming':len(codes),'tips':len(tips),'reentrant':len(types(tile,3)),
            'root_excluded':len(excluded),'binary_conflicts':len(conflicts)}


def audit_thresholds():
    checks=0
    for k in range(10):
        clauses=list(itertools.combinations(range(9),10-k)) if k else []
        for word in range(512):
            truth=all(any(word>>i&1 for i in clause) for clause in clauses)
            require(truth==(word.bit_count()>=k),'threshold projection failed')
            checks+=1
    return checks


def direct_corner_formula(tile,fixed_codes):
    shapes=orientations(tile)
    fixed=[translated(shapes[i],x,y) for i,x,y in fixed_codes]
    require(not any(overlap(a,b) for a,b in itertools.combinations(fixed,2)),'fixed overlap')
    occupied=set(itertools.chain.from_iterable(fixed));targets=set()
    for vertex in mesh_vertices(occupied):
        qs=quadrants(occupied,vertex)
        for q in range(4):
            if not qs[q] and qs[(q-1)%4] and qs[(q+1)%4]:
                dx,dy=LOWERS[q];targets.add((vertex[0]+dx,vertex[1]+dy))
    targets=sorted(targets);codes=[];squares=[]
    if targets:
        for i,shape in enumerate(shapes):
            for x in range(min(a for a,b in targets)-max(a for a,b in shape),max(a for a,b in targets)+1):
                for y in range(min(b for a,b in targets)-max(b for a,b in shape),max(b for a,b in targets)+1):
                    moved=set(translated(shape,x,y))
                    if not moved&occupied and moved.intersection(targets):codes.append((i,x,y));squares.append(moved)
    clauses=[[i+1 for i,square in enumerate(squares) if p in square] for p in targets]
    clauses.extend([-a-1,-b-1] for a,b in itertools.combinations(range(len(codes)),2) if squares[a]&squares[b])
    return codes,targets,clauses


def audit_witness(data):
    tile=tuple(map(tuple,data['tile']));shapes=orientations(tile)
    raw=data['pose_codes_doubled_translation']
    require(all(len(q)==3 and all(type(x) is int for x in q) and 0<=q[0]<8 for q in raw),'invalid pose codes')
    squares=[translated(shapes[i],Fraction(x,2),Fraction(y,2)) for i,x,y in raw]
    require(not any(overlap(a,b) for a,b in itertools.combinations(squares,2)),'witness full-footprint overlap')
    root=data['root'];require(root==0 and raw[root]==[shapes.index(tile),0,0],'wrong canonical root')
    tips=types(tile,1);providers=[];received=set()
    for i,square in enumerate(squares):
        if i==root:continue
        indices=[j for j,(v,q) in enumerate(tips) if sum(quadrants(square,v))==3 and not quadrants(square,v)[q]]
        if indices:providers.append(i);received.update(indices)
    require(providers==data['expected_providers'],'actual provider inventory differs')
    require(sorted(received)==data['expected_received_tips'],'actual received tips differ')
    # A doubled-grid halo covers every edge and vertex neighborhood of a fixed copy.
    occupied2=set()
    for i,x,y in raw:
        occupied2.update((2*a+x+dx,2*b+y+dy) for a,b in shapes[i] for dx in (0,1) for dy in (0,1))
    required=data['required_interior_copies']
    require(set([root,*providers])<=set(required),'an incoming provider lacks an interior requirement')
    fixed2=set()
    for index in required:
        i,x,y=raw[index]
        fixed2.update((2*a+x+dx,2*b+y+dy) for a,b in shapes[i] for dx in (0,1) for dy in (0,1))
    required_halo={(x+dx,y+dy) for x,y in fixed2 for dx in (-1,0,1) for dy in (-1,0,1)}
    require(required_halo<=occupied2,'a required copy is not strictly interior')
    require(boundary_disc(fixed2),'the specified five-copy inner union must be a disc')
    union_disc=boundary_disc(occupied2)
    require(data.get('require_disc') is True and union_disc,'sharp witness must be a disc')
    return {'copies':len(raw),'area':17*len(raw),'incoming_providers':providers,
            'received_tips':sorted(received),'required_interior_copies':required,
            'surrounding_union_disc':union_disc}


def run_geometry():
    from atlas import BASE,pool
    from corner_selector import corner_formula
    directory=Path(__file__).resolve().parent
    data=json.loads((BASE/'pairs.json').read_text());atlas=pool(data)
    summary={'atlas':audit_atlas(atlas,data),'threshold_assignments':audit_thresholds()}
    expected=json.loads((directory/'expected.json').read_text());native_corners=0;disc_roots=0
    tile=atlas['tile']
    for record in expected['cases']:
        codes=[(atlas['root_orientation'],0,0)]+[atlas['incoming_codes'][i] for i in record['providers']]
        if record['mode']=='corners':
            generated,_,targets,clauses=corner_formula(tile,codes)
            reference,reference_targets,reference_clauses=direct_corner_formula(tile,codes)
            require(generated==reference and targets==reference_targets and clauses==reference_clauses,'corner inventory or clause mismatch')
            native_corners+=1
        else:
            union=set(p for i,x,y in codes for p in translated(atlas['shapes'][i],x,y))
            require(boundary_disc(union),'a half-grid obstruction root is not a disc')
            disc_roots+=1
    witness=json.loads((directory/'six_charge.json').read_text());summary['witness']=audit_witness(witness)
    controls=[]
    for kind in range(3):
        changed=json.loads(json.dumps(witness))
        if kind==0:changed['pose_codes_doubled_translation'][1][1]+=1
        if kind==1:changed['expected_received_tips'].pop()
        if kind==2:changed['required_interior_copies'].pop()
        try:audit_witness(changed)
        except ValueError:controls.append(kind)
        else:raise ValueError('malformed witness control was accepted')
    summary.update({'independent_corner_instances':native_corners,'independent_disc_roots':disc_roots,
                    'rejected_controls':controls})
    return summary


if __name__=='__main__':print(json.dumps(run_geometry(),indent=2))
