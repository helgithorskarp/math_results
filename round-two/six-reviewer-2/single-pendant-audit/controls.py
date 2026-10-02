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
 from forms import tests
 records=[];sign_controls=[]
 for ri in [2,3,4,9,1000]:
  for excess in [0,1,16,257]:
   r=F(ri);l=F(1);q=4*r+excess;z=model(r,l,q);T=tests(r,l,q)
   need(all(z[k]>0 for k in ['mu','alpha','beta','etaP','nuT']),'all5 residual signs')
   need(all(psd(T[k])['rank']==len(T[k])for k in ['anti','triangle','fixed_inverse','final']),'ALL four complete sufficient forms positive')
   records.append(fixed(r,l,q));sign_controls.append([r,q,*[z[k]for k in ['mu','alpha','beta','etaP','nuT']]])
 small=[]
 for r,q in [(F(2),F(4)),(F(3),F(8))]:
  direct=fixed(r,F(1),q);z=model(r,F(1),q);actual=tests(r,F(1),q)['final'];rho=z['rho'];a=-z['Fp']/(3*r);d=z['A']-z['d'];tau=direct['tau'];Tb=direct['Tb']
  actual=[[actual[i][j]+(Tb-tau)*[a,d][i]*[a,d][j]for j in range(2)]for i in range(2)]
  need(psd(actual)['rank']==2,'ENTIRE actual small fixed Schur is PD')
  coarse=tests(r,F(1),q)['final']
  if r==2:
   need(tau==F(80584,361425),'exact exceptional Gaussian tau')
   # Verify that the coarse sufficient form really fails, not an H failure.
   determinant=coarse[0][0]*coarse[1][1]-coarse[0][1]**2
   need(coarse[0][0]<=0 or determinant<=0,'coarse small test must fail as claimed')
  small.append({'r':r,'q':q,'tau':tau,'Tb':Tb,'actual_final':actual,'coarse_final':coarse})
 return {'inverse_controls':records,'uniform_sign_controls':sign_controls,'small_actual_final_controls':small,'whole_inverse':digest(records),'whole_signs':digest(sign_controls),'whole_small':digest(small)}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s controls')));signal.alarm(60);print(json.dumps(canonical(run()),sort_keys=True,separators=(',',':')))
