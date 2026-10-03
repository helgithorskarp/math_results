"""Precisely disclosed own stationary row reconstruction from REVIEW10156.
No native target source or expected record is used.
"""
from fractions import Fraction as Q
from exact import C,F,Z,Poly,need
from retained import constants,root_normals,eval_z,derivative_z,add_dict,shifted

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

