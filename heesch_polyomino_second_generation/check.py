"""Independent exact geometry and forward RUP checking; standard library only."""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import itertools
import json

TILE=tuple((x,y) for y,row in enumerate((range(1,4),range(4),range(4),range(2,5),range(3,6))) for x in row)
FIXED=((3,0,0),(0,1,3),(4,4,-2),(6,-4,2),(6,-1,-4))
PAIR_SHA='52395c73e83ff3a1b023a1c50ebc43472caded160e4b0645c8fcbbbf905d4033'
SIGNS=((1,1),(-1,1),(-1,-1),(1,-1))
LOWER=((0,0),(-1,0),(-1,-1),(0,-1))


def require(condition,message):
    if not condition: raise ValueError(message)


def point(p,turns,mirror):
    x,y=p
    if mirror:x=-x
    for _ in range(turns):x,y=-y,x
    return x,y


def image(squares,turns,mirror):
    centers=[point((2*x+1,2*y+1),turns,mirror) for x,y in squares]
    return tuple(sorted(((x-1)//2,(y-1)//2) for x,y in centers))


def normalize(squares):
    ox=min(x for x,y in squares);oy=min(y for x,y in squares)
    return tuple(sorted((x-ox,y-oy) for x,y in squares))


def orientations():
    return tuple(sorted({normalize(image(TILE,k,m)) for k in range(4) for m in (False,True)}))


def moved(shapes,code):
    i,x,y=code
    return frozenset((a+x,b+y) for a,b in shapes[i])


def vertices(squares):
    return sorted({(x+dx,y+dy) for x,y in squares for dx in (0,1) for dy in (0,1)})


def sectors(squares,v):
    """Literal quarter-offset rectangle points, with all coordinates quadrupled."""
    return tuple(any(4*x<=4*v[0]+sx<4*x+4 and 4*y<=4*v[1]+sy<4*y+4
                     for x,y in squares) for sx,sy in SIGNS)


def tips(squares):
    return [(v,qs.index(True)) for v in vertices(squares)
            for qs in [sectors(squares,v)] if sum(qs)==1]


def incoming(shapes,receiver):
    """Bound all translations by tip boxes; test literal sectors and full copies."""
    root=moved(shapes,receiver);out=set()
    for v,q in tips(root):
        for i,shape in enumerate(shapes):
            for x in range(v[0]-max(a for a,b in shape)-1,v[0]+1):
                for y in range(v[1]-max(b for a,b in shape)-1,v[1]+1):
                    square=moved(shapes,(i,x,y))
                    if square & root:continue
                    qs=sectors(square,v)
                    if sum(qs)==3 and not qs[q]:out.add((i,x,y))
    return sorted(out)


def corner_targets(required,occupied):
    out=set()
    for v in required:
        qs=sectors(occupied,v)
        for q in range(4):
            if not qs[q] and qs[(q-1)%4] and qs[(q+1)%4]:
                dx,dy=LOWER[q];out.add((v[0]+dx,v[1]+dy))
    return sorted(out)


def bound_candidates(shapes,targets,occupied,extras=()):
    """Whole-copy bounding boxes, independent of the discovery's cell anchoring."""
    out=set(extras)
    if targets:
        xs=[p[0] for p in targets];ys=[p[1] for p in targets]
        for i,shape in enumerate(shapes):
            for x in range(min(xs)-max(a for a,b in shape),max(xs)+1):
                for y in range(min(ys)-max(b for a,b in shape),max(ys)+1):
                    square=moved(shapes,(i,x,y))
                    if not square & occupied and square.intersection(targets):out.add((i,x,y))
    return sorted(out)


def owners_at(target,cells):
    return tuple(j+1 for j,square in enumerate(cells) if target in square)


def validate_clause(clause,nv):
    require(isinstance(clause,list),'clause must be a list')
    require(all(type(x) is int and 0<abs(x)<=nv for x in clause),'bad literal')
    require(len(clause)==len(set(clause)),'repeated literal')
    require(not any(-x in clause for x in clause),'tautological certificate clause')


def propagated_contradiction(clauses,assumptions):
    assignment={}
    def assign(literal):
        variable,value=abs(literal),literal>0
        if variable in assignment:return assignment[variable]==value
        assignment[variable]=value
        return True
    for literal in assumptions:
        if not assign(literal):return True
    changed=True
    while changed:
        changed=False
        for clause in clauses:
            if any(assignment.get(abs(x))==(x>0) for x in clause if abs(x) in assignment):continue
            pending=[x for x in clause if abs(x) not in assignment]
            if not pending:return True
            if len(pending)==1:
                if not assign(pending[0]):return True
                changed=True
    return False


def rup(clauses,trace,nv):
    require(bool(trace) and trace[-1]==[],'proof must explicitly end in the empty clause')
    database=[list(c) for c in clauses]
    for clause in database:validate_clause(clause,nv)
    for j,clause in enumerate(trace):
        validate_clause(clause,nv)
        require(propagated_contradiction(database,[-x for x in clause]),'non-RUP addition at '+str(j))
        database.append(clause)
    return len(trace)


def corner_certificate(shapes,fixed,cert):
    codes=[tuple(q) for q in cert['providers']]
    require(len(codes)==len(set(codes)),'duplicate prospective provider')
    cells=[moved(shapes,q) for q in fixed+codes]
    require(not any(a&b for a,b in itertools.combinations(cells,2)),'overlapping fixed inner copies')
    occupied=set().union(*cells)
    targets=corner_targets(vertices(occupied),occupied)
    candidates=bound_candidates(shapes,targets,occupied)
    require(len(candidates)==cert['candidate_count'],'corner candidate inventory differs')
    squares=[moved(shapes,q) for q in candidates]
    cover={tuple(sorted(owners_at(p,squares))) for p in targets}
    for clause in cert['clauses']:
        validate_clause(clause,len(candidates))
        key=tuple(sorted(clause))
        if key in cover:continue
        require(len(clause)==2 and all(x<0 for x in clause),'unjustified sparse corner clause')
        a,b=(-x-1 for x in clause)
        require(bool(squares[a]&squares[b]),'false full-footprint overlap')
    return {'core_clauses':len(cert['clauses']),'rup_additions':rup(cert['clauses'],cert['rup'],len(candidates))}


def relative(first,second,shapes):
    images=[]
    tile=tuple(sorted(TILE))
    for k in range(4):
        for mirror in (False,True):
            transformed=image(first,k,mirror)
            if normalize(transformed)==tile:
                images.append((k,mirror,(min(x for x,y in transformed),min(y for x,y in transformed))))
    require(len(images)==1,'P17 orientation inverse is not unique')
    k,mirror,(ox,oy)=images[0]
    moved_second=image(second,k,mirror)
    return shapes.index(normalize(moved_second)),min(x for x,y in moved_second)-ox,min(y for x,y in moved_second)-oy


def forbidden(first,second,shapes,library):
    return relative(first,second,shapes) in library or relative(second,first,shapes) in library


def run(data,pair_path):
    require(tuple(map(tuple,data['tile']))==TILE,'changed tile')
    require(tuple(map(tuple,data['fixed_codes']))==FIXED,'changed root star')
    require(data['pair_data_sha256']==PAIR_SHA,'changed dependency declaration')
    require(hashlib.sha256(pair_path.read_bytes()).hexdigest()==PAIR_SHA,'changed pair library bytes')
    pair_data=json.loads(pair_path.read_text());library=set(map(tuple,pair_data['forbidden_poses']))
    require(set(map(tuple,pair_data['tile']))==set(TILE),'pair library for another tile')
    shapes=orientations();require(len(shapes)==8 and shapes[3]==tuple(sorted(TILE)),'orientation convention changed')
    fixed=list(FIXED);fixed_cells=[moved(shapes,q) for q in fixed]
    require(not any(a&b for a,b in itertools.combinations(fixed_cells,2)),'fixed star overlaps')
    occupied=set().union(*fixed_cells)
    possible=set().union(*(set(incoming(shapes,q)) for q in fixed))
    conditional={q for q in possible if q not in fixed and not moved(shapes,q)&occupied}
    mandatory=corner_targets(vertices(occupied),occupied)
    conditional_targets={q:corner_targets(vertices(moved(shapes,q)),occupied|set(moved(shapes,q))) for q in conditional}
    all_targets=set(mandatory).union(*conditional_targets.values())
    candidates=bound_candidates(shapes,all_targets,occupied,conditional)
    require(len(candidates)==data['final']['candidate_count'],'conditional candidate inventory differs')
    indices={q:j+1 for j,q in enumerate(candidates)}
    cells=[moved(shapes,q) for q in candidates]
    positive_cover={tuple(sorted(owners_at(p,cells))) for p in mandatory}
    conditional_cover={tuple(sorted((-indices[q],*owners_at(p,cells)))) for q,targets in conditional_targets.items() for p in targets}
    proven_cuts=set();core_count=trace_count=0
    for cert in data['single_provider_exclusions']+data['provider_conjunction_exclusions']:
        require(all(tuple(q) in conditional for q in cert['providers']),'exclusion includes an unforced interior copy')
        status=corner_certificate(shapes,fixed,cert)
        core_count+=status['core_clauses'];trace_count+=status['rup_additions']
        proven_cuts.add(tuple(sorted(-indices[tuple(q)] for q in cert['providers'])))
    reasons=Counter()
    for clause in data['final']['clauses']:
        validate_clause(clause,len(candidates));key=tuple(sorted(clause))
        if key in positive_cover:reasons['mandatory_corner_cover']+=1;continue
        if key in conditional_cover:reasons['conditional_corner_cover']+=1;continue
        if key in proven_cuts:reasons['proved_corner_cut']+=1;continue
        require(all(x<0 for x in clause) and len(clause) in (1,2),'unjustified final core clause')
        codes=[candidates[-x-1] for x in clause]
        if len(codes)==2 and cells[-clause[0]-1]&cells[-clause[1]-1]:
            reasons['full_footprint_overlap']+=1;continue
        require(all(q in conditional for q in codes),'pair library used on an ordinary outer filler')
        if len(codes)==1:
            require(any(forbidden(moved(shapes,codes[0]),square,shapes,library) for square in fixed_cells),'false interior pair unit')
            reasons['prior_interior_pair_unit']+=1
        else:
            require(forbidden(moved(shapes,codes[0]),moved(shapes,codes[1]),shapes,library),'false interior pair binary')
            reasons['prior_interior_pair_binary']+=1
    final_additions=rup(data['final']['clauses'],data['final']['rup'],len(candidates))
    root_receipts=[]
    root_tips=tips(fixed_cells[0])
    for copy,square in enumerate(fixed_cells[1:],1):
        root_receipts.append([i for i,(v,q) in enumerate(root_tips) if sum(sectors(square,v))==3 and not sectors(square,v)[q]])
    return {'agent':'six-heesch-1','role':'researcher','tile_cells':len(TILE),'fixed_copies':len(fixed),
            'root_received_tips':sorted({i for row in root_receipts for i in row}),
            'possible_incoming_union':len(possible),'conditional_provider_count':len(conditional),
            'complete_candidate_count':len(candidates),'single_provider_exclusions':len(data['single_provider_exclusions']),
            'provider_conjunction_exclusions':len(data['provider_conjunction_exclusions']),
            'subcore_clauses':core_count,'subtrace_additions':trace_count,
            'final_core_clauses':len(data['final']['clauses']),'final_rup_additions':final_additions,
            'final_core_reasons':dict(sorted(reasons.items())),
            'status':'verified all-real exclusion of the specified star under two incoming-provider generations interior'}


def controls(data,pair_path):
    variants=[]
    bad=copy.deepcopy(data);bad['fixed_codes'][1][1]+=1;variants.append(bad)
    bad=copy.deepcopy(data);bad['final']['rup'][-1]=[999999];variants.append(bad)
    bad=copy.deepcopy(data);bad['final']['clauses'][0]=[1];variants.append(bad)
    bad=copy.deepcopy(data);bad['pair_data_sha256']='0'*64;variants.append(bad)
    for bad in variants:
        try:run(bad,pair_path)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('malformed certificate accepted')
    return len(variants)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=Path(__file__).with_name('certificates.json'))
    parser.add_argument('--pair-data',type=Path,default=Path(__file__).resolve().parents[1]/'heesch_polyomino_corner_obstruction'/'pairs.json')
    parser.add_argument('--controls',action='store_true')
    a=parser.parse_args();data=json.loads(a.certificates.read_text());result=run(data,a.pair_data)
    if a.controls:result['malformed_controls_rejected']=controls(data,a.pair_data)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
