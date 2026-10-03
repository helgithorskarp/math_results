"""Independent first-stage geometry, topology cuts, mask guards and RUP.

This reader imports no mask producer or solver. Rigid-motion completeness
of original isolated90-degree sectors is an explicit ordinary proof bridge.
"""
from collections import Counter,defaultdict
import argparse,hashlib,importlib.util,json
from copy import deepcopy
from itertools import combinations,product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out

g=module('first_mask_parametric_independent',ROOT/'guard.py')
rup=module('first_mask_rup_independent',PACKAGE/'rup.py')
require=g.require
FOUR=((1,0),(0,1),(-1,0),(0,-1))

def digest(clauses,nv):
    return hashlib.sha256((f'p cnf {nv} {len(clauses)}\n'+
        ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()).hexdigest()

def recover(cells,levels):
    normalized={}
    for m in g.MATRICES:
        image=[g.physical_cell(p,m) for p in cells]
        minimum=min(x for x,y in image),min(y for x,y in image)
        shape=tuple(sorted((x-minimum[0],y-minimum[1]) for x,y in image))
        require(shape not in normalized,'template D4 symmetry was not represented explicitly')
        normalized[shape]=(m,minimum)
    order=sorted(normalized);frames=[]
    for level,poses in enumerate(levels):
        for o,x,y in poses:
            m,b=normalized[order[o]];frames.append((level,m,(x-b[0],y-b[1])))
    require(len(frames)==7 and frames[0]==(0,(1,0,0,1),(0,0)), 'wrong literal first scaffold')
    return frames

def compiler(template,tile):
    cells=list(map(tuple,template['cells']))
    universe=sorted({(x+i,y+j) for x,y in cells for i,j in product((-1,0,1),repeat=2)})
    require(len(universe)==123, 'wrong Moore envelope')
    frames=recover(cells,template['levels'][:2]);ids={p:i for i,p in enumerate(universe,1)}
    bodies=[];owners=[]
    for level,m,t in frames:
        body={}
        for p,v in ids.items():
            a,b=g.physical_cell(p,m);point=a+t[0],b+t[1]
            require(point not in body,'noninjective square map');body[point]=v
        bodies.append(body)
    for k in range(2):
        own=defaultdict(set)
        for body,(level,m,t) in zip(bodies,frames):
            if level<=k:
                for point,v in body.items():own[point].add(v)
        owners.append(own)
    clauses=set()
    def add(row):
        row=tuple(sorted(set(row)))
        if not any(-v in row for v in row):clauses.add(row)
    for i,j in combinations(range(len(bodies)),2):
        for point in bodies[i].keys()&bodies[j].keys():add([-bodies[i][point],-bodies[j][point]])
    for (x,y),v in bodies[0].items():
        for dx,dy in product((-1,0,1),repeat=2):add([-v,*owners[1].get((x+dx,y+dy),())])
    for own in owners:
        vertices={(x+i,y+j) for x,y in own for i,j in product((0,1),repeat=2)}
        for x,y in vertices:
            qs=[own.get(p,set()) for p in ((x,y),(x-1,y),(x-1,y-1),(x,y-1))]
            for i,j in ((0,2),(1,3)):
                repair=set().union(*(qs[q] for q in range(4) if q not in (i,j)))
                for v in qs[i]:
                    for w in qs[j]:add([-v,-w,*repair])
    physical=set(clauses)
    require(tile['periods']==[[22,6],[-6,22]] and len(tile['representatives'])==8,'wrong period pattern')
    representatives=[(x,y) for y in range(2) for x in range(260)]
    require(len({((22*x+6*y)%520,(-6*x+22*y)%520) for x,y in representatives})==520, 'quotient representatives collide')
    rows=[Counter() for _ in representatives]
    for rep in tile['representatives']:
        m,t=g.frame([rep['matrix'],rep['translation']])
        for p,v in ids.items():
            a,b=g.physical_cell(p,m);a+=t[0];b+=t[1]
            matches=[]
            for i,(x,y) in enumerate(representatives):
                dx,dy=a-x,b-y
                if (22*dx+6*dy)%520==0 and (-6*dx+22*dy)%520==0:matches.append(i)
            require(len(matches)==1,'lattice quotient is not bijective');rows[matches[0]][v]+=1
    for i,row in enumerate(rows):
        z=124+i
        for v,n in row.items():
            if n==1:add([-z,-v,*[w for w in row if w!=v]])
    add(range(124,644));add(range(1,124))
    base=[list(c) for c in sorted(clauses)]
    return universe,frames,owners,base,rows,physical

def check_topology(row,owners):
    level=row['level'];require(type(level) is int and level in (0,1),'bad prefix level')
    own=owners[level];sequence=list(map(tuple,row['region']));region=set(sequence)
    require(sequence==sorted(region) and region and all(len(p)==2 and all(type(z) is int for z in p) for p in region),'invalid separator region')
    boundary={(x+dx,y+dy) for x,y in region for dx,dy in FOUR}-region
    if row['kind']=='connected_separator':
        inside,outside=tuple(row['inside']),tuple(row['outside'])
        v,w=row['inside_variable'],row['outside_variable']
        require(inside in region and outside not in region,'separator endpoints were not separated')
        require(v in own.get(inside,()) and w in own.get(outside,()),'endpoint supplier differs')
        clause=sorted(set([-v,-w,*[z for point in boundary for z in own.get(point,())]]))
    else:
        require(row['kind']=='outside_separator','unknown topology clause kind')
        point=tuple(row['empty_point']);require(point in region,'hole point lies outside region')
        pairs=row['boundary_providers'];given=[tuple(p) for p,v in pairs]
        require(given==sorted(boundary),'hole boundary inventory differs')
        for p,v in pairs:require(v in own.get(tuple(p),()),'hole boundary supplier differs')
        clause=sorted(set([*own.get(point,()),*[-v for p,v in pairs]]))
    require(clause==row['clause'] and not any(-z in clause for z in clause),'separator formula differs')
    return clause

def check(data,template,tile,trace):
    universe,frames,owners,base,rows,physical=compiler(template,tile)
    require(len(base)==3407 and digest(base,643)==data['base_formula_sha256'], 'independent first-stage basis differs')
    topology_clauses=[check_topology(row,owners) for row in data['topology_cuts']]
    guards=data['parametric_cuts'];guard_checks=[];guard_clauses=[]
    expected_frames=[(m,t) for level,m,t in frames]
    for packet in guards:
        require(list(map(tuple,packet['universe']))==universe and
                set(map(tuple,packet['original_plane_source']))==set(map(tuple,template['cells'])) and
                [g.frame(row) for row in packet['initial_frames']]==expected_frames, 'guard is for a different scaffold')
        guard_checks.append(g.check(packet));guard_clauses.append(packet['cut_clause'])
    augmented=base+topology_clauses+guard_clauses
    require(data['source_sites']==123 and data['variables']==643, 'wrong variable domain')
    require(len({tuple(c) for c in augmented})==len(augmented)==data['all_clauses'], 'combined clause inventory differs')
    formula_hash=digest(augmented,643)
    require(formula_hash==data['formula_sha256'], 'whole formula hash differs')
    proof_hash=hashlib.sha256(trace.encode()).hexdigest()
    require(proof_hash==data['proof_sha256'], 'proof bytes differ')
    replay=rup.RupChecker(augmented,643).verify(trace)
    original={i for i,p in enumerate(universe,1) if p in set(map(tuple,template['cells']))}
    def satisfies(c,selected):return any(z in selected if z>0 else -z not in selected for z in c)
    require(all(satisfies(c,original) for c in physical | set(map(tuple,topology_clauses+guard_clauses))), 'original geometry control fails')
    require(all(sum(n for v,n in row.items() if v in original)==1 for row in rows), 'original period control fails')
    lower_control=g.lower.check(template)
    # Each literal first remains admissible without both no-next clauses.
    first_controls=[]
    zbase=124
    for packet in guards:
        raw=set(map(tuple,packet['literal_raw_source']))
        selected={i for i,p in enumerate(universe,1) if p in raw}
        bad_rows=[i for i,row in enumerate(rows) if sum(n for v,n in row.items() if v in selected)!=1]
        require(bad_rows,'first-only fixture does not fail this period')
        assignment=selected|{zbase+bad_rows[0]}
        require(all(satisfies(c,assignment) for c in base+topology_clauses), 'first-only control violates necessary first clauses')
        first_controls.append({'area':len(raw),'bad_period_rows':len(bad_rows),'first_only_assignment_checked':True})
    return {'agent':'six-heesch-1','role':'researcher','lemma':'Fixed first corona plus arbitrary second surround forces the specified plane tiling',
        'status':'Author-checked exact computer-assisted lemma; independently unreviewed and unformalized',
        'source_sites':123,'fixed_first_maps':7,'variables':643,'base_clauses':len(base),
        'topology_clauses':len(topology_clauses),'parametric_cuts':len(guards),'all_clauses':len(augmented),
        'base_formula_sha256':digest(base,643),'formula_sha256':formula_hash,'proof_sha256':proof_hash,
        'rup':replay,'proof_bytes':len(trace.encode()),'guard_sizes':[r['guard_atoms'] for r in guard_checks],
        'guard_free_bits':[r['syntactically_free_bits'] for r in guard_checks],
        'all_alternative_suppliers_checked':[r['all_alternative_suppliers_checked'] for r in guard_checks],
        'original_first':lower_control,'first_only_controls':first_controls,
        'periods':[[22,6],[-6,22]],'lattice_index':520,'period_copies':8,'consequent_area':65,
        'scope':'Simple S in the stated123-site envelope, prescribed packed disc first prefix/root surround, and a complete arbitrary-motion second surround; second prefix may have holes. No statement for other first motions or a global finite Heesch record.'}

def damages(data,template,tile,trace):
    cases=[]
    def reject(label,bad,first=template,period=tile,proof=trace):
        try:check(bad,first,period,proof)
        except ValueError as e:cases.append({'case':label,'rejected':True,'reason':str(e)})
        else:raise ValueError('damaged input accepted: '+label)
    bad=deepcopy(template);bad['levels'][1][0][1]+=1
    reject('changed first physical motion',data,first=bad)
    bad=deepcopy(data);bad['topology_cuts'][0]['region'].pop()
    reject('missing separator-region cell',bad)
    index=next(i for i,row in enumerate(data['topology_cuts']) if row['kind']=='connected_separator')
    bad=deepcopy(data);bad['topology_cuts'][index]['inside_variable']=124
    reject('false connected-separator endpoint supplier',bad)
    for k,packet in enumerate(data['parametric_cuts']):
        for row in g.controls(packet):cases.append({'case':f'guard{k+1}: '+row['case'],'rejected':True,'reason':row['reason']})
    shortened='\n'.join(trace.splitlines()[:-1])+'\n'
    bad=deepcopy(data);bad['proof_sha256']=hashlib.sha256(shortened.encode()).hexdigest()
    reject('removed final empty clause with updated hash',bad,proof=shortened)
    bad=deepcopy(data);bad['parametric_cuts']=[]
    base=compiler(template,tile)[3]
    owners=compiler(template,tile)[2]
    partial=base+[check_topology(row,owners) for row in bad['topology_cuts']]
    bad['all_clauses']=len(partial);bad['formula_sha256']=digest(partial,643)
    reject('removed both no-next clauses with updated formula',bad)
    return cases

def record():
    data=json.loads((ROOT/'certificate.json').read_text())
    template=json.loads((ROOT/'input.json').read_text());tile=json.loads((ROOT/'tiling.json').read_text())
    trace=(ROOT/'proof.rup').read_text()
    out=check(data,template,tile,trace);out['damaged_cases']=damages(data,template,tile,trace)
    return out

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for name,sha in manifest.items():
        require(Path(name).name==name and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha, 'file manifest differs: '+name)
    out=record()
    require(out==json.loads((ROOT/'expected.json').read_text()),'full expected result differs')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
