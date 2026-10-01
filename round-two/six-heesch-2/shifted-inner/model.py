"""Finite mask/pose compiler. Only the factor-two, depth-two instance is claimed."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from geometry import DIRS,affine,halo,holes


def components(points):
    unseen=set(points)
    out=[]
    while unseen:
        root=min(unseen);unseen.remove(root)
        part={root};todo=[root]
        while todo:
            x,y=todo.pop()
            for a,b in DIRS:
                q=(x+a,y+b)
                if q in unseen:
                    unseen.remove(q);part.add(q);todo.append(q)
        out.append(part)
    return out


class Model:
    def __init__(self,scale,depth=4):
        assert type(depth) is int and 1<=depth<=4
        self.scale=scale
        self.depth=depth
        self.fixture=json.loads((BASE/'seed.json').read_text())
        pool={(scale*x,scale*y) for x,y in self.fixture['tile']}
        for _ in range(scale+1):
            pool.update(halo(pool))
        self.cells=tuple(sorted(pool))
        self.x={p:i+1 for i,p in enumerate(self.cells)}
        self.options=[]
        self.groups=[]
        for j,record in enumerate(self.fixture['placements']):
            if record['level']>depth:continue
            group=[]
            for delta in ((0,0),) if j==0 else ((0,0),)+DIRS:
                a,b,c,d,u,v=record['pose']
                group.append(len(self.options))
                self.options.append({'copy':j,'level':record['level'],'delta':delta,
                                     'pose':(a,b,c,d,scale*u+delta[0],scale*v+delta[1])})
            self.groups.append(tuple(group))
        for o,option in enumerate(self.options):
            option['y']=len(self.cells)+o+1
        self.z_start=len(self.cells)+len(self.options)+1
        self.incidence=defaultdict(list)
        for o,option in enumerate(self.options):
            for p in self.cells:
                q=affine([p],option['pose'])[0]
                self.incidence[q].append(self.z(o,p))
        self.prefix=[]
        for k in range(depth+1):
            self.prefix.append({q:tuple(z for z in zs if self.options[self.option_of(z)]['level']<=k)
                                for q,zs in sorted(self.incidence.items())
                                if any(self.options[self.option_of(z)]['level']<=k for z in zs)})
        last=self.z_start+len(self.options)*len(self.cells)-1
        self.u=[]
        for k in range(depth+1):
            row={}
            for q in self.prefix[k]:
                last+=1;row[q]=last
            self.u.append(row)
        self.core_variables=last
        self.variables=last
        self.sequence_groups=[]
        self.stats=defaultdict(int)

    def z(self,option,p):
        return self.z_start+option*len(self.cells)+self.x[p]-1

    def option_of(self,z):
        return (z-self.z_start)//len(self.cells)

    def clauses(self):
        self.variables=self.core_variables
        self.sequence_groups=[]
        self.stats=defaultdict(int)
        def emit(c,kind):
            self.stats[kind]+=1
            return tuple(c)
        def amo(literals,kind):
            literals=tuple(literals)
            if len(literals)<=4:
                for i,a in enumerate(literals):
                    for b in literals[i+1:]:
                        yield emit((-a,-b),kind)
                return
            sequence=tuple(range(self.variables+1,self.variables+len(literals)))
            self.variables+=len(sequence)
            self.sequence_groups.append((literals,sequence))
            yield emit((-literals[0],sequence[0]),kind)
            for i in range(1,len(literals)-1):
                yield emit((-literals[i],sequence[i]),kind)
                yield emit((-sequence[i-1],sequence[i]),kind)
                yield emit((-literals[i],-sequence[i-1]),kind)
            yield emit((-literals[-1],-sequence[-1]),kind)
        yield emit((self.x[0,0],),'anchor')
        for group in self.groups:
            literals=tuple(self.options[o]['y'] for o in group)
            yield emit(literals,'choice_positive')
            yield from amo(literals,'choice_at_most_one')
        for o,option in enumerate(self.options):
            y=option['y']
            for p,x in self.x.items():
                z=self.z(o,p)
                yield emit((-z,x),'occupancy_equivalence')
                yield emit((-z,y),'occupancy_equivalence')
                yield emit((-x,-y,z),'occupancy_equivalence')
        for q,zs in sorted(self.incidence.items()):
            yield from amo(zs,'packing_at_most_one')
        for k in range(self.depth+1):
            for q,zs in self.prefix[k].items():
                u=self.u[k][q]
                yield emit((-u,)+zs,'prefix_equivalence')
                for z in zs:
                    yield emit((-z,u),'prefix_equivalence')
        for k in range(self.depth):
            for (x,y),u in self.u[k].items():
                for a,b in DIRS:
                    v=self.u[k+1].get((x+a,y+b))
                    yield emit((-u,) if v is None else (-u,v),'halo')
        for (x,y),v in self.x.items():
            neighbors=tuple(self.x[x+a,y+b] for a,b in DIRS if (x+a,y+b) in self.x)
            yield emit((-v,)+neighbors,'non_isolation')

    def preflight(self):
        digest=hashlib.sha256();clause_count=0;literals=0
        for clause in self.clauses():
            clause_count+=1;literals+=len(clause)
            digest.update((' '.join(map(str,clause))+' 0\n').encode())
        return {'agent':'six-heesch-2','role':'researcher','scale':self.scale,'depth':self.depth,
                'mask_cells':len(self.cells),'pose_options':len(self.options),
                'occupancy_variables':len(self.options)*len(self.cells),
                'prefix_variables':sum(map(len,self.u)),'total_variables':self.variables,
                'global_cells':len(self.incidence),'maximum_packing_row':max(map(len,self.incidence.values())),
                'clauses':clause_count,'literals':literals,'clause_kinds':dict(self.stats),
                'cnf_sha256':digest.hexdigest(),
                'prefix_global_cells':list(map(len,self.u))}

    def known_seed_assignment(self):
        assert self.scale==1
        tile=set(map(tuple,self.fixture['tile']))
        true={self.x[p] for p in tile}
        for o,option in enumerate(self.options):
            if option['delta']==(0,0):
                true.add(option['y'])
                true.update(self.z(o,p) for p in tile)
        for k in range(self.depth+1):
            for q,zs in self.prefix[k].items():
                if true.intersection(zs):true.add(self.u[k][q])
        # Initialize all deterministic AMO auxiliaries by their intended OR.
        for literals,sequence in self.sequence_groups:
            previous=False
            for literal,auxiliary in zip(literals,sequence):
                previous=previous or literal in true
                if previous:true.add(auxiliary)
        return true

    def decode(self,true):
        tile=tuple(p for p,v in self.x.items() if v in true)
        placements=[];choices=[]
        for group in self.groups:
            selected=[o for o in group if self.options[o]['y'] in true]
            assert len(selected)==1
            option=self.options[selected[0]]
            placements.append({'level':option['level'],'pose':list(option['pose'])})
            choices.append(list(option['delta']))
        # Read occupancies from the decoded mask/options, not auxiliary bits.
        footprints=[set(affine(tile,r['pose'])) for r in placements]
        occupied=set()
        for cells in footprints:
            assert occupied.isdisjoint(cells);occupied.update(cells)
        regions=[set().union(*(cells for cells,r in zip(footprints,placements) if r['level']<=k)) for k in range(self.depth+1)]
        assert all(halo(regions[k])<=regions[k+1] for k in range(self.depth))
        assert (0,0) in tile
        return tile,placements,footprints,regions,choices
