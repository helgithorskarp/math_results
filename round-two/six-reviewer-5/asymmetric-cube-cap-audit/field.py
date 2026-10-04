"""Independent written-definition cap reconstruction over QQ(h,q).

No author program or certificate import. Scalars and physical frame scores are
transcribed from the exposed ordinary proof, then whole leading pivots computed.
"""
import hashlib,json,pathlib,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
import sympy as sp
from sympy.polys.domains import QQ
H,Q=sp.symbols('h q');F=QQ.frac_field(H,Q);h,q=F.gens
def need(t,why):
 if not t:raise ValueError(why)
def build(h,q):
 l=h-1;s=q+3*h;N=2*q+12*h-6;ell=6*h-2
 c0=q/(2*(3*h-1))-1/(3*h-1)**2
 groups=[]
 for k,v in ((h,-(q-1)/ell),(l,-(q+2)/ell)):
  r=1+v; B2=s*(k-1)/(3*k);a=r/(2*B2);b=-2*a;c=9*r/(2*s)
  etaL=s-1-c0-a*a*B2-2*s*c*c/3
  etaF=s-1-c0-b*b*B2-2*s*c*c/(3*(k-1));p=-1-c0-a*b*B2
  mu=(2*p+etaF)/3;alpha=2*(2*etaL-p-etaF);beta=etaF-mu
  need(mu==(s-3)/3-c0-9*r*r/(2*s*(k-1)),'mu expanded')
  need(alpha==2*s-27*(2*k-3)*r*r/(s*(k-1)),'alpha expanded')
  need(beta==2*s/3-3*(k+3)*r*r/(s*(k-1)),'beta expanded')
  groups.append(dict(k=k,v=v,B2=B2,a=a,b=b,c=c,mu=mu,alpha=alpha,beta=beta))
 tau=groups[0]['mu']*groups[1]['mu']/(h*groups[0]['mu']+l*groups[1]['mu'])
 groups[0]['nu']=(h*groups[0]['mu']-l*tau)/l
 groups[1]['nu']=(l*groups[1]['mu']-h*tau)/(l-1)
 z=F.zero if hasattr(h,'numer') else 0
 def zero(n):return [[z for _ in range(n)] for _ in range(n)]
 def outer_add(m,v,w=1):
  for i in range(len(v)):
   for j in range(len(v)):m[i][j]+=w*v[i]*v[j]
 def cap(metric,frame):return [[((N-1) if i==j else 0)-frame[i][j]/metric[i] for j in range(len(metric))] for i in range(len(metric))]
 scalars={};blocks={};physical={}
 for gi,g in enumerate(groups):
  for key in ('mu','alpha','beta','nu'):scalars[f'{gi}-{key}']=g[key]
  k,a,b,c,alpha,beta,nu=[g[key] for key in ('k','a','b','c','alpha','beta','nu')]
  frame=[[2*s*s*(1+c*c),-s*c*alpha],[-s*c*alpha,alpha*alpha/2]];metric=[2*s,alpha]
  physical[f'{gi}-odd']=(metric,frame);blocks[f'{gi}-odd']=cap(metric,frame)
  metric=[2*s/3,12*s,2*beta,2*nu];frame=zero(4)
  for v,w in (([s/3,s,0,0],4),([s/3,-2*s,0,0],2),([a*s/3,c*s,-beta/2,nu],4),([b*s/3,2*c*s/(k-1),beta,nu],2)):outer_add(frame,v,w)
  physical[f'{gi}-standard']=(metric,frame);blocks[f'{gi}-standard']=cap(metric,frame)
  metric=[6*k*s,k*beta];frame=[[6*k*s*s*(1+c*c),-3*k*s*c*beta],[-3*k*s*c*beta,3*k*beta*beta/2]]
  physical[f'{gi}-trace']=(metric,frame);blocks[f'{gi}-trace']=cap(metric,frame)
 scalars['tau']=tau
 D=3*h;metric=[4*(q-1),4*D,2*D*(q-2),2*q*D,s/(3*h*l)];frame=zero(5)
 frame[0][0]=4*(q*q-1);frame[0][1]=frame[1][0]=-4*D*(q-1);frame[1][1]=4*D*D;frame[2][2]=4*D*D*(q-2);frame[3][3]=4*D*D*q
 outer_add(frame,[0,-2,q-2,q,0],3*h)
 outer_add(frame,[0,-2,q-2,-q,s/(3*h*l)],3*l)
 outer_add(frame,[-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q,-s/h],1/ell)
 physical['aggregate-five']=(metric,frame);blocks['aggregate-five']=cap(metric,frame)
 blocks['mean']=[[N-1-3*(h+l)*tau]]
 blocks['old-sum']=[[N-1-2*q]];blocks['old-difference']=[[N-1-6*h]]
 kappa=(h-1)/(h*groups[0]['nu'])+(l-1)/(l*groups[1]['nu'])+1/(h*l*tau)+4/groups[1]['beta']
 return dict(h=h,q=q,l=l,s=s,N=N,ell=ell,c0=c0,groups=groups,tau=tau,kappa=kappa,scalars=scalars,blocks=blocks,physical=physical)
def poly_record(p):return [[list(m),str(c)] for m,c in sorted(p.to_dict().items())]
def shifted(p):
 # Exact integer binomial composition. No sampling, saved signs or hash premise.
 from math import comb
 out={}
 for (a,b),c in p.to_dict().items():
  for i in range(a+1):
   for j in range(b+1):out[i,j]=out.get((i,j),QQ.zero)+c*comb(a,i)*3**(a-i)*comb(b,j)*4**(b-j)
 out={m:c for m,c in out.items() if c};need(out.get((0,0),0)>0,'strict shifted constant');need(all(c>0 for c in out.values()),'shifted coefficient sign')
 return [[list(m),str(c)] for m,c in sorted(out.items())]
def signs(a):
 p,d=a.numer,a.denom
 return dict(numerator=poly_record(p),denominator=poly_record(d),shifted_numerator=shifted(p),shifted_denominator=shifted(d))
def generate():
 t=time.monotonic();b=build(h,q);record={'scalars':{},'blocks':{},'method':'fresh full rational leading pivots, QQ(h,q), h=3+u,q=4+v'}
 for key,v in b['scalars'].items():record['scalars'][key]=signs(v)
 for key,a in b['blocks'].items():
  w=[row[:] for row in a];pivs=[]
  for i in range(len(w)):
   p=w[i][i];need(p!=0,'zero pivot');pivs.append(signs(p))
   for j in range(i+1,len(w)):
    for k in range(i+1,len(w)):w[j][k]-=w[j][i]*w[i][k]/p
  cleared=[];row_den=[]
  for row in a:
   dd=row[0].denom
   for v in row[1:]:dd=dd.lcm(v.denom)
   row_den.append(poly_record(dd));cleared.append([poly_record(v.numer*dd.exquo(v.denom)) for v in row])
  record['blocks'][key]=dict(entries=[[dict(numerator=poly_record(v.numer),denominator=poly_record(v.denom)) for v in row] for row in a],pivots=pivs,row_denominators=row_den,cleared=cleared)
 record['pivot_count']=len(record['scalars'])+sum(len(v['pivots']) for v in record['blocks'].values())
 record['inverse_bound']=signs(2-b['kappa'])
 return record
if __name__=='__main__':
 t=time.monotonic();r=generate();out=ROOT/'work/fresh-field-record.json';out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps(dict(pivots=r['pivot_count'],blocks=list(r['blocks']),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),seconds=time.monotonic()-t)))
