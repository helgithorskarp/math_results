"""New independent degree-nine quadratic motion algebra and complete records.

Written target formulas exposed; no producer executable or fixture imported.
Own earlier Fraction backend and direct-row routine are explicitly reused.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import C,F,Z,Poly,need
from retained import constants,root_normals,eval_z,derivative_z,add_dict,shifted


def coeff(poly,n):
    return poly.d.get((n,),F(0))


def truncate(poly,order=3):
    return Poly(poly.n,{k:v for k,v in poly.d.items()if k[0]<=order})


def series_power(poly,exponent,order=3):
    """Generalized binomial for constant-one rational field series."""
    need(coeff(poly,0)==1,'Series constant must be one')
    x=poly-1
    answer=Poly.const(1,1)
    term=Poly.const(1,1)
    multiplier=Q(1)
    for k in range(1,order+1):
        multiplier=multiplier*(exponent-k+1)/k
        term=truncate(term*x,order)
        answer=answer+term*multiplier
    return truncate(answer,order)


def derive_stationary(K,damage=None):
    rows=root_normals(K,'wrong_root_second_coefficient'if damage=='curvature'else None)
    normal=rows['active_normals']
    c,H,U0,rho=(K[k]for k in ('c','H','U0','rho'))
    uz=(U0+rho*H)/8
    up=uz-rho*H/2
    need(uz==F(Q(-37,36))+20*c/9-20*c*c/9,'Original six-real correction')
    need(up==F(Q(47,36))-92*c/9+92*c*c/9,'Original pair correction')
    U2=6*uz*uz+2*up*up
    J21=H*up
    J4=H*H/2
    # Solve both ORIGINAL active curvature rows, rather than feed target W,D.
    a,b,d,e=[F(normal[j]['coefficients'][n])for j,n in [(0,'W'),(0,'T'),(1,'W'),(1,'T')]]
    rhs=[]
    for row in normal:
        v={n:F(x)for n,x in row['coefficients'].items()}
        rhs.append(-v['base']-v['J21']*J21-v['J4']*J4)
    determinant=a*e-b*d
    need(determinant!=0,'Both active real rows independent')
    W=(rhs[0]*e-b*rhs[1])/determinant
    D=(a*rhs[1]-rhs[0]*d)/determinant
    if damage=='drift_row':
        D=D+1
    need(a*W+b*D==rhs[0]and d*W+e*D==rhs[1],'Both actual stationary rows solved')
    need(W==F(Q(2512,27))+5840*c/9-21392*c*c/27,'Stationary original W')
    need(D==F(Q(-4270,27))-29492*c/27+4012*c*c/3,'Stationary original D')
    Gamma=(U2-D)/(2*H)
    need(Gamma==F(Q(13,36))+1253*c/72-50*c*c/3,'Actual pair scale from second moment')
    need(K['alpha'].sign()<0 and K['gamma'].sign()>0 and K['kappa'].sign()>0,'Stationary cost positive coefficients')
    # Exact constrained Hessian: pair displacements a,a; six sum-zero
    # middle deviations around -a/3. The norm-sphere correction is included.
    a_morse=(10*K['alpha']/3+9*K['tau'])*H
    middle_morse=-K['alpha']*H
    need(a_morse==9*K['kappa']*H and a_morse.sign()>0 and middle_morse.sign()>0,'Full stationary constrained Hessian')
    return dict(uz=uz,up=up,U2=U2,J21=J21,J4=J4,W=W,D=D,Gamma=Gamma,
                real_row_determinant=determinant,pair_morse=a_morse,middle_morse=middle_morse),rows


def fixed_jet(K,J):
    H,U0,x,y=(K[n]for n in ('H','U0','x','y'))
    g2=add_dict({0:F(9)},shifted(8,9*x),shifted(7,9*y))
    g4=add_dict({0:-36-9*U0+9*H/2},shifted(8,-9*J['W']/8),
                shifted(7,9*(U0*U0-J['D'])/14),
                shifted(6,-3*U0*H/4+3*J['J21']/2),
                shifted(5,9*H*H/40-9*J['J4']/20))
    need(g4.get(5,F(0))==0,'Fixed original fourth-moment cancellation')
    return g2,g4


def all_originals(K,J,rows,damage=None):
    c=C
    omega=Z(2*c*c-1,2*c)
    g2,g4=fixed_jet(K,J)
    df=derivative_z(g2)
    roots=[]
    norms=[]
    firsts=[]
    second=[]
    for j in range(9):
        w=omega**j
        L=-eval_z(g2,w)/(9*w**8)
        need(L==-w/3-K['x']-K['y']/w,'All original first motions')
        drift=-(eval_z(g4,w)+eval_z(df,w)*L+36*w**7*L*L)/(9*w**8)
        # Q=iG/2, W=i*bracket/18, represented without inventing i in Q(c,T).
        G=(1+2*c)*(w**8+w**7-2)+w**6-1
        bracket=-G/w**8
        known=(3+4*c)*w-(1+2*c)*(1+1/w)-1/(w*w)
        need(bracket==known,'All original odd harmonic root equations')
        q2=bracket.norm()/324
        cross=(drift.t*bracket.r-drift.r*bracket.t)/9
        if damage=='cross_sign':cross=-cross
        a=drift.norm()
        norms.append(dict(j=j,a=a.serial(),b=cross.serial(),q2=q2.serial()))
        roots.append(dict(j=j,omega=w.serial(),first=L.serial(),quartic_drift=drift.serial(),i_harmonic_bracket=bracket.serial()))
        firsts.append(L);second.append(drift)
    # This written formula sheet is exposed, not a producer fixture.
    A=F(Q(-13638695,972))-16011613*c/243+20901119*c*c/243
    b2=(F(-1448)-6982*c+8224*c*c)/243
    need(F(norms[2]['a'])==A and F(norms[2]['b'])==b2 and F(norms[2]['q2'])==K['q2'],'Physical winning drift norm and cross coefficient')
    need(A.sign()>0 and b2.sign()<0,'Strict positive motion floor and cusp')
    expected={
        0:(F(0),F(0),F(0)),
        1:(F(Q(-39614,243))-338527*c/162+585536*c*c/243,
           F(Q(-301,81))-740*c/81+356*c*c/27,(13+26*c+16*c*c)/324),
        2:(A,b2,K['q2']),
        3:(F(Q(-410866,81))-11747087*c/486+2548855*c*c/81,
           (F(464)+2894*c-3816*c*c)/81,(1+4*c+4*c*c)/36),
        4:((F(-1653)-8948*c+11396*c*c)/243,
           (F(58)-160*c+160*c*c)/243,4*(1+2*c+c*c)/81)}
    signs=[]
    for j in range(5):
        a,b,q=[F(norms[j][n])for n in ('a','b','q2')]
        need((a,b,q)==expected[j],'Every written coefficient triple')
        if j:
            reflect=norms[9-j]
            need(F(reflect['a'])==a and F(reflect['b'])==-b and F(reflect['q2'])==q,'Entire reflected norm maps')
            need(second[9-j]==second[j].conjugate(),'Original drift reflection')
        if j not in (0,2):need(b.sign()==(-1 if j in(1,3)else 1),'All mixed norm signs')
        if j!=2:
            absb=b if b.sign()>=0 else -b
            gaps=[A-a,-b2-absb,K['q2']-q]
            if damage=='dominance'and j==1:gaps[0]=-gaps[0]
            need(all(x.sign()>0 for x in gaps),'Whole all-real coefficient dominance')
            signs.append(dict(j=j,gaps=[x.serial()for x in gaps]))
    need(second[0]==0 and firsts[0]==-1,'Exact marked original root retained')
    sine=rows['signed_pair_rows']
    for r in sine:
        a,b,d=[F(x)for x in r]
        coefficient=K['k']*F(Q(8,7))+(1 if damage=='odd_closure'else 0)
        need(a*coefficient+b*2*K['k']+d==0,'Both original unaveraged odd rows')
    return dict(all9_original_maps=roots,all9_affine_squared_norms=norms,
                all_competing_pair_coefficient_gaps=signs,winning_A=A.serial(),
                winning_B_over_s=(-b2).serial(),winning_q2=K['q2'].serial()),firsts,second


def literal_witness(K,J,firsts,seconds,damage=None):
    # Literal eight-critical factor and actual anchor, through eta^3.
    eta=Poly.var(2,0);z=Poly.var(2,1)
    W2=J['W']/8
    A=eta*J['uz']+eta**2*W2+eta**3*100
    B=eta*J['up']+eta**2*W2+eta**3*100
    factor=Poly.const(2,1)
    for _ in range(6):factor=truncate(factor*(z-A))
    factor=truncate(factor*truncate((z-B)**2+eta*(K['H']/2)*(1+eta*J['Gamma'])**2))*9
    primitive=Poly(2,{(n,m+1):v/(m+1)for (n,m),v in factor.d.items()})
    a_eta=Poly.const(1,1)-Poly.var(1,0)*(2 if damage=='anchor'else 1)
    anchor=Poly.const(1,0)
    for (n,m),v in primitive.d.items():anchor=anchor+truncate((Poly.var(1,0)**n)*(a_eta**m))*v
    primitive=primitive-Poly(2,{(k[0],0):v for k,v in anchor.d.items()})
    base={m:primitive.d.get((0,m),F(0))for m in range(10)}
    need(base=={m:F(1 if m==9 else -1 if m==0 else 0)for m in range(10)},'Entire anchored zeroth polynomial')
    jets=[{m:primitive.d.get((n,m),F(0))for m in range(10)}for n in range(1,4)]
    g2,g4=fixed_jet(K,J)
    need(all(jets[0][m]==g2.get(m,F(0))for m in range(10)),'Entire literal first anchored jet')
    need(all(jets[1][m]==g4.get(m,F(0))for m in range(10)),'Entire literal second anchored jet')
    omega=Z(2*C*C-1,2*C);third=[];normals=[]
    for j in range(9):
        w=omega**j;L=firsts[j];d=seconds[j]
        e=-(eval_z(jets[2],w)+eval_z(derivative_z(g4),w)*L+
             eval_z(derivative_z(g2),w)*d+
             eval_z(derivative_z(derivative_z(g2)),w)*L*L/2+
             72*w**7*L*d+84*w**6*L**3)/(9*w**8)
        n1=2*(L/w).r
        n2=L.norm()+2*(d/w).r
        n3=2*(e/w).r+2*(L.conjugate()*d).r
        if j in (3,4,5,6):need(n1==0 and n2==0 and n3.sign()<0,'Both actual active third inward normals')
        else:need(n1.sign()<0,'Every remaining original first inward normal')
        third.append(dict(j=j,third=e.serial()))
        normals.append(dict(j=j,first=n1.serial(),second=n2.serial(),third=n3.serial()))
    # FIRST power from literal squared distance; the real six denominators.
    e=Poly.var(1,0)
    real_distance=1-(1+J['uz'])*e-W2*e**2-100*e**3
    pair_distance=1-(1+J['up'])*e-W2*e**2-100*e**3
    pair_square=truncate(pair_distance**2+e*(K['H']/2)*(1+e*J['Gamma'])**2)
    exponent=Q(-1)if damage=='reciprocal_power'else Q(-1,2)
    objective=6*series_power(real_distance,Q(-1))+2*series_power(pair_square,exponent)
    T=F(Q(-2367865,5184))-32430797*C/5184+15660043*C*C/1944
    need(coeff(objective,0)==8 and coeff(objective,1)==K['C']and coeff(objective,2)==K['Bstar']and coeff(objective,3)==T,'Complete actual FIRST-power cubic objective')
    return dict(entire_primitive=primitive.serial(),all9_third_original_maps=third,
                all9_actual_inward_normals=normals,real_denominator=real_distance.serial(),
                pair_squared_distance=pair_square.serial(),entire_objective=objective.serial(),T100=T.serial())


def run(damage=None):
    K=constants()
    J,rows=derive_stationary(K,damage)
    originals,L,d=all_originals(K,J,rows,damage)
    witness=literal_witness(K,J,L,d,damage)
    return dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',
                field='Q(c),8c^3-6c-1; T=i*sin(pi/9), T^2=c^2-1; physical c in(15/16,47/50)',
                constants={n:x.serial()for n,x in K.items()},
                stationary_original_values={n:x.serial()for n,x in J.items()},
                complete_active_original_rows=rows,quadratic_motion=originals,literal_fixed100_witness=witness)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,separators=(',',':')))
