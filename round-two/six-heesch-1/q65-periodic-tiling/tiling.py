"""Search-free periodic tiling certificate reader, using lattice differences.

Unlike the producer's residue cover, reject every equal-coset pair by direct
integer lattice membership. Area equals the lattice index, so distinct cell
cosets from all representatives exhaust the quotient of the unit-cell grid.
"""
import argparse, hashlib, json
from itertools import combinations
from pathlib import Path

def require(ok, msg):
    if not ok:raise ValueError(msg)

def check(cells,certificate):
    require(isinstance(certificate,dict),'missing tiling witness')
    raw=list(map(tuple,cells));require(raw and len(raw)==len(set(raw)) and
        all(len(p)==2 and all(type(x) is int for x in p) for p in raw),'invalid source')
    periods=certificate['periods']
    require(len(periods)==2 and all(len(p)==2 and all(type(x) is int for x in p) for p in periods),'invalid periods')
    (a,b),(c,d)=periods;det=a*d-b*c;require(det!=0,'singular periods')
    footprints=[]
    reps=certificate['representatives']
    require(reps and len(reps)*len(raw)==abs(det),'copy areas do not match lattice index')
    for rep in reps:
        m=rep['matrix'];t=rep['translation']
        require(len(m)==4 and len(t)==2 and all(type(z) is int for z in m+t),'invalid affine map')
        g,h,i,j=m
        require(g*g+h*h==i*i+j*j==1 and g*i+h*j==0,'not a square-grid isometry')
        # Transform each physical closed unit square via its four vertices.
        fp=[]
        for x,y in raw:
            vertices=[(g*(x+u)+h*(y+v)+t[0],i*(x+u)+j*(y+v)+t[1]) for u in (0,1) for v in (0,1)]
            fp.append((min(q[0] for q in vertices),min(q[1] for q in vertices)))
        footprints.extend(fp)
    for (x,y),(u,v) in combinations(footprints,2):
        dx,dy=x-u,y-v
        require((d*dx-c*dy)%det or (a*dy-b*dx)%det,'two representative cells have the same lattice coset')
    return dict(area=len(raw),copies_per_period=len(reps),lattice_index=abs(det),
        checked_cell_cosets=len(footprints),plane_tiling=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path)
    args=ap.parse_args();data=json.loads(args.input.read_text());out=[]
    for row in data['records']:
        if row['certificate']:out.append(dict(label=row.get('label'),**check(row['cells'],row['certificate'])))
    print(json.dumps(dict(checked=out,negatives_claimed=False),indent=2))
if __name__=='__main__':main()
