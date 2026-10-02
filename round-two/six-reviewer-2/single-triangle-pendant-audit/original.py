"""Fresh literal original-set Gram, entire lift, frame and repair audit.

New target code/certificates never imported. All support is determined
from actual bitmask intersections, not researcher partition labels.
Fixed literal guard: n3..6, 2<=l<=n-1, N<=80; each phase45s.
"""
from fractions import Fraction as F
import argparse,json,signal
from linear import need,digest,canonical,dot,psd,mv,inverse,form
from formulas import model

def add(*vs):
 z={}
 for v in vs:
  for k,a in v.items():z[k]=z.get(k,F(0))+a
 return {k:a for k,a in z.items()if a}
def scale(a,v):return {k:a*x for k,x in v.items()if a*x}
def unit(i):return {i:F(1)}

def seed(n,l):
 need(type(n)is int and 3<=n<=6 and type(l)is int and 2<=l<=n-1,'fixed literal n3..6/l2..n-1');q=2**(n-1);f=model(F(q),F(l));N=f['N'];need(N<=80,'fixed literal N<=80');N=int(N);old=2*q-1;m=l+3;s=F(q+3)
 X=(1<<n)-1;marks=list(range(l+1));u=1<<n;v=1<<(n+1);bs=[1<<(n+2+j)for j in range(l)]
 sets=list(range(1,X+1))+[1|u,1|v,1|u|v]+[(1<<(j+1))|bs[j]for j in range(l)]+[u,v,u|v]+bs;need(len(sets)==N-1 and len(set(sets))==N-1,'complete actual distinct nonempty domain')
 t0=old;z0=t0+3;r0=z0+l;dim=r0+m;need(dim==N-1,'formal coordinate census')
 G={i:F(1)for i in range(old)};full=unit(old-1)
 H=[{i:F(-1)for i,A in enumerate(range(1,X+1))if A>>j&1}for j in marks]
 hx=scale(F(1,3),H[0]);T=[unit(t0+j)for j in range(3)];Z=[unit(z0+j)for j in range(l)];Vt=[add(hx,a)for a in T];Vp=[add(scale(F(1,3),H[j+1]),Z[j])for j in range(l)];vb=scale(F(1,l),add(*Vp));K=add(G,scale(3,hx),scale(l,vb));E=add(hx,scale(-f['rho'],vb));Js=[add(a,scale(-1,vb))for a in Vp]
 p1=add(scale(-F(1,l+4),K),scale(f['A'],E),scale(f['c'],T[1]));p2=add(scale(-F(1,l+4),K),scale(f['A'],E),scale(f['c'],T[0]));p3=add(scale(-F(1,l+4),K),scale(f['d'],E));pp=[add(scale(-F(1,l+4),K),scale(f['Fp'],E),scale(f['g'],Js[j]),scale(f['c']/l,T[2]))for j in range(l)]
 W=[[F(0)]*m for _ in range(m)]
 for i in range(m):
  for j in range(m):
   if i<3 and j<3:
    ai=[F(1,2),F(-1,2),F(0)][i];aj=[F(1,2),F(-1,2),F(0)][j];bi=[F(-1,2),F(-1,2),F(1)][i];bj=[F(-1,2),F(-1,2),F(1)][j];W[i][j]=f['mu']+ai*aj*f['alpha']+bi*bj*f['beta']
   elif i>=3 and j>=3:W[i][j]=9*f['mu']/l**2+f['nu']*(F(i==j)-F(1,l))
   else:W[i][j]=-3*f['mu']/l
 need(all(sum(row)==0 for row in W),'whole balanced private residual')
 def gram_action(a):
  out={};total=sum(a.get(i,F(0))for i in range(old))
  for i,A in enumerate(range(1,X+1)):
   comp=(X^A)-1;out[i]=s*a.get(i,F(0))+(q-3)*a.get(comp,F(0))if A!=X else s*a.get(i,F(0))
   out[i]-=total
  tsum=sum(a.get(t0+j,F(0))for j in range(3))
  for j in range(3):out[t0+j]=s*(a.get(t0+j,F(0))-tsum/3)
  for j in range(l):out[z0+j]=2*s*a.get(z0+j,F(0))/3
  for i in range(m):out[r0+i]=sum(W[i][j]*a.get(r0+j,F(0))for j in range(m))
  return {i:x for i,x in out.items()if x}
 def ip(a,b):ab=gram_action(b);return sum(x*ab.get(i,F(0))for i,x in a.items())
 priv=[add(a,unit(r0+j))for j,a in enumerate([p1,p2,p3]+pp)];columns=[unit(i)for i in range(old)]+Vt+Vp+priv
 acts=[gram_action(a)for a in columns];C=[[sum(x*acts[j].get(k,F(0))for k,x in a.items())for j in range(N-1)]for a in columns]
 total=add(*columns);empty=scale(-1,total);need(ip(add(total,scale(-F(1,l+4),K)),add(total,scale(-F(1,l+4),K)))==0,'complete actual empty vector, zero formal kernel handled')
 return locals()

