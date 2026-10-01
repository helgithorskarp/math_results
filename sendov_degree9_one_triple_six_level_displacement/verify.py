#!/usr/bin/env python3
"""Exact one-triple six-level degree-nine displacement certificate.
Actual author six-sendov-2, researcher, 2026-10-01.
Seven full homogeneous kernels, exact greedy section inverses and grouped signs.
Openly adapts the author's preceding filtered trace and full matrix arithmetic.
Ordinary proof and credited scalar/local/analytic inputs are not formalized.
"""
from fractions import Fraction as F
from math import comb, factorial, lcm
from itertools import combinations_with_replacement
from pathlib import Path
import argparse, hashlib, json
CHECKS=0
def require(ok,label):
    global CHECKS
    CHECKS+=1
    if not ok:raise ValueError(label)
class P:
    def __init__(self,value=0):
        if isinstance(value,P):value=value.t
        if isinstance(value,int):value={(0,0,0,0,0):value}
        self.t={e:int(c) for e,c in value.items() if c}
    def __add__(self,other):
        out=dict(self.t)
        for e,c in P(other).t.items():out[e]=out.get(e,0)+c
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({e:-c for e,c in self.t.items()})
    def __sub__(self,other):return self+-P(other)
    def __rsub__(self,other):return P(other)+-self
    def __mul__(self,other):
        out={}
        for e,c in self.t.items():
            for f,b in P(other).t.items():
                g=tuple(x+y for x,y in zip(e,f));out[g]=out.get(g,0)+c*b
        return P(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out*=self
        return out
    def __eq__(self,other):return self.t==P(other).t
    def dump(self):return [[*e,str(c)] for e,c in sorted(self.t.items())]
    def evaluate(self,values):
        # For rational x_j=u_j/b, a monomial of degree d equals
        # product(u_j**e_j)/b**d. Clear to the largest degree once;
        # this is the same evaluation for every integer polynomial.
        values=tuple(F(x) for x in values)
        if len(values)!=5:raise ValueError('five rational evaluation coordinates required')
        if not self.t:return F(0)
        denominator=lcm(*(x.denominator for x in values))
        numerators=[int(x*denominator) for x in values]
        degree=max(map(sum,self.t))
        powers=[[x**i for i in range(degree+1)] for x in numerators]
        cleared=sum(c*denominator**(degree-sum(e))*product(powers[j][i] for j,i in enumerate(e))
                    for e,c in self.t.items() if all(numerators[j] or not i for j,i in enumerate(e)))
        return F(cleared,denominator**degree)
def product(values):
    out=1
    for value in values:out*=value
    return out
V=[P({tuple(int(i==j) for j in range(5)):1}) for i in range(5)]
H=sum(V,P(0))
def compositions(n,k):
    if k==1:yield (n,);return
    for i in range(n+1):
        for rest in compositions(n-i,k-1):yield (i,*rest)
def trace_words(r):
    result={}
    for mask in range(1<<r):
        positions=[i for i in range(r) if mask>>i&1]
        if not positions:key=(r,);c=8**r
        else:
            key=tuple(sorted((positions[(i+1)%len(positions)]-p)%r or r for i,p in enumerate(positions)))
            c=(-1)**len(positions)*8**(r-len(positions))
        result[key]=result.get(key,0)+c
    return result
def adj3(g):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            a=[r for r in range(3) if r!=j];b=[c for c in range(3) if c!=i]
            row.append((-1)**(i+j)*(g[a[0]][b[0]]*g[a[1]][b[1]]-g[a[0]][b[1]]*g[a[1]][b[0]]))
        out.append(row)
    return out
def mm(a,b):
    return [[sum(a[i][h]*b[h][j] for h in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def independent_rows(rows):
    pivots={};selected=[]
    for original in rows:
        r=list(original)
        for j,b in sorted(pivots.items()):
            c=r[j]
            if c:r=[u-c*v for u,v in zip(r,b)]
        if any(r):
            j=next(j for j,v in enumerate(r) if v);c=r[j]
            pivots[j]=[v/c for v in r];selected.append(original)
    return selected
def solve(a,b):
    a=[list(r)+[v] for r,v in zip(a,b)];n=len(b)
    for j in range(n):
        pivots=[i for i in range(j,n) if a[i][j]]
        require(bool(pivots),'independent commutant nonzero pivot')
        i=pivots[0];a[j],a[i]=a[i],a[j];t=a[j][j]
        a[j]=[v/t for v in a[j]]
        for i in range(j+1,n):
            t=a[i][j]
            if t:a[i]=[u-t*v for u,v in zip(a[i],a[j])]
    x=[F(0)]*n
    for j in range(n-1,-1,-1):x[j]=a[j][-1]-sum(a[j][h]*x[h] for h in range(j+1,n))
    return x
def pinching(theta):
    # Adapted with attribution from the preceding author's defining
    # symmetric-commutant controls. It does not use any moment quotient.
    c=[[(theta[i] if i==j else F(0))-(theta[i]+theta[j])/8
        for j in range(8)] for i in range(8)]
    pairs=list(combinations_with_replacement(range(8),2))
    weights=[F(1 if i==j else 2) for i,j in pairs]
    ww=[theta[i]*theta[j]/8 for i,j in pairs];rows=[]
    for i in range(8):
        for j in range(i+1,8):
            row=[]
            for h,k in pairs:
                v=(c[i][h] if k==j else 0)-(c[k][j] if i==h else 0)
                if h!=k:v+=(c[i][k] if h==j else 0)-(c[h][j] if i==k else 0)
                row.append(v)
            rows.append(row)
    selected=independent_rows(rows)
    rhs=[sum(a*b for a,b in zip(row,ww)) for row in selected]
    gram=[[sum(a*b/g for a,b,g in zip(row,other,weights)) for other in selected] for row in selected]
    lam=solve(gram,rhs)
    projected=[v-sum(row[k]*b for row,b in zip(selected,lam))/weights[k] for k,v in enumerate(ww)]
    for row in rows:require(sum(a*b for a,b in zip(row,projected))==0,'full defining commutation equation')
    residual=[a-b for a,b in zip(ww,projected)]
    require(sum(g*a*b for g,a,b in zip(weights,projected,residual))==0,'defining Frobenius orthogonality')
    return sum(g*v*v for g,v in zip(weights,projected)),len(selected)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def univariate(poly):
    n=len(poly)-1;out=[F(0)]*(n+1)
    for i,c in enumerate(poly):
        for j in range(i,n+1):
            out[j]+=c*comb(n,i)*comb(n-i,j-i)*(-1)**(j-i)
    return out
def affine_power(poly,a,b):
    out=[F(0)]*len(poly)
    for i,c in enumerate(poly):
        for j in range(i+1):out[j]+=c*comb(i,j)*a**(i-j)*(b-a)**j
    return out
def power_to_bernstein(poly):
    n=len(poly)-1
    return [sum(poly[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
def certify_scalar(coefficients,a,b,label,strict=False):
    original=univariate(coefficients)
    transformed=affine_power(original,a,b)
    values=power_to_bernstein(transformed)
    require(univariate(values)==transformed,'complete scalar inverse '+label)
    for value in values:require(value>0 if strict else value>=0,'exact scalar sign '+label)
    return {'label':label,'interval':[str(a),str(b)],'degree':len(values)-1,
            'entries':len(values),'minimum':str(min(values)),
            'zeros':[i for i,v in enumerate(values) if not v],
            'coefficient_sha256':digest(list(map(str,values)))}
def j_value(u):
    return (2058+21912*u-15876*u*u+19224*u**3+3402*u**4)/((3+u)*(1+3*u)**2)
# This tail is assembled with the author's preceding public exact backend.
def section(rank):
    weights=[3 if i==rank else 1 for i in range(1,7)]
    cumulative=[sum(weights[:j]) for j in range(1,6)]
    vertices=[]
    for j,m in enumerate(cumulative):
        if m>=4:vertices.append(tuple(F(int(i==j)) for i in range(5)))
    for j in range(5):
        for h in range(j+1,5):
            if cumulative[j]<4<cumulative[h]:
                t=F(cumulative[j]*(cumulative[h]-4),4*(cumulative[h]-cumulative[j]))
                a=[F(0)]*5;a[j]=t;a[h]=1-t;vertices.append(tuple(a))
    return weights,cumulative,vertices
def levels_from_gaps(a,cumulative):
    gaps=[8*a[j]/cumulative[j] for j in range(5)]
    return tuple(1-sum(gaps[i:]) for i in range(5))+(F(1),)
def vertices_for(rank,cell):
    weights,cumulative,vertices=section(rank)
    if rank==5:
        require(cell==0 and len(vertices)==5,'rank-five simplex')
        return weights,cumulative,vertices
    require(rank in (1,2) and cell in (0,1,2),'triangulated ranks')
    def unit(j):return tuple(F(int(i==j)) for i in range(5))
    def clip(j):
        t=F(cumulative[0]*(cumulative[j]-4),4*(cumulative[j]-cumulative[0]))
        a=[F(0)]*5;a[0]=t;a[j]=1-t;return tuple(a)
    e2,e3,e4,e5=[unit(j) for j in range(1,5)]
    p3,p4,p5=[clip(j) for j in range(2,5)]
    cells=[(e2,e3,e4,e5,p5),(e2,e3,e4,p4,p5),(e2,e3,p3,p4,p5)]
    if rank==1:cells[2]=(e2,p3,e3,p4,p5)
    return weights,cumulative,list(cells[cell])
def greedy_coordinates(rank,cell,a):
    _,cumulative,_=section(rank)
    low=cumulative[0]
    eta=[F(low*(m-4),m*(4-low)) for m in cumulative[2:]]
    if cell==0:
        z=a[0]/eta[2]
        b=[a[1],a[2],a[3],a[4]-z,(1+eta[2])*z]
    elif cell==1:
        z=(a[0]-eta[2]*a[4])/eta[1]
        b=[a[1],a[2],a[3]-z,(1+eta[1])*z,(1+eta[2])*a[4]]
    else:
        z=(a[0]-eta[2]*a[4]-eta[1]*a[3])/eta[0]
        b=[a[1],a[2]-z,(1+eta[0])*z,(1+eta[1])*a[3],(1+eta[2])*a[4]]
        if rank==1:b=[b[0],b[2],b[1],b[3],b[4]]
    return b
def geometry(rank,cell):
    weights,cumulative,vertices=vertices_for(rank,cell)
    profiles=[levels_from_gaps(a,cumulative) for a in vertices]
    for a,x in zip(vertices,profiles):
        require(sum(a)==1 and all(t>=0 for t in a),'complete simplex vertex coordinates')
        require(sum(a[j]/cumulative[j] for j in range(5))<=F(1,4),'complete clipping condition')
        require(sum(m*t for m,t in zip(weights,x))==0,'literal weighted vertex balance')
        require(min(x)>=-1 and max(x)==1 and tuple(sorted(x))==x,'literal vertex unit bounds/order')
    matrix=[[vertices[j][i] for j in range(5)] for i in range(5)]
    inverse_columns=[solve(matrix,[F(int(i==j)) for i in range(5)]) for j in range(5)]
    inverse=[[inverse_columns[j][i] for j in range(5)] for i in range(5)]
    require(mm(matrix,inverse)==[[F(int(i==j)) for j in range(5)] for i in range(5)],'complete barycentric inverse matrix')
    if rank in (1,2):
        expected_columns=[greedy_coordinates(rank,cell,[F(int(i==j)) for i in range(5)]) for j in range(5)]
        expected=[[expected_columns[j][i] for j in range(5)] for i in range(5)]
        require(inverse==expected,'complete greedy inverse identity')
    for j in range(5):
        require([sum(inverse[i][h]*vertices[j][h] for h in range(5)) for i in range(5)]==[F(int(i==j)) for i in range(5)],'whole vertex roundtrip')
    scale=1
    from math import lcm
    for x in profiles:
        for t in x:scale=lcm(scale,t.denominator)
    return weights,cumulative,vertices,profiles,scale,inverse
def build_case(rank,cell):
    weights,cumulative,vertices,profiles,scale,inverse=geometry(rank,cell)
    levels=[sum((int(scale*profiles[j][i])*V[j] for j in range(5)),P(0)) for i in range(6)]
    roots=[levels[i] for i,m in enumerate(weights) for _ in range(m)]
    require(sum(roots,P(0))==0 and levels[-1]==scale*H,'complete balanced singleton-max forms')
    mu=[sum((t**r for t in roots),P(0)) for r in range(1,9)]
    traces=[P(7)]
    for r in range(1,9):traces.append(sum((c*product(mu[j-1] for j in word) for word,c in trace_words(r).items()),P(0)))
    m2,m3,m4,m5,m6=mu[1:6]
    base=[m2,8*m3,64*m4-8*m2**2,512*m5-128*m2*m3,4096*m6-512*(2*m2*m4+m3**2)+64*m2**3]
    z=(8*scale*H)**2
    gram=[[z*z*traces[i+j]-2*z*traces[i+j+2]+traces[i+j+4] for j in range(3)] for i in range(3)]
    rhs=[z*base[i]-base[i+2] for i in range(3)]
    adj=adj3(gram);d=sum((gram[0][j]*adj[j][0] for j in range(3)),P(0))
    n=sum((rhs[i]*adj[i][j]*rhs[j]*(1 if i==j else 2) for i in range(3) for j in range(i,3)),P(0))
    target=(785753*(scale*H)**2*m2-122000*m2**2-224000*m4)*d+90000*n
    for degree,poly in ((18,d),(22,n),(22,target)):
        require(all(sum(e)==degree for e in poly.t),'full homogeneous degree '+str(degree))
    return (roots,mu,traces,base,gram,rhs,d,n,target),{'rank':rank,'cell':cell,'scale':scale,'multiplicities':weights,'cumulative':cumulative,'gap_vertices':[[str(t) for t in a] for a in vertices],'level_vertices':[[str(t) for t in a] for a in profiles],'inverse_sha256':digest([[str(t) for t in row] for row in inverse])}
def complete_strict_signs(target):
    rows=[]
    for e in compositions(22,5):
        value=target.t.get(e,0);require(value>=0,'complete homogeneous strict-region coefficient')
        rows.append([*e,str(value)])
    return {'entries':len(rows),'zeros':sum(int(r[-1])==0 for r in rows),'coefficient_sha256':digest(rows)}
def grouped_signs(target):
    from collections import defaultdict
    groups=defaultdict(dict)
    for e,c in target.t.items():groups[e[2:]][e[0]]=c
    require({(i,22-sum(g)-i,*g):c for g,terms in groups.items() for i,c in terms.items()}==target.t,'complete grouped target reconstruction')
    high=[]
    for e in compositions(22,5):
        if sum(e[2:])>=4:
            value=target.t.get(e,0);require(value>=0,'complete high transverse coefficient')
            high.append([*e,str(value)])
    tables=[]
    for degree in (1,2,3):
        for gamma in compositions(degree,3):
            n=22-degree;coefficients=[F(groups[gamma].get(i,0),comb(n,i)) for i in range(n+1)]
            for a,b in ((F(0),F(1,4)),(F(1,4),F(1,3)),(F(1,3),F(1))):tables.append(certify_scalar(coefficients,a,b,'normal-'+str(gamma)))
    p0=[F(groups[(0,0,0)].get(i,0),comb(22,i)) for i in range(23)]
    for a,b in ((F(0),F(1,4)),(F(1,4),F(147,500)),(F(37,125),F(1,3)),(F(1,3),F(1))):tables.append(certify_scalar(p0,a,b,'outer-face'))
    domination=[]
    for gamma in ((1,0,0),(0,1,0),(0,0,1)):
        coeff=[F(groups[gamma].get(i,0),comb(21,i)) for i in range(22)]
        elevated=[F(22-i,22)*(coeff[i] if i<22 else 0)+F(i,22)*(coeff[i-1] if i else 0) for i in range(23)]
        require(univariate(elevated)==univariate(coeff)+[F(0)],'complete first-order degree elevation')
        for a,b in ((F(147,500),F(59,200)),(F(59,200),F(37,125))):domination.append(certify_scalar([119999*c+d for c,d in zip(p0,elevated)],a,b,'domination-'+str(gamma),True))
    require(F(6,5)/120000==F(1,100000),'all-balanced local total-deficit guard')
    require((F(119999,120000)*F(147,500))**2>=F(2,25),'all-balanced local lower scalar guard')
    require(F(37,125)**2<=F(9,100),'all-balanced local upper scalar guard')
    return {'high_entries':len(high),'high_zeros':sum(int(r[-1])==0 for r in high),'high_sha256':digest(high),'tables':tables,'domination_tables':domination,'local_q_cutoff':'1/120000','central_t_interval':['147/500','37/125']}

def full_controls(rank,cell,rows,meta):
    roots,mu,traces,base,gram,rhs,d,n,target=rows;scale=meta['scale'];big=8*scale
    profiles=[tuple(F(int(i==j)) for i in range(5)) for j in range(5)]
    profiles.append((F(1,5),)*5)
    grouped=(rank==1 and cell==2)
    if grouped:
        t=F(59,200)
        for q in (F(0),F(1,240000),F(1,120000),F(1,60000)):
            profiles.append(((1-q)*t,(1-q)*(1-t),q/3,q/3,q/3))
    records=[]
    for bary in profiles:
        require(sum(bary)==1 and all(a>=0 for a in bary),'full control barycentric domain')
        theta=[p.evaluate(bary)/scale for p in roots]
        require(sum(theta)==0 and max(map(abs,theta))==1,'full control physical normalization')
        moments=[sum(t**r for t in theta) for r in range(1,9)]
        for r in range(1,9):require(mu[r-1].evaluate(bary)==scale**r*moments[r-1],'full control scaled moment')
        c=[[(theta[i] if i==j else F(0))-(theta[i]+theta[j])/8 for j in range(8)] for i in range(8)]
        ww=[[theta[i]*theta[j]/8 for j in range(8)] for i in range(8)]
        identity=[[F(int(i==j)) for j in range(8)] for i in range(8)]
        powers=[identity]
        for r in range(1,9):powers.append(mm(powers[-1],c))
        ss=[F(7)]+[tr(powers[r]) for r in range(1,9)]
        for r in range(1,9):require(traces[r].evaluate(bary)==big**r*ss[r],'full trace versus cyclic words')
        bb=[tr(mm(ww,powers[r])) for r in range(5)]
        for r in range(5):require(base[r].evaluate(bary)==8*scale**2*big**r*bb[r],'full coupling numerator scale')
        matrices=[[[powers[r][i][j]-powers[r+2][i][j] for j in range(8)] for i in range(8)] for r in range(3)]
        gg=[[tr(mm(matrices[i],matrices[j]))-F(int(i==j==0)) for j in range(3)] for i in range(3)]
        rr=[tr(mm(ww,p)) for p in matrices]
        for i in range(3):
            require(rhs[i].evaluate(bary)==F(big**(i+4),8)*rr[i],'full filtered rhs scaling')
            for j in range(3):require(gram[i][j].evaluate(bary)==big**(i+j+4)*gg[i][j],'full filtered Gram scaling')
        det=gg[0][0]*(gg[1][1]*gg[2][2]-gg[1][2]*gg[2][1])-gg[0][1]*(gg[1][0]*gg[2][2]-gg[1][2]*gg[2][0])+gg[0][2]*(gg[1][0]*gg[2][1]-gg[1][1]*gg[2][0])
        require(d.evaluate(bary)==big**18*det,'full determinant scaling')
        psi,commutant_rank=pinching(theta)
        actual=122*moments[1]+(224*moments[3]-5760*psi)/moments[1]
        lower=None
        if det:
            require(det>0,'full control positive nonsingular Gram')
            solution=solve(gg,rr);lower=sum(a*b for a,b in zip(rr,solution))
            require(n.evaluate(bary)==64*scale**4*big**18*det*lower,'full adjugate numerator versus Gaussian solve')
            require(lower<=psi,'full commutant versus filtered projection')
            cleared=(F(785753,1000)*moments[1]-122*moments[1]**2-224*moments[3])*det+5760*det*lower
            require(target.evaluate(bary)==1000*scale**4*big**18*cleared,'entire strict target normalization')
        else:
            require(n.evaluate(bary)==0 and target.evaluate(bary)==0,'singular cleared numerators without division')
        local=False;normal=None;x=None
        if grouped:
            # Expanded order is negative triple, two middles, upper triple.
            minus=[1+t for t in theta[:3]];plus=[1-t for t in theta[5:]]
            normal=sum(minus+plus);x=(theta[4]-theta[3])/2;q=sum(bary[2:])
            require(all(t>=0 for t in minus+plus),'physical two-sided deficits')
            require(normal==F(6,5)*bary[2]+F(2,3)*bary[3]+bary[4] and x==bary[0],'full two-sided local chart mapping')
            local=(q<=F(1,120000) and F(147,500)<=bary[0]/(1-q)<=F(37,125))
            if local:
                require(normal<=F(1,100000) and F(2,25)<=x*x<=F(9,100),'all-balanced local physical guard')
                require(actual<=j_value(x*x)-200*normal,'full defining local loss control')
        if not local:require(actual<=F(785753,1000),'full defining strict-region inequality')
        records.append({'bary':list(map(str,bary)),'theta':list(map(str,theta)),
                        'D':str(det),'Psi':str(psi),'J':str(actual),
                        'filtered_lower':str(lower) if lower is not None else None,
                        'commutant_rank':commutant_rank,'branch':'local' if local else 'strict',
                        'total_deficit':str(normal) if normal is not None else None,
                        'singleton_half_difference':str(x) if x is not None else None})
    return records

def moment_sections():
    records=[]
    for rank in range(1,6):
        weights,cumulative,vertices=section(rank);values=[]
        for a in vertices:
            levels=levels_from_gaps(a,cumulative)
            require(sum(a)==1 and all(t>=0 for t in a),'complete ordered-polytope vertex')
            require(sum(a[j]/cumulative[j] for j in range(5))<=F(1,4),'complete vertex clipping plane')
            require(sum(m*t for m,t in zip(weights,levels))==0 and min(levels)>=-1 and max(levels)==1,'complete vertex physical normalization')
            value=sum(m*t*t for m,t in zip(weights,levels));values.append(value)
            if rank in (3,4):require(value<=F(16,3),'complete middle-rank moment vertex bound')
        require(len(vertices)==[7,7,9,8,5][rank-1],'complete derived polytope vertex count')
        records.append({'rank':rank,'multiplicities':weights,'cumulative':cumulative,
                        'vertices':[[str(t) for t in a] for a in vertices],
                        'vertex_mu2':list(map(str,values)),'max_mu2':str(max(values))})
    require(F(122)-F(5760,64*5)==104,'five-dimensional block-support moment coefficient')
    require(104*F(16,3)+224==F(2336,3)<F(785753,1000),'entire middle-rank strict bound')
    require(j_value(F(87,1000))-F(785753,1000)>F(1,1250),'credited scalar strict global margin')
    require(F(13,8)**4/F(10985,33554432)==F(106496,5),'credited original-root basin scaling')
    return records

CASE_ORDER=((5,0),(2,0),(2,1),(2,2),(1,0),(1,1),(1,2))
def common_record(sections):
    return {'normalization':'balanced max norm1; all at-most-five levels or six levels3+1^5',
            'threshold':'785753/1000','homogeneous_degree':22,'ordered_sections':sections}
def derive_case(rank,cell,progress=False):
    import sys,time
    start=time.monotonic()
    def stage(label):
        if progress:print(json.dumps({'case':[rank,cell],'stage':label,'seconds':time.monotonic()-start}),file=sys.stderr,flush=True)
    rows,meta=build_case(rank,cell);stage('full_integer_kernel_rebuilt')
    certificate=grouped_signs(rows[8]) if (rank,cell)==(1,2) else complete_strict_signs(rows[8])
    stage('every_target_sign_checked')
    controls=full_controls(rank,cell,rows,meta);stage('all_full_definition_controls_checked')
    return {'geometry':meta,'certificate':certificate,'full_controls':controls,
            'root_forms_sha256':digest([p.dump() for p in rows[0]]),
            'moment_sha256':digest([p.dump() for p in rows[1]]),
            'trace_sha256':digest([p.dump() for p in rows[2]]),
            'determinant_sha256':digest(rows[6].dump()),
            'numerator_sha256':digest(rows[7].dump()),'target_sha256':digest(rows[8].dump())}
def derive(progress=False):
    sections=moment_sections()
    cases=[derive_case(rank,cell,progress) for rank,cell in CASE_ORDER]
    return dict(common_record(sections),cases=cases,checks_before_manifest=CHECKS)

def verify_manifest(record,path):
    require(path.is_file(),'mandatory compact manifest absent')
    require(record==json.loads(path.read_text()),'entire regenerated manifest equality')

def verify_case(rank,cell,path,progress=False):
    common=common_record(moment_sections());common_checks=CHECKS
    case=derive_case(rank,cell,progress);case_checks=CHECKS-common_checks
    require(path.is_file(),'mandatory compact manifest absent')
    fixture=json.loads(path.read_text())
    require(set(fixture)==set(common)|{'cases','checks_before_manifest'},'complete mandatory fixture fields')
    require([(x['geometry']['rank'],x['geometry']['cell']) for x in fixture['cases']]==list(CASE_ORDER),'complete ordered fixture case identifiers')
    require(common=={k:fixture[k] for k in common},'entire regenerated common section/metadata record equality')
    require(case==fixture['cases'][CASE_ORDER.index((rank,cell))],'entire regenerated selected-case record equality')
    return {'status':'PASS_CASE','case':[rank,cell],'common':common,'record':case,
            'common_mathematical_checks':common_checks,'case_mathematical_checks':case_checks,
            'kernel_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def collect_cases(paths,manifest):
    # This audits the complete union of existing case records. It does
    # not rederive their mathematics or authenticate an external run log.
    require(len(paths)==len(CASE_ORDER),'exactly seven selected-case records required')
    require(manifest.is_file(),'mandatory compact manifest absent')
    kernel_hash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest_hash=hashlib.sha256(manifest.read_bytes()).hexdigest()
    rows=[json.loads(path.read_text()) for path in paths]
    require({tuple(row['case']) for row in rows}==set(CASE_ORDER),'complete unique case coverage')
    indexed={tuple(row['case']):row for row in rows}
    common=rows[0]['common'];common_checks=rows[0]['common_mathematical_checks']
    cases=[];mathematical_checks=common_checks
    for key in CASE_ORDER:
        row=indexed[key]
        require(row['status']=='PASS_CASE','selected-case successful status')
        require(row['kernel_sha256']==kernel_hash,'same source executable for every selected case')
        require(row['manifest_sha256']==manifest_hash,'same required fixture for every selected case')
        require(row['common']==common and row['common_mathematical_checks']==common_checks,'entire common record and check-count agreement')
        require((row['record']['geometry']['rank'],row['record']['geometry']['cell'])==key,'exact record case identifier')
        require(isinstance(row['case_mathematical_checks'],int) and row['case_mathematical_checks']>0,'positive mathematical case count')
        cases.append(row['record']);mathematical_checks+=row['case_mathematical_checks']
    record=dict(common,cases=cases,checks_before_manifest=mathematical_checks)
    verify_manifest(record,manifest)
    return record

def damaged_manifest_controls(record):
    import copy,tempfile
    rejected=0
    with tempfile.TemporaryDirectory(prefix='sendov-one-triple-manifest-') as directory:
        path=Path(directory)/'fixture.json'
        try:verify_manifest(record,path)
        except ValueError:rejected+=1
        for target in ('sign','geometry','local','pinching'):
            damaged=copy.deepcopy(record)
            if target=='sign':damaged['cases'][0]['certificate']['coefficient_sha256']='0'*64
            elif target=='geometry':damaged['cases'][0]['geometry']['gap_vertices'][0][0]='1'
            elif target=='local':damaged['cases'][-1]['certificate']['local_q_cutoff']='1/12000'
            else:damaged['cases'][0]['full_controls'][0]['Psi']='0'
            path.write_text(json.dumps(damaged))
            try:verify_manifest(record,path)
            except ValueError:rejected+=1
    require(rejected==5,'five missing/damaged fixture cases rejected')
    return rejected

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',type=Path)
    parser.add_argument('--progress',action='store_true')
    parser.add_argument('--test-manifest-rejections',action='store_true')
    parser.add_argument('--case',help='rederive one case R:C; returns PASS_CASE only')
    parser.add_argument('--write-case',type=Path,help='save the complete freshly verified selected-case record')
    parser.add_argument('--collect-cases',type=Path,nargs='+',help='audit seven saved case records; does not rederive mathematics')
    args=parser.parse_args()
    if args.case:
        if args.write_manifest or args.collect_cases or args.test_manifest_rejections:parser.error('selected case cannot emit/collect a whole manifest or test its whole rejection gate')
        try:key=tuple(map(int,args.case.split(':')))
        except ValueError:parser.error('case must be R:C')
        if key not in CASE_ORDER:parser.error('case is not one of the seven complete kernels')
        if args.write_case and args.write_case.resolve()==args.manifest.resolve():parser.error('case output must not overwrite the mandatory fixture')
        payload=verify_case(*key,args.manifest,args.progress)
        if args.write_case:args.write_case.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
        print(json.dumps({'status':'PASS_CASE','case':list(key),'checks':CHECKS,
                          'common_mathematical_checks':payload['common_mathematical_checks'],
                          'case_mathematical_checks':payload['case_mathematical_checks'],
                          'full_definition_controls':len(payload['record']['full_controls']),
                          'case_record_sha256':digest(payload['record']),
                          'kernel_sha256':payload['kernel_sha256'],
                          'manifest_sha256':payload['manifest_sha256']},sort_keys=True))
        return
    if args.write_case:parser.error('--write-case requires --case')
    if args.collect_cases:
        if args.write_manifest:parser.error('record collection is not author regeneration')
        record=collect_cases(args.collect_cases,args.manifest);status='PASS_RECORD_UNION'
    else:
        record=derive(args.progress)
        if args.write_manifest:
            args.write_manifest.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');status='AUTHOR_MANIFEST_REGENERATED'
        else:verify_manifest(record,args.manifest);status='PASS'
    rejected=damaged_manifest_controls(record) if args.test_manifest_rejections else 0
    grouped=record['cases'][-1]['certificate']
    signs=sum(row['certificate']['entries'] for row in record['cases'][:-1])+grouped['high_entries']+sum(row['entries'] for row in grouped['tables']+grouped['domination_tables'])
    print(json.dumps({'status':status,'checks':CHECKS,'target_sign_entries':signs,
                      'mathematical_checks':record['checks_before_manifest'],
                      'simplex_kernels':len(record['cases']),'scalar_tables':len(grouped['tables']),
                      'domination_tables':len(grouped['domination_tables']),
                      'full_definition_controls':sum(len(row['full_controls']) for row in record['cases']),
                      'polytope_vertices':sum(len(row['vertices']) for row in record['ordered_sections']),
                      'rejected_fixture_cases':rejected,'canonical_record_sha256':digest(record)},sort_keys=True))
if __name__=='__main__':main()
