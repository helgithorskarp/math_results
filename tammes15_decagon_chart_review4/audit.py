"""Independent fourth-decagon chart, partition, distance and clique audit."""
import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as sp
from sympy.polys.fields import field
from sympy.polys.rings import ring

K, c = field('t', sp.QQ)
R, t, u, v = ring('t,u,v', sp.QQ)
LABELS = (0,1,2,3,4,5,6,7,11,12)
FOLDS = ((1,2,7,6),(0,1,7,2),(4,2,6,7),(3,2,4,6),
         (5,4,6,2),(11,0,1,7),(12,0,7,1))
INTERVALS = ((Q(291,500),Q(59,100)),(Q(59,100),Q(593,1000)))
CERT_SHA = 'b0795cc143df1a774a41c83e4f2abd10b6bace89ba54a76c9ae0868be6b1e5eb'

def need(ok, message):
    if not ok: raise ValueError(message)

def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def metric(a,b,param):
    return (1-param)*sum(x*y for x,y in zip(a,b))+param*sum(a)*sum(b)

def closed_positive(p,lo,hi):
    z=sp.Symbol('t');p=sp.Poly(p.as_expr(),z,domain=sp.QQ)
    need(not p.is_zero,'zero strict polynomial')
    seq=p.sturm()
    def variation(x):
        signs=[int(sp.sign(f.eval(sp.Rational(x.numerator,x.denominator)))) for f in seq]
        signs=[x for x in signs if x]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    need(variation(lo)==variation(hi),'interior polynomial root')
    need(p.eval(sp.Rational(lo.numerator,lo.denominator))>0 and
         p.eval(sp.Rational(hi.numerator,hi.denominator))>0,'closed endpoint sign')

def core_and_chart():
    a={2:(K.one,K.zero,K.zero),6:(K.zero,K.one,K.zero),7:(K.zero,K.zero,K.one)}
    for new,i,j,old in FOLDS:
        need(all(metric(a[x],a[y],c)==c for x,y in [(i,j),(i,old),(j,old)]),'reflection inputs')
        a[new]=tuple(2*c/(1+c)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old]))
    D=(1+t)**3
    A={i:tuple(R.from_expr((x*(1+c)**3).as_expr()) for x in a[i]) for i in LABELS}
    need(all(metric(x,x,t)==D*D for x in A.values()),'all ten core units')
    contacts=[]
    for i,j in combinations(LABELS,2):
        gap=t*D*D-metric(A[i],A[j],t)
        if not gap:contacts.append([i,j])
        else:closed_positive(gap,INTERVALS[0][0],INTERVALS[1][1])
    need(len(contacts)==17,'exact core contact set')
    # Compare the precise polynomial-coordinate encoding, not just a graph mask.
    coordinates={i:[[int(x.get((k,0,0),0)) for k in range(x.degree(t)+1)] if x else [] for x in A[i]] for i in LABELS}
    rho=1+(1-t*t)*(u*u+v*v)+2*t*(1-t)*u*v
    Y=(rho-2-2*t*(u+v),2*u,2*v)
    need(metric(Y,Y,t)==rho*rho,'chart unit identity')
    need(Y[0]+t*(Y[1]+Y[2])==rho-2,'inverse-pole identity')
    S,T,U,V,X,Z=ring('t,u,v,x,z',sp.QQ)
    def chart(x,y):
        r=1+(1-T*T)*(x*x+y*y)+2*T*(1-T)*x*y
        return (r-2-2*T*(x+y),2*x,2*y),r
    left,rl=chart(U,V);right,rr=chart(X,Z)
    delta=[x*rr-y*rl for x,y in zip(left,right)]
    q=(1-T*T)*((U-X)**2+(V-Z)**2)+2*T*(1-T)*(U-X)*(V-Z)
    need(metric(delta,delta,T)==4*q*rl*rr,'universal chord identity')
    return [metric(A[i],Y,t)-t*D*rho for i in LABELS],contacts,digest(coordinates)

