"""Definition-level mixed attachment matrix audit, no new author imports.
Formal sparse Gram construction adapted from OWN9723 original.py.
Fixed literal n<=6,N<=96; exact Fraction arithmetic, per-phase60s.
"""
from fractions import Fraction as F
from linear import need,digest,canonical,mv,inverse,form,psd,dot
from forms import model
import argparse,json,signal

def add(*vs):
 z={}
 for v in vs:
  for k,a in v.items():z[k]=z.get(k,F(0))+a
 return {k:a for k,a in z.items() if a}
def scale(a,v):return {k:a*x for k,x in v.items() if a*x}
def unit(i):return {i:F(1)}
def seed(n,r,l):
 need(all(type(x)==int for x in [n,r,l]) and 3<=n<=6 and r>=2 and l==1 and r+1<=n,'fixed literal domain');q=2**(n-1);f=model(F(r),F(l),F(q));N=int(f['N']);need(N<=96,'fixed literal96 limit');old=2*q-1;m=3*r+l;X=(1<<n)-1;s=f['s'];w=f['w'];ell=f['ell'];t=f['t']
 us=[1<<(n+2*i) for i in range(r)];vs=[1<<(n+2*i+1) for i in range(r)];bs=[1<<(n+2*r+j) for j in range(l)]
 marked=[(1<<i)|a for i in range(r) for a in [us[i],vs[i],us[i]|vs[i]]]+[(1<<(r+j))|bs[j] for j in range(l)]
 private=[a for i in range(r) for a in [us[i],vs[i],us[i]|vs[i]]]+bs;sets=list(range(1,X+1))+marked+private;need(len(sets)==N-1 and len(set(sets))==N-1,'ALL distinct actual sets')
 t0=old;z0=t0+3*r;r0=z0+l;G={i:F(1) for i in range(old)};full=unit(old-1);Hs=[{i:F(-1) for i,A in enumerate(range(1,X+1)) if A>>j&1} for j in range(r+l)];hs=[scale(F(1,3),x) for x in Hs[:r]];Ts=[[unit(t0+3*i+j) for j in range(3)] for i in range(r)];Z=[unit(z0+j) for j in range(l)];Vt=[add(hs[i],a) for i in range(r) for a in Ts[i]];Vp=[add(scale(F(1,3),Hs[r+j]),Z[j]) for j in range(l)];hbar=scale(F(1,r),add(*hs));vbar=scale(F(1,l),add(*Vp));K=add(G,*Vt,*Vp);E=add(hbar,scale(-f['rho'],vbar));Ds=[add(x,scale(-1,hbar)) for x in hs];Js=[add(x,scale(-1,vbar)) for x in Vp]
 projections=[]
 for i in range(r):
  base=scale(-1/ell,K)
  projections += [add(base,scale(f['A'],E),scale(f['ast'],Ds[i]),scale(f['c'],Ts[i][1])),add(base,scale(f['A'],E),scale(f['ast'],Ds[i]),scale(f['c'],Ts[i][0])),add(base,scale(f['d'],E),scale(f['d'],Ds[i]),scale(f['c']/t,add(*(Ts[k][2] for k in range(r) if k!=i))))]
 projections += [add(scale(-1/ell,K),scale(f['Fp'],E),scale(f['g'],Js[j]),scale(f['c']/t,add(*(T[2] for T in Ts)))) for j in range(l)]
 amean=(l*f['C']-3*f['mu'])/(3*(r-1));bmean=F(0);W=[[F(0)]*m for _ in range(m)]
 aa=[F(1,2),F(-1,2),F(0)];bb=[F(-1,2),F(-1,2),F(1)]
 for i in range(m):
  for j in range(m):
   if i<3*r and j<3*r:
    ti,ri=divmod(i,3);tj,rj=divmod(j,3);W[i][j]=(f['mu']+aa[ri]*aa[rj]*f['alpha']+bb[ri]*bb[rj]*f['beta']) if ti==tj else amean
   elif i>=3*r and j>=3*r:W[i][j]=f['etaP'] if i==j else bmean
   else:W[i][j]=-f['C']
 need(all(sum(row)==0 for row in W),'EVERY private residual row is balanced')
 def action(a):
  out={};total=sum(a.get(i,F(0)) for i in range(old))
  for i,A in enumerate(range(1,X+1)):out[i]=s*a.get(i,F(0))+(q-3)*a.get((X^A)-1,F(0))*(A!=X)-total
  for k in range(r):
   tsum=sum(a.get(t0+3*k+j,F(0)) for j in range(3))
   for j in range(3):out[t0+3*k+j]=s*(a.get(t0+3*k+j,F(0))-tsum/3)
  for j in range(l):out[z0+j]=2*s*a.get(z0+j,F(0))/3
  for i in range(m):out[r0+i]=sum(W[i][j]*a.get(r0+j,F(0)) for j in range(m))
  return {i:x for i,x in out.items() if x}
 def ip(a,b):v=action(b);return sum(x*v.get(k,F(0)) for k,x in a.items())
 cols=[unit(i) for i in range(old)]+Vt+Vp+[add(p,unit(r0+j)) for j,p in enumerate(projections)];actions=[action(a) for a in cols];C=[[sum(x*actions[j].get(k,F(0)) for k,x in a.items()) for j in range(N-1)] for a in cols];empty=scale(-1,add(*cols));difference=add(empty,scale(1/ell,K));need(ip(difference,difference)==0,'actual entire empty -K/ell in quotient of formal Gram')
 return locals()
