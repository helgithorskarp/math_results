"""Exact dense producer: necessary Gram equations and all four sphere fibers.

Actual author six-tammes-1. The immutable9972 parent supplies the complete
conditional case cover. No float, solver or external runtime input is used.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import permutations, combinations, product
from collections import defaultdict
from hashlib import sha256
from math import gcd
import argparse
import json

from poly import add, neg, mul, divide, bernstein

R,D,Q = [F(0),F(1)], [F(2),F(-1)], [F(0),F(-3),F(2),F(2)]
LO,HI = F(7,10),F(3,4)
H = [F(-2),F(2),F(1)]
A = ((0,5,11),(0,6,11),(0,5,7),(5,9,11))
B = ((1,2,4),(2,4,8),(1,2,10),(1,10,12))
NEW = (20,21,22)
FACTORS = ([F(0),F(1)],D,[F(1),F(-1)],[F(1),F(1)],
           [F(2),F(1)],[F(-1),F(2)],[F(1),F(2)])
PARENT_SHA = 'a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187'
ROOT_CELLS = {16:(F(1891,2560),F(60513,81920)),
              17:(F(30493,40960),F(60987,81920))}


def need(condition,message):
    if not condition:
        raise ValueError(message)


def encode(p):return [str(x) for x in p]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))+'\n'
def digest(x):return sha256(canonical(x).encode()).hexdigest()


def compare_frozen(data,reference):
    """Controls only: reference must already have been freshly computed."""
    need(canonical(data)==canonical(reference),'entire typed projection of the freshly checked reference')


def primitive(p):
    if not p:return []
    denominator=1
    for v in p:denominator=denominator*v.denominator//gcd(denominator,v.denominator)
    integers=[int(v*denominator) for v in p]
    content=0
    for v in integers:content=gcd(content,abs(v))
    return [F(v//content) for v in integers]


def strip(p):
    if not p:return [],[]
    removed=[]
    for factor in FACTORS:
        power=0
        while len(p)>=len(factor):
            quotient,remainder=divide(p,factor)
            if remainder:break
            p=quotient;power+=1
        if power:removed.append([encode(factor),power])
    return primitive(p),removed


def sign(p,lo=LO,hi=HI):
    p,_=strip(p)
    bs=bernstein(p,lo,hi)
    return 1 if all(v>0 for v in bs) else -1 if all(v<0 for v in bs) else 0


def det(m):
    n=len(m);answer=[]
    for perm in permutations(range(n)):
        term=[F(-1 if sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2 else 1)]
        for i,j in enumerate(perm):term=mul(term,m[i][j])
        answer=add(answer,term)
    return answer


def inner(v,w):
    diagonal=[];sv=[];sw=[]
    for x,y in zip(v,w):diagonal=add(diagonal,mul(x,y));sv=add(sv,x);sw=add(sw,y)
    return add(mul([F(2),F(-2)],diagonal),mul(R,mul(sv,sw)))


def flip(u,v,w):return [add(mul(R,add(x,y)),neg(z)) for x,y,z in zip(u,v,w)]


def core():
    p={1:[[F(1)],[],[]],2:[[],[F(1)],[]],4:[[],[],[F(1)]]}
    p[8]=flip(p[2],p[4],p[1]);p[10]=flip(p[1],p[2],p[4]);p[12]=flip(p[1],p[10],p[2])
    return p


def reconstruct(ts):
    p=core();done={tuple(sorted(t)) for t in B};todo=set(map(tuple,ts))-done
    while todo:
        t=next((t for t in sorted(todo) if len(set(t)&set(p))==2),None)
        need(t is not None,'whole fresh parent disk propagation')
        e=sorted(set(t)&set(p));parents=[u for u in done if set(e)<=set(u)]
        need(len(parents)==1,'unique old triangle parent')
        old=next(x for x in parents[0] if x not in e);new=next(x for x in t if x not in e)
        p[new]=flip(p[e[0]],p[e[1]],p[old]);todo.remove(t);done.add(t)
    need(len(p)==9 and all(inner(v,v)==D for v in p.values()),'all nine unit points')
    for t in ts:
        for u,v in combinations(t,2):need(inner(p[u],p[v])==R,'every parent triangle contact')
    return p


def parent():
    blob=Path(__file__).with_name('PARENT.json').read_bytes()
    need(sha256(blob).hexdigest()==PARENT_SHA,'entire immutable9972 source input')
    x=json.loads(blob)
    need(x['cosine_closed_band']==['7/13','3/5'] and x['r_closed_band']==['7/10','3/4'],'parent closed bands')
    need(len(x['overlap_rows'])==137 and len(x['full_band_maps'])==53 and len(x['strict_improvement_maps'])==52,'complete parent lists')
    return x


def group_cases(x):
    groups={};points={}
    for row_number,row in enumerate(x['overlap_rows']):
        occupied=[v for v in row[1:] if v!=-1]
        if not occupied:continue
        need(len(occupied)==1 and occupied[0] in (6,7,9),'one parent shared ear')
        shape=row[0]
        if shape not in points:points[shape]=reconstruct([tuple(t) for t in x['all_shapes'][shape]])
        ear=occupied[0];label=NEW[row[1:].index(ear)];coordinate=tuple(tuple(p) for p in points[shape][label])
        key=(ear,coordinate);groups.setdefault(key,[]).append(row_number)
    answer=[{'ear':ear,'coordinate':[list(p) for p in coordinate],'rows':rows} for (ear,coordinate),rows in sorted(groups.items())]
    need(len(answer)==25 and sum(len(g['rows']) for g in answer)==106,'all shared assignments retained')
    need([sum(g['ear']==ear for g in answer) for ear in (6,7,9)]==[20,3,2],'all anchor reuse groups')
    return answer,points


def quadratic(build):
    zero,plus,minus=[det(build([F(i)])) for i in (0,1,-1)]
    return ([v/2 for v in add(add(plus,minus),neg([2*y for y in zero]))],
            [v/2 for v in add(plus,neg(minus))],zero)


def result(first,second):
    a,b,c=first;d,e,f=second
    afcd=add(mul(a,f),neg(mul(c,d)))
    return add(mul(afcd,afcd),neg(mul(add(mul(a,e),neg(mul(b,d))),add(mul(b,f),neg(mul(c,e))))))


def hrow(v):
    return [add(mul([F(2),F(-2)],v[i]),mul(R,add(add(v[0],v[1]),v[2]))) for i in range(3)]


def cramer(m,rhs):
    ns=[]
    for j in range(3):ns.append(det([[rhs[i] if k==j else m[i][k] for k in range(3)] for i in range(3)]))
    d=det(m)
    for i in range(3):need(add(add(mul(m[i][0],ns[0]),mul(m[i][1],ns[1])),mul(m[i][2],ns[2]))==mul(d,rhs[i]),'full Cramer row identity')
    return ns,d


def mod_h(p):return divide(p,H)[1]


def inverse_h(p):
    p=mod_h(p);a=p[0] if p else F(0);b=p[1] if len(p)>1 else F(0)
    norm=a*a-2*a*b-2*b*b
    need(norm!=0,'nonzero exact quadratic-field norm')
    inverse=[(a-2*b)/norm,-b/norm]
    need(mod_h(mul(p,inverse))==[F(1)],'entire quadratic-field inverse identity')
    return inverse


def nonzero_cover(p,lo,hi,path=''):
    s=sign(p,lo,hi)
    if s:return [{'path':path,'interval':[str(lo),str(hi)],'sign':s}]
    need(len(path)<16,'unfinished nonzero cover is failure')
    mid=(lo+hi)/2
    return nonzero_cover(p,lo,mid,path+'0')+nonzero_cover(p,mid,hi,path+'1')


def shared6(g,index,bp):
    s=g['coordinate'];K,L=inner(s,bp[12]),inner(s,bp[10])
    first=quadratic(lambda X:[[D,Q,Q,K],[Q,D,Q,R],[Q,Q,D,X],[K,R,X,D]])
    second=quadratic(lambda X:[[D,L,K,Q],[L,D,R,R],[K,R,D,X],[Q,R,X,D]])
    raw=result(first,second);reduced,removed=strip(raw)
    out={'anchor':index,'ear':6,'coordinate':[encode(p) for p in s],'rows':g['rows'],
         'Gram_quadratics':[[encode(p) for p in first],[encode(p) for p in second]],
         'resultant':encode(reduced),'removed_positive_factors':removed}
    sg=sign(reduced)
    if sg:
        out.update(method='nonzero_resultant',sign=sg);return out
    a,b,c=first;d,e,f=second
    ell=add(mul(d,b),neg(mul(a,e)));num=add(mul(a,f),neg(mul(d,c)))
    C=[hrow(s),hrow(bp[10]),hrow(bp[12])]
    nv,dv0=cramer(C,[mul(Q,ell),mul(R,ell),num]);dv=mul(dv0,ell)
    need(sign(ell)!=0 and sign(dv0)!=0,'whole-band forced v is nonsingular')
    out.update(common_root_linear_sign=sign(ell),basis_sign=sign(dv0),
               whole_forced_v_digest=digest([list(map(encode,nv)),encode(dv)]))
    if not raw:
        aliases=[k for k,p in core().items() if all(not add(nv[i],neg(mul(dv,p[i]))) for i in range(3))]
        need(len(aliases)==1,'continuous resultant branch has exact original-core alias')
        out.update(method='continuous_core_alias',alias=[9,aliases[0]]);return out
    quotient,remainder=divide(reduced,H)
    if not remainder:
        need(sign(quotient)!=0,'only quadratic exceptional parameter; no discarded roots')
        aliases=[k for k,p in core().items() if all(not mod_h(add(nv[i],neg(mul(dv,p[i])))) for i in range(3))]
        if aliases:
            out.update(method='quadratic_core_alias',alias=[9,aliases[0]],cofactor_sign=sign(quotient));return out
        iv=inverse_h(dv);v=[mod_h(mul(p,iv)) for p in nv]
        sf=[mod_h(p) for p in s]
        nu,du=cramer([hrow(sf),hrow(v),hrow(bp[12])],[Q,Q,R]);iu=inverse_h(du)
        u=[mod_h(mul(p,iu)) for p in nu]
        aliases=[k for k,p in core().items() if all(not mod_h(add(u[i],neg(p[i]))) for i in range(3))]
        need(len(aliases)==1,'quadratic branch has original p7 alias')
        out.update(method='quadratic_core_alias',alias=[7,aliases[0]],cofactor_sign=sign(quotient),quadratic_u_inverse_digest=digest([encode(mod_h(du)),encode(iu)]));return out
    need(index in ROOT_CELLS,'every unexcluded root case assigned a covered cell')
    lo,hi=ROOT_CELLS[index]
    out.update(method='isolated_packing',cell=[str(lo),str(hi)],
               outside_covers=[nonzero_cover(reduced,LO,lo),nonzero_cover(reduced,hi,HI)])
    if index==16:
        nu,du=cramer([hrow(s),hrow(nv),hrow(bp[12])],[Q,mul(Q,dv),R])
        need(sign(du,lo,hi)!=0,'forced u nonsingular on entire remaining cell')
        out['u_determinant_sign']=sign(du,lo,hi);n,den,label,target=nu,du,7,1
    else:n,den,label,target=nv,dv,9,12
    witness=mul(add(inner(n,bp[target]),neg(mul(R,den))),den)
    need(sign(witness,lo,hi)==1,'strict original-core packing violation over whole cell')
    out.update(pair=[label,target],packing_witness=encode(strip(witness)[0]))
    return out


def vecadd(a,b):return [add(x,y) for x,y in zip(a,b)]
def vecscale(p,v):return [mul(p,x) for x in v]
def cross(a,b):return [add(mul(a[1],b[2]),neg(mul(a[2],b[1]))),add(mul(a[2],b[0]),neg(mul(a[0],b[2]))),add(mul(a[0],b[1]),neg(mul(a[1],b[0])))]
def J(v):
    total=add(add(v[0],v[1]),v[2])
    return [add(mul([F(2),F(1)],p),neg(mul(R,total))) for p in v]


def affine_inner(x,y,T):
    x0,x1,xd=x;y0,y1,yd=y
    return (add(inner(x0,y0),mul(T,inner(x1,y1))),add(inner(x0,y1),inner(x1,y0)),mul(xd,yd))


def fibers(s,z,ear,chi,bp):
    K=inner(s,z);E=add(mul(D,D),neg(mul(K,K)))
    disc=det([[D,Q,K],[Q,D,R],[K,R,D]]);T=mul([F(2),F(1)],disc)
    need(sign(E)==1 and sign(T)==1,'both unit intersections are transverse over whole closed band')
    den=mul([F(2),F(1)],E)
    v0=vecscale([F(2),F(1)],vecadd(vecscale(add(mul(Q,D),neg(mul(K,R))),s),vecscale(add(mul(R,D),neg(mul(K,Q))),z)))
    v1=J(cross(s,z))
    qden=add(D,Q);need(sign(qden)==1,'1+q positive on closed band')
    k=mul([F(chi)], [F(-1),F(2)])
    u0=vecadd(vecscale(Q,vecadd(vecscale(den,s),v0)),vecscale(k,J(cross(s,v0))))
    u1=vecadd(vecscale(Q,v1),vecscale(k,J(cross(s,v1))))
    uden=mul(den,qden)
    zero=[[],[],[]]
    a={ear:(s,zero,[F(1)]),9 if ear==7 else 7:(v0,v1,den),6:(u0,u1,uden)}
    M=[[R,[F(-1)],R],[R,R,[F(-1)]],[[F(-1)],R,R]]
    md=det(M);need(md==mul([F(-1),F(2)],mul([F(1),F(1)],[F(1),F(1)])) and sign(md)==1,'invertible exact A leaf matrix')
    leaves=[]
    for label in (6,7,9):
        n0,n1,d=a[label];q,rem=divide(uden,d);need(not rem,'common positive affine denominator')
        leaves.append((vecscale(q,n0),vecscale(q,n1)))
    for j,label in enumerate((0,5,11)):
        n0=[];n1=[]
        for coordinate in range(3):
            ns,ds=cramer(M,[leaves[i][0][coordinate] for i in range(3)]);n0.append(ns[j])
            ns,_=cramer(M,[leaves[i][1][coordinate] for i in range(3)]);n1.append(ns[j])
        a[label]=(n0,n1,mul(ds,uden))
    identities=[]
    for label,p in sorted(a.items()):
        c0,c1,den2=affine_inner(p,p,T)
        need(c0==mul(D,den2) and not c1,'every affine A unit identity')
        identities.append(['unit',label])
    aes=sorted({tuple(sorted(e)) for t in A for e in combinations(t,2)})
    for i,j in aes:
        c0,c1,den2=affine_inner(a[i],a[j],T)
        need(c0==mul(R,den2) and not c1,'every affine original A contact')
        identities.append(['contact',i,j])
    for label,target in ((7,12),(9,10)):
        n0,n1,den=a[label]
        need(inner(n0,bp[target])==mul(R,den) and not inner(n1,bp[target]),'both prescribed cross contacts in every orientation')
        identities.append(['cross_contact',label,target])
    for label in (6,7,9):
        for other in (6,7,9):
            if label>=other:continue
            c0,c1,den2=affine_inner(a[label],a[other],T)
            need(c0==mul(Q,den2) and not c1,'entire A-ear q Gram identity')
    return a,T,identities


def positive_radical(g0,g1,T,eps,lo,hi):
    sg0=sign(g0,lo,hi);sg1=sign([eps*x for x in g1],lo,hi)
    if sg0==1 and (sg1==1 or not g1):return 'same_positive'
    difference=add(mul(g0,g0),neg(mul(T,mul(g1,g1))))
    if sg0==1 and sign(difference,lo,hi)==1:return 'constant_dominates'
    if sg1==1 and sign(neg(difference),lo,hi)==1:return 'radical_dominates'
    return None


def packing_cover(polynomials,T,eps,lo=LO,hi=HI,path=''):
    for pair,g0,g1 in polynomials:
        method=positive_radical(g0,g1,T,eps,lo,hi)
        if method:return [{'path':path,'interval':[str(lo),str(hi)],'pair':pair,'method':method,'gap_digest':digest([encode(g0),encode(g1)])}]
    need(len(path)<12,'unfinished affine packing cover is failure')
    mid=(lo+hi)/2
    return packing_cover(polynomials,T,eps,lo,mid,path+'0')+packing_cover(polynomials,T,eps,mid,hi,path+'1')


def build():
    x=parent();groups,bpoints=group_cases(x);six=[];other=[];identities=[]
    for index,g in enumerate(groups):
        bp=bpoints[x['overlap_rows'][g['rows'][0]][0]]
        if g['ear']==6:six.append(shared6(g,index,bp));continue
        for chi in (-1,1):
            ap,T,ids=fibers(g['coordinate'],bp[10 if g['ear']==7 else 12],g['ear'],chi,bp)
            identities.append([index,chi,ids])
            for row_number in g['rows']:
                row=x['overlap_rows'][row_number];points=bpoints[row[0]];shared=NEW[row[1:].index(g['ear'])]
                gaps=[]
                for label,(n0,n1,den) in sorted(ap.items()):
                    for target,p in sorted(points.items()):
                        if label==g['ear'] and target==shared:continue
                        gaps.append(([label,target],add(inner(n0,p),neg(mul(R,den))),inner(n1,p)))
                for eps in (-1,1):
                    cover=packing_cover(gaps,T,eps)
                    other.append({'anchor':index,'ear':g['ear'],'row':row_number,'eps':eps,'chi':chi,
                                  'radicand':encode(T),'cover':cover})
    need(len(six)==20 and sum(len(g['rows']) for g in six)==86,'all shared6 assignments excluded')
    need(len(other)==80 and len({g['row'] for g in other})==20,'all four fibers of other20 assignments excluded')
    expected={(r,e,c) for g in groups if g['ear']!=6 for r in g['rows'] for e,c in product((-1,1),repeat=2)}
    need({(g['row'],g['eps'],g['chi']) for g in other}==expected,'no omitted orientation or case')
    return {'format':'b7-disjoint-support-v1','actual_author':'six-tammes-1','role':'researcher',
            'parent_certificate_sha256':PARENT_SHA,'closed_cosine_band':['7/13','3/5'],'closed_r_band':['7/10','3/4'],
            'literal_scope':'All106 distinct14-point contact masks from the parent one-overlap rows; every unit pair<=c and extra contacts allowed; no face/cohort premise for these individual exclusions',
            'physical_scope':'ALL9972 hypotheses, hence full9813 physical cohort and complete A4/B7 assignment; every contact retained',
            'leaf_matrix_determinant':encode(mul([F(-1),F(2)],mul([F(1),F(1)],[F(1),F(1)]))),
            'all_shared_assignments':106,'shared6':six,'other_four_fibers':other,'affine_identity_digest':digest(identities),
            'disjoint_assignments':31,'full_band_disjoint_maps':x['full_band_maps'],
            'strict_improvement_disjoint_maps':x['strict_improvement_maps']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--emit',nargs='?',const='CERTIFICATE.json');parser.add_argument('--certificate',default='CERTIFICATE.json');args=parser.parse_args()
    result=build();whole=canonical(result).encode()
    if args.emit:Path(args.emit).write_bytes(whole)
    else:
        x=json.loads(Path(args.certificate).read_text())
        compare_frozen(x,result)
    print(canonical({'status':'PASS','shared_assignments_excluded':106,'shared6_anchors':20,'other_fibers':80,
                     'other_packing_leaves':sum(len(g['cover']) for g in result['other_four_fibers']),
                     'closed_J_maps':53,'strict_improvement_maps':52,'certificate_bytes':len(whole),'certificate_sha256':sha256(whole).hexdigest()}).strip())


if __name__=='__main__':main()
