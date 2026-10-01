#!/usr/bin/env python3
"""six-reviewer-1 independent exact distinct-mark cube-pendant H audit.
No author modules, CAS, solver, numerical roots or private data are imported.
"""
from fractions import Fraction as F
from itertools import combinations,product
from hashlib import sha256
from math import gcd
from pathlib import Path
import argparse,json

class Failure(RuntimeError):pass
CHECKS=0

def need(ok,label):
    global CHECKS
    if not ok:raise Failure(label)
    CHECKS+=1

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())
def image(a,x):return [dot(row,x) for row in a]
def matrix_hash(a):return sha256(json.dumps([[str(x) for x in row] for row in a],separators=(',',':')).encode()).hexdigest()

def psd(a):
    """Largest-diagonal pivoted integer Bareiss congruence; exact divisions.
    A positive scalar clears denominators. At a singular residual, every entry
    must vanish; diagonal-only checking would miss indefinite zero-diagonal cases.
    """
    n=len(a);need(n>0 and all(len(row)==n for row in a),'square PSD input')
    need(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'symmetric PSD input')
    den=1
    for row in a:
        for x in row:den=den*F(x).denominator//gcd(den,F(x).denominator)
    b=[[int(F(x)*den) for x in row] for row in a];previous=1;rank=0
    while b:
        size=len(b)
        if any(b[i][i]<0 for i in range(size)):raise Failure('negative diagonal in PSD congruence')
        k=max(range(size),key=lambda i:b[i][i]);pivot=b[k][k]
        if not pivot:
            if any(x for row in b for x in row):raise Failure('nonzero zero-diagonal PSD residual')
            break
        idx=[i for i in range(size) if i!=k];new=[[0]*len(idx) for _ in idx]
        for ii,i in enumerate(idx):
            for jj in range(ii,len(idx)):
                j=idx[jj];v,rem=divmod(pivot*b[i][j]-b[i][k]*b[k][j],previous)
                if rem:raise Failure('inexact fraction-free division')
                new[ii][jj]=new[jj][ii]=v
        previous=pivot;b=new;rank+=1
    return rank


def lift(c):
    rows=[sum(row,F()) for row in c]
    return [[sum(rows,F()),*[-x for x in rows]],*[[-rows[i],*row] for i,row in enumerate(c)]]

def permute(a,index):return [[a[i][j] for j in index] for i in index]

def family(n,positions):
    need(type(n) is int and 2<=n<=6,'literal n guard2..6')
    need(2<=len(positions)<=n and all(type(x) is int and 0<=x<n for x in positions) and len(set(positions))==len(positions),'distinct marks')
    old=list(range(1,1<<n));extra=[]
    for i,x in enumerate(positions):extra.extend([1<<(n+i),(1<<(n+i))|(1<<x)])
    canonical=[0,*old,*extra];own=[0,*sorted(canonical[1:],key=lambda x:(x.bit_count(),x))]
    return old,extra,canonical,own

