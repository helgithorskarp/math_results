"""Solver-free, inverse-map reader for a uniform corona-extension obstruction.

Discovery used world-cell incidence and a native SAT solver. This reader
reconstructs whole-copy conflicts by inverse affine cell maps and checks RUP.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path

D=Path(__file__).resolve().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
dep=json.loads((D/'dependencies.json').read_text())
for key in ('coupled_reader','coupled_input','coupled_dependencies','r67_fixture','rup'):
    require(sha(D/dep[key]['path'])==dep[key]['sha256'],'dependency bytes differ: '+key)
for filename in ('input.json','calibration.json'):
    require(sha(D/filename)==dep[filename+'_sha256'],'literal input bytes differ: '+filename)
spec=importlib.util.spec_from_file_location('extension_frames',D/dep['coupled_reader']['path'])
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
QUADS=((0,0),(-1,0),(-1,-1),(0,-1))

def add(clauses,literals):
    literals=set(literals)
    if not any(-z in literals for z in literals):clauses.add(tuple(sorted(literals)))

def digest(clauses,nv):
    return hashlib.sha256((f'p cnf {nv} {len(clauses)}\n'+
                          ''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()).hexdigest()

def inverse(f,pose,point):
    o,tx,ty=pose;(a,b,cc,d),(lx,ly)=f.frames[o]
    xx,yy=point[0]+lx-tx,point[1]+ly-ty
    return a*xx+cc*yy,b*xx+d*yy

def sector(f,descriptor,anchors):
    pair=list(map(tuple,descriptor['pair']));anchors=list(map(tuple,anchors))
    require(len(pair)==2 and pair[0]==f.poses[0] and pair[0]!=pair[1],'invalid fixed pair')
    require(len(anchors)==len(set(anchors)) and all(p in anchors for p in pair),'invalid fixed anchors')
    for p in anchors:
        require(len(p)==3 and all(type(z) is int for z in p) and 0<=p[0]<8,'invalid fixed pose')
    vertex=descriptor['vertex'];q=descriptor['quadrant']
    require(len(vertex)==2 and all(type(z) is int for z in vertex) and type(q) is int and 0<=q<4,'invalid corner location')
    qs=[(vertex[0]+dx,vertex[1]+dy) for dx,dy in QUADS];target=qs[q]
    adjacent=descriptor['adjacent_sources'];require(len(adjacent)==2,'two quadrant witnesses required')
    witnesses=[]
    for row,k in zip(adjacent,((q-1)%4,(q+1)%4)):
        i,source=row[0],tuple(row[1])
        require(type(i) is int and 0<=i<2 and source in f.var,'invalid quadrant witness')
        require(inverse(f,pair[i],qs[k])==source,'quadrant witness maps to wrong cell')
        witnesses.append(f.var[source])
    require(len(descriptor['edge_contact'])==2,'two contact witnesses required')
    a,b=map(tuple,descriptor['edge_contact']);require(a in f.var and b in f.var,'contact source outside U')
    ap,bp=f.position(pair[0],a),f.position(pair[1],b)
    require(abs(ap[0]-bp[0])+abs(ap[1]-bp[1])==1,'contact witnesses do not share an edge')
    witnesses.extend((f.var[a],f.var[b]))
    gap=sorted({f.var[pre] for p in anchors for pre in [inverse(f,p,target)] if pre in f.var})
    clauses=set();options=[];nv=105
    for o,((a,b,cc,d),(lx,ly)) in enumerate(f.frames):
        for u in f.U:
            nv+=1;x,y=u
            pose=(o,target[0]-a*x-b*y+lx,target[1]-cc*x-d*y+ly)
            options.append((nv,u,pose));add(clauses,[-nv,f.var[u]])
            for source,var in f.var.items():
                point=f.position(pose,source)
                for anchor in anchors:
                    pre=inverse(f,anchor,point)
                    if pre in f.var:add(clauses,[-nv,-var,-f.var[pre]])
    add(clauses,[-z for z in witnesses]+gap+[z for z,u,p in options])
    base=[list(row) for row in sorted(clauses)]
    return base,options,dict(variables=nv,clauses=len(base),supplier_options=len(options),
                             witness_variables=witnesses,gap_source_variables=gap,
                             target=list(target),formula_sha256=digest(base,nv))

def construct(data):
    require(data['nonempty'] is True and data['core_membership_units']==0,'wrong nonempty/core-free scope')
    f=c.Frames();f.I=frozenset()
    require((len(f.S),len(f.U),len(f.poses))==(68,105,7),'wrong literal domain')
    poses=f.pose_list(data['first_shifts'])
    require([list(p) for p in poses]==data['first_poses'],'first shifts and physical poses disagree')
    require(all(f.position(poses[0],u)==u for u in f.U),'root frame is not identity')
    first,nv,first_sha,gates=c.builder(f,[(i,None,p) for i,p in enumerate(poses)],False)
    require(nv==105 and not gates,'unexpected first-prefix auxiliary variables')
    conditional,options,meta=sector(f,data['descriptor'],poses)
    clauses={tuple(row) for row in first+conditional};clauses.add(tuple(f.var.values()))
    base=[list(row) for row in sorted(clauses)]
    return f,poses,first,conditional,options,base,dict(variables=meta['variables'],clauses=len(base),
                 first_clauses=len(first),first_formula_sha256=first_sha,
                 conditional=meta,formula_sha256=digest(base,meta['variables']))

def satisfies(base,chosen):
    return all(any(z in chosen if z>0 else -z not in chosen for z in row) for row in base)

def proof(data,certificate,trace,rebuilt=None):
    if rebuilt is None:rebuilt=construct(data)
    f,poses,first,conditional,options,base,meta=rebuilt
    require(meta==certificate['formula'],'independent family formula differs')
    require(certificate['geometric_exclusions']==0 and certificate['prototype_exceptions']==0,'unjustified exceptions')
    require(bool(trace.strip()),'missing proof trace')
    require(hashlib.sha256(trace.encode()).hexdigest()==certificate['rup_sha256'] and
            len(trace.encode())==certificate['rup_bytes'],'proof bytes differ')
    checked=c.rup.RupChecker(base,meta['variables']).verify(trace)
    require(checked==certificate['rup_check'],'proof manifest differs')
    return checked

def calibrated(f,poses,first,conditional,base,fixture):
    stats=c.verify_lower(fixture['s68_lower'])
    r67=json.loads((D/dep['r67_fixture']['path']).read_text());r67_stats=c.verify_lower(r67)
    raw=set(map(tuple,r67['cells']));chosen={f.var[u] for u in raw}
    reference={frozenset(f.position(p,u) for u in raw) for p in poses}
    shapes=c.images(raw)
    literal={frozenset((a+x,b+y) for a,b in shapes[o]) for level in r67['levels'] for o,x,y in level}
    require(reference==literal and satisfies(first,chosen),'R67 first-corona calibration differs')
    require(not satisfies(base,chosen),'R67 unexpectedly satisfies the supplier demand without a supplier')
    fixed=set().union(*reference)
    corner=c.verify_corner(raw,fixed,dict(steps=[],empty=[3,15,0]))
    result=dict(r67_first=r67_stats,r67_corner=corner,s68_second=stats)
    for key in ('s68_supplier','s68_existing_owner'):
        row=fixture[key];clauses,options,meta=sector(f,row['descriptor'],row['anchors'])
        require(meta==row['formula'],'calibration sector formula differs')
        selected={f.var[u] for u in f.S};occupied=set()
        for p in map(tuple,row['anchors']):
            fp={f.position(p,u) for u in f.S}
            require(not fp&occupied,'calibration fixed copies overlap');occupied|=fp
        active=all(z in selected for z in meta['witness_variables']) and not any(z in selected for z in meta['gap_source_variables'])
        require(active==row['active'],'calibration activation differs')
        if active:
            choice=next((r for r in options if list(r[2])==row['supplier']),None)
            require(choice is not None and choice[1] in f.S,'calibration supplier absent')
            z,u,p=choice;whole={f.position(p,u) for u in f.S}
            require(tuple(meta['target']) in whole and not whole&occupied,'calibration whole supplier invalid')
            selected.add(z)
        else:
            owners=[list(p) for p in map(tuple,row['anchors']) if inverse(f,p,meta['target']) in f.S]
            require(any(p not in row['descriptor']['pair'] for p in owners),'existing gap owner is not outside the fixed pair')
        require(satisfies(clauses,selected),'calibration assignment violates the conditional formula')
        result[key]=dict(active=active,checked=True)
        if active:
            disabled={f.var[u] for u in f.S if list(u)!=row['descriptor']['edge_contact'][0]}
            require(not all(z in disabled for z in meta['witness_variables']) and satisfies(clauses,disabled),
                    'disabled contact antecedent still requires a supplier')
            result['disabled_contact_control']=True
    empty=set();without_nonempty=[row for row in base if row!=list(f.var.values())]
    require(satisfies(without_nonempty,empty) and not satisfies(base,empty),'empty-mask control failed')
    result['empty_mask_control']=True
    return result

def main():
    data=json.loads((D/'input.json').read_text());cert=json.loads((D/'certificate.json').read_text())
    trace=(D/'obstruction.rup').read_text();rebuilt=construct(data);checked=proof(data,cert,trace,rebuilt)
    f,poses,first,conditional,options,base,meta=rebuilt
    calibration=calibrated(f,poses,first,conditional,base,json.loads((D/'calibration.json').read_text()))
    tests=[]
    bad=deepcopy(data);bad['nonempty']=False
    tests.append(('wrong scope',lambda:construct(bad),'wrong nonempty/core-free scope'))
    wrong=deepcopy(data);wrong['first_shifts'][0]=[0,0]
    tests.append(('displaced first copy',lambda:construct(wrong),'first shifts and physical poses disagree'))
    adjacent=deepcopy(data);adjacent['descriptor']['adjacent_sources'][0][1]=list(f.U[-1])
    tests.append(('wrong quadrant witness',lambda:construct(adjacent),'quadrant witness maps to wrong cell'))
    missing=deepcopy(cert);missing['formula']['conditional']['supplier_options']-=1
    tests.append(('missing supplier in manifest',lambda:proof(data,missing,trace,rebuilt),'independent family formula differs'))
    exception=deepcopy(cert);exception['prototype_exceptions']=1
    tests.append(('unjustified exception',lambda:proof(data,exception,trace,rebuilt),'unjustified exceptions'))
    tests.append(('missing proof',lambda:proof(data,cert,'',rebuilt),'missing proof trace'))
    tests.append(('out-of-domain proof literal',lambda:c.rup.RupChecker(base,meta['variables']).verify(str(meta['variables']+1)+' 0\n'),
                  'out-of-domain literal at line 1'))
    tests.append(('unsupported empty-clause shortcut',lambda:c.rup.RupChecker(base,meta['variables']).verify('0\n'),'non-RUP step at line 1'))
    truncated='\n'.join(trace.splitlines()[:-1])+'\n'
    tests.append(('missing terminal empty clause',lambda:c.rup.RupChecker(base,meta['variables']).verify(truncated),
                  'proof must end with an added empty clause'))
    controls=[]
    for name,check,expected in tests:
        try:check()
        except ValueError as exc:
            require(str(exc)==expected,'wrong rejection reason for '+name+': '+str(exc))
            controls.append(dict(control=name,rejected=True,reason=str(exc)))
        else:raise ValueError('damaged certificate accepted: '+name)
    out=dict(agent='six-heesch-1',role='researcher',result='No nonempty Q in U105 has a second complete-corona extension of the specified R67 first-copy tuple.',
             variables=meta['variables'],clauses=meta['clauses'],formula_sha256=meta['formula_sha256'],
             prototype_variables=105,supplier_options=len(options),core_membership_units=0,
             geometric_exclusions=0,prototype_exceptions=0,rup_check=checked,rup_bytes=len(trace.encode()),
             rup_sha256=cert['rup_sha256'],calibration=calibration,controls=controls,finite_five_solved=False)
    path=D/'expected.json'
    if path.exists():require(json.loads(path.read_text())==out,'expected evidence differs')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
