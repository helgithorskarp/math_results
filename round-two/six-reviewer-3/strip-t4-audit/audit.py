"""Independent complete-model reconstruction of the T4 Heesch certificate.

Only frozen public JSON data are read. No researcher module is imported.
Cube-coordinate permutations generate isometries; directed polygon edges
check disc topology; cell owners generate conflicts; reachable recursive
obligations validate rejection DAGs. Exact-cover search has unit propagation.
The continuous coverage proof and count-depth refinements are in REVIEW.md.
"""
import argparse
from collections import Counter, defaultdict, deque
import hashlib
from itertools import permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
VERT = ((1,1),(0,2),(-1,1),(-1,-1),(0,-2),(1,-1))


def need(condition,message):
    if not condition:raise ValueError(message)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def strip(k):
    return tuple(sorted({(0,0),(-2*k,k-1),(-2*k-1,k)} |
                        {(x,y) for r in range(k) for x in (-2*r-1,-2*r-2)
                         for y in (r+1,r+2)}))


def cube(point,p,sign):
    x,y=point;v=(x,y,-x-y)
    return sign*v[p[0]],sign*v[p[1]]


# Columns from all permutations of x+y+z=0, with global sign +/-1.
MATRICES=tuple(sorted({(cube((1,0),p,s)[0],cube((0,1),p,s)[0],
                        cube((1,0),p,s)[1],cube((0,1),p,s)[1])
                       for p in permutations(range(3)) for s in (-1,1)}))


def matrix_ok(m):
    if len(m)!=4 or not all(type(x) is int for x in m):return False
    a,b,c,d=m
    return (a*d-b*c in (-1,1) and a*a+a*c+c*c==1 and b*b+b*d+d*d==1
            and 2*a*b+a*d+b*c+2*c*d==1)


def move(cells,g):
    need(len(g)==6 and all(type(x) is int for x in g) and matrix_ok(g[:4]),
         'literal axial isometry')
    a,b,c,d,u,v=g
    return tuple(sorted((a*x+b*y+u,c*x+d*y+v) for x,y in cells))


def undo(g):
    a,b,c,d,u,v=g;det=a*d-b*c
    ia,ib,ic,id=d*det,-b*det,-c*det,a*det
    return ia,ib,ic,id,-ia*u-ib*v,-ic*u-id*v


def fringe(cells):
    s=set(cells)
    return {(x+a,y+b) for x,y in s for a,b in DIR}-s


def boundary(cells):
    """Actual polygon boundary cycles, not an empty-cell flood fill."""
    edges=set()
    for x,y in cells:
        v=[(2*x+y+a,3*y+b) for a,b in VERT]
        for p,q in zip(v,v[1:]+v[:1]):
            if (q,p) in edges:edges.remove((q,p))
            else:edges.add((p,q))
    outgoing={};incoming={}
    for p,q in edges:
        need(p not in outgoing and q not in incoming,'nonbranching honeycomb boundary')
        outgoing[p]=q;incoming[q]=p
    need(set(outgoing)==set(incoming),'closed polygon boundary')
    unseen=set(outgoing);signed=[];lengths=[]
    while unseen:
        start=min(unseen);v=start;area=0;n=0
        while True:
            need(v in unseen,'simple boundary cycle');unseen.remove(v)
            w=outgoing[v];area+=v[0]*w[1]-w[0]*v[1];n+=1;v=w
            if v==start:break
        need(area!=0,'nonzero polygon area');signed.append(area);lengths.append(n)
    need(sum(signed)==12*len(set(cells)),'exact hexagon area from all boundary cycles')
    return {'outer_cycles':sum(x>0 for x in signed),
            'hole_cycles':sum(x<0 for x in signed),
            'signed_twice_scaled_areas':sorted(signed),'boundary_edges':sum(lengths)}


def disk(cells):
    record=boundary(cells)
    need(record['outer_cycles']==1 and record['hole_cycles']==0,'topological disc')
    return record


