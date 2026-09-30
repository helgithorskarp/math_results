"""Independent exact geometry and forward RUP checking; standard library only."""
from pathlib import Path
from collections import Counter
import argparse
import copy
import hashlib
import itertools
import json

TILE=tuple((x,y) for y,row in enumerate((range(1,4),range(4),range(4),range(2,5),range(3,6))) for x in row)
FIXED=((3,0,0),(0,4,0),(6,-2,3),(7,-3,-3))
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


def doubled_cells(cells):
    return frozenset((2*x+dx,2*y+dy) for x,y in cells for dx in (0,1) for dy in (0,1))


def boundary_disc(squares):
    # Check a connected face union with exactly one simple directed boundary.
    pending=set(squares);first=min(pending);pending.remove(first);todo=[first]
    while todo:
        x,y=todo.pop()
        for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if q in pending:pending.remove(q);todo.append(q)
    require(not pending,'fixed halo union is not edge connected')
    edges=set()
    for x,y in squares:
        cycle=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            if (b,a) in edges:edges.remove((b,a))
            else:edges.add((a,b))
    outgoing={};incoming=Counter()
    for a,b in edges:
        require(a not in outgoing,'fixed halo union has a boundary pinch')
        outgoing[a]=b;incoming[b]+=1
    require(set(outgoing)==set(incoming) and all(n==1 for n in incoming.values()),'boundary is not a cycle union')
    start=min(outgoing);current=start;seen=set()
    while current not in seen:
        seen.add(current);current=outgoing[current]
    require(current==start and len(seen)==len(edges),'fixed halo union has multiple boundary cycles')
    return True


def halo_geometry(shapes,fixed,providers):
    codes=[tuple(q) for q in providers]
    require(len(codes)==len(set(codes)),'duplicate prospective provider')
    cells=[moved(shapes,q) for q in fixed+codes]
    require(not any(a&b for a,b in itertools.combinations(cells,2)),'overlapping required inner copies')
    unscaled=set().union(*cells)
    boundary_disc(unscaled)
    occupied=doubled_cells(unscaled)
    # Inverse distance test rather than dilation by translated neighborhoods.
    xmin,xmax=min(x for x,y in occupied),max(x for x,y in occupied)
    ymin,ymax=min(y for x,y in occupied),max(y for x,y in occupied)
    targets={(x,y) for x in range(xmin-1,xmax+2) for y in range(ymin-1,ymax+2)
             if (x,y) not in occupied and any(abs(x-a)<=1 and abs(y-b)<=1 for a,b in occupied)}
    doubled=tuple(tuple(sorted(doubled_cells(q))) for q in shapes)
    # Translation joins, independent of discovery's whole-copy bounding boxes.
    candidates=set()
    for i,shape in enumerate(doubled):
        joins={(x-a,y-b) for x,y in targets for a,b in shape}
        for x,y in joins:
            if not any((a+x,b+y) in occupied for a,b in shape):candidates.add((i,x,y))
    candidates=sorted(candidates)
    squares=[moved(doubled,q) for q in candidates]
    cover={tuple(sorted(owners_at(p,squares))) for p in targets}
    return candidates,squares,targets,cover


def halo_certificate(shapes,fixed,cert):
    candidates,squares,targets,cover=halo_geometry(shapes,fixed,cert['providers'])
    require(len(candidates)==cert['candidate_count'],'half-grid candidate inventory differs')
    for clause in cert['clauses']:
        validate_clause(clause,len(candidates));key=tuple(sorted(clause))
        if key in cover:continue
        require(len(clause)==2 and all(x<0 for x in clause),'unjustified sparse halo clause')
        a,b=(-x-1 for x in clause)
        require(bool(squares[a]&squares[b]),'false doubled whole-footprint overlap')
    return {'core_clauses':len(cert['clauses']),'rup_additions':rup(cert['clauses'],cert['rup'],len(candidates)),
            'complete_halo_cells':len(targets),'complete_candidates':len(candidates)}


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


