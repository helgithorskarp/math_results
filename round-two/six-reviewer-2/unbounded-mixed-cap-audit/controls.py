"""Independent exact inverse/congruence and analytic-budget controls.
Finite controls validate algebra; the inequalities in PROOF.md are uniform.
"""
from fractions import Fraction as F
from forms import model,arrow
from linear import need,digest,canonical,inverse,mv,form,psd
import json,signal

def fixed(r,l,q):
 z=model(r,l,q);N=z['N'];H=N-1;s=z['s'];m=z['m'];ell=z['ell'];rho=z['rho'];D=N-7;A0=N-q-2;J=A0*(N-4)-3*(q-1)
 G=[[F(0)]*5 for _ in range(5)];dg=[q-1,3,3*r*(q-r),3*l*(q-l),2*l*s/3]
 for i in range(5):G[i][i]=dg[i]
 G[2][3]=G[3][2]=-3*r*l;F0=[[F(0)]*5 for _ in range(5)];F0[0][0]=q*q-1;F0[0][1]=F0[1][0]=3*(q-1);F0[1][1]=9
 for i in [2,3]:
  for j in [2,3]:F0[i][j]=6*G[i][j]
 B=[[H*G[i][j]-F0[i][j] for j in range(5)] for i in range(5)];Bi=inverse(B)
 def I0(a,b):return ((q-1)*(N-4)*a[0]*b[0]+3*(q-1)*(a[0]*b[1]+a[1]*b[0])+3*A0*a[1]*b[1])/J+3*(r*(q-r)*a[2]*b[2]-r*l*(a[2]*b[3]+a[3]*b[2])+l*(q-l)*a[3]*b[3])/D+2*l*s*a[4]*b[4]/(3*H)
 hb=[0,F(1,3),1/(3*r),0,0];vb=[0,F(1,3),0,1/(3*l),1/l];K=[1,(m-3)/3,1,F(1,3),1];E=[x-rho*y for x,y in zip(hb,vb)];cols=[hb,vb,K];vectors=cols+[E]
 need(all(I0(a,b)==form(Bi,mv(G,a),mv(G,b)) for a in vectors for b in vectors),'ALL16 Gaussian inverse pairs')
 diag=[1/(3*r),1/l,ell];S3=[[(diag[i] if i==j else 0)-I0(cols[i],cols[j]) for j in range(3)] for i in range(3)];b=[I0(x,E) for x in cols];Tb=m/(3*r*l);aug=[S3[i]+[b[i]] for i in range(3)]+[b+[Tb-I0(E,E)]];T=[[1,0,0,1],[0,1,0,-rho],[0,0,1,0],[0,0,0,1]];tc=list(map(list,zip(*T)));shifted=[[form(aug,a,b) for b in tc] for a in tc];hc=[[1,-1,0,0],[3*r,l,0,0],[-3*r,-l,1,0],[0,0,0,1]];transformed=[[form(shifted,a,b) for b in hc] for a in hc];need(transformed==arrow(r,l,q),'ALL16 original augmented congruence positions');need(psd(S3)['rank']==3,'S3 PD')
 for weight,v in [(3*r,hb),(l,vb),(1/ell,K)]:
  gv=mv(G,v)
  for i in range(5):
   for j in range(5):B[i][j]-=weight*gv[i]*gv[j]
 tau=form(inverse(B),mv(G,E),mv(G,E));need(tau==I0(E,E)+form(inverse(S3),b,b) and 0<tau<Tb,'ENTIRE Gaussian/Woodbury inverse and strict tau bound');return {'r':r,'l':l,'q':q,'tau':tau,'Tb':Tb,'all_inverse_pairs':16,'all_congruence_positions':16,'whole_augmented':digest(transformed)}

def run():
 records=[];budgets=[]
 for ri in [3,4,9,1000]:
  for li in [2,3,7,1000]:
   for excess in [0,1,16,257]:
    r=F(ri);l=F(li);q=4*(r+l-2)+excess;z=model(r,l,q);s=z['s'];H=z['H'];ell=z['ell'];m=z['m'];t=z['t'];mu=z['mu'];beta=z['beta'];nu=z['nuT'];c=z['c'];d=z['d'];g=z['g'];ast=z['ast'];etaP=z['etaP'];rho=z['rho'];C=z['C']
    need(q/F(5)<mu<q/3 and etaP>2*q/3 and F(3,2)*q<z['alpha']<9*s/4 and F(3,5)*q<beta<2*s/3+5*q/(12*ell**2),'ALL residual budget controls');need(q/5<nu<q/2 and 0<z['nuL']<2*z['w']-q/ell,'ALL standard budget controls')
    Tq=H-q-6;Ts=H-q-3;LL=ast*ast*q/(6*Tq)+c*c*s/(12*Ts)+nu/(2*H)+beta/(8*H);FF=d*d*q/(6*Tq)+c*c*s/(3*t*t*Ts)+nu/(2*H)+beta/(2*H);LF=ast*d*q/(6*Tq)+c*c*s/(6*t*Ts)+nu/(2*H)-beta/(4*H);need(F(1,4)-LL>F(1,16) and F(1,2)-FF>F(3,16) and abs(LF)<F(3,40),'ALL uniform triangle budgets')
    Tb=m/(3*r*l);aZ=-l*z['Fp']/(3*r);bZ=c*l/(9*r*t);dE=z['A']-d;bD=c*(t+2*(r-1))/(6*r*t);T=6*r*s/(H-s);j=l/(3*r*m);k=F(3,2)/r;XZ=(aZ*aZ*Tb+bZ*bZ*T)/j;XD=(dE*dE*Tb+bD*bD*T)/k;need(XZ<F(1,16) and XD<F(13,36) and m*C/H<F(1,4) and 3*beta/(2*H)<F(129,256),'ALL final fixed inverse budgets')
    budgets.append([r,l,q,XZ,XD,LL,FF,LF]);records.append(fixed(r,l,q))
 for l in map(F,[2,3,8,1000]):
  for extra in [0,1,16]:records.append(fixed(F(2),l,4*l+extra))
 margins=[F(1195,5832)-F(1,5),F(2)-F(295,1568)-F(8,27)-F(3,2),F(2,3)-F(691,10368)-F(3,5),F(3,256)-F(9,1600),F(1,16)-F(1,49)-F(1,27),F(1,4)-F(183,784),F(1)-F(13,36)-F(129,256)-F(1,8),F(11,128)-F(13,576)]
 need(all(v>0 for v in margins),'ALL exact endpoint margins');return {'inverse_controls':records,'analytic_budget_controls':budgets,'strict_rational_margins':margins,'whole_inverse':digest(records),'whole_budgets':digest(budgets)}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s controls')));signal.alarm(60);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
