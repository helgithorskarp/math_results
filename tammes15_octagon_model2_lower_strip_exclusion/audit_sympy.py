"""Separate native QQ algebra and pivoted maximal-clique audit.

This imports no production algebra, cover, graph or search predicate.
Same author as check.py; it is not independent peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
from math import comb,lcm
import hashlib,json,sys,time
import sympy
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

HERE=Path(__file__).resolve().parent
L,H=Q(14,25),Q(29,50)
R,t,u,v,U,V=ring('t,u,v,U,V',QQ)
one=R.one

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rational(x):return Q(int(x.numerator),int(x.denominator))
def domain(x):
    x=Q(x);return QQ(x.numerator,x.denominator)

def coordinates(q):
    s=one+q;D=s**3
    return D,{
        0:[4*q*q*s-D,-2*q*s**2,2*q*s**2+4*q*q*s],
        1:[2*q*s**2,-D,2*q*s**2],2:[D,R.zero,R.zero],
        3:[2*q*s**2,2*q*s**2,-D],
        4:[8*q**3+4*q*q*s-2*q*s**2,8*q**3+8*q*q*s-D,-2*q*s**2-4*q*q*s],
        5:[4*q*q*s-D,2*q*s**2+4*q*q*s,-2*q*s**2],
        6:[R.zero,D,R.zero],7:[R.zero,R.zero,D]}

def metric(a,b,q):return (one-q)*sum(x*y for x,y in zip(a,b))+q*sum(a)*sum(b)
def radius(a,b,q):return one+(one-q*q)*(a*a+b*b)+2*q*(one-q)*a*b
def chart(a,b,q):
    r=radius(a,b,q);return r,[r-2-2*q*(a+b),2*a,2*b]

def beta_power(power,index,degree,lo,hi):
    return sum(Q(comb(power,k)*comb(index,k),comb(degree,k))*lo**(power-k)*(hi-lo)**k
               for k in range(min(power,index)+1))

def parse_cell(c):
    need(type(c) in (list,tuple) and len(c)==3 and all(type(x) is int for x in c),'native integer cell')
    d,i,j=c;need(0<=d<=12 and 0<=i<2**d and 0<=j<2**d,'native cell range')
    return tuple(c)

def dominate(adjacency):
    """Exact live-set containment; a nonadjacent replacement preserves cliques."""
    neighbors=[{j for j in range(len(adjacency)) if a&(1<<j)} for a in adjacency]
    alive=set(range(len(adjacency)));trace=[]
    changed=True
    while changed:
        changed=False
        for v0 in sorted(alive):
            nv=neighbors[v0]&alive
            for w0 in sorted(alive-{v0}-nv):
                if nv<=neighbors[w0]&alive:
                    trace.append([v0,w0]);alive.remove(v0);changed=True;break
    return sum(1<<k for k in alive),trace

def pivoted_clique(adjacency,active,size=7,maxstates=2000000):
    """Pivoted maximal-clique search with exact edge/triangle terminal tests."""
    states=0
    def bits(s):
        while s:
            b=s&-s;s-=b;yield b.bit_length()-1
    def expand(p,x,depth):
        nonlocal states
        states+=1
        if states>maxstates:raise RuntimeError('incomplete native clique audit: state cap')
        if depth==size:return True
        if p.bit_count()+depth<size:return False
        needed=size-depth
        if needed==1:return bool(p)
        if needed==2:return any(adjacency[k]&p for k in bits(p))
        if needed==3:
            for k in bits(p):
                later=p&~((1<<(k+1))-1);neighbors=adjacency[k]&later
                if any(adjacency[j]&neighbors for j in bits(neighbors)):return True
            return False
        union=p|x
        if not union:return False
        pivot=max(bits(union),key=lambda k:(adjacency[k]&p).bit_count())
        branch=p&~adjacency[pivot]
        for k in bits(branch):
            if expand(p&adjacency[k],x&adjacency[k],depth+1):return True
            p&=~(1<<k);x|=1<<k
            if p.bit_count()+depth<size:break
        return False
    return expand(active,0,0),states

def audit(data):
    need(data['format']==1 and data['model_index']==2 and data['core_size']==8 and data['extra_points']==7,'native fixed target')
    need(data['interval']==[[14,25],[29,50]],'native closed interval')
    D,points=coordinates(t);ra,ya=chart(u,v,t);rb,yb=chart(U,V,t)
    def univariate(p):
        need(all(not any(e[1:]) for e in p),'native univariate coordinate')
        if not p:return []
        out=[]
        for power in range(max(e[0] for e in p)+1):
            value=rational(p.get((power,0,0,0,0),QQ.zero))
            need(value.denominator==1,'native integer numerator');out.append(value.numerator)
        return out
    coordinate_hash=digest({k:[univariate(p) for p in points[k]] for k in range(8)})
    pair=ra*rb-2*((one+t)*((u-U)**2+(v-V)**2)+2*t*(u-U)*(v-V))
    need(metric(ya,ya,t)==ra*ra and metric(yb,yb,t)==rb*rb,'native chart unit identities')
    need(metric(ya,yb,t)-t*ra*rb==(one-t)*pair,'native separation identity')
    need(metric([one,R.zero,R.zero],ya,t)==ra-2,'native anchor projection identity')
    generic=[u,v,U];projection=metric([one,R.zero,R.zero],generic,t)
    need(metric(generic,generic,t)==projection**2+(one-t*t)*(v*v+U*U)+2*t*(one-t)*v*U,
         'native Schur completeness identity')
    contacts=[]
    for i in range(8):need(metric(points[i],points[i],t)==D*D,'native core units')
    for i,j in combinations(range(8),2):
        gap=t*D*D-metric(points[i],points[j],t)
        if not gap:contacts.append([i,j]);continue
        degree=max(e[0] for e in gap)
        values=[sum(rational(c)*beta_power(e[0],k,degree,L,H) for e,c in gap.items()) for k in range(degree+1)]
        need(all(z>0 for z in values),'native core packing gaps')
    need(len(contacts)==13,'native thirteen contacts')
    # Independently transform the explicit native F_i into tensor Bernstein
    # coefficients. Generic monomial basis products replace the production
    # specialized quadratic formula.
    _,yy=chart(u,v,t)
    raw=[metric(points[k],yy,t)-t*D*ra for k in range(8)]
    power_set=((0,0),(1,0),(0,1),(2,0),(1,1),(0,2))
    tensors=[]
    for p in raw:
        need(all(e[0]<=6 and (e[1],e[2]) in power_set and not e[3] and not e[4] for e in p),'native core tensor degrees')
        rows=[]
        for k in range(7):
            rows.append([sum(rational(c)*beta_power(e[0],k,6,L,H)
                         for e,c in p.items() if (e[1],e[2])==powers) for powers in power_set])
        den=lcm(*(z.denominator for row in rows for z in row))
        tensors.append([[int(z*den) for z in row] for row in rows])
    leaves=sorted(parse_cell(c) for c in data['remaining_cover_cells'])
    refined=[parse_cell(c) for c in data['refined_cells']]
    need(len(leaves)==len(set(leaves)) and len(refined)==len(set(refined)) and leaves,'native unique tree cells')
    need(all(d>=5 for d,i,j in leaves+refined),'native depth range')
    leafset=set(leaves);refinedset=set(refined);ancestors=set()
    for d,i,j in leaves+refined:
        for depth in range(d):ancestors.add((depth,i//2**(d-depth),j//2**(d-depth)))
    need(not leafset&(ancestors|refinedset),'native disjoint frontier')
    maxdepth=max(c[0] for c in leaves+refined)+1;grid=2**(maxdepth-3)
    def basis(a,h):
        return [[4*grid*grid,2*grid*(2*a+k*h),4*a*a+4*k*a*h+4*h*h*int(k==2)] for k in range(3)]
    def witness(c):
        d,i,j=c;h=8*grid//2**d;bu=basis(-4*grid+i*h,h);bv=basis(-4*grid+j*h,h)
        for label,rows in enumerate(tensors):
            if all(sum(coef*bu[r][a]*bv[s][b] for coef,(a,b) in zip(row,power_set))>0
                   for row in rows for r in range(3) for s in range(3)):return label
        return None
    visited=set();found=set();discards=[]
    def walk(c):
        visited.add(c)
        if c in leafset:found.add(c);return
        if c in ancestors|refinedset:
            d,i,j=c
            for a in range(2):
                for b in range(2):walk((d+1,2*i+a,2*j+b))
            return
        label=witness(c)
        if label is None and c[0]<5:
            d,i,j=c
            for a in range(2):
                for b in range(2):walk((d+1,2*i+a,2*j+b))
        else:
            need(label is not None,'native uncovered cell '+str(c));discards.append([list(c),'bernstein',label])
    walk((0,0,0));need(found==leafset and set(refined)<=visited,'native complete tree cover')
    # Completed-square minimization on each of the four edges of a rectangle.
    # The stationary point of the full positive quadratic is the origin.
    def rminimum(c):
        d,i,j=c;h=Q(8,2**d);x0=-4+i*h;x1=x0+h;y0=-4+j*h;y1=y0+h
        if x0<=0<=x1 and y0<=0<=y1:return Q(1)
        rho=H/(1+H);diag=1-H*H
        def q(x,y):return diag*((x+rho*y)**2+(1-rho*rho)*y*y)
        candidates=[]
        for y in (y0,y1):candidates.append(q(min(x1,max(x0,-rho*y)),y))
        for x in (x0,x1):candidates.append(q(x,min(y1,max(y0,-rho*x))))
        return 1+min(candidates)
    rmins=[rminimum(c) for c in leaves];boxes=[]
    for k,(d,i,j) in enumerate(leaves):
        h=8*grid//2**d;boxes.append((-4*grid+i*h,-4*grid+j*h,-4*grid+(i+1)*h,-4*grid+(j+1)*h))
    n=len(leaves);adjacency=[0]*n
    diagonal=(L.denominator-L.numerator)*(L.denominator+L.numerator)
    cross=L.numerator*(L.denominator-L.numerator)
    common=L.denominator**2*grid**2
    for i,(a,b,c,d) in enumerate(boxes):
        ri=rmins[i]
        for j in range(i,n):
            e,f,g,h=boxes[j];rj=rmins[j]
            cx=a+c-e-g;cy=b+d-f-h;hx=c-a+g-e;hy=d-b+h-f
            maximum=max(diagonal*((cx+sx*hx)**2+(cy+sy*hy)**2)+2*cross*(cx+sx*hx)*(cy+sy*hy)
                        for sx in (-1,1) for sy in (-1,1))
            lhs=maximum*H.denominator*ri.denominator*rj.denominator
            rhs=2*(H.denominator-H.numerator)*common*ri.numerator*rj.numerator
            if i==j:need(lhs<rhs,'native cell capacity one')
            elif lhs>=rhs:adjacency[i]+=1<<j;adjacency[j]+=1<<i
    basic_edges=sum(z.bit_count() for z in adjacency)//2
    active,trace=dominate(adjacency)
    positive,states=pivoted_clique(adjacency,active)
    need(not positive,'native possible seven-clique remains')
    result={'agent':'six-tammes-2','role':'researcher','status':'SEPARATE_NATIVE_QQ_AND_PIVOTED_NO_K7_AUDIT',
            'certified_closed_interval':data['interval'],'core_unit_identities':8,'core_contacts':contacts,
            'core_coordinates_sha256':coordinate_hash,'universal_chart_identities':5,
            'native_positive_bernstein_coefficients':63*sum(z[1]=='bernstein' for z in discards),
            'cover_cells':n,'discarded_cells':len(discards),
            'basic_edges':basic_edges,'compatibility_edges':sum(z.bit_count() for z in adjacency)//2,
            'searched_vertices':n,'pivoted_search_vertices':active.bit_count(),
            'audit_domination_deletions':len(trace),'audit_domination_sha256':digest(trace),
            'pivoted_clique_states':states,'tree_sha256':digest([leaves,discards]),'graph_sha256':digest(adjacency),
            'sympy':sympy.__version__,
            'independent_peer_review':'pending','global_tammes15_bounds':'unchanged',
            'trust_boundary':'Same-author different exact algebra, generic tensor transform, completed-square minima, full graph and pivoted maximal-clique search; written geometric reduction, not formalized.'}
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    need(contacts==expected['contacts'],'native exact contact pattern')
    for field in ('cover_cells','discarded_cells','basic_edges','compatibility_edges','searched_vertices',
                  'tree_sha256','graph_sha256','core_coordinates_sha256'):
        need(result[field]==expected[field],'native/production agreement '+field)
    return result

if __name__=='__main__':
    started=time.monotonic();data=json.loads((HERE/'certificate.json').read_text())
    print(json.dumps(audit(data),indent=2,sort_keys=True))
    print('completed separate audit in %.3f seconds'%(time.monotonic()-started),file=sys.stderr)