def children(cell):
    d,i,j=cell
    return [(d+1,2*i+a,2*j+b) for a,b in product((0,1),repeat=2)]

def partition_frontier(piece):
    leaves=[tuple(x) for x in piece['remaining_cover_cells']]
    refinements=[tuple(x) for x in piece['refined_cells']]
    need(len(leaves)==len(set(leaves)) and len(refinements)==len(set(refinements)),'duplicate tree entry')
    for z in leaves+refinements:
        need(len(z)==3 and all(type(x) is int for x in z),'integer cell triple')
        d,i,j=z;need(5<=d<=12 and 0<=i<2**d and 0<=j<2**d,'canonical bounded cell')
    internal=set(refinements)
    for d,i,j in leaves+refinements:
        while d:
            d-=1;i//=2;j//=2;internal.add((d,i,j))
    need(not set(leaves)&internal,'retained cell is split or overlaps a descendant')
    frontier={z for x in internal for z in children(x) if z not in internal}
    need(set(leaves)<=frontier,'missing retained leaf')
    need(sum((Q(1,4**z[0]) for z in frontier),Q(0))==1,'exact full-square area')
    return sorted(leaves),sorted(frontier-set(leaves)),internal

def bernstein(poly,cell,lo,hi):
    d,i,j=cell;h=sp.QQ(8,2**d);a=-4+i*h;b=-4+j*h
    f=poly.compose(t,sp.QQ(lo.numerator,lo.denominator)+sp.QQ((hi-lo).numerator,(hi-lo).denominator)*t)
    f=f.compose(u,a+h*u).compose(v,b+h*v)
    degree=(6,2,2);terms=f.to_dict();out=[]
    need(all(all(p<=n for p,n in zip(m,degree)) for m in terms),'tensor degree bound')
    for k,r,s in product(range(7),range(3),range(3)):
        out.append(sum((val*sp.QQ(comb(k,p),comb(6,p))*sp.QQ(comb(r,q),comb(2,q))*sp.QQ(comb(s,w),comb(2,w))
                        for (p,q,w),val in terms.items() if p<=k and q<=r and w<=s),sp.QQ.zero))
    return out

def cover(piece,forms,lo,hi):
    leaves,missing,internal=partition_frontier(piece);todo=deque(missing);discard=[];positive=0
    while todo:
        cell=todo.popleft();chosen=None
        for label,f in zip(LABELS,forms):
            coeff=bernstein(f,cell,lo,hi)
            if min(coeff)>0:
                chosen=label;positive+=len(coeff);break
        if chosen is not None:discard.append([list(cell),chosen])
        else:
            need(cell[0]<5,'unproved discarded chart cell '+str(cell))
            todo.extend(children(cell))
    full=leaves+[tuple(x[0]) for x in discard]
    need(len(full)==len(set(full)),'duplicate frontier cell')
    frontier=set(full)
    for d,i,j in full:
        while d:
            d-=1;i//=2;j//=2;need((d,i,j) not in frontier,'overlapping frontier cells')
    need(sum((Q(1,4**d) for d,i,j in full),Q(0))==1,'partition area including discarded cells')
    return leaves,discard,positive

def box(cell):
    d,i,j=cell;h=Q(8,2**d)
    return (-4+i*h,-4+(i+1)*h,-4+j*h,-4+(j+1)*h)

def quadratic(x,y,t):
    return (1-t)*(x-y)**2/2+(1-t)*(1+2*t)*(x+y)**2/2

def radius_minimum(cell,t):
    x0,x1,y0,y1=box(cell);xs=(x0,x1);ys=(y0,y1);values=[]
    # Nine active-set patterns: stationary interior, edge stationary points,
    # and corners. No clamped-edge helper from the source is imported.
    for sx,sy in product((-1,0,1),repeat=2):
        if sx==sy==0:x=y=Q(0)
        elif sx==0:y=ys[int(sy==1)];x=-t*y/(1+t)
        elif sy==0:x=xs[int(sx==1)];y=-t*x/(1+t)
        else:x=xs[int(sx==1)];y=ys[int(sy==1)]
        if x0<=x<=x1 and y0<=y<=y1:values.append(quadratic(x,y,t))
    need(bool(values),'rectangle minimum candidates')
    return 1+min(values)

