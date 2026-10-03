"""Solver-free physical-vertex verification of a common-source guard.

No sampled masks or producer collision witnesses are trusted. All possible
D4 suppliers in the entire source envelope are tested at every licensed gap.
"""
import argparse
from copy import deepcopy
import hashlib,importlib.util,json
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('parametric_boundary_reader',
    ROOT/'lower.py')
lower=importlib.util.module_from_spec(spec);spec.loader.exec_module(lower)
require=lower.require
Q=((0,0),(-1,0),(-1,-1),(0,-1))
MATRICES=tuple((0,sx,sy,0) if swap else (sx,0,0,sy)
               for swap in (False,True) for sx,sy in product((-1,1),repeat=2))

def physical_cell(point,m):
    x,y=point;a,b,c,d=m
    points=[(a*(x+i)+b*(y+j),c*(x+i)+d*(y+j)) for i,j in product((0,1),repeat=2)]
    return min(z[0] for z in points),min(z[1] for z in points)

def frame(raw):
    require(len(raw)==2, 'bad affine map')
    m,t=tuple(raw[0]),tuple(raw[1])
    require(m in MATRICES and len(t)==2 and all(type(z) is int for z in t), 'non-D4 affine map')
    return m,t

def check(data):
    universe=list(map(tuple,data['universe']));old=set(map(tuple,data['original_plane_source']))
    expected=sorted({(x+i,y+j) for x,y in old for i,j in product((-1,0,1),repeat=2)})
    require(universe==expected and len(universe)==123, 'incomplete source envelope')
    guard=set(data['guard_literals'])
    require(len(guard)==len(data['guard_literals']) and all(type(v) is int and 1<=abs(v)<=123 for v in guard), 'bad source guard')
    require(not any(-v in guard for v in guard), 'inconsistent source guard')
    require(data['cut_clause']==sorted(-v for v in guard), 'cut is not the negation of its source guard')
    positive={v for v in guard if v>0};negative={-v for v in guard if v<0}
    ids={p:i for i,p in enumerate(universe,1)}
    literal=set(map(tuple,data['literal_raw_source']));selected={ids[p] for p in literal}
    require(positive<=selected and not negative&selected, 'literal fixture violates the guard')
    old_selected={ids[p] for p in old}
    require(not (positive<=old_selected and not negative&old_selected), 'original plane control was excluded')
    first=data['literal_first_fixture'];lower_checked=lower.check(first)
    shift=tuple(data['normalization_shift'])
    require(literal=={(x+shift[0],y+shift[1]) for x,y in first['cells']}, 'raw/normalized source mismatch')
    initial=[frame(row) for row in data['initial_frames']]
    require(len(initial)==7 and initial[0]==((1,0,0,1),(0,0)), 'wrong prescribed first maps')
    old_poses=[pose for lev in first['levels'] for pose in lev]
    require(len(old_poses)==len(initial), 'positive first map count differs')
    shapes=lower.images(first['cells'])
    def pixels(cells,f):
        m,t=f
        return {(physical_cell(p,m)[0]+t[0],physical_cell(p,m)[1]+t[1]) for p in cells}
    for f,(o,x,y) in zip(initial,old_poses):
        normalized={(a+x+shift[0],b+y+shift[1]) for a,b in shapes[o]}
        require(pixels(literal,f)==normalized, 'physical first footprint binding differs')
    all_images={m:{physical_cell(p,m):i for p,i in ids.items()} for m in MATRICES}
    positive_images={m:set(q for q,v in table.items() if v in positive) for m,table in all_images.items()}
    def body(f):
        m,t=f
        return {(a+t[0],b+t[1]) for a,b in positive_images[m]}
    initial_cells=set().union(*(body(f) for f in initial))
    current=list(initial);records=data['certificate'];tested=0;forced=0
    require(records and records[-1]['forced_frame'] is None and
            all(r['forced_frame'] is not None for r in records[:-1]), 'missing unique terminal contradiction')
    for row in records:
        v=tuple(row['vertex']);q=row['quadrant']
        require(len(v)==2 and all(type(z) is int for z in v) and type(q) is int and 0<=q<4, 'bad sector')
        qs=[(v[0]+a,v[1]+b) for a,b in Q]
        require(any(z in initial_cells for z in qs), 'unlicensed future-copy vertex obligation')
        occupied=set().union(*(body(f) for f in current))
        for m,t in current:
            source_var=all_images[m].get((qs[q][0]-t[0],qs[q][1]-t[1]))
            require(source_var is None or source_var in negative, 'source guard does not keep the gap empty')
        require(qs[(q-1)%4] in occupied and qs[(q+1)%4] in occupied, 'source guard does not bound the90-degree gap')
        f=frame(row['forced_frame']) if row['forced_frame'] is not None else None
        if f:require(qs[q] in body(f), 'forced supplier anchor is not selected by the guard')
        alternatives=0
        for m,table in all_images.items():
            for (a,b),source_var in table.items():
                candidate=(m,(qs[q][0]-a,qs[q][1]-b))
                if candidate==f:continue
                alternatives+=1;tested+=1
                if source_var in negative:continue
                require(bool(body(candidate)&occupied), 'possible alternative supplier survives the guard')
        require(alternatives==row['alternative_suppliers'], 'candidate completeness count differs')
        if f:current.append(f);forced+=1
    return {'agent':'six-heesch-1','role':'researcher','parametric_fixed_first_cut_checked':True,
            'source_sites':len(universe),'guard_atoms':len(guard),'selected_atoms':len(positive),
            'absent_atoms':len(negative),'syntactically_free_bits':len(universe)-len(guard),
            'fixed_first_maps':len(initial),'forced_maps':forced,'all_alternative_suppliers_checked':tested,
            'clause':data['cut_clause'],'literal_first':lower_checked,
            'original_plane_guard_control':True,
            'scope':'Every simple source mask in U satisfying the guard has no additional surround of the prescribed7-copy first prefix, under arbitrary motions and allowing final holes. This is not a global Heesch bound for other source masks/first arrangements. Syntactic free bits count no admissible shapes.'}

def controls(data):
    rows=[]
    def reject(label,bad):
        try:check(bad)
        except ValueError as e:rows.append({'case':label,'rejected':True,'reason':str(e)})
        else:raise ValueError('Damaged parametric guard accepted: '+label)
    bad=deepcopy(data);bad['universe'].pop();reject('missing potential source site',bad)
    bad=deepcopy(data);bad['certificate'].pop();reject('missing terminal contradiction',bad)
    bad=deepcopy(data);bad['certificate'][0]['vertex'][0]=1000;reject('unlicensed new-copy vertex',bad)
    bad=deepcopy(data);bad['certificate'][0]['forced_frame'][1][0]+=1;reject('changed forced physical map',bad)
    bad=deepcopy(data);bad['cut_clause'][0]*=-1;reject('changed source-cut direction',bad)
    # Omit the actual selected source anchor of the first forced copy.
    universe=list(map(tuple,data['universe']));row=data['certificate'][0];m,t=frame(row['forced_frame'])
    x,y=row['vertex'];a,b=Q[row['quadrant']];point=x+a-t[0],y+b-t[1]
    anchor=next(i for i,p in enumerate(universe,1) if physical_cell(p,m)==point)
    bad=deepcopy(data);bad['guard_literals'].remove(anchor);bad['cut_clause']=sorted(-v for v in bad['guard_literals'])
    reject('missing forced source-anchor atom',bad)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);args=ap.parse_args()
    data=json.loads(args.input.read_text());out=check(data);out['damaged_cases']=controls(data)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
