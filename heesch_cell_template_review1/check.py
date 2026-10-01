"""Independent cell-template audit by six-reviewer-1, mathematical reviewer.

Untrusted public input: the explicitly pinned original certificate. No author
code, solver, or external geometry implementation is imported.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


PIN = 'e42622028ac53dc6f39de632d7dcbb958d628788a7a2178cdca039ff00dfd6ba'
BOUNDARY = ((3,0),(8,0),(8,5),(10,5),(10,8),(11,8),(11,9),
            (6,9),(6,7),(3,7),(3,6),(0,6),(0,2),(3,2))
NEAR = tuple(product((-1,0,1), repeat=2))


def require(test, message):
    if not test:
        raise ValueError(message)


def pair(x):
    require(len(x)==2 and all(type(a) is int for a in x), 'integer pair')
    return tuple(x)


def prototype():
    # Signed ray-crossing of doubled odd cell centers against doubled edges.
    inside = set()
    for x in range(-1,12):
        for y in range(-1,10):
            px,py = 2*x+1,2*y+1
            winding = 0
            for (ax,ay),(bx,by) in zip(BOUNDARY, BOUNDARY[1:]+BOUNDARY[:1]):
                ax,ay,bx,by = 2*ax,2*ay,2*bx,2*by
                if ax==bx and ax>px:
                    if ay<=py<by:
                        winding += 1
                    elif by<=py<ay:
                        winding -= 1
            require(winding in (0,1), 'simple oriented polygon scan')
            if winding:
                inside.add((x,y))
    require(len(inside)==60, 'prototype area')
    return inside


def halo(cells):
    return {(x+a,y+b) for x,y in cells for a,b in NEAR}


def frame(raw):
    m,t = raw
    require(len(m)==2 and all(len(row)==2 for row in m), 'matrix dimensions')
    m = tuple(map(tuple,m)); t = pair(t)
    require(all(type(a) is int and a in (-1,0,1) for row in m for a in row), 'matrix entries')
    require(all(sum(abs(a) for a in row)==1 for row in m) and
            all(sum(abs(m[i][j]) for i in range(2))==1 for j in range(2)),
            'signed permutation isometry')
    return m,t


def image(p, fr):
    m,t = fr
    center = (2*p[0]+1,2*p[1]+1)
    out = tuple(m[i][0]*center[0]+m[i][1]*center[1]+2*t[i] for i in range(2))
    require(all(a%2==1 for a in out), 'transformed odd center')
    return tuple((a-1)//2 for a in out)


def address(p):
    # Direct linear homomorphism, without floor division or a Bezout basis.
    x,y = p
    return x%2, (19*x-y)%120


def clause(raw):
    require(all(type(a) is int and a!=0 for a in raw), 'nonzero integer literal')
    row = frozenset(raw)
    require(not any(-a in row for a in row), 'tautological stored clause')
    return row


def masks(row):
    positive=negative=0
    for a in row:
        require(type(a) is int and a!=0, 'valid proof literal')
        bit=1<<(abs(a)-1)
        if a>0:
            positive |= bit
        else:
            negative |= bit
    return positive,negative


def propagate(database, true=0, false=0):
    """Bit-parallel unit saturation, applying all discovered units per epoch."""
    epochs = 0
    while True:
        if true&false:
            return True,true,false,epochs
        up=down=0
        for positive,negative in database:
            if positive&true or negative&false:
                continue
            remaining=(positive|negative)&~(true|false)
            if not remaining:
                return True,true,false,epochs
            if remaining&(remaining-1)==0:
                if positive&remaining:
                    up |= remaining
                else:
                    down |= remaining
        if up&false or down&true or up&down:
            return True,true|up,false|down,epochs
        if not (up&~true or down&~false):
            return False,true,false,epochs
        true |= up; false |= down; epochs += 1


def geometry(inputs):
    p=prototype();pool=tuple(map(pair,inputs['pool']));core=set(map(pair,inputs['core']))
    require(pool==tuple(sorted(halo(p))) and len(pool)==104, 'exact halo pool')
    require(set(map(pair,inputs['prototype']))==p, 'prototype matches polygon')
    require(core=={q for q in p if halo({q})<=p} and len(core)==25, 'exact eroded core')
    ids={q:i+1 for i,q in enumerate(pool)}
    levels=[[frame(fr) for fr in row] for row in inputs['frames']]
    flat=[fr for row in levels for fr in row]
    require(list(map(len,levels))==[1,6,12] and len(set(flat))==19, 'distinct whole-copy frames')
    require(levels[0]==[(((1,0),(0,1)),(0,0))], 'identity root')
    physical=defaultdict(list);prefix=[defaultdict(set) for _ in levels]
    for level,frames in enumerate(levels):
        for fr in frames:
            transformed=[image(q,fr) for q in pool]
            require(len(set(transformed))==104, 'copy cell injectivity')
            for q,z in ids.items():
                site=image(q,fr);physical[site].append(z)
                for k in range(level,3):
                    prefix[k][site].add(z)
    packing=set()
    for owners in physical.values():
        for a,b in combinations(owners,2):
            packing.add(frozenset((-a,-b)))
    surrounds=set()
    for k in range(2):
        for (x,y),owners in prefix[k].items():
            for dx,dy in NEAR:
                next_owners=prefix[k+1].get((x+dx,y+dy),set())
                for z in owners:
                    if z not in next_owners:
                        surrounds.add(frozenset([-z,*next_owners]))
    geometric=packing|surrounds
    core_units={frozenset((ids[q],)) for q in core}
    return p,pool,core,ids,levels,geometric,core_units,packing,surrounds


def periodic(inputs, ids):
    require(list(map(pair,inputs['period_generators']))==[(6,-6),(2,38)], 'stated period generators')
    require(address((6,-6))==(0,0) and address((2,38))==(0,0), 'period homomorphism')
    frames=[frame(fr) for fr in inputs['periodic_frames']]
    require(len(frames)==4 and len(set(frames))==4, 'four periodic frames')
    owners={key:[] for key in product(range(2),range(120))}
    for copy,fr in enumerate(frames):
        for p,z in ids.items():
            owners[address(image(p,fr))].append((copy,z))
    # Preserve occurrences; identifying equal prototype variables is unsound.
    pairs=set();self_collisions=set()
    for occurrences in owners.values():
        for (_,a),(_,b) in combinations(occurrences,2):
            if a==b:
                self_collisions.add(a)
            else:
                pairs.add(tuple(sorted((a,b))))
    gaps=Counter(tuple(sorted({z for _,z in row})) for row in owners.values())
    return frames,owners,pairs,self_collisions,gaps


def rup(packet):
    nv=packet['nv']
    require(type(nv) is int and nv>=104, 'variable count')
    database=[]
    for row in packet['clauses']:
        require(all(1<=abs(a)<=nv for a in row), 'input variable domain')
        database.append(masks(row))
    trace=packet['rup']
    require(trace and trace[-1]==[], 'final empty clause')
    epochs=[]
    for index,row in enumerate(trace):
        require(all(type(a) is int and 1<=abs(a)<=nv for a in row), 'RUP variable domain')
        positive,negative=masks(row)
        conflict,_,_,count=propagate(database,negative,positive)
        require(conflict, 'RUP failure at step '+str(index))
        epochs.append(count)
        database.append((positive,negative))
    return epochs


def core_removal(geometric,core,ids,seeds,packet):
    anchor=ids[min(core)]
    exceptions=[ids[tuple(s['cell'])] for s in seeds if not s['conflict'] and not s['core_forced']]
    require([list(q) for q,z in ids.items() if z in exceptions]==[[2,6],[10,8]],
            'two exceptional seeds')
    guards=[]
    for z in exceptions:
        candidates=[row for row in geometric if -z in row and
                    all(a>0 and a not in exceptions for a in row-{-z})]
        require(candidates, 'exception requires an outside cell')
        guards.append(sorted(min(candidates,key=lambda row:(len(row),tuple(sorted(row))))))
    prefix=[[-z,anchor] for z in range(1,105) if z!=anchor and z not in exceptions]
    prefix += [[-z,anchor] for z in exceptions]
    prefix += [[anchor]]
    prefix += [[ids[q]] for q in sorted(core) if ids[q]!=anchor]
    base=[sorted(row) for row in sorted(geometric,key=lambda row:tuple(sorted(row)))]
    nonempty=list(range(1,105))
    # The prefix alone is not a contradiction: verify its RUP additions
    # individually, leaving the original geometric premises unchanged.
    db=[masks(row) for row in base+[nonempty]]
    counts=[]
    for row in prefix:
        pos,neg=masks(row)
        conflict,_,_,epochs=propagate(db,neg,pos)
        require(conflict, 'core-removal RUP prefix')
        counts.append(epochs);db.append((pos,neg))
    # Every old core premise is now explicitly present. Old noncore clauses
    # retain their geometric/gate justification from the independent audit.
    core_units={frozenset((ids[q],)) for q in core}
    new_base=[row for row in packet['clauses'] if frozenset(row) not in core_units]+[nonempty]
    require(len(new_base)==1794, 'new formula:25 core units replaced by nonempty')
    trace=prefix+packet['rup']
    combined_epochs=rup({'nv':397,'clauses':new_base,'rup':trace})
    require(len(prefix)==128 and len(trace)==330, 'compact proof lengths')
    artifact={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
              'original_certificate_sha256':PIN,'anchor_cell':list(min(core)),
              'anchor_variable':anchor,'exception_cells':[[2,6],[10,8]],
              'exception_guard_clauses':guards,
              'base_change':'Replace the25 original positive core unit clauses with[1,...,104]. Keep every other original clause.',
              'prefix_rup':prefix,'append_original_rup':True,
              'scope':'Every nonempty S subset U satisfying the fixed19-copy packing and two strict surrounds contains the25-cell core and tiles by the supplied four-copy period.'}
    digest=hashlib.sha256(json.dumps(artifact,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    # Without nonemptiness, the all-false geometric model survives.
    before_anchor=[masks(row) for row in base+prefix[:103]]
    no_nonempty=propagate(before_anchor,0,1<<(anchor-1))[0]
    require(not no_nonempty, 'empty prototype is a necessary exception')
    return {'anchor':list(min(core)),'anchor_variable':anchor,
            'exceptions':[[2,6],[10,8]],'exception_guard_clauses':guards,
            'geometric_prefix_additions':len(prefix),'core_free_formula_clauses':len(new_base),
            'combined_rup_additions':len(trace),'canonical_certificate_sha256':digest,
            'nonemptiness_essential_control':True},artifact


def disc_census(cells):
    # Cell-edge connectivity, one nonsingular boundary cycle, and Euler1.
    reached={min(cells)};stack=list(reached)
    while stack:
        x,y=stack.pop()
        for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if q in cells and q not in reached:
                reached.add(q);stack.append(q)
    require(reached==cells, 'positive prefix edge connectivity')
    edge_counts=Counter();vertices=set()
    for x,y in cells:
        corners=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
        vertices.update(corners)
        for a,b in zip(corners,corners[1:]+corners[:1]):
            edge_counts[tuple(sorted((a,b)))]+=1
    require(all(v in (1,2) for v in edge_counts.values()), 'cell-complex edge incidence')
    boundary=defaultdict(set)
    for (a,b),count in edge_counts.items():
        if count==1:
            boundary[a].add(b);boundary[b].add(a)
    require(boundary and all(len(row)==2 for row in boundary.values()), 'boundary is a one-manifold')
    reached={min(boundary)};stack=list(reached)
    while stack:
        for q in boundary[stack.pop()]:
            if q not in reached:
                reached.add(q);stack.append(q)
    require(len(reached)==len(boundary), 'single boundary cycle')
    euler=len(vertices)-len(edge_counts)+len(cells)
    require(euler==1, 'disc Euler characteristic')
    return {'cells':len(cells),'vertices':len(vertices),'edges':len(edge_counts),
            'boundary_edges':len(boundary),'boundary_cycles':1,'euler':euler}


def audit(packet):
    p,pool,core,ids,levels,geometric,core_units,packing,surrounds=geometry(packet['inputs'])
    frames,owners,pairs,self_collisions,gaps=periodic(packet['inputs'],ids)
    rows=[clause(row) for row in packet['clauses']]
    nv=packet['nv'];require(type(nv) is int and nv==397, 'stated formula dimensions')
    definitions={}
    gap_seen=Counter();pair_seen=Counter();truth_cases=0
    for gate in range(105,nv+1):
        inverse=[row for row in rows if gate in row and all(abs(a)<=104 for a in row-{gate})]
        require(len(inverse)==1, 'one inverse gate definition')
        tail=inverse[0]-{gate}
        if len(tail)==2 and all(a<0 for a in tail):
            atoms=tuple(sorted(-a for a in tail))
            require(atoms in pairs, 'actual quotient collision')
            kind='collision';pair_seen[atoms]+=1
        else:
            require(all(a>0 for a in tail), 'gap definition signs')
            atoms=tuple(sorted(tail))
            require(atoms in gaps, 'complete quotient gap owners')
            kind='gap';gap_seen[atoms]+=1
        definitions[gate]=(kind,atoms)
    require(pair_seen==Counter(pairs) and gap_seen==gaps, 'all quotient failures represented')
    final=frozenset(set(definitions)|self_collisions)
    require(final in rows, 'complete periodic failure clause')
    gate_rows=defaultdict(set);classified=Counter()
    for row in rows:
        if row==final:
            classified['failure']+=1
            continue
        aux=[abs(a) for a in row if abs(a)>104]
        if not aux:
            require(row in geometric|core_units, 'geometric input clause justification')
            classified['geometric']+=1
        else:
            require(len(aux)==1 and aux[0] in definitions, 'local gate row')
            gate_rows[aux[0]].add(row)
            classified['gate']+=1
    for gate,(kind,atoms) in definitions.items():
        local=gate_rows[gate]
        require(all(abs(a) in {*atoms,gate} for row in local for a in row), 'gate variable support')
        # Complete truth table independently proves the exact biconditional.
        for values in product((False,True),repeat=len(atoms)+1):
            valuation=dict(zip((*atoms,gate),values))
            satisfied=all(any(valuation[abs(a)]==(a>0) for a in row) for row in local)
            condition=all(valuation[a] for a in atoms) if kind=='collision' else not any(valuation[a] for a in atoms)
            require(satisfied==(valuation[gate]==condition), 'gate truth-table equivalence')
            truth_cases+=1
    epochs=rup(packet)
    prefixes=[];occupied=set();discs=[]
    for k,frs in enumerate(levels):
        before=set(occupied);added=set()
        for fr in frs:
            cells={image(q,fr) for q in p}
            require(not cells&(occupied|added), 'positive witness copy disjointness')
            if k:
                require(bool(halo(cells)&before), 'positive witness contact')
            added |= cells
        occupied |= added
        if k:
            require(halo(before)<=occupied, 'positive witness strict containment')
        prefixes.append(len(occupied))
        discs.append(disc_census(occupied))
    cover=Counter(address(image(q,fr)) for fr in frames for q in p)
    require(len(cover)==240 and all(a==1 for a in cover.values()), 'positive witness periodic cover')
    database=[masks(row) for row in sorted(geometric,key=lambda c:tuple(sorted(c)))]
    seeds=[]
    core_mask=sum(1<<(ids[q]-1) for q in core)
    full_mask=(1<<104)-1
    prototype_mask=sum(1<<(ids[q]-1) for q in p)
    for z,q in enumerate(pool,1):
        conflict,true,false,count=propagate(database,1<<(z-1))
        seeds.append({'cell':list(q),'conflict':conflict,'core_forced':true&core_mask==core_mask,
                      'prototype_forced':true==prototype_mask and false==(full_mask^prototype_mask),
                      'positive':str(true),'negative':str(false),'epochs':count})
    report={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'status':'EXACT_INDEPENDENT_TEMPLATE_AUDIT',
            'prototype_cells':60,'pool_cells':104,'core_cells':25,'copy_frames':19,
            'period_index':240,'variables':nv,'clauses':len(rows),'classified_clauses':dict(classified),
            'collision_gates':sum(pair_seen.values()),'gap_gates':sum(gap_seen.values()),
            'self_collision_variables':sorted(self_collisions),'gate_truth_table_cases':truth_cases,
            'rup_additions':len(epochs),'rup_epochs':epochs,
            'geometric_packing_clauses':len(packing),'geometric_surround_clauses':len(surrounds),
            'core_free_geometric_clauses':len(geometric),'baseline_prefix_cells':prefixes,
            'baseline_disc_census':discs,
            'seed_audit':seeds,'seed_conflicts':sum(s['conflict'] for s in seeds),
            'nonconflicting_seeds_force_core':sum(not s['conflict'] and s['core_forced'] for s in seeds),
            'nonconflicting_seeds_force_prototype':sum(not s['conflict'] and s['prototype_forced'] for s in seeds)}
    refinement,artifact=core_removal(geometric,core,ids,seeds,packet)
    report['core_removal']=refinement
    return report,artifact


def controls(packet, expected):
    rejected=[]
    mutations=[]
    q=deepcopy(packet);q['inputs']['core'].pop();mutations.append(('changed eroded core',q))
    q=deepcopy(packet);q['inputs']['frames'][0][0][1][0]+=1;mutations.append(('shifted root frame',q))
    q=deepcopy(packet);q['inputs']['period_generators'][1][1]+=1;mutations.append(('wrong period lattice',q))
    core_point=tuple(packet['inputs']['core'][0]);z=packet['inputs']['pool'].index(list(core_point))+1
    q=deepcopy(packet);q['clauses'].append([-z]);mutations.append(('unjustified negative core premise',q))
    q=deepcopy(packet)
    binary=next(row for row in q['clauses'] if -105 in row and len(row)==2)
    q['clauses'].remove(binary);mutations.append(('missing gate biconditional row',q))
    q=deepcopy(packet);q['rup'].pop();mutations.append(('missing final contradiction',q))
    q=deepcopy(packet);q['rup'][0].append(398);mutations.append(('out-of-domain proof literal',q))
    for name,bad in mutations:
        try:
            audit(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Malformed control accepted: '+name)
    for vector in ((6,-6),(2,38)):
        q=deepcopy(packet)
        shift=q['inputs']['periodic_frames'][0][1]
        shift[0]+=vector[0];shift[1]+=vector[1]
        changed,_=audit(q)
        require(changed==expected, 'period representative translation control')
    # A connected cell complex with a hole/pinch must not pass a disc audit.
    for name,bad in [('vertex pinch',{(0,0),(1,1)}),
                     ('unit-cell hole',set(product(range(3),range(3)))-{(1,1)})]:
        try:
            disc_census(bad)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Bad topology accepted: '+name)
    return {'malformed_controls_rejected':rejected,'period_translation_controls':2,
            'empty_prototype_control':'nonemptiness is necessary; checked separately in core-removal prefix'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate',type=Path)
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--strengthening',type=Path)
    parser.add_argument('--emit-strengthening',type=Path)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    raw=args.certificate.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN, 'immutable input certificate hash')
    result,artifact=audit(json.loads(raw))
    if args.strengthening:
        require(artifact==json.loads(args.strengthening.read_text()), 'strengthening proof artifact')
    if args.emit_strengthening:
        args.emit_strengthening.write_text(json.dumps(artifact,sort_keys=True,indent=2)+'\n')
    if args.controls:
        result['controls']=controls(json.loads(raw),result)
    if args.expected:
        require(result==json.loads(args.expected.read_text()), 'expected independent report')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