def lift(C):
 rows=[sum(row)for row in C];q00=sum(rows);return [[q00]+[-x for x in rows]]+[[-rows[i]]+list(row)for i,row in enumerate(C)]
def basic(n,l,which):
 a=seed(n,l);f=a['f'];N=a['N'];C=[list(row)for row in a['C']];W=a['W'];m=a['m'];r0=a['r0'];s=f['s'];h=N-s;fullsets=[0]+a['sets']
 need(all(sum((B&A)==A for B in fullsets)>=1 for A in fullsets),'domain contains each actual set')
 need(all(B in fullsets for A in fullsets for B in range(A+1)if B&A==B),'every downset submember')
 stars=[sum(bool(A>>i&1)for A in fullsets)for i in range(n+2+l)];need(stars[0]==s and max(stars[1:])<s,'unique actual maximum star and every private/old star')
 need(psd(W)['rank']==m-1,'complete balanced residual rank')
 inv=inverse([row[:-1]for row in W[:-1]]);u=[F(i<3)for i in range(m-1)];kappa=form(inv,u,u);closed=9*F(l-1,l)/f['nu']+3/(l*f['Cmean']);need(kappa==closed>0,'ENTIRE deleted inverse kappa agrees with independently solved system')
 delta=F(0)if which=='seed'else (1/(12*N*(1+kappa))if which=='old'else 1/(4*(8+kappa)))
 if delta:
  # Locate actual endpoints by SETS, independently of source order.
  endpoints=[a['u'],a['v'],a['u']|a['v']];last=a['bs'][-1];j=a['sets'].index(last)
  for endpoint in endpoints:
   i=a['sets'].index(endpoint);need(endpoint&last==0,'repair pairs are actually disjoint');C[i][j]+=delta;C[j][i]+=delta
 Q=lift(C);L=[[F(1)+Q[i][j]for j in range(N)]for i in range(N)];M=[[(L[i][j]-s*F(i==j))/h for j in range(N)]for i in range(N)];P=[[F(i==j)-F(1,N)for j in range(N)]for i in range(N)]
 need(all(sum(row)==0 for row in Q),'EVERY actual lifted Q row');need(all(sum(row)==1 for row in M),'EVERY original regularity row')
 need(all(M[i][j]==M[j][i]and (not(fullsets[i]&fullsets[j])or M[i][j]==0)for i in range(N)for j in range(N)),'EVERY original symmetry/intersection/diagonal entry')
 lower=psd(L);expected=N-2 if which=='seed'else N-1;need(lower['rank']==expected,'whole lower rank')
 gap=F(1)if which=='seed'else F(3,4)
 cap=[[(N-gap)*P[i][j]-Q[i][j]for j in range(N)]for i in range(N)];upper=psd(cap);need(upper['rank']==N-1,'ENTIRE original seed/repaired cap gap')
 centered=[F(bool(A&1))-s/N for A in fullsets];need(all(v==0 for v in mv(L,centered)),'all-real centered-star lower kernel on every original row')
 if delta:
  seedQ=lift(a['C']);difference=[[Q[i][j]-seedQ[i][j]for j in range(N)]for i in range(N)]
  # Recompute the full difference independently from actual endpoint rows.
  x=[F(-3)]+[F(A in endpoints)for A in a['sets']];y=[F(-1)]+[F(A==last)for A in a['sets']]
  need(all(difference[i][j]==delta*(x[i]*y[j]+y[i]*x[j])for i in range(N)for j in range(N)),'EVERY whole repair entry, actual empty included')
  need(6*delta-kappa*delta**2>0 and (8*delta<F(1,4)if which=='new'else 3*N*delta<F(1,4)),'exact residual and whole cap perturbation margin')
 return {'n':n,'l':l,'N':N,'phase':which,'all_original_positions':N*N,'entire_C_sha256':digest(C),'entire_Q_sha256':digest(Q),'entire_M_sha256':digest(M),'entire_gap_sha256':digest(cap),'stars':stars,'lower':lower,'whole_gap_rank':upper,'kappa':kappa,'delta':delta,'whole_balanced_residual_sha256':digest(W)}

