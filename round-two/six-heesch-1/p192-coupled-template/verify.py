"""Solver-free independent cell-frame/pair-intersection frontier reader."""
from collections import deque
from copy import deepcopy
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
dependencies=json.loads((ROOT/'dependencies.json').read_text())
rup_path=ROOT/dependencies['rup']['path']
if hashlib.sha256(rup_path.read_bytes()).hexdigest()!=dependencies['rup']['sha256']:
    raise ValueError('RUP dependency bytes differ')
if hashlib.sha256((ROOT/'input.json').read_bytes()).hexdigest()!=dependencies['literal_input_sha256']:
    raise ValueError('literal input bytes differ')
spec=importlib.util.spec_from_file_location('frontier_rup',rup_path)
rup=importlib.util.module_from_spec(spec);spec.loader.exec_module(rup)
FOUR=((1,0),(-1,0),(0,1),(0,-1))
NINE=tuple(product((-1,0,1),repeat=2))


def require(ok,message):
    if not ok:raise ValueError(message)


def norm(cells):
    lo=min(x for x,y in cells),min(y for x,y in cells)
    return tuple(sorted((x-lo[0],y-lo[1]) for x,y in cells))


def images(cells):
    return tuple(sorted({norm([(sx*(y if swap else x),sy*(x if swap else y)) for x,y in cells])
                         for swap in (False,True) for sx,sy in product((-1,1),repeat=2)}))


def halo(cells):
    return {(x+dx,y+dy) for x,y in cells for dx,dy in NINE}-set(cells)


def connected(cells,start):
    seen={start};todo=deque([start])
    while todo:
        x,y=todo.popleft()
        for dx,dy in FOUR:
            q=x+dx,y+dy
            if q in cells and q not in seen:seen.add(q);todo.append(q)
    return seen


def disc(cells):
    cells=set(cells)
    if not cells or connected(cells,min(cells))!=cells:return False
    for vertex in {(x+dx,y+dy) for x,y in cells for dx,dy in product((0,1),repeat=2)}:
        x,y=vertex
        qs=[(x,y),(x-1,y),(x-1,y-1),(x,y-1)]
        bits=[q in cells for q in qs]
        if sum(bits)==2 and bits[0]==bits[2]:return False
    ax,bx=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    ay,by=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    empty={(x,y) for x in range(ax,bx+1) for y in range(ay,by+1)}-cells
    return connected(empty,(ax,ay))==empty


class Frames:
    def __init__(self,core=None):
        data=json.loads((ROOT/'input.json').read_text())
        seed=norm(data['seed_cells'])
        self.S=frozenset((2*x+i,2*y+j) for x,y in seed for i,j in product((0,1),repeat=2))
        boundary={q for q in self.S if any((q[0]+dx,q[1]+dy) not in self.S for dx,dy in FOUR)}
        self.I=self.S-boundary if core is None else frozenset(map(tuple,core))
        require(bool(self.I) and self.I<=self.S,'invalid fixed core')
        exterior={(x+dx,y+dy) for x,y in self.S for dx,dy in FOUR}-self.S
        self.U=tuple(sorted(self.S|exterior));self.var={q:i for i,q in enumerate(self.U,1)}
        shapes=images(self.S);require(len(shapes)==8,'ambiguous reference frame')
        matrices=[(sx,0,0,sy) if not swap else (0,sx,sy,0)
                  for swap in (False,True) for sx,sy in product((-1,1),repeat=2)]
        self.frames=[]
        for shape in shapes:
            matched=[]
            for a,b,c,d in matrices:
                raw=[(a*x+b*y,c*x+d*y) for x,y in self.S]
                if norm(raw)==shape:matched.append(((a,b,c,d),(min(x for x,y in raw),min(y for x,y in raw))))
            require(len(matched)==1,'ambiguous cell-index matrix')
            self.frames.append(matched[0])
        self.poses=[(o,2*x,2*y) for level in data['seed_levels'] for o,x,y in level]

    def position(self,pose,cell):
        o,tx,ty=pose;(a,b,c,d),(lx,ly)=self.frames[o];x,y=cell
        return a*x+b*y-lx+tx,c*x+d*y-ly+ty

    def pose_list(self,shifts):
        require(len(shifts)==6 and all(tuple(q) in NINE for q in shifts),'invalid selected unit shifts')
        return [self.poses[0]]+[(o,x+dx,y+dy) for (o,x,y),(dx,dy) in zip(self.poses[1:],shifts)]

    def geometry(self,raw,shifts):
        raw=set(map(tuple,raw));require(self.I<=raw<=set(self.U),'mask outside selected domain')
        poses=self.pose_list(shifts)
        footprints=[{self.position(p,q) for q in raw} for p in poses]
        require(footprints[0]==raw,'reference root is not identity')
        occupied=set()
        for fp in footprints:
            require(not fp&occupied,'whole-copy overlap');occupied.update(fp)
        require(halo(raw)<=occupied,'root surround incomplete')
        root_disc=disc(raw)
        touches=all(fp&halo(raw) for fp in footprints[1:])
        union_disc=disc(occupied)
        return dict(root_disc=root_disc,all_neighbors_touch=touches,first_union_disc=union_disc,
                    first_admissible=root_disc and touches and union_disc,
                    root_cells=len(raw),first_cells=len(occupied))


