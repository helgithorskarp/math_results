"""Independent affine-cell, Bezout-quotient and forward-RUP certificate reader.

No SAT solver or research generator is imported. A prototype is any selected
subset of the stated one-halo pool containing its stated eroded core. If its
19 fixed whole copies form two strict surrounds, four fixed periodic frames
exactly cover the plane. Disc/contact hypotheses only restrict this family.
"""
from collections import Counter
from pathlib import Path
import hashlib
import itertools
import json
import sys


def require(test, message):
    if not test:
        raise ValueError(message)


def integer_point(p):
    require(len(p)==2 and all(type(z) is int for z in p),'invalid integer point')
    return tuple(p)


def near(cells):
    return {(x+a,y+b) for x,y in cells for a,b in itertools.product([-1,0,1],repeat=2)}


def signed_frame(fr):
    matrix,shift=fr
    require(len(matrix)==2 and all(len(row)==2 for row in matrix),'invalid matrix dimensions')
    matrix=tuple(map(tuple,matrix));shift=integer_point(shift)
    require(all(type(z) is int and z in [-1,0,1] for row in matrix for z in row),'invalid signed matrix')
    require(all(sum(abs(z) for z in row)==1 for row in matrix) and
            all(sum(abs(matrix[i][j]) for i in range(2))==1 for j in range(2)),'matrix is not a signed permutation')
    return matrix,shift


def affine_cell(point,fr):
    # A signed unit-square image has lower-left offset equal to the sum
    # of negative coefficients. Discovery instead transformed four vertices.
    matrix,(tx,ty)=fr
    x,y=point
    return (matrix[0][0]*x+matrix[0][1]*y+sum(min(0,a) for a in matrix[0])+tx,
            matrix[1][0]*x+matrix[1][1]*y+sum(min(0,a) for a in matrix[1])+ty)


