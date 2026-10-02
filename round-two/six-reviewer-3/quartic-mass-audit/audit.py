"""Independent s=0 scalar exclusion. No producer source or fixture import.
The defining mathematical proof is visible; the owned9550 matrix machinery
is credited and regenerated. New eliminants and evidence are derived here.
"""
import hashlib,json
from fractions import Fraction as F
from polys import Poly,cast,symbol,need
from pencil import audit as pencil
from exact import degree,primitive,divide,quotient,determinant,scalar,coefficients,sylvester,evaluate,lagrange,mt,ma,mm,unit

def load(rec):
 terms={}
 for name,z in rec.items():
  need(len(z)==2 and F(z[1])==0,'real whole input coefficient');k=[]
  if name!='1':
   for item in name.split('*'):
    x,_,n=item.partition('^');k.append((x,int(n) if n else 1))
  terms[tuple(sorted(k))]=(F(z[0]),0)
 return Poly(terms)
def audit():
 base=pencil();basehash=hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 need(basehash=='7afaf2e4aac5b52080b03d7e133eeb8f77f295ad8703f90c3406820916468f9c','entire unchanged owned9550 reconstruction')
 M=[[load(x).substitute({'s':0}) for x in row] for row in base['whole_matrix']]
 B,E,r,t,v,w=map(symbol,['B','E','r','t','v','w']);R=[a*t*t+b*t+c for a,b,c in M];checks={}
 def eq(label,p,q):
  need(p==q,label);checks[label]=cast(p).record()
 def minor(rows):
  a,b,c=[M[i] for i in rows]
  return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
 H=2112*E+10976*r*r+7344*r+1143;K=14400*E+65856*r*r+38160*r+4725;W=5488*r*r+7280*r+1875
 D=262144*E*E*r+102400*E*E+786432*E*r**3+663552*E*r*r+153600*E*r+5760*E+36864*r**4+18432*r**3-1152*r*r-864*r+81
 eq('t0 constant unit',M[0][2]-14*M[4][2],cast(-192))
 eq('complete R3',18816*R[3],t*(B*t*K-112*H))
 eq('complete 023 minor',minor([0,2,3]),F(5,774144)*(7*r+3)*H*D)
 eq('complete H K W',2112*K-14400*H,-3456*W)
 Estar=-(10976*r*r+7344*r+1143)/2112
 m024=minor([0,2,4]);divB=m024.divide_monomial({'B':1});hsub=divB.substitute({'E':Estar});hquot,hrem=divide(hsub,W)
 eq('whole H0 remainder',hsub,hquot*W+hrem)
 L=primitive(hrem);need(degree(L,'r')==1 and degree(L,'B')==0,'derived linear branch remainder')
 eq('derived visible L',L,6641762363050556*r+2323226157581397)
 mh=sylvester(W,L,'r',2,1);dh=determinant(evaluate(mh,{}));need(dh==8017052714249480766100811232,'full H0 nonzero determinant')
 Y=[];Wi=[];dvalues=[2,1,2,2]
 for i,d in zip([0,1,2,4],dvalues):
  terms={}
  for key,z in R[i].terms.items():
   m=dict(key);b=m.pop('B',0);j=m.pop('t',0);k=b+d-j
   need(k>=0 and k%2==0,'complete scalar-clearing parity')
   if k:m['v']=m.get('v',0)+k//2
   if j:m['w']=m.get('w',0)+j
   kk=tuple(sorted(m.items()));terms[kk]=(z[0]+terms.get(kk,(F(0),0))[0],0)
  y=Poly(terms);eq('complete clearing '+str(i),y.substitute({'v':B*B,'w':B*t}),B**d*R[i]);need(degree(y,'v')<=1 and degree(y,'w')<=2,'whole affine v quadratic w')
  y2,y1,y0=[y.coefficient('w',j) for j in [2,1,0]];cleared=y2*(112*H)**2+y1*(112*H)*K+y0*K*K
  eq('whole clearing syzygy '+str(i),K*K*y-cleared,(K*w-112*H)*(y2*(K*w+112*H)+K*y1))
  Y.append(y);Wi.append(primitive(cleared))
 X=[];Af=[]
 a0,b0=Wi[0].coefficient('v',1),Wi[0].coefficient('v',0)
 for j,power in [(1,1),(3,2)]:
  aj,bj=Wi[j].coefficient('v',1),Wi[j].coefficient('v',0);x=a0*bj-aj*b0
  eq('undivided affine syzygy '+str(j),a0*Wi[j]-aj*Wi[0],x)
  q=quotient(x,H**power);eq('whole H quotient '+str(j),q*H**power,x);X.append(x);Af.append(primitive(q))
 A5,A4=Af;need([(degree(p,'E'),degree(p,'r')) for p in Af]==[(5,10),(4,9)],'full elimination degrees')
 ex=[primitive(p.substitute({'r':F(-3,7)})) for p in Af];me=sylvester(ex[0],ex[1],'E',5,4);de=determinant(evaluate(me,{}));need(de!=0,'whole r=-3/7 determinant nonzero')
 resultants=[];quotients=[]
 for A,m,bound in [(A5,5,40),(A4,4,34)]:
  matrix=sylvester(D,A,'E',2,m)
  need(degree(D,'E')==2 and degree(A,'E')==m,'formal E degrees')
  need(max(degree(D.coefficient('E',j),'r') for j in range(3))<=4 and max(degree(A.coefficient('E',j),'r') for j in range(m+1))<=10-(m==4),'rowwise determinant degree bound')
  nodes=list(range(-bound//2,bound//2+1));values=[determinant(evaluate(matrix,{'r':x})) for x in nodes]
  need(all(x.denominator==1 for x in values),'all rational Gaussian determinants integer')
  arr=lagrange(nodes,values);need(all(x.denominator==1 for x in arr),'whole reconstructed integer determinant')
  sp=sum((cast(z)*r**j for j,z in enumerate(arr)),cast(0));q=quotient(sp,(8*r+3)**3);qp=primitive(q)
  eq('whole resultant factor '+str(m),sp,scalar(q.coefficient('r',degree(q,'r')))/scalar(qp.coefficient('r',degree(qp,'r')))*(8*r+3)**3*qp)
  resultants.append({'formal_matrix':[[z.record() for z in row] for row in matrix],'degree_bound':bound,'nodes':nodes,'values':list(map(str,values)),'whole_coefficients':list(map(str,arr)),'content':str(scalar(q.coefficient('r',degree(q,'r')))/scalar(qp.coefficient('r',degree(qp,'r'))))});quotients.append(qp)
 need([degree(p,'r') for p in quotients]==[22,19],'whole quotient degrees')
 arrays=[coefficients(p,'r') for p in quotients];prime=263;need(all(prime%d for d in range(2,17)),'prime263')
 reductions=[mt([int(x) for x in arr],prime) for arr in arrays];need([len(a) for a in reductions]==[23,20],'both whole leading degrees retained')
 u,z=unit(*reductions,prime);eqmod=ma(mm(u,reductions[0],prime),mm(z,reductions[1],prime),prime);need(eqmod==[1],'ENTIRE new prime263 Bezout unit')
 eq('last D specialization',D.substitute({'r':F(-3,8)}),4096*E*E)
 eq('last H specialization',H.substitute({'r':F(-3,8),'E':0}),cast(F(-135,2)))
 eq('last K specialization',K.substitute({'r':F(-3,8),'E':0}),cast(-324))
 eq('last scalar residual',Y[0].substitute({'r':F(-3,8),'E':0,'w':F(70,3)}),14*v)
 # A genuinely projective boundary is assessed separately from finite t.
 infinity=[z[0] for z in M]
 return {'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','owned9550_sha256':basehash,'whole_s0_matrix':[[z.record() for z in row] for row in M],'whole_s0_residuals':[z.record() for z in R],'whole_checks':checks,'H0':{'whole_minor':m024.record(),'substitution':hsub.record(),'quotient':hquot.record(),'remainder':hrem.record(),'primitive_L':L.record(),'full_matrix':[[z.record() for z in row] for row in mh],'determinant':str(dh)},'whole_Y':[z.record() for z in Y],'whole_Wi':[z.record() for z in Wi],'whole_X':[z.record() for z in X],'whole_A':[z.record() for z in Af],'exceptional_r':{'full_matrix':[[z.record() for z in row] for row in me],'determinant':str(de)},'resultants':resultants,'whole_quotients':[z.record() for z in quotients],'new_modular_unit':{'prime':prime,'reductions':reductions,'leading_coefficients':[z[-1] for z in reductions],'U':u,'V':z,'whole_unit':eqmod},'projective_leading_column':[z.record() for z in infinity],'inherited_B0_whole_unit':base['obstruction'],'scope':'no common finite complex scalar root for s=0; actual distinct real original stationary corollary retains original chart premises'}

if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,separators=(',',':')))