def builder(frames,motions,joint):
    clauses=set();nv=105
    def add(zs):
        zs=set(zs)
        if not any(-z in zs for z in zs):clauses.add(tuple(sorted(zs)))
    for q in frames.I:add([frames.var[q]])
    if joint:
        for j in range(1,7):
            ys=[y for group,y,p in motions if group==j]
            add(ys)
            for a,b in combinations(ys,2):add([-a,-b])
        nv=159
    # Independent pairwise intersections of complete option footprints.
    fp=[{frames.position(p,q):v for q,v in frames.var.items()} for group,y,p in motions]
    for i,(j,y,p) in enumerate(motions):
        for k in range(i):
            group,z,pose=motions[k]
            if group==j:continue
            for point in fp[i].keys()&fp[k].keys():
                v,w=fp[i][point],fp[k][point]
                if joint:
                    add(([-y] if y else [])+([-z] if z else [])
                        +([] if frames.U[v-1] in frames.I else [-v])
                        +([] if frames.U[w-1] in frames.I else [-w]))
                else:add([-v,-w])
    target={(x+dx,y+dy) for x,y in frames.U for dx,dy in NINE}
    gates={}
    if joint:
        keys=sorted((point,y,v) for (_,y,p),footprint in zip(motions,fp) if y
                    for point,v in footprint.items() if point in target and frames.U[v-1] not in frames.I)
        for point,y,v in keys:
            nv+=1;gates[y,v]=nv
            add([-nv,y]);add([-nv,v]);add([nv,-y,-v])
    suppliers={point:[] for point in target}
    for (_,y,p),footprint in zip(motions,fp):
        for point,v in footprint.items():
            if point not in target:continue
            term=v if not y else y if frames.U[v-1] in frames.I else gates[y,v]
            suppliers[point].append(term)
    for (x,y),v in frames.var.items():
        for dx,dy in NINE:add([-v]+suppliers[x+dx,y+dy])
    if joint:add([-frames.var[q] if q in frames.S else frames.var[q] for q in frames.U if q not in frames.I])
    base=[list(zs) for zs in sorted(clauses)]
    dimacs=(f'p cnf {nv} {len(base)}\n'+''.join(' '.join(map(str,zs))+' 0\n' for zs in base)).encode()
    return base,nv,hashlib.sha256(dimacs).hexdigest(),gates


def verify_joint(data):
    f=Frames();require(sorted(f.I)==list(map(tuple,data['core'])),'the supplied core is not the fixed35-cell interior')
    require((len(f.S),len(f.I),len(f.U),len(f.poses))==(68,35,105,7),'literal template dimensions differ')
    require(data['classification_complete'] and data['complete'],'certificate is not a completed prototype classification')
    motions=[(0,None,f.poses[0])]
    for j,(o,x,y) in enumerate(f.poses[1:],1):
        for k,(dx,dy) in enumerate(NINE):motions.append((j,105+9*(j-1)+k+1,(o,x+dx,y+dy)))
    base,nv,digest,gates=builder(f,motions,True)
    require((nv,len(base),digest)==(data['variables'],data['clauses'],data['formula_sha256']),
            'independent joint formula differs')
    negatives=[];positive=[];exceptions=[]
    for row in data['records']:
        raw=set(map(tuple,row['cells']));shifts=list(map(tuple,row['shifts']))
        require(len(raw)==row['area'],'prototype area differs')
        chosen={f.var[q] for q in raw}
        ys={105+9*j+NINE.index(delta)+1 for j,delta in enumerate(shifts)}
        chosen|=ys;chosen|={z for (y,v),z in gates.items() if y in ys and v in chosen}
        require(all(any(z in chosen if z>0 else -z not in chosen for z in zs) for zs in base),
                'supplied geometry does not satisfy reconstructed model')
        geom=f.geometry(raw,shifts)
        require(geom['root_disc']==row['prototype_disc'] and geom['first_admissible']==row['first_admissible'],
                'geometric classification differs')
        if geom['first_admissible']:
            positive.append(dict(area=len(raw),shifts=shifts,first_cells=geom['first_cells']))
            exceptions.append([-v if f.U[v-1] in raw else v for v in range(1,106)])
        else:
            blocker=[-v if f.U[v-1] in raw else v for v in range(1,106)]
            if geom['root_disc']:blocker+=sorted((-y for y in ys),reverse=True)
            require(blocker==row['blocker'],'geometric blocker has the wrong scope')
            negatives.append(blocker)
    require(negatives==data['blockers'],'unjustified geometric blocker')
    proof=None
    classification=bool(data.get('classification_complete'))
    if classification:
        require(exceptions==data['exception_blockers'],'exception mask does not match a checked positive')
        require(bool(data['checked_negative'])==(not positive),'negative flag disagrees with the exceptions')
        proof=rup.RupChecker(base+negatives+exceptions,nv).verify(data['trace'])
    elif data['checked_negative']:
        require(not positive,'an admissible mask contradicts a negative claim')
        proof=rup.RupChecker(base+negatives,nv).verify(data['trace'])
    return dict(variables=nv,clauses=len(base),formula_sha256=digest,
                checked_negative=bool(proof) and not positive,checked_exclusions=len(negatives),
                classification_complete=bool(proof) and classification,proof_check=proof,
                positive_disc_models=positive,full_family_census=False)


