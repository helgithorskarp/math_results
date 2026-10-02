"""Solver-free core-free P192 scaffold rigidity and exact calibration.

Root clauses use the byte-pinned prior normalized-cell reader, which differs
from discovery's physical-square/global-incidence compiler. Outer exclusions
use inverse cell-index maps, independently of footprint intersections.
"""
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

D=Path(__file__).resolve().parent
dep=json.loads((D/'dependencies.json').read_text())
def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for key in ('coupled_reader','coupled_input','coupled_dependencies','rup'):
    require(sha(D/dep[key]['path'])==dep[key]['sha256'],'dependency bytes differ: '+key)
require(sha(D/'input.json')==dep['literal_input_sha256'],'literal input bytes differ')
require(sha(D/'reduced-fixture.json')==dep['reduced_fixture_sha256'],'fixture bytes differ')
spec=importlib.util.spec_from_file_location('core_free_cells',D/dep['coupled_reader']['path'])
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)


def construct(data):
    f=c.Frames();f.I=frozenset()
    levels=[[(o,2*x,2*y) for o,x,y in poses] for poses in data['known_levels']]
    literal={ (2*x+i,2*y+j) for x,y in data['cells'] for i in (0,1) for j in (0,1) }
    require(f.S==literal,'literal parent cells differ')
    require(f.poses==levels[0]+levels[1],'first literal poses differ')
    require(tuple(map(len,levels))==(1,6,14,22),'reference layer counts differ')
    require((len(f.S),len(f.U),len(f.I))==(68,105,0),'domain or empty core differs')
    require(all(f.position(levels[0][0],q)==q for q in f.U),'root frame is not identity')
    motions=[(0,None,levels[0][0])]
    for group,(o,x,y) in enumerate(levels[1],1):
        for k,(dx,dy) in enumerate(c.NINE):motions.append((group,105+9*(group-1)+k+1,(o,x+dx,y+dy)))
    root,nv,unused,gates=c.builder(f,motions,True)
    changed=[-f.var[q] if q in f.S else f.var[q] for q in f.U]
    clauses={tuple(z) for z in root};clauses.remove(tuple(sorted(changed)))
    clauses.add(tuple(f.var.values()))
    before_outer=set(clauses)
    outer_conflicts=set()
    for i,j in combinations(range(14),2):
        p,r=levels[2][i],levels[2][j]
        o,tx,ty=r;(a,b,cc,d),(lx,ly)=f.frames[o]
        for q,v in f.var.items():
            x,y=f.position(p,q);x+=lx-tx;y+=ly-ty
            preimage=(a*x+cc*y,b*x+d*y)
            if preimage in f.var:outer_conflicts.add(tuple(sorted(set((-v,-f.var[preimage])))))
    clauses|=outer_conflicts
    base=[list(z) for z in sorted(clauses)]+[changed]
    digest=hashlib.sha256((f'p cnf {nv} {len(base)}\n'+''.join(' '.join(map(str,z))+' 0\n' for z in base)).encode()).hexdigest()
    return f,levels,motions,gates,base,nv,digest,before_outer,outer_conflicts,changed


def assign(f,motions,gates,raw,shifts):
    chosen={f.var[q] for q in raw}
    ys={105+9*j+c.NINE.index(tuple(s))+1 for j,s in enumerate(shifts)}
    chosen|=ys;chosen|={z for (y,v),z in gates.items() if y in ys and v in chosen}
    return chosen
def satisfies(base,chosen):return all(any(z in chosen if z>0 else -z not in chosen for z in clause) for clause in base)


def calibration(f,levels):
    occupied=set();count=0;stats=[]
    for k,poses in enumerate(levels):
        prior=set(occupied);h=c.halo(prior) if k else set()
        for p in poses:
            fp={f.position(p,q) for q in f.S}
            require(not fp&occupied,'reference copies overlap')
            if k:require(bool(fp&h),'reference new copy misses prior prefix')
            occupied|=fp;count+=1
        if k:require(h<=occupied,'reference collar incomplete')
        require(c.disc(occupied),'reference prefix is not a disc')
        stats.append(dict(level=k,copies=count,cells=len(occupied)))
    return stats


def main():
    data=json.loads((D/'input.json').read_text());cert=json.loads((D/'certificate.json').read_text())
    f,levels,motions,gates,base,nv,digest,reduced,conflicts,changed=construct(data)
    require((nv,len(gates),len(base),digest)==(cert['variables'],cert['and_gates'],cert['clauses'],cert['formula_sha256']),'reconstructed formula differs')
    require(cert['second_layer_indices']==list(range(14)) and cert['core_membership_units']==0 and cert['nonempty'] is True,'hypothesis manifest differs')
    parent=assign(f,motions,gates,f.S,[(0,0)]*6)
    require(satisfies(base[:-1],parent) and not satisfies(base,parent),'parent calibration or exclusion differs')
    stats=calibration(f,levels)
    fixture=json.loads((D/'reduced-fixture.json').read_text());raw=set(map(tuple,fixture['cells']))
    regression=assign(f,motions,gates,raw,fixture['shifts'])
    require(len(raw)==67 and satisfies(list(reduced)+[changed],regression),'published reduced-premise fixture differs')
    require(not satisfies(base,regression),'outer packing hypothesis does not exclude the fixture')
    # A missing nonempty clause admits the literal empty mask, showing that
    # connectedness or a hidden anchor is not being used to impose nonemptiness.
    empty=assign(f,motions,gates,set(),[(0,0)]*6)
    without_nonempty=[z for z in base if z!=list(f.var.values())]
    require(satisfies(without_nonempty,empty) and not satisfies(base,empty),'nonempty premise control failed')
    # Shape/frame data is mathematical input: one displaced outer copy changes
    # the formula and must not silently be treated as the same scaffold.
    damaged=json.loads(json.dumps(data));damaged['known_levels'][2][0][1]+=1
    require(construct(damaged)[6]!=digest,'displaced-frame control failed')
    for bad in ('0\n',f'{nv+1} 0\n'):
        try:c.rup.RupChecker(base,nv).verify(bad)
        except ValueError:pass
        else:raise ValueError('damaged RUP control was accepted')
    trace=(D/'rigidity.rup').read_text()
    require(sha(D/'rigidity.rup')==cert['rup_sha256'] and len(trace.encode())==cert['rup_bytes'],'certificate bytes differ')
    proof=c.rup.RupChecker(base,nv).verify(trace)
    require(proof['additions']==cert['rup_additions'] and cert['geometric_exclusions']==0 and cert['explicit_prototype_exceptions']==0,'proof manifest differs')
    out=dict(agent='six-heesch-1',role='researcher',result='Every nonempty mask in U105 satisfying the first-frame root surround and internal14-copy packing equals S68.',
             membership_variables=105,placement_selectors=54,and_gates=len(gates),variables=nv,clauses=len(base),
             formula_sha256=digest,rup_additions=proof['additions'],rup_bytes=len(trace.encode()),
             core_membership_units=0,geometric_exclusions=0,prototype_exceptions=0,
             baseline=stats,regression_fixture_area=67,controls=5,finite_five_solved=False)
    expected=D/'expected.json'
    if expected.exists():require(json.loads(expected.read_text())==out,'expected evidence differs')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
