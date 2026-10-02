"""Exact whole physical model for the fixed repeated triangle profile (2,1).

The ordinary complete-space bridge is in PROOF.md; this is not a general
private-facet cap closure. No floating arithmetic or external corpus.
"""
from fractions import Fraction as F
from exact import require,psd_rank,dot,matvec,gram,unit,scale,vecadd,zero

def params(q,mode='mean',dchoice=F(0),cchoice=F(-2,5),fraction=F):
 require(mode=='mean' and dchoice==0 and cchoice==F(-2,5),'proved fixed-profile recipe only')
 q=fraction(q);s=q+6;w=q+5;N=2*q+18;H=N-1;rho=(q-1)/(q+2);E2=q/6+rho*rho*(q+3)/3;common=(10*q-4)/100
 if fraction is F:require(q>=4,'physical domain realq>=4')
 cL=cchoice*(q-8)/s
 G=-3*(q-8)/(10*rho*(q+3));FF=G-cL*s/(rho*(q+3))
 d=dchoice*(q-11)/q
 A=(-2*d-2*FF-G)/4
 b=(F(3,5)*(q-11)-d*q)/s
 if mode=='mean':cH=-(F(9,5)*(q-11)+(2*FF+G)*q/2)/(4*s)
 elif mode=='direct':cH=F(-2,5)*(q-11)/s
 else:raise ValueError('unknown parameter mode')
 a=(F(3,5)*(q-11)-A*q+2*cH*s)/s
 require(mode!='mean' or 2*a+b==0,'heavy-facet-standard projection mean')
 etaHL=w-common-A*A*E2-a*a*s/6-2*s*cH*cH/3
 etaHF=w-common-d*d*E2-b*b*s/6-2*s*cH*cH/3-s*cL*cL/6
 etaLL=w-common-FF*FF*E2-2*s*cL*cL/3
 etaLF=w-common-G*G*E2
 pairH=-1-common-A*d*E2-a*b*s/6;pairL=-1-common-FF*G*E2
 muH=(2*pairH+etaHF)/3;muL=(2*pairL+etaLF)/3
 alphaH=2*(2*etaHL-pairH-etaHF);betaH=etaHF-muH
 alphaL=2*(2*etaLL-pairL-etaLF);betaL=etaLF-muL
 nu=2*muH-muL/2
 return locals()

def construct(q,mode='mean',dchoice=F(0),cchoice=F(-2,5),fraction=F):
 p=params(q,mode,dchoice,cchoice,fraction);q,s,w,N,H=[p[z] for z in ['q','s','w','N','H']]
 size=20;Gamma=zero(size,size)
 # old4: gp,h0,Ax,Ay; heavy B1; Tu,Tv for each heavy pair; lightY,Tu,Tv; private W first8.
 Gamma[0][0]=q-1;Gamma[1][1]=6
 Gamma[2][2]=Gamma[3][3]=6*(q-1);Gamma[2][3]=Gamma[3][2]=-6
 Gamma[4][4]=s/6;Gamma[9][9]=s/6
 for start in [5,7,10]:
  Gamma[start][start]=Gamma[start+1][start+1]=2*s/3
  Gamma[start][start+1]=Gamma[start+1][start]=-s/3
 def e(i):return unit(size,i)
 gp,h0,Ax,Ay=[e(i) for i in range(4)]
 Hx=vecadd(h0,Ax);Hy=vecadd(h0,Ay);hx=scale(F(1,6),Hx);hy=scale(F(1,6),Hy)
 B=[e(4),scale(-1,e(4))];Y=e(9)
 Ts=[]
 for start in [5,7,10]:Ts.append([e(start),e(start+1),scale(-1,vecadd(e(start),e(start+1)))])
 VbarL=vecadd(hy,Y);E=vecadd(hx,scale(-p['rho'],VbarL))
 K=vecadd(gp,scale(-1,h0),Hx,scale(F(1,2),Hy),scale(3,Y))
 common=scale(F(-1,10),K)
 V=[]
 for i in range(2):V.extend(vecadd(hx,B[i],Ts[i][a]) for a in range(3))
 V.extend(vecadd(VbarL,Ts[2][a]) for a in range(3))
 P=[]
 for i in range(2):
  for a in range(2):P.append(vecadd(common,scale(p['A'],E),scale(p['a'],B[i]),scale(p['cH'],Ts[i][1-a])))
  P.append(vecadd(common,scale(p['d'],E),scale(p['b'],B[i]),scale(p['cH'],Ts[1-i][2]),scale(p['cL']/2,Ts[2][2])))
 P.extend(vecadd(common,scale(p['FF'],E),scale(p['cL'],Ts[2][1-a])) for a in range(2))
 P.append(vecadd(common,scale(p['G'],E)))
 require(vecadd(*P)==scale(F(-9,10),K),'all projection balance positions')
 W=zero(9,9)
 for i in range(9):
  fi,ai=divmod(i,3)
  for j in range(9):
   fj,aj=divmod(j,3)
   if fi!=fj:
    z=p['muL']/2-p['muH'] if fi<2 and fj<2 else -p['muL']/2
   else:
    mu,alpha,beta=[p[name+('H' if fi<2 else 'L')] for name in ['mu','alpha','beta']]
    wa=[F(1,2),F(-1,2),F(0)];wf=[F(-1,2),F(-1,2),F(1)]
    z=mu+wa[ai]*wa[aj]*alpha+wf[ai]*wf[aj]*beta
   W[i][j]=z
 require(all(sum(row)==0 for row in W),'whole residual balance')
 for i in range(8):
  for j in range(8):Gamma[12+i][12+j]=W[i][j]
 U=[]
 for i in range(9):
  residual=e(12+i) if i<8 else scale(-1,vecadd(*(e(12+j) for j in range(8))))
  U.append(vecadd(P[i],residual))
 empty=common
 # Old cube frame exact moments; untouched proper symmetric2q and antisymmetric12 directions omitted.
 S=zero(size,size);S[0][0]=q*q-1;S[1][1]=36;S[0][1]=S[1][0]=6*(q-1)
 for i in [2,3]:
  for j in [2,3]:S[i][j]=12*Gamma[i][j]
 for row in V+U+[empty]:
  x=matvec(Gamma,row)
  for i in range(size):
   for j in range(size):S[i][j]+=x[i]*x[j]
 cap=[[H*Gamma[i][j]-S[i][j] for j in range(size)] for i in range(size)]
 return p,Gamma,S,cap,{'V':V,'P':P,'U':U,'empty':empty,'K':K,'W':W,'Ts':Ts,'B':B,'E':E}