class Atlas:
    def __init__(self,tile):
        self.tile=tile;self.set=set(tile)
        orbit={}
        for m in MATRICES:
            raw=move(tile,m+(0,0));u,v=min(raw)
            normalized=tuple((x-u,y-v) for x,y in raw)
            orbit[normalized]=m
        need(len(MATRICES)==len(orbit)==12,'all motions and trivial prototype stabilizer')
        self.oriented=tuple(sorted(orbit))
        self._frames={tile:(1,0,0,1,0,0)}
        # Match opposite unit edges through their two neighboring cell centers.
        contacts=set()
        for oriented in self.oriented:
            own=set(oriented)
            for x,y in tile:
                for a,b in DIR:
                    q=(x+a,y+b)
                    if q in self.set:continue
                    for u,v in oriented:
                        if (u-a,v-b) in own:continue
                        t=tuple((i+q[0]-u,j+q[1]-v) for i,j in oriented)
                        if self.set.isdisjoint(t):contacts.add(t)
        self.raw=tuple(sorted(contacts));self.index={t:i for i,t in enumerate(self.raw)}
        self.rawset=set(self.raw)

    def frame(self,t):
        if t not in self._frames:
            solutions=[]
            for m in MATRICES:
                raw=move(self.tile,m+(0,0));a,b=min(raw);x,y=min(t)
                g=m+(x-a,y-b)
                if move(self.tile,g)==t:solutions.append(g)
            need(len(solutions)==1,'unique full-footprint frame');self._frames[t]=solutions[0]
        return self._frames[t]

    def reciprocal(self,t):return move(self.tile,undo(self.frame(t)))

    def domain(self,indices):
        need(len(indices)==len(set(indices)) and all(type(i) is int and 0<=i<len(self.raw)
             for i in indices),'original raw-domain indices')
        out={self.raw[i] for i in indices}
        need(all(self.reciprocal(t) in out for t in out),'reciprocal domain')
        return out

    def compatible(self,a,b,domain):
        if set(a)&set(b):return False
        if not set(b)&fringe(a):return True
        return move(b,undo(self.frame(a))) in domain and move(a,undo(self.frame(b))) in domain

    def pool(self,fixed,domain):
        occupied=set().union(*map(set,fixed));required=tuple(sorted(fringe(occupied)))
        old={t:{move(u,self.frame(t)) for u in domain} for t in fixed}
        candidates=set().union(*old.values())
        candidates={u for u in candidates if occupied.isdisjoint(u) and set(u)&set(required)
                    and all(not set(u)&fringe(t) or u in old[t] for t in fixed)}
        return required,tuple(sorted(candidates))


class Model:
    def __init__(self,atlas,required,tiles,domain=None):
        self.atlas=atlas;self.required=tuple(sorted(required));self.tiles=tuple(sorted(tiles))
        self.domain=domain;self.owners=defaultdict(int)
        for i,t in enumerate(self.tiles):
            for q in t:self.owners[q]|=1<<i
        self.at=[self.owners[q] for q in self.required]
        slots={q:j for j,q in enumerate(self.required)}
        self.cover=[sum(1<<slots[q] for q in t if q in slots) for t in self.tiles]
        need(all(self.cover),'every candidate covers a required original cell')
        self.full=(1<<len(self.required))-1;self.all=(1<<len(self.tiles))-1
        self.rows={};self.failed=set();self.nodes=0

    def conflict(self,i):
        if i not in self.rows:
            t=self.tiles[i];overlap=0;touching=0
            for x,y in t:
                overlap|=self.owners[(x,y)]
                if self.domain is not None:
                    for a,b in DIR:touching|=self.owners[(x+a,y+b)]
            result=overlap
            if self.domain is not None:
                choices=touching&~overlap
                while choices:
                    bit=choices&-choices;choices-=bit;j=bit.bit_length()-1
                    if not self.atlas.compatible(t,self.tiles[j],self.domain):result|=bit
            need((result>>i)&1,'chosen full footprint removes itself')
            self.rows[i]=result
        return self.rows[i]

    def search(self,forced=None):
        """Unit propagation, then minimum-cell exact-cover branching."""
        initial=(self.all,self.full) if forced is None else (
            self.all&~self.conflict(forced),self.full&~self.cover[forced])
        def solve(available,remaining):
            self.nodes+=1
            if self.nodes>100000:raise RuntimeError('fixed 100000-node guard; incomplete')
            if (available,remaining) in self.failed:return False
            original=available,remaining
            while remaining:
                bits=remaining;minimum=None;best=None
                while bits:
                    bit=bits&-bits;bits-=bit
                    legal=available&self.at[bit.bit_length()-1];count=legal.bit_count()
                    if count==0:self.failed.add(original);return False
                    if minimum is None or count<minimum:minimum=count;best=legal
                    if count==1:break
                if minimum>1:break
                i=best.bit_length()-1;available&=~self.conflict(i);remaining&=~self.cover[i]
            if not remaining:return True
            while best:
                bit=best&-best;best-=bit;i=bit.bit_length()-1
                if solve(available&~self.conflict(i),remaining&~self.cover[i]):return True
            self.failed.add(original);return False
        return solve(*initial)

    def rejection(self,data):
        need(data['pool_sha256']==fingerprint({'required':self.required,'tiles':self.tiles}),
             'complete original-cell and candidate-pool fingerprint')
        root=tuple(int(x,16) for x in data['root'])
        need(root==(self.all,self.full),'full unpruned rejection root')
        states={}
        for a,r,q in data['nodes']:
            key=int(a,16),int(r,16)
            need(key not in states and key[1]!=0 and not key[0]&~self.all
                 and not key[1]&~self.full,'proper distinct non-success state')
            need(type(q) is int and 0<=q<len(self.required) and (key[1]>>q)&1,
                 'split on an actual uncovered cell')
            states[key]=q
        done=set();active=set()
        def prove(key):
            if key in done:return
            need(key in states and key not in active,'all branches have acyclic failed obligations')
            active.add(key);a,r=key;choices=a&self.at[states[key]]
            while choices:
                bit=choices&-choices;choices-=bit;i=bit.bit_length()-1
                child=a&~self.conflict(i),r&~self.cover[i]
                need(child[1].bit_count()<r.bit_count(),'strict uncovered-cell descent')
                need(child[1]!=0,'a successful branch cannot be certified failed')
                prove(child)
            active.remove(key);done.add(key)
        prove(root)
        for key in states:prove(key)
        need(done==set(states),'every original DAG state checked')
        return len(done)


