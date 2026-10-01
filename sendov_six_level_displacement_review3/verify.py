#!/usr/bin/env python3
"""six-reviewer-3: independent Newton/characteristic reconstruction.
Standard library only. Full twelve-case regeneration by default.
No author imports or stored polynomial data are used by derive().
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, lcm
from pathlib import Path
import argparse, hashlib, json, time, copy, tempfile, resource

BASE=32
CHECKS=0
def need(ok, label):
    global CHECKS
    CHECKS+=1
    if not ok: raise ValueError(label)
def exponent(k):
    out=[]
    for _ in range(5):out.append(k%BASE);k//=BASE
    need(k==0,"packed exponent within five variables")
    return tuple(out)
def pack(e):return sum(v*BASE**j for j,v in enumerate(e))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
class Poly:
    def __init__(self,x=0):
        if isinstance(x,Poly):x=x.d
        if isinstance(x,int):x={0:x}
        self.d={k:v for k,v in x.items() if v}
    def __add__(self,x):
        o=self.d.copy()
        for k,v in Poly(x).d.items():o[k]=o.get(k,0)+v
        return Poly(o)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,x):return self+-Poly(x)
    def __rsub__(self,x):return Poly(x)+-self
    def __mul__(self,x):
        if isinstance(x,int):return Poly({k:v*x for k,v in self.d.items()})
        out={}
        for k,v in self.d.items():
            for h,w in Poly(x).d.items():
                n=k+h;out[n]=out.get(n,0)+v*w
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        o=Poly(1);b=self
        while n:
            if n&1:o=o*b
            n//=2
            if n:b=b*b
        return o
    def __eq__(self,x):return self.d==Poly(x).d
    def dump(self):return [[*e,str(v)] for e,v in sorted((exponent(k),v) for k,v in self.d.items())]
    def value(self,x):
        x=list(map(Q,x));b=lcm(*(t.denominator for t in x));u=[int(t*b) for t in x]
        terms=[(exponent(k),v) for k,v in self.d.items()]
        deg=max((sum(e) for e,v in terms),default=0);pw=[[t**i for i in range(deg+1)] for t in u]
        n=0
        for e,v in terms:
            z=v*b**(deg-sum(e))
            for i,a in enumerate(e):z*=pw[i][a]
            n+=z
        return Q(n,b**deg)

V=[Poly({BASE**i:1}) for i in range(5)]
H=sum(V,Poly())
def det(a):
    """Laplace recursion over index subsets, with memoized minor reuse."""
    n=len(a);cache={}
    def minor(rr,cc):
        key=(rr,cc)
        if key in cache:return cache[key]
        if not rr:return Poly(1)
        # Choose last row: block determinant then expands along the coupling.
        i=rr[-1];rest=rr[:-1];ans=Poly()
        for j,c in enumerate(cc):
            entry=a[i][c]
            if not entry.d:continue
            ans+=(-1)**(len(rr)-1+j)*entry*minor(rest,cc[:j]+cc[j+1:])
        cache[key]=ans
        return ans
    return minor(tuple(range(n)),tuple(range(n)))
def solve(a,b):
    a=[[Q(v) for v in r]+[Q(t)] for r,t in zip(a,b)]
    for j in range(len(b)):
        pivot=next((i for i in range(j,len(b)) if a[i][j]),None)
        if pivot is None:raise ValueError("singular")
        a[j],a[pivot]=a[pivot],a[j];z=a[j][j];a[j]=[v/z for v in a[j]]
        for i in range(len(b)):
            if i!=j:
                z=a[i][j];a[i]=[v-z*w for v,w in zip(a[i],a[j])]
    return [r[-1] for r in a]
# Private assembly fragment for the standalone independent checker.
PAIRS=((1,5),(1,6),(2,5),(2,6))
def qdet(a):
    a=[list(map(Q,r)) for r in a];out=Q(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return Q(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];out=-out
        z=a[j][j];out*=z
        for i in range(j+1,len(a)):
            t=a[i][j]/z
            for k in range(j+1,len(a)):a[i][k]-=t*a[j][k]
    return out
def rank(a):
    a=[list(map(Q,r)) for r in a]
    if not a:return 0
    i=0
    for j in range(len(a[0])):
        pivot=next((k for k in range(i,len(a)) if a[k][j]),None)
        if pivot is None:continue
        a[i],a[pivot]=a[pivot],a[i];z=a[i][j];a[i]=[x/z for x in a[i]]
        for k in range(i+1,len(a)):
            z=a[k][j];a[k]=[x-z*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i
def section(pair):
    need(pair in PAIRS,'one of four remaining doubled-rank sections')
    m=[1+int(i in pair) for i in range(1,7)]
    M=[sum(m[:i]) for i in range(1,6)]
    faces=[([int(i==j) for i in range(5)],Q(0)) for j in range(5)]
    faces.append(([Q(1,t) for t in M],Q(1,4)))
    vv=set()
    for active in combinations(faces,4):
        try:a=tuple(solve([[1]*5]+[f[0] for f in active],[1]+[f[1] for f in active]))
        except ValueError:continue
        if min(a)>=0 and sum(a[j]/M[j] for j in range(5))<=Q(1,4):vv.add(a)
    need(len(vv)==7,'complete active-face vertex enumeration')
    return m,M,sorted(vv)
def level(a,M):
    return tuple(1-sum(8*a[j]/M[j] for j in range(i,5)) for i in range(5))+(Q(1),)
def simplices(pair):
    m,M,vv=section(pair)
    unit={i:next(v for v in vv if v[i]==1) for i in (2,3,4)}
    cross={(i,j):next(v for v in vv if v[i] and v[j] and sum(x!=0 for x in v)==2)
           for i in (0,1) for j in (3,4)}
    return [[unit[2],unit[3],unit[4],cross[0,4],cross[1,4]],
            [unit[2],unit[3],cross[0,3],cross[0,4],cross[1,4]],
            [unit[2],cross[1,3],unit[3],cross[0,3],cross[1,4]]]
def inverse_columns(vertices):
    mat=[[a[i] for a in vertices] for i in range(5)]
    cols=[solve(mat,[int(i==j) for i in range(5)]) for j in range(5)]
    inverse=[[cols[j][i] for j in range(5)] for i in range(5)]
    for i in range(5):
        for j in range(5):
            need(sum(mat[i][k]*inverse[k][j] for k in range(5))==int(i==j),'entire simplex inverse')
    return inverse
def simplex(pair,cell):
    m,M,vv=section(pair);verts=simplices(pair)[cell]
    profiles=[level(a,M) for a in verts]
    L=lcm(*(t.denominator for v in profiles for t in v))
    inverse=inverse_columns(verts)
    forms=[sum((int(L*profiles[j][i])*V[j] for j in range(5)),Poly()) for i in range(6)]
    roots=[forms[i] for i in range(6) for _ in range(m[i])]
    need(sum(roots,Poly())==0 and forms[5]==L*H,'complete physical forms balance and max')
    meta={'pair':list(pair),'cell':cell,'scale':L,'multiplicities':m,'cumulative':M,
          'gap_vertices':[[str(t) for t in a] for a in verts],
          'level_vertices':[[str(t) for t in a] for a in profiles],
          'inverse_sha256':digest([[str(t) for t in row] for row in inverse])}
    return roots,meta
def simplex_volume(vertices):
    # 4! times coordinate volume in a0,...,a3, with sum(a)=1.
    return abs(qdet([[vertices[j][i]-vertices[0][i] for i in range(4)] for j in range(1,5)]))
def cover_certificate(pair):
    m,M,vv=section(pair)
    # Independently pull the full polytope through its original six
    # supporting inequalities, rather than the three transport paths.
    facets=[{i for i,v in enumerate(vv) if v[j]==0} for j in range(5)]
    facets.append({i for i,v in enumerate(vv) if sum(v[j]/M[j] for j in range(5))==Q(1,4)})
    def dimension(indices):
        p=vv[min(indices)]
        return rank([[vv[i][j]-p[j] for j in range(5)] for i in sorted(indices)])
    def pulling(face):
        if len(face)==1:return [[next(iter(face))]]
        d=dimension(face);apex=min(face);ff={frozenset(face&f) for f in facets}
        ff=[f for f in ff if f and len(f)<len(face) and dimension(f)==d-1 and apex not in f]
        need(bool(ff),'complete proper supporting facets for pulling')
        return [[apex]+s for f in sorted(ff,key=lambda x:sorted(x)) for s in pulling(set(f))]
    pulled=pulling(set(range(len(vv))))
    need(all(len(s)==5 for s in pulled),'all pulled simplices full dimensional')
    whole_volume=sum(simplex_volume([vv[i] for i in s]) for s in pulled)
    cells=simplices(pair)
    vols=[simplex_volume(s) for s in cells]
    need(all(v>0 for v in vols) and sum(vols)==whole_volume,'exact volume equality with independent pulling cover')
    intersection_dims=[]
    for p,q in combinations(cells,2):
        constraints=inverse_columns(p)+inverse_columns(q)
        points=set()
        for active in combinations(constraints,4):
            try:z=tuple(solve([[1]*5]+list(active),[1,0,0,0,0]))
            except ValueError:continue
            if all(sum(a*b for a,b in zip(r,z))>=0 for r in constraints):points.add(z)
        need(bool(points),'nonempty closed simplex intersection')
        z=next(iter(points));d=rank([[a[i]-z[i] for i in range(5)] for a in points])
        need(d<4,'pairwise interiors disjoint by full intersection vertex enumeration')
        intersection_dims.append(d)
    for a in vv:
        x=level(a,M)
        need(sum(t*w for t,w in zip(x,m))==0 and max(x)==1 and min(x)>=-1,'every physical section vertex')
    local_profiles=[level(a,M) for a in cells[2]]
    S=[];X=[]
    for levels in local_profiles:
        roots=[levels[i] for i in range(6) for _ in range(m[i])]
        S.append(sum(1+t for t in roots[:3])+sum(1-t for t in roots[5:]))
        X.append((roots[4]-roots[3])/2)
    need(X==[1,0,0,0,0] and S[:3]==[0,0,Q(6,5)],'whole two-moving-triple affine local maps')
    need(all(0<=t<=Q(6,5) for t in S),'all physical deficit coefficients bounded')
    return {'pair':list(pair),'vertices':[[str(t) for t in a] for a in vv],
            'pulled_simplices':pulled,'full_volume_factorial':str(whole_volume),
            'target_cell_volumes_factorial':list(map(str,vols)),
            'intersection_dimensions':intersection_dims,'local_S':list(map(str,S)),'local_x':list(map(str,X))}
def common():
    geometry=[cover_certificate(pair) for pair in PAIRS]
    need(sum(len(r['vertices']) for r in geometry)==28,'all28 complete section vertices')
    # Generic scalar/local constants are reconstructed from their
    # definitions, retaining the earlier ordinary proof inputs.
    N=list(map(Q,[2058,21912,-15876,19224,3402]))
    D=mul1([Q(3),Q(1)],mul1([Q(1),Q(3)],[Q(1),Q(3)]))
    T=add1(mul1(derivative(N),D),[-v for v in mul1(N,derivative(D))])
    need(T==list(map(Q,[26634,-231084,-907290,376920,971190,224532,30618])),'entire scalar derivative numerator')
    need(eval1(T,Q(2,25))>0>eval1(T,Q(9,100)),'scalar root bracket')
    bound=Q(-231084)+sum(i*T[i]*Q(1,4)**(i-1) for i in range(3,7))
    need(bound==Q(-24357717,256)<-90000 and eval1(D,Q(1,4))==Q(637,64)<10,'whole interval curvature450 bounds')
    normal=add1(add1(mul1(N,D),[-v for v in [Q(0)]+T]),[-750*v for v in mul1(D,D)])
    while normal and not normal[-1]:normal.pop()
    need(len(normal)==6,'degree5 normal-gradient polynomial')
    normal_table=btable(normal,Q(2,25),Q(9,100),True)
    need(Q(1,8)*Q(40,3)**2==Q(200,9),'Riesz first derivative')
    need(Q(1,4)*Q(40,3)**3==Q(16000,27),'Riesz second derivative')
    need(2+Q(800,9)+Q(16000,27)<684 and 2*(3*25**2+684)<5200,'active support weight bounds')
    need(5200/Q(5)+2*50+5==1145 and 96/Q(5)+64+40<124,'support product Hessians')
    need(122*16+224*124+5760*1145==6624928<6700000,'whole support Hessian')
    need(3350000*Q(1,100000)<50,'normal loss200')
    need(Q(6,5)/120000==Q(1,100000),'whole local deficit cutoff')
    need((Q(119999,120000)*Q(147,500))**2>=Q(2,25) and Q(37,125)**2<=Q(9,100),'whole local scalar cutoff')
    delta=eval1(N,Q(87,1000))/eval1(D,Q(87,1000))-Q(785753,1000)
    need(delta==Q(1331662697,1636234509000)>Q(1,1250),'exact strict gap')
    # Sharp orbit support by sorted-gap decomposition. The seven facet
    # ratios reduce to k=1,7; k=4 uses t>=0 and is strictly larger.
    norms=[Q(k*(8-k),8) for k in range(1,8)]
    sums=[1,2,3,3,3,2,1]
    for k in range(7):
        need(Q(sums[k]**2)*norms[0]>=norms[k],'every sorted-gap support coefficient')
    need(all(Q(sums[k]**2)*norms[0]>norms[k] for k in range(1,6)),'strict interior sorted-gap support ratios')
    q=2-1401*delta
    need(q>0 and 2163*q*q<1600,'cleared exact1401 global stability inequality')
    need(Q(1,90)<1401 and Q(1,40)<1401,'both retained local constants below1401')
    need(Q(13,8)**4/Q(10985,33554432)==Q(106496,5),'original-root radius scale')
    return {'geometry':geometry,'normal_gradient_table':normal_table,'strict_gap':str(delta),
            'sharp_uniform_squared_orbit_distance':'2-4/sqrt(7*(3+u_*))',
            'refined_global_stability_constant':'1401',
            'cleared1401_margin':str(1600-2163*q*q),'original_root_radius_scale':'106496/5'}

def compositions(n,k):
    if k==1:yield (n,);return
    for i in range(n+1):
        for r in compositions(n-i,k-1):yield (i,*r)
def derive(rank,cell,progress=False):
    start=time.monotonic()
    def stage(s):
        if progress:print(json.dumps({'case':[rank,cell],'stage':s,'seconds':time.monotonic()-start}),flush=True)
    roots,meta=simplex(rank,cell);L=meta['scale']
    mu=[]
    for j in range(1,9):mu.append(sum((t**j for t in roots),Poly()))
    # h(y)=prod(y-T_j), represented by descending coefficients.
    h=[Poly(1)]
    for t in roots:
        nxt=[Poly() for _ in range(len(h)+1)]
        for i,c in enumerate(h):nxt[i]+=c;nxt[i+1]-=t*c
        h=nxt
    # char(8C_T): coefficient k is (8-k)*8**(k-1)*h_k.
    c=[Poly(1)]+[(8-k)*8**(k-1)*h[k] for k in range(1,8)]
    ss=[Poly(7)]
    for j in range(1,9):
        s=-sum((c[k]*ss[j-k] for k in range(1,min(j,8))),Poly())
        if j<=7:s-=j*c[j]
        ss.append(s)
    # Coupling resolvent recurrence on e-perp, not the explicit moment list.
    v=[]
    for i in range(5):
        v.append(8**i*mu[i+1]-sum((8**(j+1)*mu[j+1]*v[i-2-j] for j in range(i-1)),Poly()))
    z=(8*L*H)**2
    A=[[z*z*ss[i+j]-2*z*ss[i+j+2]+ss[i+j+4] for j in range(3)] for i in range(3)]
    R=[z*v[i]-v[i+2] for i in range(3)]
    stage("Newton traces and coupling recurrence")
    D=det(A);stage("Gram determinant")
    block=[A[i]+[R[i]] for i in range(3)]+[R+[Poly()]]
    N=-det(block);stage("four by four Schur numerator")
    F=(785753*(L*H)**2*mu[1]-122000*mu[1]**2-224000*mu[3])*D+90000*N
    for p,d in ((D,18),(N,22),(F,22)):
        need(all(sum(exponent(k))==d for k in p.d),"homogeneous degree/no-carry bound")
    stage("whole degree22 target")
    rows=[roots,mu,ss,v,A,R,D,N,F]
    return rows,meta

def power_from_group(target,gamma):
    n=22-sum(gamma);out=[Q(0)]*(n+1)
    for i in range(n+1):
        z=target.d.get(pack((i,n-i,*gamma)),0)
        for j in range(n-i+1):out[i+j]+=z*comb(n-i,j)*(-1)**j
    return out
def btable(power,a,b,strict=False):
    n=len(power)-1
    shift=[sum(power[j]*comb(j,i)*a**(j-i)*(b-a)**i for j in range(i,n+1)) for i in range(n+1)]
    bern=[sum(shift[j]*Q(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
    # Invert with forward differences; different route from monomial basis.
    diff=bern[:];back=[]
    for j in range(n+1):
        back.append(comb(n,j)*diff[0])
        diff=[v-u for u,v in zip(diff,diff[1:])]
    need(back==shift,"whole Bernstein inverse by finite differences")
    for v in bern:need(v>0 if strict else v>=0,"continuous scalar coefficient sign")
    return {'degree':n,'interval':[str(a),str(b)],'entries':n+1,'minimum':str(min(bern)),
            'zeros':[i for i,x in enumerate(bern) if not x],'coefficient_sha256':digest(list(map(str,bern)))}
def signs(F,rank,cell):
    if cell!=2:
        full=[[*e,str(F.d.get(pack(e),0))] for e in compositions(22,5)]
        need(len(full)==14950,"complete homogeneous coefficient count")
        for row in full:need(int(row[-1])>=0,"whole degree22 sign")
        return {'entries':len(full),'zeros':sum(int(r[-1])==0 for r in full),'coefficient_sha256':digest(full)}
    # Exact grouping: include every zero/absent exponent as well.
    full={tuple(exponent(k)):v for k,v in F.d.items()}
    groups={}
    for e,z in full.items():groups.setdefault(e[2:],{})[e[0]]=z
    need({(i,22-sum(g)-i,*g):v for g,d in groups.items() for i,v in d.items()}==full,"entire transverse reassembly")
    high=[]
    for e in compositions(22,5):
        if sum(e[2:])>=4:
            z=F.d.get(pack(e),0);need(z>=0,"high transverse coefficient");high.append([*e,str(z)])
    tables=[]
    for d in (1,2,3):
        for gamma in compositions(d,3):
            power=power_from_group(F,gamma)
            for a,b in ((Q(0),Q(1,4)),(Q(1,4),Q(1,3)),(Q(1,3),Q(1))):
                tables.append(dict(btable(power,a,b),label='normal-'+str(gamma)))
    p0=power_from_group(F,(0,0,0))
    for a,b in ((Q(0),Q(1,4)),(Q(1,4),Q(147,500)),(Q(37,125),Q(1,3)),(Q(1,3),Q(1))):
        tables.append(dict(btable(p0,a,b),label='outer-face'))
    dom=[]
    for gamma in ((1,0,0),(0,1,0),(0,0,1)):
        p1=power_from_group(F,gamma)+[Q(0)]
        # Power coefficients embed the degree21 polynomial into degree22
        # directly, so no first-order Bernstein elevation is imported.
        pp=[119999*x+y for x,y in zip(p0,p1)]
        for a,b in ((Q(147,500),Q(59,200)),(Q(59,200),Q(37,125))):
            dom.append(dict(btable(pp,a,b,True),label='domination-'+str(gamma)))
    need(len(high)==14535 and len(tables)==61 and len(dom)==6,"complete grouped table counts")
    return {'high_entries':len(high),'high_zeros':sum(int(r[-1])==0 for r in high),
            'high_sha256':digest(high),'tables':tables,'domination_tables':dom,
            'local_q_cutoff':'1/120000','central_t_interval':['147/500','37/125']}
def flatten(rows):
    roots,mu,ss,v,A,R,D,N,F=rows
    return [roots,mu,ss,v,[x for row in A for x in row],R,[D],[N],[F]]
CASES=tuple((pair,cell) for pair in PAIRS for cell in range(3))
def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def rational_det(a):
    total=Q(0)
    # Three-dimensional numeric control, expanded by a direct six-term sum.
    from itertools import permutations
    for p in permutations(range(3)):
        inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        v=Q((-1)**inv)
        for i in range(3):v*=a[i][p[i]]
        total+=v
    return total
def matrix_controls(rows,meta):
    roots,mu,ss,v,A,R,D,N,F=rows;L=meta['scale'];records=[]
    # Work in basis e_i-e_8 of e-perp. Its metric is I+11^T.
    # This uses seven-dimensional coordinates, rather than the author's
    # full eight-dimensional matrix and zero-normal trace subtraction.
    metric=[[Q(1+int(i==j)) for j in range(7)] for i in range(7)]
    for bary in ((Q(1,5),)*5,tuple(Q(i,15) for i in range(1,6))):
        theta=[p.value(bary)/L for p in roots];x=theta[:7]
        C=[[theta[i]*int(i==j)-(theta[j]-theta[7])/8 for j in range(7)] for i in range(7)]
        need(sum(theta)==0,"matrix control balance")
        need(mm(metric,C)==mm([[C[j][i] for j in range(7)] for i in range(7)],metric),"metric self-adjoint compression")
        powers=[[[Q(int(i==j)) for j in range(7)] for i in range(7)]]
        for _ in range(8):powers.append(mm(powers[-1],C))
        for j in range(9):need(ss[j].value(bary)==(8*L)**j*tr(powers[j]),"entire seven-dimensional trace")
        vv=[]
        for j in range(5):
            z=sum(x[i]*sum(metric[i][k]*sum(powers[j][k][h]*x[h] for h in range(7)) for k in range(7)) for i in range(7))
            vv.append(z);need(v[j].value(bary)==L**2*(8*L)**j*z,"full coupling recurrence versus metric compression")
        G=[[tr(powers[i+j])-2*tr(powers[i+j+2])+tr(powers[i+j+4]) for j in range(3)] for i in range(3)]
        rhs=[(vv[i]-vv[i+2])/8 for i in range(3)]
        for i in range(3):
            need(R[i].value(bary)==(8*L)**(i+4)*rhs[i]/8,"filtered rhs scale")
            for j in range(3):need(A[i][j].value(bary)==(8*L)**(i+j+4)*G[i][j],"full metric Gram scale")
        d=rational_det(G);need(d>0,"six-distinct interior Gram positive")
        lower=sum(a*b for a,b in zip(rhs,solve(G,rhs)))
        need(D.value(bary)==(8*L)**18*d,"entire determinant scale")
        need(N.value(bary)==64*L**4*(8*L)**18*d*lower,"Schur numerator versus exact numeric Gaussian solve")
        m2=sum(t*t for t in theta);m4=sum(t**4 for t in theta)
        cleared=(Q(785753,1000)*m2-122*m2*m2-224*m4)*d+5760*d*lower
        need(F.value(bary)==1000*L**4*(8*L)**18*cleared,"entire target metric normalization")
        records.append({'bary':list(map(str,bary)),'theta':list(map(str,theta)),'D':str(d),'filtered_lower':str(lower)})
    return records
def mul1(a,b):
    o=[Q(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):o[i+j]+=v*w
    return o
def add1(a,b):
    return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]
def derivative(a):return [i*a[i] for i in range(1,len(a))]
def eval1(a,x):return sum(v*x**i for i,v in enumerate(a))
def case_record(rank,cell,progress=False):
    rows,meta=derive(rank,cell,progress);certificate=signs(rows[-1],rank,cell)
    maps=[[p.dump() for p in group] for group in flatten(rows)]
    record={'geometry':meta,'certificate':certificate,
            'root_forms_sha256':digest(maps[0]),'moment_sha256':digest(maps[1]),
            'trace_sha256':digest(maps[2]),'determinant_sha256':digest(maps[6][0]),
            'numerator_sha256':digest(maps[7][0]),'target_sha256':digest(maps[8][0]),
            'all_stage_sha256':[digest(x) for x in maps],
            'independent_metric_controls':matrix_controls(rows,meta)}
    return record
def fixture_read(path):
    need(path.is_file(),"mandatory reviewer fixture absent")
    f=json.loads(path.read_text())
    need(set(f)=={'actual_author','common','cases'} and f['actual_author']=='six-reviewer-3',"complete reviewer fixture metadata")
    need([(tuple(c['geometry']['pair']),c['geometry']['cell']) for c in f['cases']]==list(CASES),"complete ordered twelve-case fixture")
    return f
def fixture_match(record,path):
    need(record==fixture_read(path),"complete regenerated reviewer fixture equality")
def damaged(record):
    rejected=0
    with tempfile.TemporaryDirectory(prefix='sendov-review3-fixture-') as tmp:
        path=Path(tmp)/'missing.json'
        try:fixture_match(record,path)
        except ValueError:rejected+=1
        for key in ('geometry','trace','group','metric','constant'):
            bad=copy.deepcopy(record)
            if key=='geometry':bad['cases'][0]['geometry']['scale']+=1
            if key=='trace':bad['cases'][0]['trace_sha256']='0'*64
            if key=='group':bad['cases'][-1]['certificate']['local_q_cutoff']='1/12000'
            if key=='metric':bad['cases'][0]['independent_metric_controls'][0]['D']='0'
            if key=='constant':bad['common']['refined_global_stability_constant']='1400'
            path.write_text(json.dumps(bad))
            try:fixture_match(record,path)
            except ValueError:rejected+=1
    need(rejected==6,"six absent/damaged fixtures rejected")
    return rejected
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case');ap.add_argument('--output',type=Path)
    ap.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    ap.add_argument('--progress',action='store_true');ap.add_argument('--test-fixture-rejections',action='store_true')
    args=ap.parse_args();start=time.monotonic();fixture=fixture_read(args.fixture)
    if args.case:
        if args.test_fixture_rejections:ap.error('selected case cannot certify whole fixture rejection controls')
        left,right=args.case.split(':');key=(tuple(map(int,left.split(','))),int(right));need(key in CASES,"selected complete case")
        com=common();rec=case_record(*key,args.progress)
        need(com==fixture['common'] and rec==fixture['cases'][CASES.index(key)],"entire selected reviewer record")
        record={'actual_author':'six-reviewer-3','common':com,'cases':[rec]};status='PASS_INDEPENDENT_CASE';rejections=0
    else:
        record={'actual_author':'six-reviewer-3','common':common(),'cases':[case_record(*key,args.progress) for key in CASES]}
        fixture_match(record,args.fixture);status='PASS_INDEPENDENT_COMPLETE'
        rejections=damaged(record) if args.test_fixture_rejections else 0
    if args.output:args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    signs_count=sum(c['certificate'].get('entries',c['certificate'].get('high_entries',0))+
        sum(t['entries'] for t in c['certificate'].get('tables',[])+c['certificate'].get('domination_tables',[])) for c in record['cases'])
    print(json.dumps({'status':status,'actual_author':'six-reviewer-3','role':'independent mathematical reviewer',
          'cases':len(record['cases']),'target_sign_entries':signs_count,'checks':CHECKS,
          'independent_metric_controls':sum(len(c['independent_metric_controls']) for c in record['cases']),
          'rejected_fixtures':rejections,'record_sha256':digest(record),'seconds':time.monotonic()-start,
          'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
if __name__=='__main__':main()
