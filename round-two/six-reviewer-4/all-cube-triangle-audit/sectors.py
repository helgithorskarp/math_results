"""Fresh original-row aggregation. Works over rational numbers or QQ(h,q)."""
from fractions import Fraction as F
def params(h,q):
 D=3*h;s=q+D;ell=6*h+1;N=2*q+12*h;w=s-1
 c0=(q-1+(2*q-3)*D)/(ell*ell);B2=s*(h-1)/(3*h)
 a=3*h*(ell-q+1)/(2*ell*s*(h-1));b=-2*a;c=9*(ell-q+1)/(2*ell*s)
 etaL=w-c0-a*a*B2-2*s*c*c/3
 etaF=w-c0-b*b*B2-2*s*c*c/(3*(h-1))
 p=-1-c0-a*b*B2
 mu=(2*p+etaF)/3;alpha=2*(2*etaL-p-etaF);beta=etaF-mu;nu=2*h*mu/(2*h-1)
 return dict(h=h,q=q,D=D,s=s,ell=ell,N=N,w=w,c0=c0,B2=B2,a=a,b=b,c=c,etaL=etaL,etaF=etaF,p=p,mu=mu,alpha=alpha,beta=beta,nu=nu)
def aggregate(metric,rows):
 zero=metric[0]*0;n=len(metric);S=[[zero for _ in range(n)]for _ in range(n)]
 for count,coord in rows:
  inner=[metric[i]*coord[i]for i in range(n)]
  for i in range(n):
   for j in range(n):S[i][j]+=count*inner[i]*inner[j]
 return S

def matrices(p):
 h,q,D,s,ell,N,a,b,c,alpha,beta,nu=[p[k]for k in('h','q','D','s','ell','N','a','b','c','alpha','beta','nu')];zero=h*0
 gm=[2*s,alpha]
 # Physical coordinates, rather than copied frame entries; each marked/private leaf retained.
 leaf=aggregate(gm,[(2,[F(1,2),zero]),(2,[c/2,-F(1,2)])])
 gs=[2*s/3,12*s,2*beta,2*nu]
 standard=aggregate(gs,[(4,[F(1,2),F(1,12),zero,zero]),(2,[F(1,2),-F(1,6),zero,zero]),(4,[a/2,c/12,-F(1,4),F(1,2)]),(2,[b/2,c/(6*(h-1)),F(1,2),F(1,2)])])
 ge=[4*(q-1),4*D,2*D*(q-2),12*h*s,2*h*beta]
 even=aggregate(ge,[
  (q/2-1,[1/(2*(q-1)),zero,1/(q-2),zero,zero]),
  (q,[1/(2*(q-1)),zero,zero,zero,zero]),
  (q/2-1,[1/(2*(q-1)),zero,-1/(q-2),zero,zero]),
  (1,[-F(1,2),F(1,2),zero,zero,zero]),
  (4*h,[zero,-1/(2*D),1/(2*D),1/(12*h),zero]),
  (2*h,[zero,-1/(2*D),1/(2*D),-1/(6*h),zero]),
  (4*h,[-1/(2*ell),1/(2*ell),-1/ell,c/(12*h),-1/(4*h)]),
  (2*h,[-1/(2*ell),1/(2*ell),-1/ell,-c/(6*h),1/(2*h)]),
  (1,[-1/(2*ell),1/(2*ell),-1/ell,zero,zero])])
 go=[2*q*D,12*h*s,2*h*beta,2*h*nu]
 odd=aggregate(go,[(q,[1/q,zero,zero,zero]),
  (4*h,[1/(2*D),1/(12*h),zero,zero]),(2*h,[1/(2*D),-1/(6*h),zero,zero]),
  (4*h,[zero,c/(12*h),-1/(4*h),1/(2*h)]),(2*h,[zero,-c/(6*h),1/(2*h),1/(2*h)])])
 return dict(leaf=(gm,leaf),standard=(gs,standard),even=(ge,even),odd=(go,odd))