def check(q,mode='mean',dchoice=F(0),cchoice=F(-2,5)):
 p,G,S,cap,v=construct(q,mode,dchoice,cchoice)
 status={'q':str(q),'mode':mode,'dchoice':str(dchoice),'cchoice':str(cchoice)}
 for label,matrix in [('physical_Gram',G),('whole_changed_cap',cap)]:
  try:status[label]={'PD':psd_rank(matrix)==20}
  except ValueError as exc:status[label]={'PD':False,'reason':str(exc)}
 status['scalars']={z:str(p[z]) for z in ['muH','muL','alphaH','alphaL','betaH','betaL','nu']}
 return status

def blocks(G,S,cap,vec):
 e=lambda i:unit(20,i)
 def w(i):return e(12+i) if i<8 else scale(-1,vecadd(*(e(12+j) for j in range(8))))
 WA=[vecadd(w(3*i),scale(-1,w(3*i+1))) for i in range(3)]
 WF=[scale(F(1,3),vecadd(scale(2,w(3*i+2)),scale(-1,w(3*i)),scale(-1,w(3*i+1)))) for i in range(3)]
 M=[scale(F(1,3),vecadd(*(w(3*i+j) for j in range(3)))) for i in range(3)]
 TA=[vecadd(t[0],scale(-1,t[1])) for t in vec['Ts']]
 TS=[vecadd(t[0],t[1],scale(-2,t[2])) for t in vec['Ts']]
 groups=[('heavy-anti-1',[TA[0],WA[0]]),('heavy-anti-2',[TA[1],WA[1]]),('light-anti',[TA[2],WA[2]]),
         ('heavy-standard',[e(4),vecadd(TS[0],scale(-1,TS[1])),vecadd(M[0],scale(-1,M[1])),vecadd(WF[0],scale(-1,WF[1]))]),
         ('fixed',[e(i) for i in range(4)]+[vecadd(TS[0],TS[1]),e(9),TS[2],vecadd(WF[0],WF[1]),WF[2],vecadd(M[0],M[1])])]
 vectors=[v for _,vs in groups for v in vs];require(len(vectors)==20,'complete20 physical vector count')
 require(len(G)==20 and len(cap)==20,'complete physical matrices')
 GB=gram(G,vectors,zero(20,20));CB=gram(cap,vectors,zero(20,20))
 integerG=gram([[F(i==j) for j in range(20)] for i in range(20)],vectors,zero(20,20))
 from exact import psd_rank
 require(psd_rank(integerG)==20,'constant physical change invertible')
 labels=[label for label,vs in groups for _ in vs]
 cross=0
 for i in range(20):
  for j in range(20):
   if labels[i]!=labels[j]:require(GB[i][j]==0 and CB[i][j]==0,'every cross-sector original identity');cross+=1
 require([row[:2] for row in GB[:2]]==[row[2:4] for row in GB[2:4]],'both heavyanti Gram copies identical')
 require([row[:2] for row in CB[:2]]==[row[2:4] for row in CB[2:4]],'both heavyanti cap copies identical')
 answer={};offset=0
 for label,vs in groups:
  k=len(vs)
  if label!='heavy-anti-2':answer[label]=[row[offset:offset+k] for row in CB[offset:offset+k]]
  offset+=k
 return answer,{'cross_sector_positions':cross,'heavy_anti_equal_positions':8,'physical_change_rank':20}