def physical(n,l):
 a=seed(n,l);f=a['f'];q=a['q'];N=a['N'];ip=a['ip'];cols=a['columns']+[a['empty']];T=a['T'];H=a['H'];r0=a['r0'];Z=a['Z'];Wv=[unit(r0+j)for j in range(l+3)]
 gp=scale(F(1,2),add(a['G'],scale(-1,a['full'])));h0=scale(F(-1,2),add(a['G'],a['full']));As=[add(x,scale(-1,h0))for x in H];TA=add(T[0],scale(-1,T[1]));TS=add(T[0],T[1],scale(-2,T[2]));WA=add(Wv[0],scale(-1,Wv[1]));M0=scale(F(1,3),add(*Wv[:3]));WF=add(Wv[2],scale(-1,M0));fixed=[gp,h0,As[0],add(*As[1:]),TS,add(*Z),WF,M0];anti=[TA,WA];standard=[add(As[1],scale(-1,As[j+2]))for j in range(l-1)]+[add(Z[0],scale(-1,Z[j+1]))for j in range(l-1)]+[add(Wv[3],scale(-1,Wv[j+4]))for j in range(l-1)]
 basis=anti+fixed+standard;Gram=[[ip(x,y)for y in basis]for x in basis];table=[[ip(x,c)for c in cols]for x in basis];frame=[[dot(x,y)for y in table]for x in table];need(psd(Gram)['rank']==3*l+7,'ENTIRE changed Gram rank and dimensions')
 need(psd([[(N-1)*Gram[i][j]-frame[i][j]for j in range(len(basis))]for i in range(len(basis))])['rank']==3*l+7,'ENTIRE physical changed cap, no quotient only')
 for i in range(len(basis)):
  for j in range(len(basis)):
   if (i<2 and j>=2)or(2<=i<10 and j>=10):need(Gram[i][j]==frame[i][j]==0,'full sector cross orthogonality')
 antiG=[2*f['s'],f['alpha']]
 need(all(((N-1)*Gram[i][j]-frame[i][j])/(antiG[i]*antiG[j])==f['anti'][i][j]for i in range(2)for j in range(2)),'ALL4 physical anti inverse-Gram congruence positions')
 gamma=[[F(0)]*8 for _ in range(8)];diags=[q-1,3,3*(q-1),3*l*(q-l),6*f['s'],2*l*f['s']/3,f['beta'],f['mu']]
 for i in range(8):gamma[i][i]=diags[i]
 gamma[2][3]=gamma[3][2]=F(-3*l);need([[Gram[i+2][j+2]for j in range(8)]for i in range(8)]==gamma,'EVERY fixed8 Gram position')
 F0=[[F(0)]*8 for _ in range(8)];F0[0][0]=q*q-1;F0[0][1]=F0[1][0]=3*(q-1);F0[1][1]=9
 for i in [2,3]:
  for j in [2,3]:F0[i][j]=6*gamma[i][j]
 def embed(v):return dict(zip([0,1,2,3,5],v))
 hx=[F(embed(f['hx']).get(i,0))for i in range(8)];vb=[F(embed(f['vb']).get(i,0))for i in range(8)];K=[F(embed(f['K']).get(i,0))for i in range(8)];Ec=[F(embed(f['E']).get(i,0))for i in range(8)];ts=[F(i==4)for i in range(8)];wf=[F(i==6)for i in range(8)];mean=[F(i==7)for i in range(8)];zp=[-l*f['Fp']*Ec[i]/3+f['c']*ts[i]/9+mean[i]for i in range(8)];di=[(f['A']-f['d'])*Ec[i]+f['c']*ts[i]/6-F(3,2)*wf[i]for i in range(8)]
 grouped=[list(row)for row in F0]
 for weight,vec in [(F(1,6),ts),(3,hx),(l,vb),(F(1,l+4),K),(F(3*(l+3),l),zp),(F(2,3),di)]:
  gvec=mv(gamma,vec)
  for i in range(8):
   for j in range(8):grouped[i][j]+=weight*gvec[i]*gvec[j]
 need(grouped==[[frame[i+2][j+2]for j in range(8)]for i in range(8)],'EVERY whole original fixed8 grouping entry, including ACTUALempty')
 base=[[(N-1)*gamma[i][j]-F0[i][j]for j in range(8)]for i in range(8)];tsg=mv(gamma,ts)
 for i in range(8):
  for j in range(8):base[i][j]-=tsg[i]*tsg[j]/6
 oldix=[0,1,2,3,5];base5=[[base[i][j]for j in oldix]for i in oldix];inv=inverse(base5);g5=[[gamma[i][j]for j in oldix]for i in oldix];vectors=f['C']+[f['E']]
 need(all(form(inv,mv(g5,x),mv(g5,y))==f['I0'](x,y)for x in vectors for y in vectors),'ALL16 direct5 Gaussian inverse formula pairs')
 for weight,v in [(3,f['hx']),(l,f['vb']),(F(1,l+4),f['K'])]:
  gv=mv(g5,v)
  for i in range(5):
   for j in range(5):base5[i][j]-=weight*gv[i]*gv[j]
 tau=form(inverse(base5),mv(g5,f['E']),mv(g5,f['E']));wood=f['I0'](f['E'],f['E'])+form(inverse(f['S3']),f['b'],f['b']);need(tau==wood<f['Tb'],'exact5 inverse /3Woodbury tau and strict bound')
 # Entire nonorthogonal pendant-difference metric, not only one copy.
 stdg=[6*q,4*f['s']/3,2*f['nu']]
 stdD=[6*q*(N-7),4*f['s']*(N-1)/3,2*f['nu']*(N-1)];b=[q,2*f['s']/3,0];p=[f['g']*q,2*f['s']*f['g']/3,f['nu']]
 for i in range(3*(l-1)):
  for j in range(3*(l-1)):
   ci,ri=divmod(i,l-1);cj,rj=divmod(j,l-1);metric=F(2 if ri==rj else 1,2)
   need(Gram[10+i][10+j]==(stdg[ci]*metric if ci==cj else 0),'EVERY standard copy cross Gram tensor')
   sc=(stdD[ci]if ci==cj else 0)-2*b[ci]*b[cj]-2*p[ci]*p[cj]
   need((N-1)*Gram[10+i][10+j]-frame[10+i][10+j]==sc*metric,'EVERY standard complete cap tensor position')
 # Exact old eigenactions on complete proper-pair constant/antisymmetric
 # bases, with marked directions projected out for the latter.
 pairs=[(A,a['X']^A)for A in range(1,a['X'])if A<(a['X']^A)];oldframe=a['gram_action'];untouched=[]
 pairconstant=[add(unit(A-1),unit(B-1),scale(-1,unit(pairs[0][0]-1)),scale(-1,unit(pairs[0][1]-1)))for A,B in pairs[1:]]
 antis=[add(unit(A-1),scale(-1,unit(B-1)))for A,B in pairs];Ag=[[ip(x,y)for y in As]for x in As];Ainv=inverse(Ag)
 for raw in antis:
  coeff=mv(Ainv,[ip(x,raw)for x in As]);w=add(raw,*(scale(-c,x)for c,x in zip(coeff,As)))
  if ip(w,w):untouched.append(w)
 for eig,vectors in [(2*q,pairconstant),(6,untouched)]:
  for vec in vectors:
   need(all(ip(vec,x)==0 for x in basis),'every untouched vector orthogonal to all changed coordinates')
   # Every original physical frame action tested through every original column.
   products=[ip(vec,x)for x in cols]
   action=add(*(scale(t,x)for t,x in zip(products,cols)))
   need(all(ip(add(action,scale(-eig,vec)),x)==0 for x in cols),'EVERY whole original untouched eigenaction')
 return {'n':n,'l':l,'N':N,'changed_dimension':len(basis),'whole_changed_Gram_sha256':digest(Gram),'whole_changed_frame_sha256':digest(frame),'whole_grouped_fixed8_sha256':digest(grouped),'complete_table_sha256':digest(table),'all_changed_positions':len(basis)**2,'all_fixed_positions':64,'all_inverse_pairs':16,'tau':tau,'Tb':f['Tb'],'untouched_pair_constant_directions':len(pairconstant),'untouched_antisymmetric_spanning_vectors':len(untouched),'all_untouched_eigenaction_positions':(len(pairconstant)+len(untouched))*N}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('n',type=int);p.add_argument('l',type=int);p.add_argument('phase',choices=['seed','old','new','physical']);a=p.parse_args();signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s literal original phase')));signal.alarm(45);x=physical(a.n,a.l)if a.phase=='physical'else basic(a.n,a.l,a.phase);print(json.dumps(canonical(x),sort_keys=True,separators=(',',':')))