def patch(atlas,data):
    cells=[];levels=[]
    for row in data['placements']:
        level=row['level'];need(type(level) is int and level>=0,'nonnegative integer level')
        cells.append(move(atlas.tile,tuple(row['pose'])));levels.append(level)
    need(levels.count(0)==1 and cells[levels.index(0)]==atlas.tile,'one original root')
    occupied=set()
    for t in cells:need(occupied.isdisjoint(t),'disjoint whole copies');occupied.update(t)
    graph=[set() for _ in cells]
    for i,t in enumerate(cells):
        for j in range(i):
            if set(cells[j])&fringe(t):graph[i].add(j);graph[j].add(i)
    distance={levels.index(0):0};queue=deque(distance)
    while queue:
        i=queue.popleft()
        for j in graph[i]:
            if j not in distance:distance[j]=distance[i]+1;queue.append(j)
    need(len(distance)==len(cells) and all(distance[i]==k for i,k in enumerate(levels)),
         'literal contact distances agree with every listed corona level')
    previous=set();rows=[]
    for k in range(max(levels)+1):
        layer=[t for t,l in zip(cells,levels) if l==k]
        need(layer,'nonempty consecutive layer');union=previous.union(*map(set,layer))
        if k:need(fringe(previous)<=union,'complete predecessor halo, including holes')
        topology=disk(union)
        rows.append({'level':k,'copies':len(layer),'cumulative_cells':len(union),
                     'hole_cells':0,'boundary_edges':topology['boundary_edges']})
        previous=union
    return rows


def inventory(atlas,domain):
    model=Model(atlas,fringe(atlas.tile),tuple(domain),domain)
    solutions=set();nodes=0
    def visit(available,remaining,chosen):
        nonlocal nodes
        nodes+=1
        if nodes>100000:raise RuntimeError('fixed inventory node guard; incomplete')
        if not remaining:solutions.add(tuple(sorted(chosen)));return
        choices=[(available&model.at[j],j) for j in range(len(model.required)) if (remaining>>j)&1]
        legal,j=min(choices,key=lambda x:(x[0].bit_count(),-x[1]))
        while legal:
            bit=legal&-legal;legal-=bit;i=bit.bit_length()-1
            visit(available&~model.conflict(i),remaining&~model.cover[i],chosen+(i,))
    visit(model.all,model.full,())
    return tuple(sorted(tuple(sorted(atlas.index[model.tiles[i]] for i in row)) for row in solutions)),nodes


