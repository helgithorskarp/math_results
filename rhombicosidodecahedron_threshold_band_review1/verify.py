"""Independent threshold branch audit by six-reviewer-1.
Q(sqrt(5)) arithmetic copied from own earlier independent axial census;
no author or solver code imported. Compact geometric fixture is untrusted.
"""
from fractions import Fraction as F
from functools import total_ordering, cmp_to_key
from itertools import combinations, permutations, product
from pathlib import Path
import copy, hashlib, json, sys

def need(ok,message):
    if not ok: raise ValueError(message)

@total_ordering
class Q:
    __slots__=('a','b')
    def __init__(self,a=0,b=0):self.a,self.b=F(a),F(b)
    @staticmethod
    def cast(x):return x if isinstance(x,Q) else Q(x)
    def __add__(self,x):
        x=Q.cast(x);return Q(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,x):return self+-Q.cast(x)
    def __rsub__(self,x):return Q.cast(x)+-self
    def __mul__(self,x):
        x=Q.cast(x);return Q(self.a*x.a+5*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Q.cast(x);n=x.a*x.a-5*x.b*x.b
        need(n!=0,'quadratic inverse zero')
        return self*Q(x.a/n,-x.b/n)
    def __rtruediv__(self,x):return Q.cast(x)/self
    def __eq__(self,x):
        try:x=Q.cast(x)
        except (TypeError,ValueError):return False
        return (self.a,self.b)==(x.a,x.b)
    def __hash__(self):return hash((self.a,self.b))
    def sign(self):
        a,b=self.a,self.b
        if not b:return (a>0)-(a<0)
        if not a:return (b>0)-(b<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        n=a*a-5*b*b
        need(n!=0,'irrational order separation')
        return ((a>0)-(a<0)) if n>0 else ((b>0)-(b<0))
    def __lt__(self,x):return (self-Q.cast(x)).sign()<0
    def __abs__(self):return self if self.sign()>=0 else -self
    def encode(self):return [str(self.a),str(self.b)]
    def __repr__(self):return '('+str(self.a)+')+('+str(self.b)+')sqrt5'

Z=Q();ONE=Q(1);PHI=Q(F(1,2),F(1,2));R2=7+8*PHI

def dot(x,y):return sum((a*b for a,b in zip(x,y)),Z)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,c):return tuple(a*c for a in x)
def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def det(M):return dot(M[0],cross(M[1],M[2]))
def mv(M,x):return tuple(dot(row,x) for row in M)
def encode(x):return [q.encode() for q in x]
def canonical(x):
    first=next((a.sign() for a in x if a!=Z),0)
    need(first!=0,'zero projective point')
    return x if first>0 else scale(x,-1)

def vertices():
    seeds=[(ONE,ONE,PHI*PHI*PHI),(PHI*PHI,PHI,2*PHI),(2+PHI,Z,PHI*PHI)]
    result=set()
    for seed in seeds:
        for s in range(3):
            q=seed[s:]+seed[:s]
            for signs in product([-1,1],repeat=3):result.add(tuple(x*t for x,t in zip(q,signs)))
    result=sorted(result)
    need(len(result)==60 and all(dot(x,x)==R2 for x in result),'RID vertex model/radii')
    need(all(scale(x,-1) in result for x in result),'central symmetry')
    return result

def decode(pair): return Q(F(pair[0]))+F(pair[1])*PHI
def vector(rows): return tuple(decode(row) for row in rows)
def project(v,m): return sub(v,scale(m,dot(v,m)/dot(m,m)))
def root(x):
    # Binary search on a fixed dyadic grid, testing exact quadratic-field squares.
    x=Q.cast(x);need(x>=0,'negative root');g=2**48;lo,hi=0,16*g
    need(Q(F(hi,g)**2)>x,'root range')
    while hi-lo>1:
        mid=(hi+lo)//2
        if Q(F(mid,g)**2)<=x:lo=mid
        else:hi=mid
    need(Q(F(lo,g)**2)<=x<Q(F(hi,g)**2),'outward root')
    return F(lo,g),F(hi,g)

BETA=(19-8*PHI)/29
D=F(42008277980669,1846406179243000)
REFS=[(Z,(2-PHI)/3,Q(-1)),(Z,ONE,(3*PHI-1)/11)]

def circular(points,m):
    ex=(ONE,Z,Z);ey=cross(m,ex)
    def compare(p,q):
        a,b=dot(p,ex),dot(p,ey);c,d=dot(q,ex),dot(q,ey)
        ah=0 if b>0 or (b==0 and a>=0) else 1
        ch=0 if d>0 or (d==0 and c>=0) else 1
        if ah!=ch:return ah-ch
        return -(a*d-b*c).sign()
    return sorted(points,key=cmp_to_key(compare))

def geometry(V,m):
    heights={v:dot(v,m)*dot(v,m)/dot(m,m) for v in V}
    need(min(heights.values())==BETA,'threshold minimum')
    active=sorted(v for v,h in heights.items() if h==BETA)
    need(len(active)==8,'eight original circle preimages')
    pos=[v for v in active if dot(v,m)>0]
    tangent=circular([project(v,m) for v in pos],m)
    need(len(tangent)==4,'positive tangent quadrilateral')
    distances=[]
    for a,b in zip(tangent,tangent[1:]+tangent[:1]):
        e=sub(b,a);ee=dot(e,e);t=-dot(a,e)/ee
        need(0<t<1,'interior disk contact')
        # Correct halfplane orientation, origin and all other corners on same side.
        side=dot(m,cross(e,scale(a,-1)))
        need(side!=0 and all(dot(m,cross(e,sub(p,a)))*side>=0 for p in tangent),'centered tangent hull')
        foot=add(a,scale(e,t));distances.append(dot(foot,foot))
    disk=min(distances);need(disk==(39+37*PHI)/29,'sharp threshold disk')
    cl,cu=root(BETA);rl,ru=root(disk);s=(cu-F(83,200))/rl
    zl,zu=root(1-s*s)
    need(F(1001,1000)**2*(1+zl)>2 and F(1001,1000)*s<D,'honest chord bound from independent roots')
    eta=cu*D+F(9,4)*D*D
    hl,hu=root(BETA+9*eta)
    need(BETA-F(83,200)**2+9*eta<F(2,5)**2,'radial candidate distance')
    eligible=sorted(v for v in V if heights[v]<=Q((hu+F(9,2)*D)**2))
    need(len(eligible)==(8 if m==REFS[0] else 12) and set(active)<=set(eligible),'complete original pool')
    eh=max(heights[v] for v in eligible);el,eu=root(eh)
    need(eh==(BETA if m==REFS[0] else (171-72*PHI)/145),'maximum eligible original height')
    flat=F(2,5)+eta+eu*D+F(9,4)*D*D
    circle=circular([project(v,m) for v in active],m)
    need(len(set(circle))==8 and all(dot(p,p)==R2-BETA for p in circle),'circle radii')
    gaps=[dot(sub(p,q),sub(p,q)) for p,q in combinations(circle,2)]
    need(min(gaps)>F(9,4) and F(3,2)-2*eta>F(4,5),'distinct candidate assignment')
    need(flat<F(9,20),'uniform planar candidate buffer')
    return {'m':m,'active':active,'positive':sorted(pos),'circle':circle,'eligible':eligible,
            'eta':eta,'flat':flat,'disk':disk,'max_height':eh}

def matching(data):
    m=data['m'];circle=data['circle']
    source=sorted({canonical(p) for p in circle})
    dest=sorted({canonical(project(v,m)) for v in data['eligible']})
    S=[p for a in source for p in (a,scale(a,-1))]
    T=[p for a in dest for p in (a,scale(a,-1))]
    pairs=list(combinations(range(8),2))
    sr={ij:root(dot(sub(S[ij[0]],S[ij[1]]),sub(S[ij[0]],S[ij[1]]))) for ij in pairs}
    tr={ij:root(dot(sub(T[ij[0]],T[ij[1]]),sub(T[ij[0]],T[ij[1]]))) for ij in combinations(range(len(T)),2)}
    survivors=[];total=0;best_rejected=None;stream=hashlib.sha256()
    for ids in permutations(range(len(dest)),4):
        for bits in product((0,1),repeat=4):
            total+=1;images=[2*j+t for j,bit in zip(ids,bits) for t in (bit,1-bit)]
            lower=[]
            for a,b in pairs:
                dl,du=tr[tuple(sorted((images[a],images[b])))];sl,su=sr[a,b]
                lower.append(max(sl-du,dl-su))
            gap=max(lower)
            # Deliberately weaker UNIFORM test, independent of the author's two tolerances.
            if gap<=F(26,25):
                maps={p:T[i] for p,i in zip(S,images)}
                shifts=[k for k in range(8) if all(maps[circle[i]]==circle[(i+k)%8] for i in range(8))]
                reversals=[k for k in range(8) if all(maps[circle[i]]==circle[(k-i)%8] for i in range(8))]
                need(set(maps.values())==set(circle),'noncircle metric survivor')
                need(len(shifts)+len(reversals)==1,'non-dihedral metric survivor')
                survivors.append({'shifts':shifts,'reversals':reversals})
            else:best_rejected=gap if best_rejected is None else min(gap,best_rejected)
            stream.update(json.dumps([ids,bits,str(gap)],separators=(',',':')).encode())
    need(total==(384 if len(dest)==4 else 5760),'complete signed injections')
    need(len(survivors)==4 and sorted(k for r in survivors for k in r['shifts'])==[0,4],'four survivors')
    need(best_rejected>F(26,25),'strict pair-distance buffer')
    return {'assignments':total,'uniform_pair_tolerance':'26/25','survivors':survivors,
            'minimum_rejected_max_pair_gap_lower':str(best_rejected),'full_assignment_stream_sha256':stream.hexdigest()}

def moment(data):
    m=data['m'];p=data['positive']
    weights=[(11+3*PHI)/58,(18-3*PHI)/58,(18-3*PHI)/58,(11+3*PHI)/58]
    need(sum(weights,Z)==1 and all(w>0 for w in weights),'positive moment weights')
    M=tuple(tuple(sum((w*v[i]*v[j] for w,v in zip(weights,p)),Z) for j in range(3)) for i in range(3))
    lx,lt=(49+45*PHI)/29,(135+195*PHI)/29
    need(mv(M,m)==scale(m,BETA),'normal eigenvector')
    need(mv(M,(ONE,Z,Z))==(lx,Z,Z),'x eigenvector')
    e=(Z,-m[2],m[1]);need(mv(M,e)==scale(e,lt),'tangent eigenvector')
    need(BETA<lx<lt and sum((M[i][i] for i in range(3)),Z)==R2,'moment spectrum')
    # Stronger rational full-chord coefficient, without changing the receiver domain.
    k=F(94,25);need(k*k*(BETA+lx)>4*lt,'improved moment chord coefficient')
    h=k*D;theta=F(101,100)*h
    need(h<F(1,10) and F(101,100)**2*F(399,400)>1,'arcsine branch')
    need(theta<F(9,100) and F(1,22)*(1-theta*theta/8)-theta/2>0,'full angle and Cayley gate')
    return {'matrix_sqrt5':[[q.encode() for q in r] for r in M],
            'proved_full_chord_coefficient':str(k),'full_spatial_angle_upper':str(theta)}

def bounds(path):
    x=y=F(-1);width=F(2)
    for ch in path:
        need(ch in '0123','path digit');width/=2;k=int(ch)
        if k&1:x+=width
        if k&2:y+=width
    return x,y,width

def tensor_from_values(values):
    # Independent Lagrange-to-Bernstein conversion at 0,1/2,1 in each variable.
    temp=[]
    for row in values:temp.append([row[0],2*row[1]-(row[0]+row[2])/2,row[2]])
    return [[temp[0][j],2*temp[1][j]-(temp[0][j]+temp[2][j])/2,temp[2][j]] for j in range(3)]

def interpolation_identities():
    bases=[(1,-2,1),(0,2,-2),(0,0,1)]
    nodes=(F(0),F(1,2),F(1))
    for a,b in product(range(3),repeat=2):
        bern=tensor_from_values([[s**a*t**b for t in nodes] for s in nodes])
        expanded=[[F(0) for _ in range(3)] for _ in range(3)]
        for j,i in product(range(3),repeat=2):
            for x,y in product(range(3),repeat=2):expanded[x][y]+=bern[j][i]*bases[i][x]*bases[j][y]
        need(all(expanded[x][y]==int((x,y)==(a,b)) for x,y in product(range(3),repeat=2)),'full interpolation identity')
    return 9

def cover(case,data,V):
    m=data['m'];z=1-D*D/2;alpha=F(17,16)*D/z;gamma=D/z
    need(dot(m,m)<F(17,16)**2 and z>0,'whole-cap rectangle')
    U=[add(m,add((Q(sx*alpha),Z,Z),scale((Z,-m[2],m[1]),sy*gamma)))
       for sx,sy in product((-1,1),repeat=2)]
    rows=[];supports=0
    need(len(case['contacts'])==16,'sixteen contacts')
    for c in case['contacts']:
        v=vector(c['original_vertex']);e=vector(c['original_edge'])
        need(v in V and (add(v,e) in V or sub(v,e) in V) and dot(e,e)==4,'actual original edge')
        corners=[]
        for u in U:
            mu=cross(e,u);H=dot(mu,v);torque=cross(v,mu)
            need(dot(mu,u)==0 and H>0,'outward nonzero support')
            need(all(dot(mu,sub(v,w))>=0 for w in V),'full original support');supports+=60
            corners.append((v,mu,H,torque))
        rows.append(corners)
    # Coverage by pairwise prefix incompatibility and exact total dyadic area.
    faces=case['faces'];need([(r['axis'],r['sign']) for r in faces]==list(product(range(3),(-1,1))),'signed faces')
    face_outputs=[];total_coeff=0
    for face in faces:
        leaves=face['leaves'];paths=[r[0] for r in leaves]
        need(len(set(paths))==len(paths),'distinct leaves')
        need(all(not a.startswith(b) and not b.startswith(a) for a,b in combinations(paths,2)),'prefix free')
        need(sum((F(1,4)**len(p) for p in paths),F(0))==1,'whole closed face')
        stream=hashlib.sha256();count=0
        for path,j,saved in leaves:
            need(type(j) is int and 0<=j<16 and len(path)<=4,'leaf schema')
            x,y,w=bounds(path)
            def least(a,b):return F(0) if a<=0<=b else min(a*a,b*b)
            n2=1+least(x,x+w)+least(y,y+w);ell=F(saved)
            need(ell>=1 and ell*ell<=n2,'outward face norm')
            axis=face['axis'];others=[i for i in range(3) if i!=axis]
            for v,mu,H,torque in rows[j]:
                def evaluate(s,t):
                    a=[Z,Z,Z];a[axis]=Q(face['sign']);a[others[0]]=Q(x+w*s);a[others[1]]=Q(y+w*t)
                    L=dot(torque,a);B=dot(v,a)*dot(mu,a)-H*dot(a,a)
                    return L,ell*L+F(1,22)*B
                affine=[evaluate(s,t)[0] for s,t in product((F(0),F(1)),repeat=2)]
                grid=[[evaluate(s,t)[1] for t in (F(0),F(1,2),F(1))] for s in (F(0),F(1,2),F(1))]
                bern=tensor_from_values(grid)
                need(all(q>0 for q in affine+[a for r in bern for a in r]),'strict complete coefficients')
                count+=13
                stream.update(json.dumps([q.encode() for q in affine+[a for r in bern for a in r]],separators=(',',':')).encode())
        total_coeff+=count
        face_outputs.append({'axis':face['axis'],'sign':face['sign'],'leaves':len(leaves),'coefficients':count,'independent_coefficient_stream_sha256':stream.hexdigest()})
    return {'faces':face_outputs,'strict_coefficients':total_coeff,'original_support_comparisons':supports}

def alignment(V,data):
    a=(2*PHI-1)/5;A=((Q(-1),Z,Z),(Z,a,-2*a),(Z,-2*a,-a))
    need(det(A)==1 and all(dot(A[i],A[j])==Q(i==j) for i in range(3) for j in range(3)),'proper alignment')
    need(mv(A,mv(A,REFS[0]))==REFS[0],'involution')
    need(dot(mv(A,REFS[0]),REFS[1])>0 and cross(mv(A,REFS[0]),REFS[1])==(Z,Z,Z),'positive reference transfer')
    need({mv(A,v) for v in data[0]['active']}==set(data[1]['active']),'complete circle transfer')
    need({mv(A,v) for v in V}!=set(V),'alignment not body symmetry')
    return A

def damaged_controls(case,data,V):
    mutations=[]
    def add_mutation(name,mutate):
        c=copy.deepcopy(case);mutate(c);mutations.append((name,c))
    add_mutation('missing_signed_face',lambda c:c['faces'].pop())
    add_mutation('missing_closed_leaf',lambda c:c['faces'][0]['leaves'].pop())
    add_mutation('duplicate_closed_leaf',lambda c:c['faces'][0]['leaves'].append(c['faces'][0]['leaves'][0]))
    add_mutation('overlapping_ancestor',lambda c:c['faces'][0]['leaves'].append(['',0,'1']))
    add_mutation('unknown_contact',lambda c:c['faces'][0]['leaves'][0].__setitem__(1,16))
    add_mutation('false_axis_norm',lambda c:c['faces'][0]['leaves'][0].__setitem__(2,'9'))
    add_mutation('nonoriginal_endpoint',lambda c:c['contacts'][0]['original_vertex'][0].__setitem__(0,'100'))
    add_mutation('nonoriginal_edge',lambda c:c['contacts'][0]['original_edge'][0].__setitem__(0,'100'))
    add_mutation('reversed_support',lambda c:c['contacts'][0].__setitem__('original_edge',[[str(-F(a)),str(-F(b))] for a,b in c['contacts'][0]['original_edge']]))
    rejected=[]
    for name,c in mutations:
        try:cover(c,data,V)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted damaged fixture '+name)
    return rejected

def check(fixture):
    V=vertices();cases=fixture['cases'];need(len(cases)==2,'two cases')
    data=[geometry(V,m) for m in REFS];A=alignment(V,data)
    result=[]
    for j,(case,row) in enumerate(zip(cases,data)):
        need(vector(case['reference'])==REFS[j],'reference identity')
        for c in case['contacts']:
            v=vector(c['original_vertex']);need(v in V and mv(A,v) in V,'both original class preimages')
        result.append({'case':j,'original_pool_size':len(row['eligible']),'noncircle_originals_sqrt5':[encode(v) for v in row['eligible'] if v not in row['active']],
                       'maximum_pool_height_squared_sqrt5':row['max_height'].encode(),
                       'independent_flat_match_upper':str(row['flat']),
                       'matching':matching(row),'moment':moment(row),'cover':cover(case,row,V)})
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','result':'PASS','threshold_cases':result,
            'full_tensor_interpolation_identities':interpolation_identities(),
            'rejected_corruptions':damaged_controls(cases[0],data[0],V),
            'complete_signed_assignments':sum(r['matching']['assignments'] for r in result),
            'closed_axis_leaves':sum(f['leaves'] for r in result for f in r['cover']['faces']),
            'strict_coefficients':sum(r['cover']['strict_coefficients'] for r in result),
            'original_support_comparisons':sum(r['cover']['original_support_comparisons'] for r in result),
            'normal_chord_bound':str(D),'target_global_verdict':'OUTSIDE_SCOPE: winning and two mixed branches not independently checked here'}

def main():
    here=Path(__file__).resolve().parent;fixture=json.loads((here/'fixture.json').read_text());result=check(fixture)
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if '--emit' in sys.argv:print(raw,end='')
    else:
        need(raw==(here/'expected.json').read_text(),'complete expected record')
        print(json.dumps({'result':'PASS','complete_signed_assignments':6144,'threshold_leaves':168,'strict_coefficients':8736,'sha256':hashlib.sha256(raw.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
