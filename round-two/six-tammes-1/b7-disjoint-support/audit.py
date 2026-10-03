"""Same-author separate sparse/Taylor auditor; no producer or dense import.

Sparse arithmetic/face propagation credit: author's9972 audit source. New Gram
coefficients are collected bivariately, resultants use Sylvester/Bareiss, and
positive signs use rational Taylor bounds, not producer Bernstein coefficients.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import permutations,combinations,product
from collections import defaultdict
from hashlib import sha256
from math import gcd
from functools import lru_cache
import argparse,json

LO,HI=F(7,10),F(3,4)
PARENT_SHA='a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
A=((0,5,11),(0,6,11),(0,5,7),(5,9,11))
B=((1,2,4),(2,4,8),(1,2,10),(1,10,12))
NEW=(20,21,22)
ROOT_CELLS={16:(F(1891,2560),F(60513,81920)),17:(F(30493,40960),F(60987,81920))}


def require(ok,why):
    if not ok:raise ValueError(why)


def P(*c):return {i:F(x) for i,x in enumerate(c) if x}
def plus(*ps):
    answer=defaultdict(F)
    for p in ps:
        for i,v in p.items():answer[i]+=v
    return {i:v for i,v in answer.items() if v}
def scale(p,c):return {i:v*c for i,v in p.items() if v*c}
def times(p,q):
    answer=defaultdict(F)
    for i,v in p.items():
        for j,w in q.items():answer[i+j]+=v*w
    return {i:v for i,v in answer.items() if v}
def serial(p):return [str(p.get(i,F(0))) for i in range(max(p,default=-1)+1)]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canonical(x).encode()).hexdigest()


def compare_frozen(data,reference):
    """Controls only: both primary arithmetic baselines must already pass."""
    require(canonical(data)==canonical(reference),'entire typed projection of a freshly audited reference')


R,D,Q,H=P(0,1),P(2,-1),P(0,-3,2,2),P(-2,2,1)
FACTORS=(R,D,P(1,-1),P(1,1),P(2,1),P(-1,2),P(1,2))


def quotient(p,q):
    require(q,'nonzero polynomial divisor');remainder=dict(p);answer={};degree=max(q)
    while remainder and max(remainder)>=degree:
        i=max(remainder)-degree;c=remainder[max(remainder)]/q[degree]
        answer[i]=answer.get(i,F(0))+c
        remainder=plus(remainder,{j+i:-c*v for j,v in q.items()})
    answer={i:v for i,v in answer.items() if v}
    require(plus(times(answer,q),remainder)==p,'entire sparse division identity')
    return answer,remainder


def primitive(p):
    if not p:return {}
    den=1
    for v in p.values():den=den*v.denominator//gcd(den,v.denominator)
    integer={i:int(v*den) for i,v in p.items()};content=0
    for v in integer.values():content=gcd(content,abs(v))
    return {i:F(v//content) for i,v in integer.items()}


@lru_cache(maxsize=None)
def stripped_cached(code):
    p={i:F(v) for i,v in enumerate(code) if F(v)};removed=[]
    if not p:return (),()
    for f in FACTORS:
        count=0
        while p and max(p)>=max(f):
            q,r=quotient(p,f)
            if r:break
            p=q;count+=1
        if count:removed.append((tuple(serial(f)),count))
    p=primitive(p)
    return tuple(serial(p)),tuple(removed)


def strip(p):
    code,removed=stripped_cached(tuple(serial(p)))
    return {i:F(v) for i,v in enumerate(code) if F(v)},[[list(f),n] for f,n in removed]


def value(p,x):
    y=F(0)
    for i in range(max(p,default=-1),-1,-1):y=y*x+p.get(i,0)
    return y


@lru_cache(maxsize=None)
def positive_cached(code,lo,hi,depth=0):
    p={i:F(v) for i,v in enumerate(code) if F(v)}
    if not p or value(p,lo)<=0 or value(p,hi)<=0:return False
    center=(lo+hi)/2;radius=(hi-lo)/2;expansion={}
    for i in range(max(p),-1,-1):expansion=plus(times(expansion,P(center,radius)),P(p.get(i,0)))
    if expansion.get(0,0)>sum(abs(v) for i,v in expansion.items() if i):return True
    if depth>=18:return False
    middle=(lo+hi)/2
    return positive_cached(code,lo,middle,depth+1) and positive_cached(code,middle,hi,depth+1)


def positive(p,lo=LO,hi=HI):
    p,_=strip(p)
    return positive_cached(tuple(serial(p)),lo,hi)


def signed(p,s,lo=LO,hi=HI):
    require(type(s) is int and s in (-1,1),'explicit signed nonzero obligation')
    require(positive(scale(p,s),lo,hi),'complete rational Taylor positive cover')
    return s


def gram(v,w):
    answer={}
    for i in range(3):
        for j in range(3):answer=plus(answer,times(D if i==j else R,times(v[i],w[j])))
    return answer


def reflected(u,v,w):return tuple(plus(times(R,plus(a,b)),scale(c,-1)) for a,b,c in zip(u,v,w))


def points(ts):
    root=(1,2,4);p={1:(P(1),P(),P()),2:(P(),P(1),P()),4:(P(),P(),P(1))}
    done={root};remaining=set(map(tuple,ts))-{root}
    while remaining:
        progress=False
        for t in sorted(remaining):
            parents=[u for u in done if len(set(t)&set(u))==2]
            if not parents:continue
            require(len(parents)==1,'complete original triangle tree')
            e=sorted(set(t)&set(parents[0]));new=next(v for v in t if v not in e);old=next(v for v in parents[0] if v not in e)
            require(new not in p,'fresh parent corner propagation')
            p[new]=reflected(p[e[0]],p[e[1]],p[old]);done.add(t);remaining.remove(t);progress=True;break
        require(progress,'entire face propagation completes')
    require(len(p)==len(ts)+2 and all(gram(v,v)==D for v in p.values()),'whole unit-coordinate table')
    for t in ts:
        for i,j in combinations(t,2):require(gram(p[i],p[j])==R,'every triangle contact')
    return p


def base():return points(B)


def determinant(matrix):
    m=[[dict(p) for p in row] for row in matrix];n=len(m);previous=P(1);sgn=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if m[i][k]),None)
        if pivot is None:return {}
        if pivot!=k:m[k],m[pivot]=m[pivot],m[k];sgn=-sgn
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=plus(times(m[k][k],m[i][j]),scale(times(m[i][k],m[k][j]),-1))
                m[i][j],rem=quotient(numerator,previous);require(not rem,'every Bareiss division exact')
        previous=m[k][k]
        for i in range(k+1,n):m[i][k]={}
    return scale(m[-1][-1],sgn)


def expanded_det(matrix):
    n=len(matrix);answer={}
    for perm in permutations(range(n)):
        term=P(-1 if sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2 else 1)
        for i,j in enumerate(perm):term=times(term,matrix[i][j])
        answer=plus(answer,term)
    return answer


def quadratic_direct(matrix):
    # The marker None is X. Collect a bivariate determinant coefficient-wise.
    n=len(matrix);answer=defaultdict(F)
    for perm in permutations(range(n)):
        term={(0,0):F(-1 if sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2 else 1)}
        for i,j in enumerate(perm):
            entry={(0,1):F(1)} if matrix[i][j] is None else {(k,0):v for k,v in matrix[i][j].items()}
            product_=defaultdict(F)
            for (a,b),v in term.items():
                for (c,d),w in entry.items():product_[a+c,b+d]+=v*w
            term={key:v for key,v in product_.items() if v}
        for key,v in term.items():answer[key]+=v
    require(all(j<=2 for (i,j),v in answer.items() if v),'entire deg_X<=2 Gram determinant')
    return tuple({i:v for (i,j),v in answer.items() if j==power and v} for power in (2,1,0))


def resultant(a,b):
    p,q,r=a;s,t,u=b;zero={}
    return determinant([[p,q,r,zero],[zero,p,q,r],[s,t,u,zero],[zero,s,t,u]])


def hrow(v):
    return tuple(plus(*(times(D if i==j else R,v[j]) for j in range(3))) for i in range(3))


def cramer(m,rhs):
    d=expanded_det(m);n=[]
    for j in range(3):n.append(expanded_det([[rhs[i] if k==j else m[i][k] for k in range(3)] for i in range(3)]))
    require(all(plus(*(times(m[i][j],n[j]) for j in range(3)))==times(d,rhs[i]) for i in range(3)),'entire independently expanded Cramer rows')
    return tuple(n),d


def mod_h(p):return quotient(p,H)[1]
def inverse_h(p):
    p=mod_h(p);a=p.get(0,F(0));b=p.get(1,F(0));norm=a*a-2*a*b-2*b*b
    require(norm!=0,'nonzero exact quadratic norm');inv=P((a-2*b)/norm,-b/norm)
    require(mod_h(times(p,inv))==P(1),'full field inverse coefficient identity')
    return inv


def group_cases(x):
    tables={};all_groups={}
    for number,row in enumerate(x['overlap_rows']):
        occupied=[v for v in row[1:] if v!=-1]
        if not occupied:continue
        require(len(occupied)==1 and occupied[0] in (6,7,9),'parent full one-overlap case')
        if row[0] not in tables:tables[row[0]]=points(x['all_shapes'][row[0]])
        ear=occupied[0];label=NEW[row[1:].index(ear)];coordinate=tables[row[0]][label]
        key=(ear,tuple(tuple(F(v) for v in serial(p)) for p in coordinate))
        all_groups.setdefault(key,[]).append(number)
    groups=[{'ear':ear,'coordinate':tuple({i:v for i,v in enumerate(p) if v} for p in coordinate),'rows':rows} for (ear,coordinate),rows in sorted(all_groups.items())]
    require(len(groups)==25 and sum(len(g['rows']) for g in groups)==106,'all complete physical assignments')
    require([sum(g['ear']==ear for g in groups) for ear in (6,7,9)]==[20,3,2],'all reuse anchors without packing quotient')
    return groups,tables


def leaves_cover(leaves,lo,hi,check_leaf):
    paths=[];rebuilt=[]
    for leaf in leaves:
        path=leaf['path'];require(type(path) is str and all(c in '01' for c in path) and len(path)<=18,'finite binary cover path')
        a,b=lo,hi
        for c in path:
            mid=(a+b)/2
            if c=='0':b=mid
            else:a=mid
        record=check_leaf(leaf,a,b);record['path']=path;record['interval']=[str(a),str(b)]
        paths.append(path);rebuilt.append(record)
    require(len(set(paths))==len(paths),'no repeated cover leaf')
    require(all(not b.startswith(a) for a in paths for b in paths if a!=b),'prefix-free parameter leaves')
    require(sum(F(1,2**len(p)) for p in paths)==1,'complete closed parameter cover')
    return rebuilt


def shared6(g,index,bp,record):
    s=g['coordinate'];K,L=gram(s,bp[12]),gram(s,bp[10])
    first=quadratic_direct([[D,Q,Q,K],[Q,D,Q,R],[Q,Q,D,None],[K,R,None,D]])
    second=quadratic_direct([[D,L,K,Q],[L,D,R,R],[K,R,D,None],[Q,R,None,D]])
    raw=resultant(first,second);reduced,removed=strip(raw)
    out={'anchor':index,'ear':6,'coordinate':[serial(p) for p in s],'rows':g['rows'],'Gram_quadratics':[[serial(p) for p in first],[serial(p) for p in second]],'resultant':serial(reduced),'removed_positive_factors':removed}
    method=record['method'];out['method']=method
    if method=='nonzero_resultant':
        out['sign']=signed(reduced,record['sign']);return out
    a,b,c=first;d,e,f=second
    ell=plus(times(d,b),scale(times(a,e),-1));num=plus(times(a,f),scale(times(d,c),-1))
    C=[hrow(s),hrow(bp[10]),hrow(bp[12])]
    nv,dv0=cramer(C,[times(Q,ell),times(R,ell),num]);dv=times(dv0,ell)
    out.update(common_root_linear_sign=signed(ell,record['common_root_linear_sign']),basis_sign=signed(dv0,record['basis_sign']),whole_forced_v_digest=digest([[serial(p) for p in nv],serial(dv)]))
    if method=='continuous_core_alias':
        require(not raw,'identically zero resultant retained without an exclusion')
        aliases=[k for k,p in base().items() if all(not plus(nv[i],scale(times(dv,p[i]),-1)) for i in range(3))]
        require(len(aliases)==1,'exact entire continuous alias');out['alias']=[9,aliases[0]];return out
    if method=='quadratic_core_alias':
        cofactor,rem=quotient(reduced,H);require(not rem,'entire exceptional quadratic factor')
        out['cofactor_sign']=signed(cofactor,record['cofactor_sign'])
        aliases=[k for k,p in base().items() if all(not mod_h(plus(nv[i],scale(times(dv,p[i]),-1))) for i in range(3))]
        if aliases:out['alias']=[9,aliases[0]];return out
        iv=inverse_h(dv);v=tuple(mod_h(times(p,iv)) for p in nv);sf=tuple(mod_h(p) for p in s)
        nu,du=cramer([hrow(sf),hrow(v),hrow(bp[12])],[Q,Q,R]);iu=inverse_h(du);u=tuple(mod_h(times(p,iu)) for p in nu)
        aliases=[k for k,p in base().items() if all(not mod_h(plus(u[i],scale(p[i],-1))) for i in range(3))]
        require(len(aliases)==1,'exact quadratic p7 alias');out.update(alias=[7,aliases[0]],quadratic_u_inverse_digest=digest([serial(mod_h(du)),serial(iu)]));return out
    require(method=='isolated_packing' and index in ROOT_CELLS,'only complete remaining root-cell case')
    lo,hi=ROOT_CELLS[index];out['cell']=[str(lo),str(hi)]
    def nz(leaf,a,b):return {'sign':signed(reduced,leaf['sign'],a,b)}
    out['outside_covers']=[leaves_cover(record['outside_covers'][0],LO,lo,nz),leaves_cover(record['outside_covers'][1],hi,HI,nz)]
    if index==16:
        n,den=cramer([hrow(s),hrow(nv),hrow(bp[12])],[Q,times(Q,dv),R])
        out['u_determinant_sign']=signed(den,record['u_determinant_sign'],lo,hi);label,target=7,1
    else:n,den,label,target=nv,dv,9,12
    witness=times(plus(gram(n,bp[target]),scale(times(R,den),-1)),den)
    require(positive(witness,lo,hi),'strict forced original-core violation on entire remaining cell')
    out.update(pair=[label,target],packing_witness=serial(strip(witness)[0]));return out


def vplus(a,b):return tuple(plus(x,y) for x,y in zip(a,b))
def vmul(p,v):return tuple(times(p,x) for x in v)
def cross(a,b):return tuple(plus(times(a[(i+1)%3],b[(i+2)%3]),scale(times(a[(i+2)%3],b[(i+1)%3]),-1)) for i in range(3))
def dual_normal(a,b):
    # Independently use crossed physical dot rows, then exact scalar division.
    n=cross(hrow(a),hrow(b));answer=[]
    for p in n:
        q,r=quotient(p,P(2,-2));require(not r,'full dual-normal divisibility');answer.append(q)
    return tuple(answer)


def affine_gram(x,y,T):
    x0,x1,xd=x;y0,y1,yd=y
    return plus(gram(x0,y0),times(T,gram(x1,y1))),plus(gram(x0,y1),gram(x1,y0)),times(xd,yd)


def fibers(s,z,ear,chi,bp):
    K=gram(s,z);E=plus(times(D,D),scale(times(K,K),-1))
    disc=expanded_det([[D,Q,K],[Q,D,R],[K,R,D]]);T=times(P(2,1),disc)
    require(positive(E) and positive(T),'closed-band transverse first intersection')
    den=times(P(2,1),E)
    v0=vmul(P(2,1),vplus(vmul(plus(times(Q,D),scale(times(K,R),-1)),s),vmul(plus(times(R,D),scale(times(K,Q),-1)),z)))
    v1=dual_normal(s,z)
    qden=plus(D,Q);require(positive(qden),'positive1+q denominator')
    k=scale(P(-1,2),chi)
    u0=vplus(vmul(Q,vplus(vmul(den,s),v0)),vmul(k,dual_normal(s,v0)))
    u1=vplus(vmul(Q,v1),vmul(k,dual_normal(s,v1)));ud=times(den,qden);zero=(P(),P(),P())
    ap={ear:(s,zero,P(1)),9 if ear==7 else 7:(v0,v1,den),6:(u0,u1,ud)}
    M=[[R,P(-1),R],[R,R,P(-1)],[P(-1),R,R]];md=expanded_det(M)
    require(md==times(P(-1,2),times(P(1,1),P(1,1))) and positive(md),'entire nonsingular leaf matrix')
    leaves=[]
    for label in (6,7,9):
        n0,n1,d=ap[label];q,rem=quotient(ud,d);require(not rem,'common affine denominator')
        leaves.append((vmul(q,n0),vmul(q,n1)))
    roots0=[[] for _ in range(3)];roots1=[[] for _ in range(3)]
    for coordinate in range(3):
        ns,ds=cramer(M,[leaves[i][0][coordinate] for i in range(3)])
        for j in range(3):roots0[j].append(ns[j])
        ns,_=cramer(M,[leaves[i][1][coordinate] for i in range(3)])
        for j in range(3):roots1[j].append(ns[j])
    for j,label in enumerate((0,5,11)):ap[label]=(tuple(roots0[j]),tuple(roots1[j]),times(ds,ud))
    ids=[]
    for label,p in sorted(ap.items()):
        c0,c1,d2=affine_gram(p,p,T);require(c0==times(D,d2) and not c1,'every affine unit identity');ids.append(['unit',label])
    aes=sorted({tuple(sorted(e)) for t in A for e in combinations(t,2)})
    for i,j in aes:
        c0,c1,d2=affine_gram(ap[i],ap[j],T);require(c0==times(R,d2) and not c1,'every affine original contact');ids.append(['contact',i,j])
    for label,target in ((7,12),(9,10)):
        n0,n1,d=ap[label];require(gram(n0,bp[target])==times(R,d) and not gram(n1,bp[target]),'both original cross contacts');ids.append(['cross_contact',label,target])
    for i,j in combinations((6,7,9),2):
        c0,c1,d2=affine_gram(ap[i],ap[j],T);require(c0==times(Q,d2) and not c1,'entire q Gram')
    return ap,T,ids


def radical_positive(g0,g1,T,eps,method,lo,hi):
    require(type(eps) is int and eps in (-1,1),'both explicit radical signs')
    if method=='same_positive':require(positive(g0,lo,hi) and (not g1 or positive(scale(g1,eps),lo,hi)),'same-sign radical positivity')
    elif method=='constant_dominates':require(positive(g0,lo,hi) and positive(plus(times(g0,g0),scale(times(T,times(g1,g1)),-1)),lo,hi),'positive constant dominates radical')
    elif method=='radical_dominates':require(positive(scale(g1,eps),lo,hi) and positive(plus(times(T,times(g1,g1)),scale(times(g0,g0),-1)),lo,hi),'positive radical dominates absolute constant')
    else:raise ValueError('unknown radical sign mechanism')


def audit(data):
    blob=Path(__file__).with_name('PARENT.json').read_bytes();require(sha256(blob).hexdigest()==PARENT_SHA,'whole immutable parent input')
    parent=json.loads(blob);groups,tables=group_cases(parent)
    six=[];other=[];identities=[];fibers_by_anchor={}
    for index,g in enumerate(groups):
        bp=tables[parent['overlap_rows'][g['rows'][0]][0]]
        if g['ear']!=6:
            for chi in (-1,1):
                ap,T,ids=fibers(g['coordinate'],bp[10 if g['ear']==7 else 12],g['ear'],chi,bp)
                fibers_by_anchor[index,chi]=ap,T;identities.append([index,chi,ids])
    require(len(data['shared6'])==20,'complete shared6 case list')
    for index,g in enumerate(groups[:20]):
        record=data['shared6'][index];bp=tables[parent['overlap_rows'][g['rows'][0]][0]]
        six.append(shared6(g,index,bp,record))
    records={}
    for record in data['other_four_fibers']:
        key=(record['row'],record['eps'],record['chi'])
        require(all(type(v) is int for v in key),'integer branch labels, never bool/float')
        require(key not in records,'no duplicate orientation record');records[key]=record
    expected={(r,e,c) for g in groups if g['ear']!=6 for r in g['rows'] for e,c in product((-1,1),repeat=2)}
    require(set(records)==expected,'all and only80 complete sphere branches')
    for index,g in enumerate(groups[20:],20):
        for chi in (-1,1):
            ap,T=fibers_by_anchor[index,chi]
            for row_number in g['rows']:
                row=parent['overlap_rows'][row_number];bp=tables[row[0]];shared=NEW[row[1:].index(g['ear'])]
                for eps in (-1,1):
                    record=records[row_number,eps,chi]
                    def checked(leaf,lo,hi):
                        pair=leaf['pair'];require(len(pair)==2 and all(type(v) is int for v in pair),'literal point-pair labels')
                        label,target=pair;require(label in ap and target in bp and not(label==g['ear'] and target==shared),'two DISTINCT assigned physical points')
                        n0,n1,den=ap[label];g0=plus(gram(n0,bp[target]),scale(times(R,den),-1));g1=gram(n1,bp[target])
                        method=leaf['method'];radical_positive(g0,g1,T,eps,method,lo,hi)
                        return {'pair':pair,'method':method,'gap_digest':digest([serial(g0),serial(g1)])}
                    cover=leaves_cover(record['cover'],LO,HI,checked)
                    other.append({'anchor':index,'ear':g['ear'],'row':row_number,'eps':eps,'chi':chi,'radicand':serial(T),'cover':cover})
    expected_record={'format':'b7-disjoint-support-v1','actual_author':'six-tammes-1','role':'researcher','parent_certificate_sha256':PARENT_SHA,
                     'closed_cosine_band':['7/13','3/5'],'closed_r_band':['7/10','3/4'],
                     'literal_scope':'All106 distinct14-point contact masks from the parent one-overlap rows; every unit pair<=c and extra contacts allowed; no face/cohort premise for these individual exclusions',
                     'physical_scope':'ALL9972 hypotheses, hence full9813 physical cohort and complete A4/B7 assignment; every contact retained',
                     'leaf_matrix_determinant':serial(times(P(-1,2),times(P(1,1),P(1,1)))),
                     'all_shared_assignments':106,'shared6':six,'other_four_fibers':other,'affine_identity_digest':digest(identities),
                     'disjoint_assignments':31,'full_band_disjoint_maps':parent['full_band_maps'],'strict_improvement_disjoint_maps':parent['strict_improvement_maps']}
    require(canonical(data)==canonical(expected_record),'whole independently reconstructed typed record and every checked cover')
    return expected_record


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',default='CERTIFICATE.json');parser.add_argument('--emit');args=parser.parse_args()
    data=json.loads(Path(args.certificate).read_text());result=audit(data);blob=canonical(result).encode()
    if args.emit:Path(args.emit).write_bytes(blob)
    print(canonical({'status':'PASS','shared_assignments_excluded':106,'shared6_anchors':20,'other_fibers':80,'other_packing_leaves':sum(len(g['cover']) for g in result['other_four_fibers']),
                     'closed_J_maps':53,'strict_improvement_maps':52,'certificate_bytes':len(blob),'certificate_sha256':sha256(blob).hexdigest()}).strip())


if __name__=='__main__':main()
