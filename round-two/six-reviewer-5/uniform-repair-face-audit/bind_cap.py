"""Stdlib-only original23-coordinate binding of EVERY cap map and dual energy."""
import json,math,sys
from pathlib import Path
from fractions import Fraction as F
from literal_check import require,table,short,pair,solve,original
from parse_exact import rational
from bind_lower import value
P=Path(__file__).resolve().parent

def compile(x):
    if isinstance(x,dict):return {a:compile(b) for a,b in x.items()}
    if isinstance(x,list):return [compile(v) for v in x]
    if isinstance(x,str):return rational(x)
    return x
def ev(x,q,k):
    if isinstance(x,dict):return {a:ev(b,q,k) for a,b in x.items()}
    if isinstance(x,list):return [ev(v,q,k) for v in x]
    if not isinstance(x,tuple):return F(x)
    def one(p):return sum((c*q**i*k**j for (i,j),c in p.items()),F(0))
    return one(x[0])/one(x[1])

def counted(q,k):
    ch=lambda n,r:math.comb(n,r) if 0<=r<=n else 0
    keys=sorted((c,z,w) for c in range(8) for z in range(3) for w in range(3)
        if (1<=c.bit_count()+z+w<=2 or c.bit_count()+z+w==3 and c.bit_count()>=2) and (c,z,w)!=(6,1,0))
    masses=[ch(k,z)*ch(q-k,w) for c,z,w in keys];T=table(q);N=(q*q+13*q+16)//2-k;s=3*q+4
    require(len(keys)==23 and sum(masses)==N-1,'entire original23 census')
    C=[];D=[];U=[]
    for i,(c,z,w) in enumerate(keys):
        cr=[];dr=[];ur=[]
        for j,(d,zz,ww) in enumerate(keys):
            count=0 if c&d else ch(k-z,zz)*ch(q-k-w,ww)
            b0,b1=T[tuple(sorted(((c.bit_count(),z+w),(d.bit_count(),zz+ww))))] if count else (F(0),F(0))
            v=s*masses[i]*int(i==j)-masses[i]*masses[j]+masses[i]*count*b0
            cr.append(v);dr.append(masses[i]*count*b1);ur.append(N*masses[i]*int(i==j)-masses[i]*masses[j]-v)
        C.append(cr);D.append(dr);U.append(ur)
    return keys,masses,C,D,U

def even(keys,A):
    flip=lambda c:(c&1)|((c&2)<<1)|((c&4)>>1)
    reps=sorted(set((min(c,flip(c)),z,w) for c,z,w in keys))
    groups=[[i for i,(c,z,w) in enumerate(keys) if (min(c,flip(c)),z,w)==v] for v in reps]
    E=[[sum((A[i][j] for i in I for j in J),F(0)) for J in groups] for I in groups]
    return reps,groups,E

