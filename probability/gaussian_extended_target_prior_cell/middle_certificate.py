"""Two exact backward-prior hinge controls, with group averaging."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from common import r,m,exp_neg,gaussian_constant,quadrature_error
import time

def histogram(h,M,bits,progress=False):
 Q=1<<bits;den=256*Q*Q;ns=[4,12]
 tables={a:[exp_neg((h*j-a)**2/2,bits) for j in range(-M,M+1)] for p in r.X+r.Y for a in p}
 atoms=[[tuple(tables[a] for a in p) for p in P] for P in [r.X,r.Y]]
 hist=[Counter(),Counter()];peak=[0,0];num=0;sites=0;digest=sha256();start=time.monotonic()
 for point,mult in m.orbits(M):
  i,j,k=(a+M for a in point)
  xx=[tx[i][1]*ty[j][1]*tz[k][1] for tx,ty,tz in atoms[0]]
  yl=[tx[i][0]*ty[j][0]*tz[k][0] for tx,ty,tz in atoms[1]]
  yu=[tx[i][1]*ty[j][1]*tz[k][1] for tx,ty,tz in atoms[1]]
  sx=sum(xx);sl=sum(yl);su=sum(yu);gl=sl//(16*Q*Q)
  for typ,ids in enumerate([range(4),range(4,16)]):
   if gl>Q//512:hist[typ][gl]-=2*ns[typ]*mult
   for label in ids:
    f=(15*sx+16*xx[label]+den-1)//den
    g=(17*su-16*yu[label]+den-1)//den
    # All coefficients in g equal17 except the selected coefficient1.
    if f>Q//512:hist[typ][f]+=mult
    if g>Q//512:hist[typ][g]+=mult
    peak[typ]=max(peak[typ],f)
    digest.update(f'{typ},{f},{g},{gl},{mult};'.encode())
  num+=1;sites+=mult
  if progress and num%100000==0:print('orbits',num,'seconds',round(time.monotonic()-start,1),flush=True)
 r.need(sites==(2*M+1)**3,'orbit size')
 return hist,peak,ns,num,digest.hexdigest()

def sweep(hist,left,right):
 value=sum(c*max(v-left,0) for v,c in hist.items());slope=-sum(c for v,c in hist.items() if v>left);best=value;arg=left;prev=left
 knots=sorted({v for v in hist if left<v<=right}|{right})
 for v in knots:
  value+=slope*(v-prev)
  if value>best:best=value;arg=v
  slope+=hist.get(v,0);prev=v
 return best,arg,len(knots)

def calculate(h=F(1,16),M=120,bits=48,progress=True):
 start=time.monotonic();hist,peaks,ns,num,digest=histogram(h,M,bits,progress);Q=1<<bits;cl,cu=gaussian_constant(bits);quad,tail=quadrature_error(h,F(6),bits);rows=[]
 for typ in range(2):
  val,arg,knots=sweep(hist[typ],Q//512,9*Q//32);poly=F(val,Q*ns[typ])*h**3*(cl if val<0 else cu);bound=poly+2*(quad+tail)+r.EPS
  peak=F(peaks[typ],Q)+3*h*h/8+F(61,100)*r.EPS
  r.need(bound<-F(1,256),'middle bound')
  r.need(peak<F(9,32),'source peak')
  rows.append({'type':['core','flap'][typ],'poly':str(poly),'bound':str(bound),'arg':str(F(arg,Q)),'knots':knots,'peak':str(peak)})
 return {'histogram_sha256':digest,'rows':rows,'orbits':num,'sites':(2*M+1)**3,'quad':str(quad),'tail':str(tail)}
