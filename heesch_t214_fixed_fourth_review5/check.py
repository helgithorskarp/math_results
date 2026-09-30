"""Fresh vertex-anchor inventory and direct star checks; no upstream imports."""
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
from hashlib import sha256
import json,time,resource,argparse

BASE=Path(__file__).resolve().parent

def need(c,m):
    if not c:raise ValueError(m)

def verts(c):
    k,x,y=c
    return ((x,y),(x+1,y),(x,y+1)) if k==0 else ((x+1,y),(x,y+1),(x+1,y+1))

def cell(vs):
    vs=set(map(tuple,vs));x=min(v[0] for v in vs);y=min(v[1] for v in vs)
    k=0 if (x,y) in vs else 1
    need(vs==set(verts((k,x,y))),'Not a unit triangle')
    return k,x,y

def metric_matrices():
    return sorted((a,b,c,d) for a,b,c,d in product((-1,0,1),repeat=4)
                  if a*a+a*c+c*c==1 and b*b+b*d+d*d==1
                  and 2*a*b+a*d+b*c+2*c*d==1 and abs(a*d-b*c)==1)

def point(v,m,t=(0,0)):
    x,y=v;a,b,c,d=m
    return a*x+b*y+t[0],c*x+d*y+t[1]

def rotate(shape,m):
    return frozenset(cell(point(v,m) for v in verts(c)) for c in shape)

def translate(shape,t):
    x,y=t
    return frozenset((k,u+x,v+y) for k,u,v in shape)

def posekey(p):return tuple(p['matrix']),tuple(p['translation'])

def footprint(shape,p):return translate(rotate(shape,tuple(p['matrix'])),p['translation'])

def compose(p,q):
    m,t=posekey(p);n,s=posekey(q);a,b,c,d=m;e,f,g,h=n
    return {'matrix':[a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h],
            'translation':list(point(s,m,t))}