def lift(C):
 rows=list(map(sum,C));return [[sum(rows)]+[-x for x in rows]]+[[-rows[i]]+row for i,row in enumerate(C)]
def basic(n,r,l,phase):
 a=seed(n,r,l);f=a['f'];N=a['N'];C=[list(x) for x in a['C']];W=a['W'];m=a['m'];s=f['s'];sets=[0]+a['sets'];P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
 stars=[sum(bool(A>>i&1) for A in sets) for i in range(n+2*r+l)];need(stars[:r]==[s]*r and max(stars[r:])<s,'EVERY old/private star and all maximum marks')
 for A in sets:
  B=A
  while True:
   need(B in sets,'EVERY actual downset submember')
   if B==0:break
   B=(B-1)&A
 need(psd(W)['rank']==m-1,'whole residual rank')
 u=[F(i<3) for i in range(m-1)];kappa=form(inverse([row[:-1] for row in W[:-1]]),u,u);closed=F(r-1,r)/f['nuT']+3/(r*f['C']);need(kappa==closed>0,'complete deleted inverse equals spectral formula')
 seedQ=lift(C);B=[[(N-1)*P[i][j]-seedQ[i][j]+F(1,N) for j in range(N)] for i in range(N)];need(psd(B)['rank']==N,'ENTIRE strict seed cap including actual empty');zeta=None;delta=F(0)
 if phase=='old':delta=1/(4*(8+kappa)) # target's credited sharp repair
 if phase=='strict':
  Bi=inverse(B);zeta=1/sum(Bi[i][i] for i in range(N));need(zeta>0 and psd([[B[i][j]-zeta*F(i==j) for j in range(N)] for i in range(N)])['rank']==N,'rational inverse-trace lower bound');delta=min(1/(1+kappa),zeta/16)
 if delta:
  last=a['sets'].index(a['bs'][-1]);endpoints=[a['us'][0],a['vs'][0],a['us'][0]|a['vs'][0]]
  for e in endpoints:
   j=a['sets'].index(e);need(e&a['bs'][-1]==0,'actual disjoint repair endpoints');C[last][j]+=delta;C[j][last]+=delta
  need(6*delta-kappa*delta*delta>0,'positive exact deleted residual Schur')
 Q=lift(C);L=[[F(1)+Q[i][j] for j in range(N)] for i in range(N)];M=[[(L[i][j]-s*F(i==j))/(N-s) for j in range(N)] for i in range(N)]
 need(all(sum(row)==0 for row in Q) and all(sum(row)==1 for row in M),'ALL actual regularity rows');need(all(M[i][j]==M[j][i] and (not(sets[i]&sets[j]) or M[i][j]==0) for i in range(N) for j in range(N)),'ALL actual symmetry/intersection/diagonal positions');rank=psd(L)['rank'];need(rank==N-r-1+(phase!='seed'),'ENTIRE lower rank');gap=F(1) if phase=='seed' else (1-8*delta if phase=='old' else 1+zeta/2);cap=[[(N-gap)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)];need(psd(cap)['rank']==N-1,'ENTIRE original cap at stated gap')
 for j in range(r):
  centered=[F(bool(A>>j&1))-s/N for A in sets];need(all(v==0 for v in mv(L,centered)),'EVERY row of EACH maximum-star kernel')
 if delta:
  x=[F(-3)]+[F(A in endpoints) for A in a['sets']];y=[F(-1)]+[F(A==a['bs'][-1]) for A in a['sets']];need(all(Q[i][j]-seedQ[i][j]==delta*(x[i]*y[j]+y[i]*x[j]) for i in range(N) for j in range(N)),'EVERY entire original repair position');need(dot(x,x)==12 and dot(y,y)==2 and dot(x,y)==3,'full lifted Gram, norm3+sqrt24<8')
 return {'n':n,'r':r,'l':l,'N':N,'phase':phase,'whole_positions':N*N,'stars':stars,'whole_C':digest(C),'whole_Q':digest(Q),'whole_M':digest(M),'whole_gap':digest(cap),'lower_rank':rank,'kappa':kappa,'delta':delta,'zeta':zeta,'gap':gap,'matrix_for_late_comparison':{'C':C,'Q':Q,'M':M},'scalar_parameters':{k:f[k] for k in ['d','g','Fp','A','ast','c','etaL','etaF','etaP','pair','mu','alpha','beta','C','nuT','nuL']}}

