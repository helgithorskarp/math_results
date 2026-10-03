"""Credited reusable direct original-row algebra from our independently published
moving-budget audit e2234154. No producer code or record is imported."""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import C,F,Z,Poly,need

def constants():
    c = C
    y = 1/(3*(1+c))
    x = F(Q(2,3))-y
    H,U0 = 14*y,-8*x
    k,rho = -7*(1+2*c)/18,(c-5)/3
    alpha = F(Q(-527,360))+41*c/90+13*c*c/90
    tau = (k+rho)**2/2
    B = F(Q(2311,108))+4934*c/27-1976*c*c/9
    E = F(Q(6653,324))+23915*c/486-15839*c*c/243
    K1 = B-alpha*H*H/2
    K0 = K1-(U0+rho*H)**2/16
    return dict(c=c,y=y,x=x,H=H,U0=U0,k=k,rho=rho,alpha=alpha,tau=tau,
                Bstar=B,KE=E,K1=K1,K0=K0,sigma=alpha+rho*rho/2,
                gamma=tau+5*alpha/9,kappa=tau+10*alpha/27,
                q2=(8+25*c+20*c*c)/162,C=F(Q(8,3))+y)

def eval_z(polynomial, value):
    return sum((Z(coefficient)*value**exponent for exponent,coefficient in polynomial.items()),Z(0))

def derivative_z(polynomial):
    return {n-1:a*n for n,a in polynomial.items() if n}

def shifted(n, coefficient):
    return {n:F(coefficient),0:-F(coefficient)}

def add_dict(*polynomials):
    out = {}
    for p in polynomials:
        for k,v in p.items():
            out[k] = out.get(k,F(0))+v
    return out

def root_normals(K, damage=None):
    """Solve the actual coefficient equation at every ninth-root label.

    For p=z^9-1+eta*f+eta^2*g, solve first and second displacements
    directly, then form the coefficient of half the squared modulus.
    Five original g4 coefficient directions are retained separately.
    """
    c,x,y,H,U0 = (K[n] for n in ('c','x','y','H','U0'))
    omega = Z(2*c*c-1,2*c)
    need(omega**9==1 and omega!=1,'Ninth-root realization')
    f = add_dict({0:F(9)},shifted(8,9*x),shifted(7,9*y))
    g = dict(
        base=add_dict({0:-36-9*U0+9*H/2},shifted(7,9*U0*U0/14),
                      shifted(6,-3*U0*H/4),shifted(5,9*H*H/40)),
        W=shifted(8,Q(-9,8)),T=shifted(7,Q(-9,14)),
        J21=shifted(6,Q(3,2)),J4=shifted(5,Q(-9,20)))
    if damage=='wrong_root_second_coefficient':
        curvature = 35
    else:
        curvature = 36
    rows = []
    for j in (3,4):
        w = omega**j
        first = -eval_z(f,w)/(9*w**8)
        values = {}
        for label,poly in g.items():
            correction = eval_z(poly,w)
            if label=='base':
                correction = correction+curvature*w**7*first*first+eval_z(derivative_z(f),w)*first
            second = -correction/(9*w**8)
            values[label] = (second/w).r+(first.norm()/2 if label=='base' else F(0))
        need((first/w).r==0,'Active first radial coefficient does not vanish')
        A,B = 1-w.r,1-(w*w).r
        need(values['W']==-A/8 and values['T']==-B/14,'Actual active linear rows')
        need(values['J21']==(1-(w**6).r)/6,'Actual mixed-moment normal')
        need(values['J4']==-(1-(w**5).r)/20,'Actual fourth-moment normal')
        rows.append(dict(j=j,first=first.serial(),coefficients={n:a.serial()for n,a in values.items()}))
    d = 2*c*c-1
    w4 = 1/(c+d)
    w3 = (F(7)-(1-d)/(c+d))*Q(2,3)
    need(w3.sign()>0 and w4.sign()>0,'Positive original dual weights')
    weighted = {}
    for label in g:
        weighted[label] = sum((F(row['coefficients'][label])*weight for row,weight in zip(rows,(w3,w4))),F(0))
    need(weighted['W']==-1 and weighted['T']==F(Q(-1,2)),'Both exact dual rows')
    need(weighted['base']+8+2*U0-3*H/2==K['K0'],'Direct curvature constant')
    need(weighted['J21']-F(Q(3,2))==K['rho'],'Direct original mixed-cost coefficient')
    need(weighted['J4']+F(Q(3,8))==K['sigma'],'Direct fourth-cost coefficient')
    sine_rows = []
    for j in (3,4):
        row = ((omega**j).t/8,(omega**(2*j)).t/14,(omega**(6*j)).t/18)
        need(row[0]*8*K['k']/7+row[1]*2*K['k']+row[2]==0,'Unaveraged signed cubic constraint')
        sine_rows.append(row)
    determinant = sine_rows[0][0]*sine_rows[1][1]-sine_rows[1][0]*sine_rows[0][1]
    need(determinant!=0,'Independent unaveraged pair rows')
    motion = []
    for j in range(9):
        w = omega**j
        T = w*(3+4*c)-(1+w**(-1))*(1+2*c)-w**(-2)
        norm = T.norm()/324
        gap = K['q2']-norm
        need(gap==0 if j in(2,7) else gap.sign()>0,'Every original motion norm/winning label')
        motion.append(dict(j=j,complex_bracket=T.serial(),squared_norm=norm.serial(),gap=gap.serial()))
    return dict(active_normals=rows,weights=[w3.serial(),w4.serial()],
                weighted_normal={n:a.serial()for n,a in weighted.items()},
                signed_pair_rows=[[a.serial()for a in row]for row in sine_rows],
                signed_pair_determinant=determinant.serial(),all9_motion=motion)
