"""Independent Q(zeta36)[mu] anchored primitive, nine roots, and cost.

six-reviewer-1 / independent reviewer. Own field/interval operations reused
from fourth-coercivity-audit; author programs and fixtures are not inputs.
"""
from math import comb
from fractions import Fraction as Q
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from field import E,C,W,need
from intervals import Box,physical_cosine


def clean(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)


def pc(x):return clean([E(x)])
ZERO=();ONE=pc(1);MU=(E(0),E(1))


def pa(*ps):
    out=[E(0)]*max((len(p)for p in ps),default=0)
    for p in ps:
        for j,x in enumerate(p):out[j]=out[j]+x
    return clean(out)


def ps(p,x):return clean([v*x for v in p])


def pm(p,q):
    out=[E(0)]*(len(p)+len(q)-1)if p and q else []
    for j,x in enumerate(p):
        for k,y in enumerate(q):
            if x and y:out[j+k]=out[j+k]+x*y
    return clean(out)


def pp(p,n):
    out=ONE
    for _ in range(n):out=pm(out,p)
    return out


def sa(*ss,n=5):return [pa(*(s[j]if j<len(s)else ZERO for s in ss))for j in range(n+1)]
def sm(a,b,n=5):return [pa(*(pm(a[k],b[j-k])for k in range(j+1)if k<len(a)and j-k<len(b)))for j in range(n+1)]
def ss(a,x):return [ps(v,x)for v in a]


def sp(a,m,n=5):
    out=[ONE]+[ZERO]*n
    for _ in range(m):out=sm(out,a,n)
    return out


def sj(x,n=5):return [pc(x)]+[ZERO]*n
def rec(p):return [v.record()for v in p]
def rs(a):return [rec(p)for p in a]


def cubic_coordinates(v):
    """Full 12-coordinate solve, no guessed real-field decoding."""
    basis=[E(1),C,C*C]
    rows=[[b.v[j]for b in basis]+[v.v[j]]for j in range(12)]
    rank=0
    for col in range(3):
        k=next((j for j in range(rank,12)if rows[j][col]),None)
        need(k is not None,'cubic basis rank')
        rows[k],rows[rank]=rows[rank],rows[k]
        a=rows[rank][col];rows[rank]=[x/a for x in rows[rank]]
        for j in range(12):
            if j!=rank and rows[j][col]:
                a=rows[j][col];rows[j]=[x-a*y for x,y in zip(rows[j],rows[rank])]
        rank+=1
    need(all(not any(r)for r in rows[3:]),'whole cubic-field remainder')
    ans=[rows[j][-1]for j in range(3)]
    need(sum((a*b for a,b in zip(ans,basis)),E(0))==v,'all12 cubic reconstruction')
    return ans


def enclosure(v,c):
    a=cubic_coordinates(v)
    return a[0]+a[1]*c+a[2]*c*c


def constants():
    c=C;y=1/(3*(1+c));x=E(Q(2,3))-y;H=14*y;U=-8*x;rho=(c-5)/3
    uz=(U+rho*H)/8;up=uz-rho*H/2
    w2=(E(Q(2512,27))+Q(5840,9)*c-Q(21392,27)*c*c)/8
    gamma=E(Q(13,36))+Q(1253,72)*c-Q(50,3)*c*c
    m0=-E(Q(17403419,34992))-Q(45702565,17496)*c+Q(180635,54)*c*c
    b0=-E(Q(1162307,23328))-Q(5484833,11664)*c+Q(52426519,93312)*c*c
    M0=E(Q(8148040331,629856))+Q(78878749667,1259712)*c-Q(51194418673,629856)*c*c
    beta0=E(Q(27821775167,17915904))+Q(80418819893,8957952)*c-Q(12650091319,1119744)*c*c
    m1=Q(56,9)*(c-c*c);b1=E(Q(1,2))+2*c
    M1=-E(Q(51583,972))-Q(175385,486)*c+448*c*c
    beta1=E(Q(1771,324))-Q(94039,1296)*c+Q(12347,162)*c*c
    beta2=Q(2,7)*(1+c)
    Bstar=E(Q(2311,108))+Q(4934,27)*c-Q(1976,9)*c*c
    Tstar=-E(Q(60800959,17496))-Q(307083769,17496)*c+Q(10980067,486)*c*c
    Gstar=E(Q(183619658945,2519424))+Q(444829186913,1259712)*c-Q(288729410449,629856)*c*c
    L=-E(Q(101920,243))-Q(1218245,486)*c+Q(251888,81)*c*c
    Gmean=E(Q(340367352475,839808))+Q(808137564635,419904)*c-Q(1052841914857,419904)*c*c
    return locals()