def compatibility(leaves,lo,hi):
    grid=2**max(d for d,i,j in leaves);boxes=[]
    for d,i,j in leaves:
        h=8*grid//2**d;boxes.append((-4*grid+i*h,-4*grid+(i+1)*h,-4*grid+j*h,-4*grid+(j+1)*h))
    radii=[radius_minimum(z,hi) for z in leaves];need(min(radii)>=1,'positive radius minima')
    a=lo.denominator*(lo.denominator-lo.numerator)
    b=(lo.denominator-lo.numerator)*(lo.denominator+2*lo.numerator)
    den=2*lo.denominator**2*grid**2;adj=[0]*len(leaves);slack=None;cuts=0
    for i,j in combinations(range(len(leaves)+1),2):
        # Bijection onto all pairs with replacement (i,j-1), including self.
        j-=1;x0,x1,y0,y1=boxes[i];z0,z1,w0,w1=boxes[j]
        maximum=max(a*(x-y)**2+b*(x+y)**2 for x in (x0-z1,x1-z0) for y in (y0-w1,y1-w0))
        ri,rj=radii[i],radii[j]
        lhs=2*maximum*hi.denominator*ri.denominator*rj.denominator
        rhs=(hi.denominator-hi.numerator)*den*ri.numerator*rj.numerator
        if lhs<rhs:
            cuts+=1;n=2*(rhs-lhs);d=hi.denominator*den*ri.numerator*rj.numerator
            if slack is None or n*slack[1]<slack[0]*d:slack=(n,d)
        else:
            need(i!=j,'cell packing capacity exceeds one')
            adj[i]|=1<<j;adj[j]|=1<<i
        if i<2 and j<10:
            left=box(leaves[i]);right=box(leaves[j])
            ref=max(quadratic(x,y,lo) for x in (left[0]-right[1],left[1]-right[0])
                    for y in (left[2]-right[3],left[3]-right[2]))
            need(Q(maximum,den)==ref,'integer diagonal-basis bound vs rational reference')
    return adj,Q(*slack),cuts

def clique_audit(adj):
    """Count ordered four-cliques and rule out a later fifth vertex.

    Relabel by increasing degree, then enumerate increasing clique tuples.
    Every four-clique has exactly one increasing tuple. A five-clique has
    a first four-tuple with its fifth vertex in the common later neighbors.
    No coloring routine or author graph-builder is used.
    """
    order=sorted(range(len(adj)),key=lambda z:(adj[z].bit_count(),z))
    ranks={z:i for i,z in enumerate(order)}
    relabeled=[]
    for z in order:
        row=0;bits=adj[z]
        while bits:
            bit=bits&-bits;bits-=bit;row|=1<<ranks[bit.bit_length()-1]
        relabeled.append(row)
    later=[row&~((1<<(i+1))-1) for i,row in enumerate(relabeled)]
    triangles=fours=0;witness=None
    for i,neighbors in enumerate(later):
        while neighbors:
            jb=neighbors&-neighbors;neighbors-=jb;j=jb.bit_length()-1
            third=later[i]&later[j]
            while third:
                kb=third&-third;third-=kb;k=kb.bit_length()-1;triangles+=1
                fourth=later[i]&later[j]&later[k]
                while fourth:
                    lb=fourth&-fourth;fourth-=lb;l=lb.bit_length()-1;fours+=1
                    need(not (later[i]&later[j]&later[k]&later[l]),'compatible five-clique')
                    if witness is None:witness=[order[x] for x in (i,j,k,l)]
    maximum=4 if fours else 3 if triangles else 2 if any(adj) else int(bool(adj))
    return {'ordered_triangles':triangles,'ordered_four_cliques':fours,
            'maximum_clique_size':maximum,'maximum_witness':witness,
            'order_sha256':digest(order)}