def construct(n,positions,old_core=False):
    old,extra,canonical,own=family(n,positions);r=len(positions);q=1<<(n-1);m=len(old);N=len(canonical);s=q+1
    c0=[[F((q+1)*(a==b)+(q if old_core else q-1)*((a^b)==2*q-1)-1) for b in old] for a in old]
    need(psd(c0)==m,'old core positive definite')
    hs=[[F(-bool(a&(1<<x))) for a in old] for x in positions]
    hsimages=[image(c0,h) for h in hs];one=[F(1)]*m;Gimage=image(c0,one)
    hgram=[[dot(h,img) for img in hsimages] for h in hs]
    need(hgram==[[(F(q) if i==j else F(q,2) if old_core else F(0)) for j in range(r)] for i in range(r)],'all marked star Gram entries')
    k=[1+sum(h[j] for h in hs) for j in range(m)];mean=[sum(h[j] for h in hs)/r for j in range(m)]
    R=r+1;b=F(r*(q-r-2),R*q*(r-1));eta=F(r*q,R)+F(2*r,R*R)-b*b*F(q*(r-1),r)
    newco=[]
    for h in hs:newco.extend([[-k[j]/R+b*(h[j]-mean[j]) for j in range(m)],h])
    rawco=[]
    for h in hs:rawco.extend([[-v/q for v in h],h])
    def gram(co,raw):
        out=[[F(0)]*(m+2*r) for _ in range(m+2*r)]
        for i in range(m):out[i][:m]=c0[i][:]
        images=[image(c0,x) for x in co]
        for j,img in enumerate(images):
            for i,x in enumerate(img):out[i][m+j]=out[m+j][i]=x
        for i,x in enumerate(co):
            for j,img in enumerate(images):
                residual=F(0)
                if i%2==0 and j%2==0:
                    residual=(q-F(1,q))*(i==j) if raw else eta if i==j else -eta/(r-1)
                out[m+i][m+j]=dot(x,img)+residual
        return out
    raw=gram(rawco,True);Qraw=lift(raw);T=sum(Qraw[i][i] for i in range(N));B=Qraw[0][0]
    if old_core:
        return {'canonical':canonical,'own':own,'c0':c0,'hs':hs,'hsimages':hsimages,'k':k,'q':q,'r':r,'N':N,'s':s,'raw':raw,'Qraw':Qraw,'T':T,'B':B}
    h0=[-(one[i]+int(old[i]==2*q-1))/2 for i in range(m)]
    gp=[one[i]+h0[i] for i in range(m)];zc=[mean[i]-h0[i] for i in range(m)]
    coords=[gp,h0,zc];metric=[F(q-1),F(1),F(q-r,r)]
    need([[dot(v,image(c0,w)) for w in coords] for v in coords]==[[metric[i]*(i==j) for j in range(3)] for i in range(3)],'literal symmetric-sector Gram metric')
    need(image(c0,h0)==[one[i]+2*h0[i] for i in range(m)],'literal h0 full old-frame action')
    need(image(c0,gp)==[(q+1)*gp[i]+(q-1)*h0[i] for i in range(m)],'literal Gperp full old-frame action')
    need(image(c0,zc)==[2*x for x in zc],'literal Z full old-frame action')
    need([[raw[m+2*i][m+2*j] for j in range(r)] for i in range(r)]==[[F(q)*(i==j) for j in range(r)] for i in range(r)],'raw singleton mutual orthogonality')
    need(eta>0,'positive simplex residual')
    seed=gram(newco,False);Qseed=lift(seed)
    need(Qseed[0][0]==F(R*q-2*r,R*R),'seed actual empty energy')
    need(B==(2*r+1)*q-4*r+F(2*r,q),'raw empty energy')
    need(T==2*q*q+4*r*q-4*r+F(2*r,q),'raw full trace')
    raw_bound=4*q+B;loss=raw_bound-N+2
    eps=1/(2*(1+T));eps_new=1/(2*loss)
    need(loss>=6 and 0<eps<eps_new<1,'larger rational repair')
    beta=2-eps*loss;need(beta>F(3,2),'published-matrix stronger gap')
    Qmix=[[(1-eps)*a+eps*b for a,b in zip(x,y)] for x,y in zip(Qseed,Qraw)]
    Qnew=[[(1-eps_new)*a+eps_new*b for a,b in zip(x,y)] for x,y in zip(Qseed,Qraw)]
    idx=[canonical.index(x) for x in own]
    return {'canonical':canonical,'own':own,'c0':c0,'hs':hs,'hsimages':hsimages,'k':k,'q':q,'r':r,'N':N,'s':s,'Qseed':permute(Qseed,idx),'Qraw':permute(Qraw,idx),'Qmix':permute(Qmix,idx),'Qnew':permute(Qnew,idx),'T':T,'B':B,'raw_bound':raw_bound,'loss':loss,'epsilon':eps,'epsilon_new':eps_new,'beta':beta}


