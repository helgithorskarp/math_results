"""Exact controls of the ordinary all-count inequalities; uniform proof is separate."""
from fractions import Fraction as F
from model import forms
from sectors import parameters
from exact import require,psd_rank

def constants():
    margins={
      'mean_lower':F(1195,5832)-F(1,5),
      'etaP_lower':F(68,81)-F(2,3),
      'etaP_coefficient':F(4)-F(5,4)-F(27,98)-F(64,27),
      'alpha_lower':F(2)-F(295,1568)-F(8,27)-F(3,2),
      'alpha_upper':F(1,4)-F(207,1152),
      'beta_lower':F(2,3)-F(691,10368)-F(3,5),
      'triangle_projection_LL':F(1,80)-F(3,1568)-F(1,108),
      'triangle_projection_FF':F(1,72)-F(1,96)-F(1,432),
      'triangle_projection_LF':F(1,100)-F(1,224)-F(1,216),
      'beta_ratio':F(1,4096)-F(5,27648),
      'triangle_diagonal1':F(1,4)-F(1,80)-F(1,8)-F(1,24)-F(1,4096)-F(1,16),
      'triangle_diagonal2':F(1,2)-F(1,72)-F(1,8)-F(1,6)-F(1,1024)-F(3,16),
      'triangle_cross_upper':F(3,40)-F(1,100)-F(1,16),
      'triangle_cross_lower':F(3,40)-F(1,100)+F(2,75)-F(1,12)-F(1,2048),
      'triangle_determinant':F(3,256)-F(9,1600),
      'fixed_Z_budget':F(1,16)-F(1,49)-F(1,27),
      'fixed_D_budget':F(1,4)-F(3,16)-F(1,28)-F(1,98),
      'fixed_beta_ratio':F(129,256)-F(1,2)-F(5,2304),
      'fixed_D_diagonal':F(1)-F(13,36)-F(129,256)-F(1,8),
      'fixed_determinant':F(11,128)-F(13,576)}
    require(all(z>0 for z in margins.values()),'every exact written constant margin strictly positive')
    require(margins['alpha_lower']==F(659,42336),'exact alpha lower constant')
    require(margins['beta_lower']==F(1,51840),'exact beta lower constant')
    require(margins['triangle_determinant']==F(39,6400),'exact standard determinant constant')
    require(margins['fixed_determinant']==F(73,1152),'exact fixed determinant constant')
    return {k:str(v) for k,v in margins.items()}

def scalar(q,r,l):
    require(type(r) is int and type(l) is int and r>=3 and l>=2 and q>=4*(r+l-2),'analytic r>=3/l>=2 domain')
    p=parameters(q,r,l,'cap-harmonic');f=forms(q,r,l)
    q,s,w,t,ell,rho=[p[k] for k in ('q','s','w','t','ell','rho')]
    d,g,c,A,ast,E2,Di2,common=[p[k] for k in ('d','g','c','A','ast','E2','Di2','common')]
    X=A*A*E2+ast*ast*Di2;Y=d*d*(E2+Di2);Z=A*d*E2+ast*d*Di2
    beta=2*s/3-8*d*d*q/27+d*g*rho*w/(3*r)-d*d*rho*rho*w/l-4*s*c*c*(r-1)/(9*t*t)
    alpha=2*s-4*X+2*Z+2*Y-8*s*c*c/3+4*s*c*c*(r-1)/(3*t*t)
    mu=(q-3*common-d*d*q/9-d*g*rho*w/r-2*s*c*c*(r-1)/(3*t*t))/3
    etaP=w-common-g*g*(w+q/(3*r*rho*rho))-2*s*c*c*r/(3*t*t)
    require((alpha,beta,mu,etaP)==(p['alpha'],p['beta'],p['mu'],p['etaP']),'all four unsimplified/simplified exact scalar identities')
    require(ast==((3-2*r)*d-3*l*g/(r*rho))/(6*(r-1)),'exact standard projection simplification')
    require(p['etaL']==mu+(alpha+beta)/4 and p['etaF']==mu+beta,'both exact residual diagonals')
    require(F(3,2)*q<alpha<F(9,4)*s,'both uniform alpha budgets')
    require(F(3,5)*q<beta<2*s/3+5*q/(12*ell*ell),'both uniform beta budgets')
    require(q/5<mu<q/3 and p['nuT']>mu and p['nuT']<q/2,'all strict mean/standard triangle budgets')
    require(abs(A)<=F(3,14) and abs(ast)<=F(3,28),'both exact projection bounds')
    require(X<=F(59,1568)*q and Y<=F(69,8)*q/(ell*ell) and 2*abs(Z)<=X+Y,'uniform quadratic budgets')
    require(f['anti'][0][0]>F(4,9) and f['anti'][1][1]>F(7,18),'both anti diagonal budgets')
    require(f['pendant'][0][0]>F(1,4) and f['pendant'][1][1]>1/(10*ell),'both pendant diagonal budgets')
    require(abs(f['pendant'][0][1])<1/(4*ell),'pendant cross budget')
    require(f['triangle'][0][0]>F(1,16) and f['triangle'][1][1]>F(3,16),'both triangle diagonal budgets')
    require(abs(f['triangle'][0][1])<F(3,40),'triangle cross budget')
    require(f['XZ']<F(1,16) and f['XD']<F(13,36),'both conditional fixed non-diagonal budgets')
    require(f['final'][0][0]/f['j']>F(11,16) and f['final'][1][1]/f['k']>F(1,8),'both normalized fixed diagonals')
    require(f['final'][0][1]**2/(f['j']*f['k'])<F(13,576),'normalized fixed cross square')
    require(all(psd_rank(f[name])==len(f[name]) for name in ('anti','pendant','triangle','augmented','final')),'all complete sufficient forms strictly positive')
    return {'r':r,'l':l,'q':str(q),'alpha':str(alpha),'beta':str(beta),'mu':str(mu),
            'etaP':str(etaP),'nuT':str(p['nuT']),'nuL':str(p['nuL']),'C':str(p['cross']),
            'XZ':str(f['XZ']),'XD':str(f['XD'])}