def inverse(p):
    (a,b,c,d),(x,y)=posekey(p);det=a*d-b*c
    m=(d//det,-b//det,-c//det,a//det)
    return {'matrix':list(m),'translation':list(point((-x,-y),m))}

def vertex_faces(shape):
    out=defaultdict(set)
    for c in shape:
        for v in verts(c):out[v].add(c)
    return out

def star(v):
    x,y=v
    return {(0,x,y),(1,x-1,y),(0,x-1,y),(1,x-1,y-1),(0,x,y-1),(1,x,y-1)}

def boundary(shape):
    edges=Counter()
    for c in shape:
        vs=verts(c)
        for i in range(3):edges[tuple(sorted((vs[i],vs[(i+1)%3])))]+=1
    need(all(n in (1,2) for n in edges.values()),'Edge incidence')
    exposed=[edge for edge,n in edges.items() if n==1]
    links=defaultdict(list)
    for a,b in exposed:links[a].append(b);links[b].append(a)
    need(all(len(row)==2 for row in links.values()),'Pinched boundary')
    if links:
        seen={next(iter(links))};stack=list(seen)
        while stack:
            for v in links[stack.pop()]:
                if v not in seen:seen.add(v);stack.append(v)
        need(len(seen)==len(links),'Multiple boundary components')
    # Together with face edge-connectivity this verifies the disc meshes.
    cells=set(shape);visited={next(iter(cells))};todo=list(visited)
    while todo:
        k,x,y=todo.pop()
        neighbors=((1,x,y),(1,x-1,y),(1,x,y-1)) if k==0 else ((0,x,y),(0,x+1,y),(0,x,y+1))
        for n in neighbors:
            if n in cells and n not in visited:visited.add(n);todo.append(n)
    need(visited==cells,'Disconnected tile mesh')
    return set(links)

def independent_inventory(shape,fixed):
    occupied=set()
    for p in fixed:
        f=footprint(shape,p);need(occupied.isdisjoint(f),'Fixed overlap');occupied.update(f)
    boundary_vertices=boundary(occupied)
    required=set().union(*(star(v) for v in boundary_vertices))-occupied
    tile_boundary=boundary(shape)
    trials=0;result={};feet={}
    for m in metric_matrices():
        rotated=rotate(shape,m)
        rotated_vertices={point(v,m) for v in tile_boundary}
        shifts={(v[0]-u[0],v[1]-u[1]) for v in boundary_vertices for u in rotated_vertices}
        trials+=len(shifts)
        for t in sorted(shifts):
            tx,ty=t
            if any((k,x+tx,y+ty) in occupied for k,x,y in rotated):continue
            f=translate(rotated,t)
            need(bool(f&required),'Contact copy has no halo cell')
            key=m,t;result[key]={'matrix':list(m),'translation':list(t)};feet[key]=f
    keys=sorted(result)
    return [result[k] for k in keys],[feet[k] for k in keys],sorted(required),occupied,trials

def providers(shape,target,missing,gap):
    result={}
    vf=vertex_faces(shape)
    for m in metric_matrices():
        rotated=rotate(shape,m)
        for v in vf:
            u=point(v,m);t=(target[0]-u[0],target[1]-u[1]);f=translate(rotated,t)
            sector=f&star(target)
            if missing in f and len(sector) in (1,2) and sector<=gap:
                result[(m,t)] = (f,{'matrix':list(m),'translation':list(t)})
    return [(p,f) for f,p in (result[k] for k in sorted(result))]

def pattern_checks(shape,patterns):
    output=[]
    for pat in patterns:
        occupied=set()
        for p in pat['poses']:
            f=footprint(shape,p);need(occupied.isdisjoint(f),'Pattern overlap');occupied.update(f)
        if pat['kind']=='small_hole':
            hole=set(map(tuple,pat['hole_cells']));need(hole.isdisjoint(occupied),'Hole occupied')
            for k,x,y in hole:
                ns=((1,x,y),(1,x-1,y),(1,x,y-1)) if k==0 else ((0,x,y),(0,x+1,y),(0,x,y+1))
                need(all(n in hole or n in occupied for n in ns),'Hole not enclosed')
            need(0<len(hole)<len(shape),'Area obstruction')
            output.append({'kind':pat['kind'],'area':len(hole)});continue
        targets=pat.get('targets',[{'vertex':pat.get('target'),'cell':pat.get('missing_cell')}])
        options=[];counts=[]
        for row in targets:
            v=tuple(row['vertex']);missing=tuple(row['cell']);filled=occupied&star(v);gap=star(v)-occupied
            need(len(gap) in (1,2) and missing in gap,'Small sector geometry')
            if len(gap)==2:
                left,right=gap
                need(len(set(verts(left))&set(verts(right)))==2,'Disconnected 120-degree gap')
            all_providers=providers(shape,v,missing,gap);counts.append(len(all_providers))
            options.append([(p,f) for p,f in all_providers if f.isdisjoint(occupied)])
        if pat['kind']=='empty_corner':need(not options[0],'Empty corner has provider')
        else:need(all(options) and all(f!=h and not f.isdisjoint(h) for p,f in options[0] for q,h in options[1]),'No forced clash')
        output.append({'kind':pat['kind'],'provider_counts':counts,'available_counts':[len(row) for row in options],
                       'forced_poses':[[p for p,f in row] for row in options]})
    return output

def narrow_pool(shape):
    result={}
    for v,incident in vertex_faces(shape).items():
        if len(incident)!=5:continue
        gap=star(v)-shape;need(len(gap)==1,'Narrow gap')
        for p,f in providers(shape,v,next(iter(gap)),gap):
            if f.isdisjoint(shape):result[posekey(p)]=p
    need(len(result)==59,'Narrow provider inventory')
    return [result[k] for k in sorted(result)]

def core_semantics(shape,data,poses,feet,required):
    core=json.loads((BASE/'unit-core.json').read_text())
    fixed=data['fixed_poses'];lookup={posekey(p):0 for p in fixed}
    lookup.update({posekey(p):i for i,p in enumerate(poses,1)})
    new_clauses={};instance_counts=[]
    for pi,pat in enumerate(data['patterns'],1):
        this=set()
        for anchor in fixed+poses:
            selected=[]
            for relative in pat['poses']:
                key=posekey(compose(anchor,relative))
                if key not in lookup:break
                selected.append(lookup[key])
            else:
                clause=tuple(-i for i in sorted(set(selected)-{0}))
                need(bool(clause),'Forbidden fixed pattern')
                this.add(clause);new_clauses.setdefault(clause,{'pattern':pi,'anchor':anchor})
        instance_counts.append(len(this))
    pool=narrow_pool(shape)
    excluded={1,2,3,5,6,7,8,10,11,12,13,14,15,16,22,24,26,28,30,32,34,36,38,43,44,45,46,47,48,49,51,52,53,54,56,57,58,59}
    old={}
    for row in data['imported_pair_lemmas']:
        i=row['attachment'];need(i in excluded and posekey(row['pose'])==posekey(pool[i-1]),'Imported pair indexing')
        old[posekey(row['pose'])]=i;old[posekey(inverse(row['pose']))]=i
    owners={c:[] for c in required}
    for i,f in enumerate(feet,1):
        for c in f&owners.keys():owners[c].append(i)
    counters=Counter();old_used=set();witnesses=[]
    for row in core['core']:
        lits=row['literals'];cid=row['source_clause']
        need(bool(lits) and len(set(lits))==len(lits) and all(0<abs(v)<=len(poses) for v in lits),'Malformed clause')
        if lits[0]>0:
            need(all(v>0 for v in lits) and 1<=cid<=len(required),'Positive clause convention')
            c=required[cid-1];need(lits==owners[c],'Incomplete halo cover clause')
            witness={'kind':'halo','cell':c}
        else:
            need(all(v<0 for v in lits),'Mixed clause')
            ids=[-v for v in lits]
            if len(ids)==2 and not feet[ids[0]-1].isdisjoint(feet[ids[1]-1]):
                witness={'kind':'overlap','cell':min(feet[ids[0]-1]&feet[ids[1]-1])}
            elif tuple(lits) in new_clauses:
                witness={'kind':'new_pattern',**new_clauses[tuple(lits)]}
            else:
                need(len(ids) in (1,2),'Unrecognized geometric exclusion')
                options=[]
                if len(ids)==1:
                    p=poses[ids[0]-1]
                    for fi,fixedpose in enumerate(fixed):
                        relative=posekey(compose(inverse(fixedpose),p))
                        if relative in old:options.append((old[relative],fi))
                else:
                    relative=posekey(compose(inverse(poses[ids[0]-1]),poses[ids[1]-1]))
                    if relative in old:options.append((old[relative],None))
                need(bool(options),'Clause has no sound geometric justification')
                attachment,fi=min(options,key=lambda pair:pair[0]);old_used.add(attachment)
                witness={'kind':'imported_pair','attachment':attachment,'fixed_index':fi}

        counters[witness['kind']]+=1;witnesses.append({'source_clause':cid,**witness})
    return core,{'clauses_by_geometry':dict(counters),'used_old_attachments':sorted(old_used),
                 'new_pattern_instance_counts':instance_counts,'new_pattern_distinct':len(new_clauses),
                 'clause_witnesses':witnesses}

def check_trace(core,steps=None,conflict=None):
    clauses={row['source_clause']:row['literals'] for row in core['core']}
    need(len(clauses)==len(core['core']),'Repeated source clause')
    assigned={}
    for lit,cid in core['core_steps'] if steps is None else steps:
        need(cid in clauses and lit in clauses[cid] and abs(lit) not in assigned,'Invalid unit step')
        need(all(assigned.get(abs(v))==-v for v in clauses[cid] if v!=lit),'Step is not unit')
        assigned[abs(lit)]=lit
    final=core['conflict_source_clause'] if conflict is None else conflict
    need(final in clauses and all(assigned.get(abs(v))==-v for v in clauses[final]),'No terminal contradiction')
    return len(assigned)

def prefix_checks(shape,fixed):
    occupied=set();previous=set();previous_vertices=set();rows=[]
    for level in range(5):
        added=0
        for p in fixed:
            if p['level']!=level:continue
            need(tuple(p['matrix']) in metric_matrices(),'Fixed nonisometry')
            f=footprint(shape,p);need(f.isdisjoint(occupied),'Prefix overlap')
            if level:need(bool(set(vertex_faces(f))&previous_vertices),'No previous contact')
            occupied.update(f);added+=1
        boundary(occupied)
        need(all(star(v)<=occupied for v in previous_vertices),'Incomplete previous surround')
        previous=set(occupied);previous_vertices=set(vertex_faces(previous))
        rows.append({'level':level,'added_copies':added,'cells':len(occupied)})
    need([r['added_copies'] for r in rows]==[1,5,11,23,39],'Prefix copy counts')
    return rows

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',action='store_true');args=parser.parse_args()
    start=time.monotonic();data=json.loads((BASE/'input.json').read_text())
    shape=frozenset(cell(vs) for vs in data['triangles'])
    need(len(shape)==214 and len(metric_matrices())==12,'Tile identity')
    need(sha256((json.dumps({'triangles':data['triangles']},separators=(',',':'))+'\n').encode()).hexdigest()==
         '8d42c74f1e219ae37f34d5706f83ab4eb20e921ada66d70090c8a539f481335f','Triangle input identity')
    prefixes=prefix_checks(shape,data['fixed_poses'])
    checks=pattern_checks(shape,data['patterns'])
    poses,feet,required,occupied,trials=independent_inventory(shape,data['fixed_poses'])
    need(sha256((json.dumps(poses,separators=(',',':'))+'\n').encode()).hexdigest()==data['source_pose_sha256'],
         'Independent inventory differs entry by entry')
    core,semantics=core_semantics(shape,data,poses,feet,required)
    steps=check_trace(core)
    for bad_steps,bad_final in [(core['core_steps'][1:],None),(core['core_steps'][:1],core['conflict_source_clause'])]:
        try:check_trace(core,bad_steps,bad_final)
        except ValueError:continue
        raise ValueError('Invalid unit certificate accepted')
    witnesses=semantics.pop('clause_witnesses')
    semantics['clause_witness_sha256']=sha256(json.dumps(witnesses,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result={'reviewer':'six-reviewer-5','role':'reviewer','prefixes':prefixes,'patterns':checks,
            'candidates':len(poses),'halo':len(required),'vertex_anchored_trials':trials,
            'semantics':semantics,'unit_steps':steps,'core_clauses':len(core['core']),
            'core_variables':len({abs(v) for row in core['core'] for v in row['literals']}),
            'core_literals':sum(len(row['literals']) for row in core['core']),
            'source_pose_sha256':data['source_pose_sha256'],
            'input_sha256':sha256((BASE/'input.json').read_bytes()).hexdigest(),
            'unit_core_sha256':sha256((BASE/'unit-core.json').read_bytes()).hexdigest(),
            'rejected_invalid_traces':2}
    rendered=json.dumps(result,indent=2)+'\n'
    if args.record:(BASE/'expected.json').write_text(rendered)
    else:need(json.loads((BASE/'expected.json').read_text())==result,'Expected evidence mismatch')
    print(rendered,end='')

if __name__=='__main__':main()