def certificate(fam,Q,s,low_nullity,margin=None):
    N=len(fam);M=[[(Q[i][j]+1-s*(i==j))/(N-s) for j in range(N)] for i in range(N)]
    need(len(set(fam))==N and fam[0]==0,'empty-inclusive unique family')
    present=set(fam)
    for a in fam:
        x=a
        while True:
            need(x in present,'literal downset closure')
            if not x:break
            x=(x-1)&a
    star=max(sum(bool(a&(1<<i)) for a in fam) for i in range(max(fam).bit_length()))
    need(star==s,'largest literal star')
    need(all(sum(row)==1 for row in M),'all literal row sums')
    need(all(M[i][j]==M[j][i] and (not(fam[i]&fam[j]) or M[i][j]==0) for i in range(N) for j in range(N)),'all literal symmetry/support entries')
    low=[[Q[i][j]+1 for j in range(N)] for i in range(N)]
    need(psd(low)==N-low_nullity,'complete lower PSD rank')
    for mark in range(max(fam).bit_length()):
        f=[int(bool(a&(1<<mark))) for a in fam]
        if sum(f)==s:
            need(image(low,[F(x)-F(s,N) for x in f])==[0]*N,'every forced star kernel')
    if margin is not None:
        upper=[[(N-margin)*((i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)]
        need(psd(upper)==N-1,'complete full scaled upper margin/rank')
    index=sorted(range(N),key=lambda i:fam[i]);normalized=permute(M,index)
    return M,{'N':N,'s':s,'lower_rank':N-low_nullity,'upper_rank':N-1 if margin is not None else None,'matrix_sha256':matrix_hash(normalized),'scaled_upper_margin':str(margin) if margin is not None else None}


def literal(n,positions):
    data=construct(n,positions);N,r,s=data['N'],data['r'],data['s'];fam=data['own'];out={}
    for key,nullity,margin in [('Qseed',r+1,F(2)),('Qraw',r,None),('Qmix',r,data['beta']),('Qnew',r,F(3,2))]:
        M,out[key]=certificate(fam,data[key],s,nullity,margin)
        if key=='Qmix':original=M
    bound=data['raw_bound'];P=[[(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    need(psd([[bound*P[i][j]-data['Qraw'][i][j] for j in range(N)] for i in range(N)])==N-1,'full linear-in-q raw operator bound')
    out.update(n=n,r=r,positions=positions,epsilon=str(data['epsilon']),epsilon_new=str(data['epsilon_new']),beta=str(data['beta']),raw_operator_bound=str(bound),raw_trace=str(data['T']),raw_empty_energy=str(data['B']))
    return out,(fam,original,s,r)


# Bivariate rational polynomials in (u,t), generated from matrix entries.
def pc(a):return {(0,0):F(a)} if a else {}
def pa(*args):
    out={}
    for a in args:
        for e,v in a.items():out[e]=out.get(e,F())+v
    return {e:v for e,v in out.items() if v}
def pn(a):return {e:-v for e,v in a.items()}
def pm(*args):
    out=pc(1)
    for a in args:
        new={}
        for (i,j),v in out.items():
            for (k,l),w in a.items():new[i+k,j+l]=new.get((i+k,j+l),F())+v*w
        out={e:v for e,v in new.items() if v}
    return out
def pp(a,n):return pm(*([a]*n))
def det3(a):return pa(pm(a[0][0],a[1][1],a[2][2]),pm(a[0][1],a[1][2],a[2][0]),pm(a[0][2],a[1][0],a[2][1]),pn(pm(a[0][2],a[1][1],a[2][0])),pn(pm(a[0][1],a[1][0],a[2][2])),pn(pm(a[0][0],a[1][2],a[2][1])))
def prec(a):return [[list(e),str(v)] for e,v in sorted(a.items())]

def polynomial_margin():
    u={(1,0):F(1)};t={(0,1):F(1)};r=pa(t,pc(2));q=pa(u,r,pc(1));R=pa(r,pc(1));N=pm(pc(2),pa(q,r));g=pa(q,pc(-1));qr=pa(q,pn(r))
    num=[[pa(pm(pa(r,pc(2)),q),r),pm(pc(2),r),qr],
         [pm(pc(2),r,g),pm(pc(2),pa(pp(r,2),pc(1))),pm(pc(2),r,qr)],
         [pm(r,g),pm(pc(2),pp(r,2)),pa(pm(pc(2),R),pm(qr,pa(pm(pc(2),r),pc(1))))]]
    A=[[pa(pm(pa(N,pc(-2)),R) if i==j else {},pn(num[i][j])) for j in range(3)] for i in range(3)]
    two=pa(*[pa(pm(A[i][i],A[j][j]),pn(pm(A[i][j],A[j][i]))) for i,j in combinations(range(3),2)])
    coefficients=[det3(A),pm(R,two),pm(pp(R,2),pa(*(A[i][i] for i in range(3)))),pp(R,3)]
    # A has real spectrum because it is a positive-metric self-adjoint operator.
    # All coefficients of det(lambda*R*I+A) are positive, so no root<=0.
    for p in coefficients:need(all(v>0 for v in p.values()),'formal positive symmetric characteristic coefficients')
    q=pa(u,pc(4));first=pa(pm(pc(9),pp(q,2)),pn(pm(pc(4),pp(pa(q,pc(-4)),2))))
    anti_det=pa(pm(pc(9),pp(q,2),pa(pm(pc(2),q),pc(2))),pn(pm(pc(4),pp(pa(q,pc(-4)),2),pa(pm(pc(2),q),pc(2)))),pn(pm(q,pa(pm(pc(8),pp(q,2)),pm(pc(40),q),pc(-64)))))
    anti_trace=pm(pc(5),pa(pm(pc(3),q),pc(2)))
    for p in [first,anti_det,anti_trace]:need(all(v>0 for v in p.values()),'formal positive r2 antisymmetric coefficients')
    need(anti_det==pm(pc(2),pa(pp(q,3),pm(pc(17),pp(q,2)),pc(-64))),'independent antisymmetric determinant formula')
    return {'symmetric_characteristic_numerators':[prec(p) for p in coefficients],'variables':['u=q-r-1','t=r-2'],'common_denominator':'(r+1)^3','r2_first_numerator_over_9q':prec(first),'r2_determinant_numerator_over_9q':prec(anti_det),'r2_trace_numerator_over9':prec(anti_trace)}


def sector(q,r):
    need(type(q) is int and type(r) is int and ((q,r)==(2,2) or r>=2 and q>=r+1),'sector parameter domain')
    R=r+1;N=2*q+2*r;z=F(q-r,r);b=F(r*(q-r-2),R*q*(r-1))
    eta=F(r*q,R)+F(2*r,R*R)-b*b*F(q*(r-1),r);e=F(r,r-1)*eta
    need(e>0,'positive standard residual')
    num=[[(r+2)*q+r,2*r,q-r],[2*r*(q-1),2*(r*r+1),2*r*(q-r)],[r*(q-1),2*r*r,2*R+(q-r)*(2*r+1)]]
    dim=2 if z==0 else 3;metric=[F(q-1),F(1),z][:dim]
    sym=[[metric[i]*((N-2)*(i==j)-F(num[i][j],R)) for j in range(dim)] for i in range(dim)]
    anti=[[F((N-2)*q)-(q+2)*q-b*b*q*q,-b*q*e],[-b*q*e,(N-2)*e-e*e]]
    need(psd(sym)==dim and psd(anti)==2,'full two-margin sector slacks')
    need((2*q+r-2)==(dim+2*(r-1)+max(q-2,0)+max(q-r-1,0)),'complete sector dimensions')
    need(N-2*q>=2 and N-2>=2,'untouched sector two margins')
    if r>=3:
        theta=b*b*q/(q+2*r-2)+e/N
        need(theta<F(45,64),'uniform standard rank-one budget')
    return {'q':q,'r':r,'b':str(b),'eta':str(eta),'symmetric_dimension':dim,'symmetric_slack_sha256':matrix_hash(sym),'standard_slack_sha256':matrix_hash(anti)}


def old_core(n):
    data=construct(n,[0,1,2],True);q=data['q'];N=data['N'];C=data['c0'];m=len(C);hs=data['hs'];h=[sum(x[i] for x in hs) for i in range(m)];k=data['k'];G=[F(1)]*m
    ch=image(C,h);cg=image(C,G);B0=[(x-1)/(q+1) for x in cg]
    vectors=[[x/2 for x in h],[1-B0[i]+h[i]/2 for i in range(m)],B0]
    images=[image(C,v) for v in vectors];norms=[F(3*q,2),F(q*(q-3),2*(q+1)),F((q+2)*(q-1),q+1)];gaps=[5,2*q+5,q+4]
    for i in range(3):
        for j in range(3):
            inner=dot(vectors[i],images[j]);known=dot(images[i],images[j])+sum(dot(x,images[i])*dot(x,images[j]) for x in hs)
            need(inner==(norms[i] if i==j else 0),'old orthogonal directions in original indices')
            need(N*inner-known==(norms[i]*gaps[i] if i==j else 0),'old full known-frame cap compression')
        need(dot(k,images[i])==norms[i],'old K projections')
    need(dot(h,ch)==6*q and dot(k,ch)==3*q,'old h/K identities')
    need(dot(ch,ch)+sum(dot(x,ch)**2 for x in hs)==6*q+12*q*q,'old known frame h energy')
    need(data['T']==2*q*q+11*q-8+F(3,q),'old full raw trace')
    certificate(data['canonical'],data['Qraw'],q+1,3)
    theta3=sum(F(x,y) for x,y in zip(norms,gaps))/3;theta4=theta3*F(3,4)
    ray=5-F(3*q,8)
    if q==8:need(theta3==F(1987,1890)>1 and theta4==F(1987,2520)<1,'q8 centered/free distinction')
    if q>=16:need(ray<0 and theta3>1 and F(q,10)>1,'all sufficiently large old-core obstructions')
    return {'n':n,'q':q,'rayleigh_upper_bound':str(ray),'theta_three_unknown':str(theta3),'theta_four_unknown':str(theta4),'raw_trace':str(data['T']),'ordinary_lower_rank':N-3}


def maxima(n,positions):
    _,_,fam,_=family(n,positions);vertices=fam[1:];best=0;winners=set()
    def search(chosen,candidates):
        nonlocal best,winners
        if len(chosen)+len(candidates)<best:return
        if len(chosen)>best:best=len(chosen);winners=set()
        if len(chosen)==best:winners.add(tuple(sorted(chosen)))
        for i,a in enumerate(candidates):search(chosen+[a],[b for b in candidates[i+1:] if a&b])
    search([],vertices)
    stars={tuple(sorted(a for a in vertices if a&(1<<x))) for x in positions}
    need(best==(1<<(n-1))+1 and winners==stars,'exhaustive independent maximum families')
    return {'n':n,'positions':positions,'maximum_size':best,'maximum_families':len(winners)}


def product_certificate(left,right,label):
    fa,ma,sa,ra=left;fb,mb,sb,rb=right;na=len(fa);nb=len(fb);N=na*nb
    shift=max(fa).bit_length();fam=[a|(b<<shift) for a in fa for b in fb]
    M=[[ma[i][k]*mb[j][l] for k in range(na) for l in range(nb)] for i in range(na) for j in range(nb)]
    density=max(F(sa,na),F(sb,nb));S=density*N;need(S.denominator==1,'integer product largest star');S=int(S)
    nullity=(ra if F(sa,na)==density else 0)+(rb if F(sb,nb)==density else 0)
    Q=[[(N-S)*M[i][j]+S*(i==j)-1 for j in range(N)] for i in range(N)]
    _,record=certificate(fam,Q,S,nullity,F(1,4))
    record.update(label=label,eligible_star_nullity=nullity)
    return record


def damage_controls():
    caught=[]
    def reject(label,fn):
        try:fn()
        except Failure:caught.append(label)
        else:raise Failure('damage not rejected: '+label)
    reject('zero-diagonal indefinite',lambda:psd([[F(0),F(1)],[F(1),F(0)]]))
    reject('negative pivot',lambda:psd([[F(-1),F(0)],[F(0),F(1)]]))
    reject('asymmetric slack',lambda:psd([[F(1),F(1)],[F(0),F(1)]]))
    reject('duplicate marks',lambda:construct(3,[0,0]))
    reject('out-of-range mark',lambda:construct(3,[0,3]))
    reject('bounded literal guard',lambda:construct(7,[0,1]))
    d=construct(2,[0,1]);q=[row[:] for row in d['Qmix']];q[0][0]+=1
    reject('corrupted empty contribution',lambda:certificate(d['own'],q,d['s'],d['r'],F(1,2)))
    reject('wrong largest star',lambda:certificate(d['own'],d['Qmix'],d['s']+1,d['r'],F(1,2)))
    reject('wrong claimed rank',lambda:certificate(d['own'],d['Qmix'],d['s'],d['r']+1,F(1,2)))
    reject('zero simplex residual outside domain',lambda:sector(2,3))
    return caught


def build():
    cases=[];saved={}
    for n in range(2,7):
        for r in range(2,n+1):
            rec,mat=literal(n,list(range(r)));cases.append(rec);saved[n,r]=mat
    relabel,_=literal(4,[3,1,0])
    params=[(2,2)]+[(q,r) for r in range(2,21) for q in sorted({r+1,2*(r+1),1<<20})]
    sectors=[sector(q,r) for q,r in params]
    poly=polynomial_margin()
    olds=[old_core(n) for n in range(3,7)]
    singletons=([0,1,2],[[F(0),F(1,2),F(1,2)],[F(1,2),F(0),F(1,2)],[F(1,2),F(1,2),F(0)]],1,2)
    products=[product_certificate(saved[2,2],saved[2,2],'equal-density boundary product'),product_certificate(saved[3,3],singletons,'unequal-density strict singleton product')]
    maximum_cases=[maxima(2,[0,1]),maxima(3,[0,1]),maxima(3,[0,1,2])]
    damages=damage_controls()
    return {'agent':'six-reviewer-1','method':'independent set indexing; pivoted integer Bareiss; full frame characteristic-polynomial certificate','literal_cases':cases,'relabeled_case':relabel,'sectors':sectors,'polynomial_certificate':poly,'old_core_cases':olds,'products':products,'maximum_family_cases':maximum_cases,'rejected_damage_controls':damages,'checks':CHECKS}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'));parser.add_argument('--emit-fixture',type=Path);args=parser.parse_args()
    record=build();raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.emit_fixture:args.emit_fixture.write_bytes(raw)
    else:need(record==json.loads(args.fixture.read_text()),'complete fresh record versus fixture')
    print(json.dumps({'agent':'six-reviewer-1','checks':record['checks'],'canonical_cases':len(record['literal_cases']),'sector_cases':len(record['sectors']),'old_core_cases':len(record['old_core_cases']),'products':len(record['products']),'maximum_family_cases':len(record['maximum_family_cases']),'damage_controls':len(record['rejected_damage_controls']),'fixture_sha256':sha256(raw).hexdigest()}))

if __name__=='__main__':main()