def receipt_vector(shapes,codes,cells,recipient,providers):
    reentrant=[v for v in vertices(TILE) if sum(sectors(TILE,v))==3]
    require(len(reentrant)==5,'changed intrinsic source labels')
    vector=[0]*5
    for j in providers:
        oi,tx,ty=codes[j];images=[]
        for k in range(4):
            for mirror in (False,True):
                transformed=image(TILE,k,mirror)
                if normalize(transformed)==shapes[oi]:
                    ox=min(x for x,y in transformed);oy=min(y for x,y in transformed)
                    images.append([(point(v,k,mirror)[0]-ox+tx,point(v,k,mirror)[1]-oy+ty) for v in reentrant])
        require(len(images)==1,'ambiguous intrinsic source orientation')
        for v,q in tips(cells[recipient]):
            qs=sectors(cells[j],v)
            if sum(qs)==3 and not qs[q]:
                require(v in images[0],'contact is not an intrinsic reentrant corner')
                vector[images[0].index(v)]+=1
    return vector


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
    proven_cuts=set();core_count=trace_count=0;cut_kinds=Counter();halo_summaries=[]
    for cert in data['cuts']:
        require(all(tuple(q) in conditional for q in cert['providers']),'exclusion includes an unforced interior copy')
        require(cert['kind'] in ('corner','halo'),'unknown cut type')
        status=(corner_certificate if cert['kind']=='corner' else halo_certificate)(shapes,fixed,cert)
        cut_kinds[cert['kind']]+=1
        if cert['kind']=='halo':halo_summaries.append({k:status[k] for k in ('complete_halo_cells','complete_candidates')})
        core_count+=status['core_clauses'];trace_count+=status['rup_additions']
        proven_cuts.add(tuple(sorted(-indices[tuple(q)] for q in cert['providers'])))
    reasons=Counter()
    for clause in data['final']['clauses']:
        validate_clause(clause,len(candidates));key=tuple(sorted(clause))
        if key in positive_cover:reasons['mandatory_corner_cover']+=1;continue
        if key in conditional_cover:reasons['conditional_corner_cover']+=1;continue
        if key in proven_cuts:reasons['proved_inner_pattern_cut']+=1;continue
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
    vector=receipt_vector(shapes,fixed,fixed_cells,0,list(range(1,len(fixed))))
    require(vector==[1,2,2,0,0],'changed negative-star receipt vector')
    return {'agent':'six-heesch-1','role':'researcher','tile_cells':len(TILE),'fixed_copies':len(fixed),
            'root_received_tips':sorted({i for row in root_receipts for i in row}),
            'specified_star_receipt_vector':vector,
            'possible_incoming_union':len(possible),'conditional_provider_count':len(conditional),
            'complete_candidate_count':len(candidates),'proved_cut_kinds':dict(sorted(cut_kinds.items())),
            'halo_subinventories':halo_summaries,'fixed_halo_unions_checked_discs':len(halo_summaries),
            'subcore_clauses':core_count,'subtrace_additions':trace_count,
            'final_core_clauses':len(data['final']['clauses']),'final_rup_additions':final_additions,
            'final_core_reasons':dict(sorted(reasons.items())),
            'status':'verified all-real exclusion of star B under two incoming-provider generations interior'}


def controls(data,pair_path):
    variants=[]
    bad=copy.deepcopy(data);bad['fixed_codes'][1][1]+=1;variants.append(bad)
    bad=copy.deepcopy(data);bad['final']['rup'][-1]=[999999];variants.append(bad)
    bad=copy.deepcopy(data);bad['final']['clauses'][0]=[1];variants.append(bad)
    bad=copy.deepcopy(data);bad['pair_data_sha256']='0'*64;variants.append(bad)
    # Omit an owner from a complete demanded-cell clause, choosing a modified
    # owner set that is not the complete owner set of any other halo target.
    shapes=orientations();first=next(i for i,c in enumerate(data['cuts']) if c['kind']=='halo')
    _,_,_,cover=halo_geometry(shapes,list(FIXED),data['cuts'][first]['providers'])
    mutation=None
    for j,clause in enumerate(data['cuts'][first]['clauses']):
        if all(x>0 for x in clause) and len(clause)>1:
            for x in clause:
                trial=[q for q in clause if q!=x]
                if tuple(sorted(trial)) not in cover:mutation=(j,trial);break
        if mutation:break
    require(mutation is not None,'no geometry control fixture found')
    bad=copy.deepcopy(data);bad['cuts'][first]['clauses'][mutation[0]]=mutation[1];variants.append(bad)
    for bad in variants:
        try:run(bad,pair_path)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('malformed certificate accepted')
    return len(variants)


