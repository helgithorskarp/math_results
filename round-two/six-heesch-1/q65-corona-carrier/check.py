"""Solver-free construction and conditional all-motion corner reader."""
from copy import deepcopy
import hashlib,json
from itertools import product
from pathlib import Path
import lower
BASE=Path(__file__).resolve().parent
QUADS=((0,0),(-1,0),(-1,-1),(0,-1))
require=lower.require

def packing(shapes,poses):
    occupied=set()
    for pose in poses:
        require(len(pose)==3 and all(type(z) is int for z in pose),'invalid proof pose')
        o,x,y=pose;require(0<=o<len(shapes),'bad proof orientation')
        footprint={(a+x,b+y) for a,b in shapes[o]}
        require(not footprint&occupied,'proof hosts overlap');occupied|=footprint
    return occupied

def corner(cells,fixed,cert):
    shapes=lower.images(cells)
    original={(x+dx,y+dy) for x,y in fixed for dx,dy in product((0,1),repeat=2)}
    occupied=set(fixed)
    def choices(v,q):
        require(tuple(v) in original,'new forced-copy vertex is not an original-prefix obligation')
        require(type(q) is int and 0<=q<4,'invalid quadrant')
        x,y=v;qs=[(x+dx,y+dy) for dx,dy in QUADS]
        require(qs[q] not in occupied and qs[(q-1)%4] in occupied and qs[(q+1)%4] in occupied,'not an isolated empty 90-degree sector')
        px,py=qs[q];feasible=[]
        # Different from discovery's full-footprint trial: a translation is
        # forbidden iff occupied-minus-source contains that integer vector.
        for o,shape in enumerate(shapes):
            forbidden={(x-a,y-b) for x,y in occupied for a,b in shape}
            feasible.extend((o,px-a,py-b) for a,b in shape if (px-a,py-b) not in forbidden)
        return sorted(feasible)
    for step in cert['steps']:
        require(len(step)==6 and all(type(z) is int for z in step),'invalid corner step')
        x,y,q,o,tx,ty=step
        require(choices((x,y),q)==[(o,tx,ty)],'corner force is not the stated unique whole copy')
        occupied|={(a+tx,b+ty) for a,b in shapes[o]}
    terminal=cert['empty'];require(len(terminal)==3 and all(type(z) is int for z in terminal),'bad terminal sector')
    require(not choices(terminal[:2],terminal[2]),'terminal sector has an admissible whole supplier')
    return dict(forces=len(cert['steps']),supplier_trials_per_sector=len(shapes)*len(cells),empty=terminal)

def obstruction(fixture,ob):
    require(ob['parent_levels']==fixture['levels'][:-1],'conditional parent differs from construction')
    support=list(map(tuple,ob['support_poses']))
    require(support and support==sorted(set(support)),'invalid conditional support')
    require(set(support)<=set(map(tuple,fixture['levels'][-1])),'support copy absent from constructed fourth')
    parent=[tuple(q) for lev in ob['parent_levels'] for q in lev]
    shapes=lower.images(fixture['cells']);fixed=packing(shapes,parent+support)
    result=corner(fixture['cells'],fixed,ob['certificate'])
    return dict(fixed_three_corona_copies=len(parent),support_fourth_copies=len(support),
        original_prefix_hosts=len(parent)+len(support),**result)

def verify():
    data=json.loads((BASE/'input.json').read_text())
    fixture=json.loads((BASE/'four-coronas.json').read_text());ob=json.loads((BASE/'obstruction.json').read_text())
    require(data['cells']==fixture['cells'] and len(data['cells'])==65,'literal prototype binding differs')
    construction=lower.check(fixture);conditional=obstruction(fixture,ob)
    tests=[]
    def rejects(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError):tests.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    bad=deepcopy(fixture);bad['levels'][4][0][1]+=1
    rejects('moved whole fourth copy',lambda:lower.check(bad))
    bad=deepcopy(fixture);bad['levels'][1].pop()
    rejects('missing first copy',lambda:lower.check(bad))
    bad=deepcopy(fixture);bad['levels'][0][0][0]=(bad['levels'][0][0][0]+1)%8
    rejects('changed root orientation',lambda:lower.check(bad))
    bad_ob=deepcopy(ob);bad_ob['certificate']['steps'][0][4]+=1
    rejects('wrong forced placement',lambda:obstruction(fixture,bad_ob))
    bad_ob=deepcopy(ob);bad_ob['certificate']['empty'][2]=0
    rejects('occupied terminal quadrant',lambda:obstruction(fixture,bad_ob))
    bad_ob=deepcopy(ob);bad_ob['parent_levels']=bad_ob['parent_levels'][:-1]
    rejects('changed conditional parent',lambda:obstruction(fixture,bad_ob))
    shapes=lower.images(fixture['cells']);parent=[tuple(q) for lev in ob['parent_levels'] for q in lev]
    # The actual fourth is a positive control: its three-corona parent admits
    # a surround, so applying this no-next certificate to the parent alone
    # must fail. Optional support hypotheses cannot silently disappear.
    fixed_parent=packing(shapes,parent)
    rejects('dropped all seven support hosts',lambda:corner(fixture['cells'],fixed_parent,ob['certificate']))
    fixed=packing(shapes,parent+list(map(tuple,ob['support_poses'])))
    original={(x+dx,y+dy) for x,y in fixed for dx,dy in product((0,1),repeat=2)}
    first=ob['certificate']['steps'][0];o,tx,ty=first[3:]
    forced={(a+tx,b+ty) for a,b in shapes[o]}
    newvertices={(x+dx,y+dy) for x,y in forced for dx,dy in product((0,1),repeat=2)}-original
    require(newvertices,'license test has no new forced vertex')
    v=min(newvertices);bad_ob=deepcopy(ob);bad_ob['certificate']['steps'][0][:2]=list(v)
    rejects('new-copy same-stage corner obligation',lambda:obstruction(fixture,bad_ob))
    return dict(agent='six-heesch-1',role='researcher',construction=construction,
        conditional_obstruction=conditional,damaged_cases_rejected=tests,
        status='Four disc coronas and a monotone conditional no-fifth obstruction; no global finite upper or exact Heesch value.')

def main():
    result=verify();expected=json.loads((BASE/'expected.json').read_text())
    require(result==expected,'expected reader evidence differs')
    manifest=json.loads((BASE/'manifest.json').read_text())
    require(sorted(manifest)==sorted(p.name for p in BASE.iterdir() if p.is_file() and p.name!='manifest.json'),'manifest file coverage differs')
    for name,digest in manifest.items():require(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,'manifest mismatch: '+name)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
