"""Complete source-height inventories with fixed whole copies and occupied cells.

The additional blocked cells are guaranteed occupied by a moving fixed copy.
They are not additional whole tiles or new halo obligations.
"""
import deps
import strip_parametric_geometry as G
from strip_point_suppliers import supplier_systems
from strip_notch_intervals import parameter_partition,allowed_intervals

def blocked_heights(matrix,point,column,blocked):
    # If source(column,z) maps to point, the blocked cell has source
    # coordinates(column+du,z+dv), where(du,dv)=M^-1(blocked-point).
    m=G.inverse((matrix,(0,0),(0,0)))[0]
    x,y=G.sub(blocked[0],point[0]),G.sub(blocked[1],point[1])
    du=G.add(G.scale(m[0],x),G.scale(m[1],y))
    dv=G.add(G.scale(m[2],x),G.scale(m[3],y))
    rows=[]
    for d,lo,hi in G.COLS:
        active=G.atom('eq',G.add(du,G.constant(column-d)))
        if active is not False:
            rows.append((G.sub(lo,dv),G.add(G.sub(hi,dv),(0,1)),active))
    return tuple(rows)

def systems_for(case):
    systems=supplier_systems(case['point'],case['fixed'])
    for s in systems:
        extra=tuple(row for p in case['blocked']
                    for row in blocked_heights(s['matrix'],case['point'],s['column'],p))
        s['forbidden']=tuple(s['forbidden'])+extra
    return systems

def produce(case,guard):
    systems=systems_for(case);part=parameter_partition(systems);classes=[]
    for interval in part['intervals']:
        if len(interval['representatives'])!=1:raise ValueError('Unexpected parameter period')
        k=interval['representatives'][0];atlas=set()
        for s in systems:
            guard()
            for lo,hi in allowed_intervals(s,k):
                a,b=G.sub(hi,lo)
                width=b if a==0 else (max(a*interval['lo']+b,a*interval['hi']+b)
                                      if interval['hi'] is not None else None)
                if width is None or not 0<width<=32:
                    raise RuntimeError('Unbounded/wide source family; no truncated proof')
                M=s['matrix'];c=s['column']
                for j in range(width):
                    z=G.add(lo,(0,j))
                    atlas.add((M,G.sub(G.sub(case['point'][0],(0,M[0]*c)),G.scale(M[1],z)),
                               G.sub(G.sub(case['point'][1],(0,M[2]*c)),G.scale(M[3],z))))
        classes.append({**interval,'atlas':sorted(atlas)})
    atlas=sorted(set().union(*(set(c['atlas']) for c in classes)))
    return {'name':case['name'],'point':case['point'],'fixed':case['fixed'],
            'blocked':case['blocked'],'systems':systems,'partition':part,
            'classes':classes,'atlas':atlas}