def verify_lower(data):
    cells=set(map(tuple,data['cells']));require(disc(cells),'prototype is not a disc')
    shapes=images(cells);occupied=set();stats=[]
    for k,ps in enumerate(data['levels']):
        previous=set(occupied)
        for o,x,y in ps:
            fp={(a+x,b+y) for a,b in shapes[o]}
            require(not fp&occupied,'lower whole-copy overlap')
            if k:require(bool(fp&halo(previous)),'lower copy misses prior prefix')
            occupied|=fp
        if k:require(halo(previous)<=occupied,'lower incomplete collar')
        require(disc(occupied),'lower prefix is not a disc')
        stats.append(dict(level=k,copies=sum(map(len,data['levels'][:k+1])),cells=len(occupied)))
    require(len(data['levels'][0])==1 and set(cells)=={(a+data['levels'][0][0][1],b+data['levels'][0][0][2])
                                                     for a,b in shapes[data['levels'][0][0][0]]},'wrong literal lower root')
    return stats


def verify_corner(raw,fixed,certificate):
    """Replay via forbidden translation differences, not whole-copy trials."""
    occupied=set(fixed)
    original={(x+dx,y+dy) for x,y in fixed for dx,dy in product((0,1),repeat=2)}
    shapes=images(raw);quads=((0,0),(-1,0),(-1,-1),(0,-1))
    def inventory(vertex,q):
        require(tuple(vertex) in original,'required corner is not an original prefix vertex')
        require(type(q) is int and 0<=q<4,'invalid corner quadrant')
        x,y=vertex;qs=[(x+dx,y+dy) for dx,dy in quads]
        require(qs[q] not in occupied and qs[(q-1)%4] in occupied and qs[(q+1)%4] in occupied,
                'required corner is not an isolated empty sector')
        point=qs[q];feasible=[]
        for o,shape in enumerate(shapes):
            forbidden={(x-a,y-b) for x,y in occupied for a,b in shape}
            feasible.extend((o,point[0]-a,point[1]-b) for a,b in shape
                            if (point[0]-a,point[1]-b) not in forbidden)
        return feasible
    for row in certificate['steps']:
        require(len(row)==6 and all(type(z) is int for z in row),'invalid corner force')
        x,y,q,o,tx,ty=row
        choices=inventory((x,y),q)
        require(choices==[(o,tx,ty)],'claimed corner force is not a singleton')
        occupied|={(a+tx,b+ty) for a,b in shapes[o]}
    final=certificate['empty'];require(len(final)==3,'invalid terminal corner')
    require(not inventory(final[:2],final[2]),'terminal corner has a whole-copy supplier')
    return dict(forces=len(certificate['steps']),terminal_candidates=len(shapes)*len(raw),empty=final)


