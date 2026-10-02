"""Exact all-k copies covering an affine point, disjoint from fixed copies.

Enumerate source columns and source height. Overlap becomes a union of height
intervals. A finite atlas is returned only when every surviving interval has
bounded constant length in every exact parameter class.
"""

import deps
from strip_columns import MATRICES,require
from strip_parametric_geometry import COLS,add,sub,scale,constant,value,atom,both,inverse,compose
from strip_notch_intervals import parameter_partition,allowed_intervals

IDENTITY=((1,0,0,1),(0,0),(0,0))


def transform(g,point):
    m,a,b=g;x,y=point
    return add(add(scale(m[0],x),scale(m[1],y)),a),add(add(scale(m[2],x),scale(m[3],y)),b)


def overlap_heights(matrix,point,source_column):
    alpha,beta,gamma,delta=matrix;pu,pv=point;rows=[]
    for c,lo,hi in COLS:
        for d,L,H in COLS:
            if beta:
                n=sub(constant(d-alpha*(c-source_column)),pu)
                require(n[0]%beta==0,'Nonconstant congruence in height inventory')
                if n[1]%beta:continue
                C=(n[0]//beta,n[1]//beta)
                image_v=add(add(pv,constant(gamma*(c-source_column))),scale(delta,C))
                active=both(atom('ge',sub(image_v,L)),atom('ge',sub(H,image_v)))
                if active is False:continue
                first=sub(lo,C);last=sub(hi,C)
            else:
                active=atom('eq',add(pu,constant(alpha*(c-source_column)-d)))
                if active is False:continue
                offset=add(pv,constant(gamma*(c-source_column)))
                if delta==1:
                    first=add(sub(offset,H),lo);last=add(sub(offset,L),hi)
                else:
                    first=add(sub(L,offset),lo);last=add(sub(H,offset),hi)
            rows.append((first,add(last,constant(1)),active))
    return tuple(rows)


def supplier_systems(point,fixed):
    rows=[]
    for m in MATRICES:
        for c,lo,hi in COLS:
            forbidden=[]
            for g in fixed:
                ig=inverse(g);relmatrix=compose(ig,(m,(0,0),(0,0)))[0]
                forbidden.extend(overlap_heights(relmatrix,transform(ig,point),c))
            rows.append({'matrix':m,'column':c,'lo':lo,'hi':add(hi,constant(1)),
                         'forbidden':tuple(forbidden)})
    return rows


def finite_suppliers(point,fixed,max_width=32):
    systems=supplier_systems(point,fixed);part=parameter_partition(systems);classes=[]
    for interval in part['intervals']:
        k=interval['representatives'][0];out=set()
        for s in systems:
            for lo,hi in allowed_intervals(s,k):
                A,B=sub(hi,lo)
                width=B if A==0 else (max(A*interval['lo']+B,A*interval['hi']+B)
                                      if interval['hi'] is not None else None)
                if width is None or not 0<width<=max_width:
                    return {'finite':False,'reason':'A height family varies with k or exceeds fixed width',
                            'partition':part,'example':{'matrix':s['matrix'],'column':s['column'],'interval':(lo,hi)}}
                alpha,beta,gamma,delta=s['matrix'];c=s['column']
                for j in range(width):
                    v=add(lo,constant(j))
                    out.add((s['matrix'],sub(sub(point[0],constant(alpha*c)),scale(beta,v)),
                              sub(sub(point[1],constant(gamma*c)),scale(delta,v))))
        classes.append({**interval,'atlas':sorted(out)})
    atlas=sorted(set().union(*(set(c['atlas']) for c in classes)))
    return {'finite':True,'partition':part,'classes':classes,'atlas':atlas}