def positive_comparison(data):
    """Recheck the older packing, including every actual provider generation."""
    require(data['origin_fixture_sha256']=='c5f4c30ceff27b40a39ef006960b7b5de22489c52e71b429196d1f51cdc32f04','changed positive-fixture provenance')
    shapes=orientations();codes=[];levels=[]
    for row in data['poses']:
        code=row['code'];level=row['level']
        require(isinstance(code,list) and len(code)==3 and all(type(x) is int for x in code),'bad positive pose')
        require(0<=code[0]<8 and type(level) is int and 0<=level<=3,'bad positive orientation or level')
        codes.append(tuple(code));levels.append(level)
    require(len(codes)==36 and len(set(codes))==36,'positive packing must have36 distinct copies')
    require(codes[0]==(3,0,0) and [i for i,l in enumerate(levels) if l==0]==[0],'changed positive root')
    cells=[moved(shapes,q) for q in codes]
    require(not any(a&b for a,b in itertools.combinations(cells,2)),'positive copies overlap')
    prefixes=[set().union(*(s for s,l in zip(cells,levels) if l<=h)) for h in range(4)]
    for h,prefix in enumerate(prefixes):
        boundary_disc(prefix)
        if h:
            require(all((x+dx,y+dy) in prefix for x,y in prefixes[h-1] for dx in (-1,0,1) for dy in (-1,0,1)),'positive prefix is not strictly surrounded')
            old_vertices=set(vertices(prefixes[h-1]))
            require(all(old_vertices.intersection(vertices(s)) for s,l in zip(cells,levels) if l==h),'positive corona contains a noncontacting copy')
    whole=prefixes[3]
    inner=[all((v[0]+dx,v[1]+dy) in whole for v in vertices(s) for dx,dy in LOWER) for s in cells]
    providers=[]
    for receiver in cells:
        receiver_tips=tips(receiver)
        providers.append([j for j,s in enumerate(cells) if any(sum(sectors(s,v))==3 and not sectors(s,v)[q] for v,q in receiver_tips)])
    needed={0}|set(providers[0])|{k for j in providers[0] for k in providers[j]}
    require(all(inner[j] for j in needed),'actual first or second provider is not interior')
    require(sorted(codes[j] for j in providers[0])==[(0,4,0),(4,-3,-3),(6,-2,3)],'changed comparison star D')
    vector=receipt_vector(shapes,codes,cells,0,providers[0])
    require(vector==[1,2,2,0,0],'changed comparison receipt vector')
    return {'copies':36,'complete_disc_coronas':3,'actual_incoming_providers':len(providers[0]),
            'root_provider_codes':[list(q) for q in sorted(codes[j] for j in providers[0])],
            'required_interior_copies':len(needed),'receipt_vector':vector,
            'all_actual_two_generation_copies_interior':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates',type=Path,default=Path(__file__).with_name('certificates.json'))
    parser.add_argument('--pair-data',type=Path,default=Path(__file__).resolve().parents[1]/'heesch_polyomino_corner_obstruction'/'pairs.json')
    parser.add_argument('--positive',type=Path,default=Path(__file__).with_name('positive_comparison.json'))
    parser.add_argument('--controls',action='store_true')
    a=parser.parse_args();data=json.loads(a.certificates.read_text());result=run(data,a.pair_data)
    positive=json.loads(a.positive.read_text());result['positive_comparison']=positive_comparison(positive)
    if a.controls:
        count=controls(data,a.pair_data)
        bad=copy.deepcopy(positive);bad['poses'][1]['code']=[3,0,0]
        try:positive_comparison(bad)
        except (ValueError,KeyError,IndexError):count+=1
        else:raise ValueError('overlapping positive comparison accepted')
        result['malformed_controls_rejected']=count
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