def run(damage=None, fifth_center=0):
    v=constants();checks=[];out={}
    def eq(a,b,name):
        need(a==b,name);checks.append(name)
    c=v['c'];H=v['H'];y=v['y'];x=v['x']
    m=(v['m0'],v['m1']);b=(v['b0'],v['b1']);M=(v['M0'],v['M1'])
    beta=(v['beta0'],v['beta1'],v['beta2'])
    if damage=='third-mean':m=(v['m0'],E(0))
    if damage=='fourth-scale':beta=(v['beta0'],v['beta1'],E(0))
    Az=[ZERO,pc(v['uz']),pa(pc(v['w2']),ps(MU,-Q(1,3))),m,M,pc(fifth_center)]
    Bz=[ZERO,pc(v['up']),pa(pc(v['w2']),MU),m,M,pc(fifth_center)]
    if damage=='unbalanced':Az[2]=pa(pc(v['w2']),ps(MU,-Q(1,2)))
    scale=[ONE,pc(v['gamma']),b,beta,ZERO,ZERO]
    pair2=[ZERO]+ss(sm(scale,scale),H/2)[:5]
    minusA=ss(Az,-1);minusB=ss(Bz,-1)
    # Direct dense derivative: (z-A)^6[(z-B)^2+H eta S^2/2].
    f6=[ss(sp(minusA,6-j),comb(6,j))for j in range(7)]
    f2=[sa(sm(minusB,minusB),pair2),ss(minusB,2),sj(1)]
    der=[[ZERO]*6 for _ in range(9)]
    for j,a in enumerate(f6):
        for k,bp in enumerate(f2):der[j+k]=sa(der[j+k],sm(a,bp))
    primitive=[[ZERO]*6]+[ss(der[j],Q(9,j+1))for j in range(9)]
    anchor=[ONE,pc(-1),ZERO,ZERO,ZERO,ZERO]
    value=[ZERO]*6
    for row in reversed(primitive):value=sa(sm(value,anchor),row)
    primitive[0]=ss(value,-1)
    # Separate translated integral in w=z-A.
    d=sa(Az,ss(Bz,-1));d2=sa(sm(d,d),pair2)
    closed=[[ZERO]*6 for _ in range(10)]
    for power,factor in [(9,sj(1)),(8,ss(d,Q(9,4))),(7,ss(d2,Q(9,7)))]:
        for j in range(power+1):closed[j]=sa(closed[j],ss(sm(factor,sp(minusA,power-j)),comb(power,j)))
    value=[ZERO]*6
    for row in reversed(closed):value=sa(sm(value,anchor),row)
    closed[0]=sa(closed[0],ss(value,-1))
    for j in range(10):eq(primitive[j],closed[j],'whole literal-translated primitive '+str(j))
    value=[ZERO]*6
    for row in reversed(primitive):value=sa(sm(value,anchor),row)
    eq(value,[ZERO]*6,'whole exact marked-root anchor')
    eq(primitive[9],sj(1),'whole monic leading column')
    out['primitive_eta0_to5_by_z_power']=[rs(row)for row in primitive]
    roots=[];normals=[];inward=[]
    for j in range(9):
        z=W**j;root=[pc(z)]+[ZERO]*5
        inv=1/(9*z**8)
        for n in range(1,6):
            resid=[ZERO]*(n+1)
            for row in reversed(primitive):resid=sa(sm(resid,root,n),row,n=n)
            root[n]=ps(resid[n],-inv)
        if damage=='root-fourth' and j==4:root[4]=pa(root[4],ONE)
        resid=[ZERO]*6
        for row in reversed(primitive):resid=sa(sm(resid,root),row)
        eq(resid,[ZERO]*6,'all original root equations '+str(j))
        conj=[tuple(x.conjugate()for x in p)for p in root]
        normal=ss(sa(sm(root,conj),[pc(-1)]),Q(1,2))
        nu=-(E(Q(1,3))+x*z.real()+y*(z*z).real())
        eq(normal[1],pc(nu),'individual first normal '+str(j))
        if j in [3,4,5,6]:
            for n in range(1,5):eq(normal[n],ZERO,'individual active normal '+str((j,n)))
        # All omitted odd epsilon orders vanish; epsilon9 response is independent.
        r9=1-z
        if damage=='inward-sign':r9=-r9
        eq(9*z**8*r9+9*(1-z**8),E(0),'original inward root equation '+str(j))
        n9=(r9*z.conjugate()).real();eq(n9,-(1-z.real()),'individual inward normal '+str(j))
        inward.append({'root':r9.record(),'normal':n9.record()})
        roots.append(rs(root));normals.append(rs(normal))
    out['all_nine_original_roots_eta0_to5']=roots
    out['all_nine_half_normals_eta0_to5']=normals
    out['all_nine_epsilon9_inward']=inward
    # Complete root census plus anchor slot, real reflection at every coefficient.
    eq(roots[0],rs(anchor),'literal original anchor root branch')
    for j in range(1,9):
        reflected=[[v.conjugate().record()for v in p]for p in [tuple(E(row)for row in p)for p in roots[j]]]
        eq(reflected,roots[9-j],'whole original root conjugation '+str(j))
    # Repair columns at BOTH orders and ALL nine labels, from actual primitive.
    columns=[]
    for j in range(9):
        z=W**j;A=1-z.real();B=1-(z*z).real()
        rc=-(1-z**8)*z # -p_repair/(9 z^8)
        rscl=-H*Q(1,7)*(z**7-1)*z
        eq((rc*z.conjugate()).real(),-A,'individual common-center repair '+str(j))
        eq((rscl*z.conjugate()).real(),H*B/7,'individual scale repair '+str(j))
        columns.append({'A':A.record(),'B':B.record(),'center':rc.record(),'scale':rscl.record()})
    out['all_nine_order3_and4_repair_columns']=columns
    det=Q(3,2)*H*Q(1,7)*((1+c)-(2-2*c*c))
    eq(det,2*c-1,'entire two-row determinant')
    # Direct positive scalar branch: reciprocal small gap and inverse pair square.
    gapA=sa(anchor,ss(Az,-1));gapB=sa(anchor,ss(Bz,-1))
    recip=[ONE]+[ZERO]*5
    for n in range(1,6):recip[n]=ps(pa(*(pm(gapA[k],recip[n-k])for k in range(1,n+1))),-1)
    eq(sm(gapA,recip),sj(1),'whole scalar reciprocal branch')
    sq=sa(sm(gapB,gapB),pair2);h=sa(sq,[pc(-1)])
    invsqrt=[ONE]+[ZERO]*5;power=[ONE]+[ZERO]*5;binc=Q(1)
    for n in range(1,6):
        power=sm(power,h);binc*=Q(-(2*n-1),2*n)
        invsqrt=sa(invsqrt,ss(power,binc))
    eq(sm(sm(invsqrt,invsqrt),sq),sj(1),'whole positive inverse-square-root branch')
    F=sa(ss(recip,6),ss(invsqrt,2))
    wanted=[pc(8),pc(E(Q(8,3))+y),pc(v['Bstar']),pc(v['Tstar']),(v['Gstar'],v['L'],E(Q(4,3)))]
    if damage=='scalar-linear':wanted[4]=(v['Gstar'],E(0),E(Q(4,3)))
    for n in range(5):eq(F[n],wanted[n],'entire first-power coefficient '+str(n))
    out['direct_first_power_eta0_to5']=rs(F)
    eq(E(6)+2,E(8),'whole epsilon9 common-center FIRST response')
    mu0=-Q(3,8)*v['L'];difference=Q(3,16)*v['L']**2
    eq(v['Gstar']-difference,v['Gmean'],'whole reduced Gmean')
    eq(pa(pc(v['Gmean']),ps(pp(pa(MU,pc(-mu0)),2),Q(4,3))),F[4],'whole completed mean square')
    w4=1/(c+2*c*c-1);w3=Q(2,3)*(7-(2-2*c*c)*w4)
    if damage=='dual-weight':w4=-w4
    eq(w3*Q(3,2)+w4*(1+c),E(8),'entire positive dual center payment')
    eq(w3*Q(3,2)+w4*(2-2*c*c),E(7),'entire positive dual scale payment')
    out['coefficient_constants']={k:v[k].record()for k in ['Bstar','Tstar','Gstar','L','Gmean']}
    out['coefficient_constants'].update(mu_star=mu0.record(),strict_improvement=difference.record(),w3=w3.record(),w4=w4.record(),determinant=det.record())
    cb=physical_cosine();signs={}
    values={'H':H,'x':x,'y':y,'minus_L':-v['L'],'mu_minus8':mu0-8,'16_minus_mu':16-mu0,'minus_Gstar':-v['Gstar'],'strict_improvement':difference,'minus_Gmean':-v['Gmean'],'w3':w3,'w4':w4,'determinant':det}
    for j in [0,1,2,7,8]:values['inactive_minus_normal_'+str(j)]=E(Q(1,3))+x*(W**j).real()+y*(W**(2*j)).real()
    for j in [3,4,5,6]:values['active_inward_margin_'+str(j)]=1-(W**j).real()
    for name,value in values.items():
        bound=enclosure(value,cb);need(bound.lo>0,'strict physical sign '+name);checks.append('strict physical sign '+name);signs[name]=bound.record()
    out['all_strict_rational_signs']=signs;out['physical_cosine_interval']=cb.record()
    out['check_names']=checks;out['complete']=True
    return out


if __name__=='__main__':
    import argparse,json,hashlib
    a=argparse.ArgumentParser();a.add_argument('--output');a.add_argument('--damage');args=a.parse_args()
    result=run(args.damage);raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    if args.output:
        from pathlib import Path
        Path(args.output).write_bytes(raw)
    print(json.dumps({'complete':True,'checks':len(result['check_names']),'whole_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))