def inputs(folder):
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    out={}
    for entry in manifest['runtime_files']:
        p=folder/entry['name'];raw=p.read_bytes()
        need(hashlib.sha256(raw).hexdigest()==entry['sha256'],'frozen public JSON '+p.name)
        out[p.stem]=json.loads(raw)
    return out


def rejected(action):
    try:action()
    except ValueError:return
    raise ValueError('damaged mathematical control accepted')


def controls(atlas,domain,example):
    count=0
    for m in [(1,1,0,1),(1,0,0,2),(1,0,0,True)]:
        rejected(lambda m=m:move(atlas.tile,tuple(m)+(0,0)));count+=1
    rejected(lambda:disk(set(DIR)));count+=1
    rejected(lambda:disk({(0,0),(10,10)}));count+=1
    required,tiles=atlas.pool((atlas.tile,atlas.raw[example[0]]),domain)
    model=Model(atlas,required,tiles,domain)
    bad=json.loads(json.dumps(example[1]));bad['pool_sha256']='0'*64
    rejected(lambda:model.rejection(bad));count+=1
    bad=json.loads(json.dumps(example[1]));bad['nodes']=[]
    rejected(lambda:model.rejection(bad));count+=1
    bad=json.loads(json.dumps(example[1]));bad['nodes'][0][2]=len(required)
    rejected(lambda:model.rejection(bad));count+=1
    tiny=Model(atlas,((0,0),),(((0,0),),))
    false={'pool_sha256':fingerprint({'required':tiny.required,'tiles':tiny.tiles}),
           'root':['0x1','0x1'],'nodes':[['0x1','0x1',0]]}
    rejected(lambda:tiny.rejection(false));count+=1
    need(tiny.search(),'one-cell positive search control')
    for t in domain:
        u=atlas.reciprocal(t)
        if u!=t:
            ids=[atlas.index[x] for x in domain if x!=t]
            rejected(lambda:atlas.domain(ids));count+=1;break
    need(count==10,'all ten independent damaged controls')
    return count