def physical(n,r,l):
 a=seed(n,r,l);f=a['f'];N=a['N'];q=a['q'];ip=a['ip'];cols=a['cols']+[a['empty']];Ts=a['Ts'];r0=a['r0'];Z=a['Z'];Wv=[unit(r0+j) for j in range(3*r+l)];M=[scale(F(1,3),add(*Wv[3*i:3*i+3])) for i in range(r)];WF=[add(Wv[3*i+2],scale(-1,M[i])) for i in range(r)];WA=[add(Wv[3*i],scale(-1,Wv[3*i+1])) for i in range(r)];TA=[add(T[0],scale(-1,T[1])) for T in Ts];TS=[add(T[0],T[1],scale(-2,T[2])) for T in Ts];gp=scale(F(1,2),add(a['G'],scale(-1,a['full'])));h0=scale(F(-1,2),add(a['G'],a['full']));As=[add(x,scale(-1,h0)) for x in a['Hs']]
 fixed=[gp,h0,add(*As[:r]),add(*As[r:]),add(*TS),add(*Z),add(*WF),add(*M)]
 anti=[v for i in range(r) for v in [TA[i],WA[i]]]
 tri=[add(xs[0],scale(-1,xs[j])) for xs in [As[:r],TS,M,WF] for j in range(1,r)]
 pend=[add(xs[0],scale(-1,xs[j])) for xs in [As[r:],Z,Wv[3*r:]] for j in range(1,l)]
 basis=anti+fixed+tri+pend;Gram=[[ip(x,y) for y in basis] for x in basis];table=[[ip(x,c) for c in cols] for x in basis];frame=[[dot(x,y) for y in table] for x in table];dim=6*r+3*l+1;need(len(basis)==dim and psd(Gram)['rank']==dim,'COMPLETE changed sector dimensions/positive metric');need(psd([[(N-1)*Gram[i][j]-frame[i][j] for j in range(dim)] for i in range(dim)])['rank']==dim,'ENTIRE strict physical changed cap')
 labels=[('anti',i//2) for i in range(2*r)]+[('fixed',0)]*8+[('triangle',0)]*len(tri)+[('pendant',0)]*len(pend)
 for i in range(dim):
  for j in range(dim):
   if labels[i]!=labels[j]:need(Gram[i][j]==frame[i][j]==0,'EVERY sector cross orthogonality')
 gamma=[[F(0)]*8 for _ in range(8)];dg=[q-1,3,3*r*(q-r),3*l*(q-l),6*r*f['s'],2*l*f['s']/3,r*f['beta'],r*l*f['C']/3]
 for i in range(8):gamma[i][i]=dg[i]
 gamma[2][3]=gamma[3][2]=-3*r*l;offset=2*r;need(gamma==[[Gram[offset+i][offset+j] for j in range(8)] for i in range(8)],'EVERY fixed physical Gram entry')
 F0=[[F(0)]*8 for _ in range(8)];F0[0][0]=q*q-1;F0[0][1]=F0[1][0]=3*(q-1);F0[1][1]=9
 for i in [2,3]:
  for j in [2,3]:F0[i][j]=6*gamma[i][j]
 hb=[F(0),F(1,3),F(1,3*r),F(0),F(0),F(0),F(0),F(0)];vb=[F(0),F(1,3),F(0),F(1,3*l),F(0),F(1,l),F(0),F(0)];K=[F(1),F(3*r+l-3,3),F(1),F(1,3),F(0),F(1),F(0),F(0)];E=[x-f['rho']*y for x,y in zip(hb,vb)];ts=[F(i==4) for i in range(8)];wf=[F(i==6) for i in range(8)];mean=[F(i==7) for i in range(8)];zp=[-l*f['Fp']*E[i]/(3*r)+f['c']*l*ts[i]/(9*r*f['t'])+mean[i]/r for i in range(8)];di=[(f['A']-f['d'])*E[i]+f['c']*(f['t']+2*(r-1))*ts[i]/(6*r*f['t'])-3*wf[i]/(2*r) for i in range(8)];grouped=[list(row) for row in F0]
 for weight,v in [(F(1,6*r),ts),(3*r,hb),(l,vb),(1/f['ell'],K),(F(3*r*(3*r+l),l),zp),(F(2*r,3),di)]:
  gv=mv(gamma,v)
  for i in range(8):
   for j in range(8):grouped[i][j]+=weight*gv[i]*gv[j]
 need(grouped==[[frame[offset+i][offset+j] for j in range(8)] for i in range(8)],'EVERY complete fixed grouping position including actual empty')
 for count,start,ds,base,updates in [(r-1,2*r+8,[6*q,12*f['s'],2*f['nuT'],2*f['beta']],[6*q*(N-q-7),12*f['s']*(N-q-4),2*f['nuT']*(N-1),2*f['beta']*(N-1)],[(4,[f['ast']*q,f['c']*f['s'],f['nuT'],-f['beta']/2]),(2,[f['d']*q,2*f['c']*f['s']/f['t'],f['nuT'],f['beta']])]),(l-1,2*r+8+4*(r-1),[6*q,4*f['s']/3,2*f['nuL']],[6*q*(N-7),4*f['s']*(N-1)/3,2*f['nuL']*(N-1)],[(2,[q,2*f['s']/3,0]),(2,[f['g']*q,2*f['s']*f['g']/3,f['nuL']])])]:
  for i in range(len(ds)*count):
   for j in range(len(ds)*count):
    ci,ri=divmod(i,count);cj,rj=divmod(j,count);metric=F(2 if ri==rj else 1,2);need(Gram[start+i][start+j]==(ds[ci]*metric if ci==cj else 0),'EVERY nonorthogonal class standard Gram metric');cap=(base[ci] if ci==cj else 0)-sum(k*v[ci]*v[cj] for k,v in updates);need((N-1)*Gram[start+i][start+j]-frame[start+i][start+j]==cap*metric,'EVERY standard complete cap update metric')
 pairs=[(A,a['X']^A) for A in range(1,a['X']) if A<(a['X']^A)]
 pairconstant=[add(unit(A-1),unit(B-1),scale(-1,unit(pairs[0][0]-1)),scale(-1,unit(pairs[0][1]-1))) for A,B in pairs[1:]]
 antis=[add(unit(A-1),scale(-1,unit(B-1))) for A,B in pairs];Ainv=inverse([[ip(x,y) for y in As] for x in As]);untouched=[]
 for raw in antis:
  coeff=mv(Ainv,[ip(x,raw) for x in As]);v=add(raw,*(scale(-c,x) for c,x in zip(coeff,As)))
  if ip(v,v):untouched.append(v)
 for eig,vectors in [(2*q,pairconstant),(6,untouched)]:
  for v in vectors:
   need(all(ip(v,x)==0 for x in basis),'ALL untouched changed orthogonality');need(all(ip(v,x)==0 for x in cols[2*q-1:]),'ALL new/empty untouched orthogonality');need(a['action'](v)==scale(eig,v),'EVERY whole old-frame eigenaction coefficient')
 return {'untouched_constant':len(pairconstant),'untouched_anti_spanning':len(untouched),'n':n,'r':r,'l':l,'N':N,'changed_dimension':dim,'whole_changed_positions':dim*dim,'whole_Gram':digest(Gram),'whole_frame':digest(frame),'whole_actual_table':digest(table),'whole_fixed_grouping':digest(grouped),'all_cross_positions':dim*dim,'full_class_standard_positions':len(tri)**2+len(pend)**2}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('n',type=int);p.add_argument('r',type=int);p.add_argument('l',type=int);p.add_argument('phase',choices=['seed','old','strict','physical']);a=p.parse_args();signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed60s original phase')));signal.alarm(60);print(json.dumps(canonical(physical(a.n,a.r,a.l) if a.phase=='physical' else basic(a.n,a.r,a.l,a.phase)),sort_keys=True,separators=(',',':')))