def run(certificate):
    need(sp.__version__=='1.14.0','pinned SymPy version')
    need(certificate['format']==1 and certificate['core_key']==[6,1,1],'fixed core and format')
    need(len(certificate['pieces'])==2,'complete interval union')
    forms,contacts,coordinate_hash=core_and_chart();out=[]
    for piece,(lo,hi) in zip(certificate['pieces'],INTERVALS):
        need([Q(*x) for x in piece['interval']]==[lo,hi],'fixed closed interval')
        leaves,discard,positive=cover(piece,forms,lo,hi)
        adj,slack,cuts=compatibility(leaves,lo,hi);cliques=clique_audit(adj)
        need(cliques['maximum_clique_size']<=4,'compatible five-clique')
        out.append({'interval':piece['interval'],'retained_cells':len(leaves),'discarded_cells':len(discard),
                    'positive_tensor_coefficients':positive,'graph_sha256':digest(adj),
                    'edges':sum(x.bit_count() for x in adj)//2,'strict_distance_cuts_including_self':cuts,
                    'minimum_squared_chord_slack':str(slack),'clique_audit':cliques,
                    'independent_frontier_witness_sha256':digest(sorted(discard))})
    margin=min(Q(x['minimum_squared_chord_slack']) for x in out)/2
    exponent=0
    while Q(1,10**exponent)>margin:exponent+=1
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer','sympy':sp.__version__,
            'core_coordinate_sha256':coordinate_hash,'contacts':contacts,'pieces':out,
            'proved_extra_pair_cosine_excess_at_least':str(Q(1,10**exponent)),
            'scope':'Explicit local core only. Exact shared tree input, independent construction/coverage/sign/distance/clique implementation; upstream reduction and lower strip not recertified.'}

def controls(certificate):
    import copy
    tested=0
    for n in (5,6):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=[0]*n
            for bit,(i,j) in enumerate(edges):
                if mask&(1<<bit):adj[i]|=1<<j;adj[j]|=1<<i
            expected=any(all(adj[i]&(1<<j) for i,j in combinations(z,2))
                         for z in combinations(range(n),5))
            try:clique_audit(adj);observed=False
            except ValueError as e:
                need(str(e)=='compatible five-clique','unexpected clique rejection');observed=True
            need(observed==expected,'definition-level independent clique control')
            tested+=1
    variants=[];piece=certificate['pieces'][0]
    z=copy.deepcopy(piece);z['remaining_cover_cells'].append(z['remaining_cover_cells'][0]);variants.append(z)
    z=copy.deepcopy(piece);z['refined_cells'].append(z['refined_cells'][0]);variants.append(z)
    z=copy.deepcopy(piece);z['remaining_cover_cells'][0]=[5,-1,0];variants.append(z)
    z=copy.deepcopy(piece);z['remaining_cover_cells'][0]=[0,0,0];variants.append(z)
    z=copy.deepcopy(piece);z['refined_cells'].append(z['remaining_cover_cells'][0]);variants.append(z)
    for z in variants:
        try:partition_frontier(z)
        except ValueError:pass
        else:raise ValueError('invalid frontier accepted')
    # A missing entire cover must fail a real polynomial sign obligation.
    forms,_,_=core_and_chart();z=copy.deepcopy(piece);z['remaining_cover_cells']=[]
    try:cover(z,forms,*INTERVALS[0])
    except ValueError:pass
    else:raise ValueError('empty admissible cover accepted')
    return {'definition_graphs':tested,'rejected_frontiers':len(variants)+1}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('certificate',type=Path);parser.add_argument('--check',type=Path);parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args();data=args.certificate.read_bytes()
    need(hashlib.sha256(data).hexdigest()==CERT_SHA,'pinned certificate bytes')
    certificate=json.loads(data)
    if args.selftest:print(json.dumps(controls(certificate),sort_keys=True),file=__import__('sys').stderr)
    result=run(certificate)
    if args.check:need(result==json.loads(args.check.read_text()),'expected independent output')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