def bezout(a,b):
    if not b:
        return abs(a),(1 if a>0 else -1),0
    g,p,q=bezout(b,a%b)
    return g,q,p-(a//b)*q


def canonical(row):
    require(all(type(z) is int and z!=0 for z in row),'invalid literal')
    require(len(row)==len(set(row)) and not any(-z in row for z in row),'duplicate literal or tautological stored row')
    return tuple(sorted(row))


def disc_prefix(cells):
    def fill(seed,available):
        found={seed};stack=[seed]
        while stack:
            x,y=stack.pop()
            for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if q in available and q not in found:
                    found.add(q);stack.append(q)
        return found
    require(cells and fill(min(cells),cells)==cells,'baseline prefix is disconnected')
    xmin,xmax=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    ymin,ymax=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    background={(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)}-cells
    require(fill((xmin,ymin),background)==background,'baseline prefix has a hole')
    anchors={(x-a,y-b) for x,y in cells for a,b in itertools.product([0,1],repeat=2)}
    for x,y in anchors:
        bits=[(x,y) in cells,(x+1,y) in cells,(x,y+1) in cells,(x+1,y+1) in cells]
        require(bits not in [[True,False,False,True],[False,True,True,False]],'baseline prefix has a vertex pinch')


def check_rup(clauses,trace,nv):
    database=[tuple(c) for c in clauses]
    for row in trace:
        require(all(type(z) is int and 1<=abs(z)<=nv for z in row),'invalid RUP variable')
        assignment={};conflict=False
        for z in row:
            value=z<0
            if abs(z) in assignment and assignment[abs(z)]!=value:
                conflict=True
            assignment[abs(z)]=value
        changed=True
        while changed and not conflict:
            changed=False
            for c in database:
                if any(abs(z) in assignment and assignment[abs(z)]==(z>0) for z in c):
                    continue
                unassigned=[z for z in c if abs(z) not in assignment]
                if not unassigned:
                    conflict=True;break
                if len(unassigned)==1:
                    z=unassigned[0];assignment[abs(z)]=z>0;changed=True
        require(conflict,'RUP addition is not unit-propagation justified')
        database.append(tuple(row))
    require(trace and trace[-1]==[],'RUP does not conclude contradiction')


def verify(packet):
    data=packet['inputs']
    prototype=set(map(integer_point,data['prototype']))
    pool=list(map(integer_point,data['pool']))
    require(len(prototype)==60 and len(pool)==len(set(pool)) and pool==sorted(pool),'invalid baseline/pool')
    require(set(pool)==near(prototype),'pool is not exactly the baseline plus its one-cell halo')
    core=set(map(integer_point,data['core']))
    expected_core={p for p in prototype if near({p})<=prototype}
    require(core==expected_core,'mandatory core is not exactly the eroded baseline')
    ids={p:i+1 for i,p in enumerate(pool)};nb=len(pool)
    frames=[[signed_frame(fr) for fr in row] for row in data['frames']]
    require(list(map(len,frames))==[1,6,12],'wrong whole-copy template sizes')
    flat=list(itertools.chain.from_iterable(frames))
    require(len(set(flat))==19,'repeated physical copy frame')
    periodic=[signed_frame(fr) for fr in data['periodic_frames']]
    require(len(periodic)==4 and len(set(periodic))==4,'wrong periodic copy frames')
    v,w=map(integer_point,data['period_generators'])
    det=v[0]*w[1]-w[0]*v[1]
    require(det==240,'wrong positive period determinant')
    a,p,q=bezout(v[0],w[0]);require(a>0 and p*v[0]+q*w[0]==a and det%a==0,'Bezout failure')
    c=det//a;b=(p*v[1]+q*w[1])%c
    def residue(pt):
        x,y=pt
        return x%a,(y-(x//a)*b)%c
    board=set(itertools.product(range(a),range(c)))
    periodic_owners={key:[] for key in board}
    for fr in periodic:
        for pt,z in ids.items():
            periodic_owners[residue(affine_cell(pt,fr))].append(z)
    bad_pairs={tuple(sorted(pair)) for row in periodic_owners.values() for pair in itertools.combinations(row,2)}
    expected_pairs={pair for pair in bad_pairs if pair[0]!=pair[1]}
    self_collisions={aa for aa,bb in bad_pairs if aa==bb}
    expected_gaps=Counter(tuple(sorted(set(row))) for row in periodic_owners.values())
    # Non-vacuity control: the original60-cell template is a whole-copy
    # packing with strict root/first surrounds, and its four frames tile.
    occupied=set();prefixes=[]
    for k,row in enumerate(frames):
        added=set()
        for fr in row:
            cells={affine_cell(pt,fr) for pt in prototype}
            require(not cells&occupied and not cells&added,'baseline whole-copy overlap')
            if k:
                copy_vertices={(x+a,y+b) for x,y in cells for a,b in itertools.product([0,1],repeat=2)}
                old_vertices={(x+a,y+b) for x,y in occupied for a,b in itertools.product([0,1],repeat=2)}
                require(bool(copy_vertices&old_vertices),'baseline copy lacks previous-prefix contact')
            added.update(cells)
        if k:
            require(near(occupied)<=occupied|added,'baseline strict surround missing')
        occupied.update(added);prefixes.append(len(occupied));disc_prefix(occupied)
    baseline_keys=[residue(affine_cell(pt,fr)) for fr in periodic for pt in prototype]
    require(len(baseline_keys)==det and set(baseline_keys)==board,'baseline period is not an exact cover')
    clauses=[canonical(row) for row in packet['clauses']];nv=packet['nv']
    require(type(nv) is int and nv>=nb and all(1<=abs(z)<=nv for row in clauses for z in row),'invalid formula dimensions')
    definitions={};gate_clauses=set();pairs=[];gaps=[]
    for gate in range(nb+1,nv+1):
        inverse=[row for row in clauses if gate in row and all(abs(z)<=nb for z in row if z!=gate)]
        require(len(inverse)==1,'auxiliary gate lacks one defining inverse row')
        row=inverse[0];others=[z for z in row if z!=gate]
        if len(others)==2 and all(z<0 for z in others):
            aa,bb=sorted(-z for z in others)
            require(aa!=bb and (aa,bb) in expected_pairs,'collision gate lacks a true quotient collision')
            expected={canonical([gate,-aa,-bb]),canonical([-gate,aa]),canonical([-gate,bb])}
            pairs.append((aa,bb));definitions[gate]=('collision',(aa,bb))
        else:
            require(all(z>0 for z in others),'unknown auxiliary gate kind')
            xs=tuple(sorted(others));require(xs in expected_gaps,'gap gate lacks a complete quotient owner list')
            expected={canonical([gate,*xs]),*(canonical([-gate,-x]) for x in xs)}
            gaps.append(xs);definitions[gate]=('gap',xs)
        require(expected<=set(clauses),'auxiliary gate is not a biconditional')
        gate_clauses.update(expected)
    require(Counter(pairs)==Counter(expected_pairs) and Counter(gaps)==expected_gaps,'failure gates omit or duplicate a quotient obstruction')
    final=canonical(sorted(set(definitions)|self_collisions))
    require(final in clauses,'formula does not require a complete gap/overlap obstruction')
    physical_owners={};prefix_owners=[{} for k in range(3)]
    for k,row in enumerate(frames):
        for fr in row:
            for pt,z in ids.items():
                site=affine_cell(pt,fr)
                physical_owners.setdefault(site,[]).append(z)
                for lev in range(k,3):
                    prefix_owners[lev].setdefault(site,set()).add(z)
    geometric={canonical([ids[pt]]) for pt in core}
    for row in physical_owners.values():
        for aa,bb in itertools.combinations(row,2):
            geometric.add(canonical([-aa] if aa==bb else [-aa,-bb]))
    for k in range(2):
        for site,row in prefix_owners[k].items():
            for target in near({site}):
                owners=prefix_owners[k+1].get(target,set())
                for z in row:
                    if z not in owners:
                        geometric.add(canonical([-z,*sorted(owners)]))
    allowed=geometric|gate_clauses|{final}
    require(set(clauses)<=allowed,'an input clause is not justified by the geometric hypotheses or a failure gate')
    check_rup(clauses,packet['rup'],nv)
    return {'agent':'six-heesch-1','role':'researcher','pool_cells':nb,'core_cells':len(core),
            'whole_copy_frames':len(flat),'variables':nv,'clauses':len(clauses),'rup_additions':len(packet['rup']),
            'baseline_prefix_cells':prefixes,'baseline_disc_prefixes':[True,True,True],
            'period_generators':[v,w],'triangular_basis':[(a,b),(0,c)],
            'period_area':det,'conclusion':'every prototype in this pool retaining this core and realizing these two strict surrounds tiles the plane in the given four-copy period; its area is60',
            'limitation':'no claim outside this cell pool/core/copy template; no finite-five construction',
            'status':'author-checked geometric encoding and solver-free RUP; unformalized and independently unreviewed'}


if __name__=='__main__':
    path=Path(sys.argv[1]);result=verify(json.loads(path.read_text()))
    result['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(result,indent=2))