def verify_layouts(data):
    f=Frames();raw=set(map(tuple,data['cells']));require(disc(raw),'layout prototype is not a disc')
    require(f.I<=raw<=set(f.U),'layout prototype is outside the core/domain')
    root={f.position(f.poses[0],q) for q in raw};require(root==raw,'layout root is not identity')
    owners={};copies=[];clauses=set()
    for j,p in enumerate(f.poses[1:]):
        for k,(dx,dy) in enumerate(NINE):
            pose=(p[0],p[1]+dx,p[2]+dy);y=9*j+k+1
            fp={f.position(pose,q) for q in raw};copies.append((j,y,pose,fp))
            for point in fp:owners.setdefault(point,[]).append((j,y))
            if not fp&halo(root):clauses.add((-y,))
    for j in range(6):
        ys=list(range(9*j+1,9*j+10));clauses.add(tuple(ys))
        clauses.update(tuple(sorted((-a,-b))) for a,b in combinations(ys,2))
    for point,entries in owners.items():
        if point in root:clauses.update((-y,) for j,y in entries)
        for (j,y),(k,z) in combinations(entries,2):
            if j!=k:clauses.add(tuple(sorted((-y,-z))))
    for point in halo(root):clauses.add(tuple(y for j,y in owners.get(point,[])))
    base=[list(zs) for zs in sorted(clauses)]
    dimacs=('p cnf 54 '+str(len(base))+'\n'+''.join(' '.join(map(str,zs))+' 0\n' for zs in base)).encode()
    require((len(base),hashlib.sha256(dimacs).hexdigest())==(data['clauses'],data['formula_sha256']),
            'independent layout formula differs')
    blockers=[];records=[]
    for row in data['records']:
        shifts=list(map(tuple,row['shifts']));chosen={9*j+NINE.index(delta)+1 for j,delta in enumerate(shifts)}
        require(sorted(chosen)==row['selected'],'layout selector decoding differs')
        require(all(any(z in chosen if z>0 else -z not in chosen for z in zs) for zs in base),
                'layout does not satisfy its complete packing/surround formula')
        geom=f.geometry(raw,shifts);require(geom['first_admissible']==row['first_admissible'],'layout geometry differs')
        fixed=set(root)
        for j,y,p,fp in copies:
            if y in chosen:fixed|=fp
        record=dict(first_admissible=geom['first_admissible'],shifts=shifts)
        if geom['first_admissible']:
            require(row.get('corner_certificate') is not None,'uncertified admissible layout')
            record['corner']=verify_corner(raw,fixed,row['corner_certificate'])
        blocker=sorted(-y for y in chosen);require(blocker==row['blocker'],'layout blocker differs')
        blockers.append(blocker);records.append(record)
    require(blockers==data['blockers'] and not data['exceptions'],'layout census has unresolved exceptions')
    require(data['complete'] and data['checked_negative'],'layout result is not a completed exclusion')
    proof=rup.RupChecker(base+blockers,54).verify(data['trace'])
    return dict(variables=54,clauses=len(base),formula_sha256=data['formula_sha256'],checked_negative=True,
                checked_layouts=len(records),records=records,proof_check=proof,
                scope='Only the specified six first placements; hypothetical second motions unrestricted.')


def main():
    joint=json.loads((ROOT/'classification.json').read_text());joint['trace']=(ROOT/'residual.rup').read_text()
    candidate=json.loads((ROOT/'exception.json').read_text())
    layouts=json.loads((ROOT/'layouts.json').read_text());layouts['trace']=(ROOT/'layout.rup').read_text()
    positives=[row for row in joint['records'] if row['first_admissible']]
    require(len(positives)==1,'the stated prototype exception is not unique')
    require(positives[0]['cells']==candidate['cells']==layouts['cells'],'prototype files disagree')
    f=Frames();raw=set(map(tuple,candidate['cells']));shapes=images(raw)
    reference={frozenset(f.position(p,q) for q in raw) for p in f.pose_list(positives[0]['shifts'])}
    literal={frozenset((a+x,b+y) for a,b in shapes[o]) for level in candidate['levels'] for o,x,y in level}
    require(reference==literal,'literal first corona differs from the prototype exception')
    require(len(layouts['records'])==1 and layouts['records'][0]['shifts']==positives[0]['shifts'],
            'the sole exception layout differs between certificates')
    controls=[]
    bad=deepcopy(joint);bad['exception_blockers'][0][0]*=-1
    bad2=deepcopy(joint);bad2['trace']=''
    bad3=deepcopy(candidate);bad3['levels'][1][0]=deepcopy(bad3['levels'][0][0])
    bad4=deepcopy(layouts);bad4['records'][0]['corner_certificate']['empty'][2]=1
    bad5=deepcopy(layouts);bad5['records'].clear()
    for label,call in [('changed exception mask',lambda:verify_joint(bad)),
                       ('missing residual proof',lambda:verify_joint(bad2)),
                       ('overlapping positive pose',lambda:verify_lower(bad3)),
                       ('false corner sector',lambda:verify_layouts(bad4)),
                       ('missing exception layout',lambda:verify_layouts(bad5))]:
        try:call()
        except ValueError as exc:controls.append(dict(control=label,rejected=True,reason=str(exc)))
        else:raise ValueError('damaged control accepted: '+label)
    print(json.dumps(dict(agent='six-heesch-1',role='researcher',classification=verify_joint(joint),
                         layouts=verify_layouts(layouts),lower=verify_lower(candidate),damaged_controls=controls),sort_keys=True))


if __name__=='__main__':main()