def main(folder):
    data=inputs(folder);upper=data['upper'];atlas=Atlas(strip(4));disk(atlas.tile)
    need(len(atlas.raw)==568 and fingerprint(atlas.raw)==upper['raw_sha256'],
         'complete independently aligned contact atlas')
    need(tuple(map(tuple,data['lower']['tile']))==atlas.tile,'literal nineteen-cell lower prototype')
    lower=patch(atlas,data['lower']);need([x['copies'] for x in lower]==[1,5,12,21],'three-corona lower')
    control_tile=tuple(map(tuple,data['control15']['tile']))
    control=Atlas(control_tile)
    def normal(cells):
        x,y=min(cells);return tuple((a-x,b-y) for a,b in cells)
    need(normal(strip(3)) in control.oriented,'primary T3 congruence')
    control_rows=patch(control,data['control15'])
    need([x['copies'] for x in control_rows]==[1,6,13,21,35],'known T3 four-corona control')
    first=Model(atlas,fringe(atlas.tile),atlas.raw)
    exclusions=upper['first_exclusions']
    need(len(exclusions)==len(set(exclusions))==243,'all first exclusions distinct')
    for i in exclusions:
        need(type(i) is int and 0<=i<len(atlas.raw),'original first-support index')
        need(not first.search(i),'independent first-support exclusion')
    survivors=set(range(len(atlas.raw)))-set(exclusions)
    reciprocal={i for i in survivors if atlas.index[atlas.reciprocal(atlas.raw[i])] in survivors}
    need(len(reciprocal)==240,'exact reciprocal first-support prefilter')
    atlas.domain(sorted(reciprocal));early_nodes=first.nodes
    r1=upper['round1_exclusions'];need(len(r1)==len(set(r1))==50 and set(r1)<=reciprocal,'round-one fixed contacts')
    for i in r1:
        required,tiles=atlas.pool((atlas.tile,atlas.raw[i]),atlas.rawset)
        model=Model(atlas,required,tiles)
        need(not model.search(),'independent full-E0 pair rejection');early_nodes+=model.nodes
    current=reciprocal-set(r1)
    need(sorted(current)==upper['domains']['1'] and len(current)==190,'derived necessary D1')
    records=[];states=0
    for r in (2,3):
        domain=atlas.domain(sorted(current));proofs=upper['later_exclusions'][str(r)]
        excluded=set(map(int,proofs));need(excluded<=current,'only input contacts are deleted')
        for label,certificate in sorted(proofs.items(),key=lambda x:int(x[0])):
            required,tiles=atlas.pool((atlas.tile,atlas.raw[int(label)]),domain)
            model=Model(atlas,required,tiles,domain);n=model.rejection(certificate);states+=n
            records.append({'round':r,'raw_contact':int(label),'required':len(required),
                            'candidates':len(tiles),'states':n,'pool_sha256':certificate['pool_sha256']})
        current-=excluded
        need(sorted(current)==upper['domains'][str(r)],'complete derived next necessary domain')
        atlas.domain(sorted(current))
    d3=atlas.domain(sorted(current));d2=atlas.domain(upper['domains']['2'])
    need(len(d2)==43 and len(d3)==29,'exact necessary later-domain sizes')
    stars,nodes=inventory(atlas,d3)
    expected=tuple(sorted(tuple(sorted(x['contacts'])) for x in upper['root_stars']))
    need(stars==expected and len(stars)==len(set(stars))==17,'complete independently enumerated root stars')
    stable=data['stable'];need(len(stable)==29 and {x['contact'] for x in stable}==current,'one fixed-point witness per contact')
    witness_records=[]
    for row in stable:
        fixed=(atlas.tile,atlas.raw[row['contact']])
        copies=(*fixed,*(move(atlas.tile,tuple(g)) for g in row['neighbors']))
        occupied=set()
        for t in copies:need(occupied.isdisjoint(t),'disjoint fixed-point witness');occupied.update(t)
        need(fringe(set().union(*map(set,fixed)))<=occupied,'whole two-root halo covered')
        need(all(atlas.compatible(a,b,d3) for i,a in enumerate(copies) for b in copies[:i]),
             'all actual positive witness contacts in D3')
        witness_records.append({'contact':row['contact'],'copies':len(copies),'footprints_sha256':fingerprint(copies)})
    for row in upper['root_stars']:
        fixed=(atlas.tile,*(atlas.raw[i] for i in row['contacts']))
        required,tiles=atlas.pool(fixed,d2)
        n=Model(atlas,required,tiles,d2).rejection(row['second_rejection']);states+=n
        records.append({'round':'root-star','raw_contacts':row['contacts'],'required':len(required),
                        'candidates':len(tiles),'states':n,'pool_sha256':row['second_rejection']['pool_sha256']})
    need(len(records)==178 and states==387,'every late original rejection and every state verified')
    first_label=next(iter(upper['later_exclusions']['2']))
    damage=controls(atlas,atlas.domain(upper['domains']['1']),
                    (int(first_label),upper['later_exclusions']['2'][first_label]))
    return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','status':'VERIFIED',
            'method':'cube isometries; directed boundary cycles; cell-owner conflicts; unit propagation; recursive rejection obligations',
            'original_canonical_upper_sha256':fingerprint(upper),
            'raw_contacts':len(atlas.raw),'raw_sha256':fingerprint(atlas.raw),'domain_sizes':[568,190,43,29],
            'first_exclusions':243,'pair_E0_exclusions':50,'independent_early_search_nodes':early_nodes,
            'root_stars':stars,'star_size_histogram':dict(sorted(Counter(map(len,stars)).items())),
            'independent_inventory_nodes':nodes,'late_rejection_records':records,'DAG_states':states,
            'fixed_point_witnesses':witness_records,'lower_coronas':lower,'known_T3_control':control_rows,
            'damaged_controls':damage,'proved_refinements':['all-layer-holes depth maximum3',
                'E3 equals D3; all later Er equal D3; D3 is greatest pair-operator fixed point'],
            'trust':'complete ordinary geometry/depth/finite-coverage proof unformalized; exact CPython; frozen public data decoded and independently checked'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path);args=parser.parse_args();result=main(args.input_dir)
    if args.output:args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'complete_evidence_sha256':fingerprint(result),
                      'DAG_states':result['DAG_states'],'root_stars':len(result['root_stars']),
                      'early_search_nodes':result['independent_early_search_nodes'],'damaged_controls':result['damaged_controls']},sort_keys=True))