def main():
    vec=compile(json.loads((P/'cap-vector-polynomials.json').read_text()))
    delta=compile(json.loads((P/'cap-derivative-polynomials.json').read_text()))
    lower=json.loads((P/'lower-signs.json').read_text())
    opt=compile(json.loads((P/'optimization-polynomials.json').read_text()))
    capshort=compile(json.loads((P/'cap-short-polynomials.json').read_text()))
    const_groups=[(0,),(0,),(1,),(2,4),(3,5),(6,),(7,),(1,),(2,4),(3,5),(6,)]
    const_r=[1,2,0,0,0,0,0,1,1,1,1]
    std_groups=[(0,),(0,),(1,),(2,4),(3,5),(6,)];std_r=[1,2,1,1,1,1]
    records=[]
    for q,k in ((21,7),(26,7),(27,7),(32,8),(100,20),(257,48),(258,48)):
        keys,m,C,D,U=counted(q,k)
        if q==21:
            literal=original(q,k)
            require(literal['keys']==keys and literal['C']==C and literal['D']==D and literal['U']==U,'ENTIRE actual127449 pair binding, all1587 original coefficient entries')
        v=ev(vec,q,k);de=ev(delta,q,k);r=q-k
        V=[[c/v['denominator'] for c in row] for row in v['V']]
        Vs=[row[0]/v['standard_denominator'] for row in v['standard_V']]
        if '--omit-standard' in sys.argv:Vs=[F(0)]*len(Vs)
        beta=V[10]
        X=[]
        for c,z,w in keys:
            size=z+w;j=next(i for i,(g,n) in enumerate(zip(const_groups,const_r)) if c in g and size==n)
            std=next((i for i,(g,n) in enumerate(zip(std_groups,std_r)) if c in g and size==n),None)
            X.append([V[j][a]+(Vs[std]*beta[a]*(-z+F(k,r)*w) if std is not None else 0) for a in range(3)])
        anchors=[keys.index(t) for t in ((1,0,0),(3,0,0),(5,0,0),(2,0,0),(4,0,0))]
        for i in range(23):
            if i in anchors:continue
            for a in range(3):require(sum(U[i][j]*X[j][a] for j in range(23))==0,'every ORIGINAL cap stationary row')
        expected_rows=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)],[F(0),F(0),F(1)]]
        require([X[i] for i in anchors]==expected_rows,'every original physical anchor normalization')
        M=pair(U,X);Dc=pair(D,X)
        require(Dc==[[a/de['denominator'] for a in row] for row in de['numerator']],'all9 COMPLETE original cap Delta entries incl mean-zero correction')
        reps,groups,EU=even(keys,U);direct,W=short(EU,[reps.index(t) for t in ((1,0,0),(3,0,0),(2,0,0))])
        require(direct==M,'independent full17 original cap Schur')
        require(all(W[t]==X[i] for t,g in enumerate(groups) for i in g),'every full physical minimizer coordinate')
        a=value(lower['a0'],{'q':q,'k':k});b=F(2*(3*q+4)*(3*q*q+3*q-2),6*q*q+5*q-2)
        H=[[M[i][j] for j in range(2)] for i in range(2)];u=[M[i][2] for i in range(2)];w=[F(-1),F(1)]
        require(H[0][0]>0 and H[0][0]*H[1][1]-H[0][1]**2>0,'finite cap H positive')
        K=[[H[i][j]+a*w[i]*w[j] for j in range(2)] for i in range(2)];y=[u[i]+a*w[i] for i in range(2)]
        h=[row[0] for row in solve(K,[[-c] for c in y])];ell=-h[0]+h[1]
        R=M[2][2]+a+sum(y[i]*h[i] for i in range(2));t=a*(1+ell)/2
        op=ev(opt,q,k);cs=ev(capshort,q,k)
        require(M==[[c/cs['denominator'] for c in row] for row in cs['numerator']],'every original cap short field coefficient')
        require(h==[op['h0_numerator']/op['vertex_denominator'],op['h1_numerator']/op['vertex_denominator']] and R==op['R_numerator']/op['R_denominator'],'complete original optimizer/residual field binding')
        require(0<t<2*a*b/(a+b),'finite interior vertex')
        psi=[[Dc[i][j]+F((-1 if i==0 else 1)*(-1 if j==0 else 1),2*q**4) for j in range(3)] for i in range(3)]
        require(psi[0][0]>0 and psi[0][0]*psi[1][1]-psi[0][1]**2>0,'finite rank2 Psi positive')
        require(Dc[0][0]*Dc[1][1]-Dc[0][1]**2<0,'actual cap Delta indefinite, not a PSD premise')
        _,_,EC=even(keys,C);_,_,ED=even(keys,D)
        LS,LV=short(EC,[reps.index(t) for t in ((2,0,0),(3,0,0))],[reps.index((1,0,0)),reps.index((0,1,0))])
        require(LS==[[a,a],[a,a]],'entire original lower a normalization')
        zl=[F(1) if c==0 else F(-1) if c==7 else F(0) for c,z,w0 in reps]
        xl=[row[0]+ell*row[1] for row in LV];alpha=sum(zl[i]*ED[i][j]*zl[j] for i in range(17) for j in range(17))
        cross=sum(zl[i]*ED[i][j]*xl[j] for i in range(17) for j in range(17));xl=[xl[i]-cross/alpha*zl[i] for i in range(17)]
        xu=[h[0]*row[0]+h[1]*row[1]+row[2] for row in W]
        e0=lambda A,x:sum(x[i]*A[i][j]*x[j] for i in range(17) for j in range(17))
        require(e0(EC,xl)+e0(EU,xu)==R,'ENTIRE original two-plane intercept')
        joint=e0(ED,xl)-e0(ED,xu)
        require(joint<-F((1+ell)**2,2*q**4),'stronger original joint derivative margin')
        # Trades are evaluated separately, without averaging arbitrary competitors.
        original_low=[F(0)]*23;original_up=[F(0)]*23
        for ti,g in enumerate(groups):
            for i in g:original_low[i]=xl[ti];original_up[i]=xu[ti]
        def anchor(x,c):return x[keys.index((c,0,0))]
        trades=[]
        for target,opposite in ((2,5),(4,3)):
            rb=2*anchor(original_low,1)*anchor(original_low,target)-2*anchor(original_low,target)*anchor(original_low,opposite)
            rbu=-2*anchor(original_up,1)*anchor(original_up,target)+2*anchor(original_up,target)*anchor(original_up,opposite)
            require(rb==-2*ell and rbu==2*ell and rb+rbu==0,'separate original b/c trade coefficient cancels')
            trades.append([str(rb),str(rbu)])
        require(2*anchor(original_low,2)*anchor(original_low,4)-2*anchor(original_up,2)*anchor(original_up,4)==0,'original B coefficient cancels')
        records.append(dict(q=q,k=k,N=(q*q+13*q+16)//2-k,R=str(R),R_sign=1 if R>0 else -1 if R<0 else 0,
                            t=str(t),ell=str(ell),joint_slope=str(joint),separate_original_trades=trades,all_optimizer_fields=True,all23_stationary_rows=True,all17_minimizer_coordinates=True,all9_Delta_positions=True))
        print('original binding',q,k,'R sign',records[-1]['R_sign'],flush=True)
    out=dict(status='complete finite ORIGINAL cap vector/Delta/dual bindings',records=records,CAS_imported=False,producer_code_used=False,
             trust='counted controls after literal q21 whole-entry binding; not proof of uniformity or all Pell members')
    (P/'cap-binding.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
