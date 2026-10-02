"""Reviewer transcription of signed written9641 formulas, not target code.

The same formulas are checked in two representations: bivariate rationals
and direct Fraction values; the full original-set construction is separate.
"""
from fractions import Fraction as F
from linear import need

def vadd(a,b):return [x+y for x,y in zip(a,b)]
def vscale(c,a):return [c*x for x in a]
def pair(a,B,b):return sum(a[i]*B[i][j]*b[j]for i in range(len(a))for j in range(len(b)))
def model(q,l):
 s=q+3;w=q+2;N=2*q+6+2*l;m=l+3;ell=l+4;rho=(q-1)/(q+1)
 d=3*(q-ell-1)/(ell*q);g=(q-ell+1)/(ell*w);Fp=-g/rho;A=(-d-l*Fp)/2;c=(A-d)*q/s
 common=(ell*q-4)/ell**2;e2=q/3+rho**2*w/l
 etaL=w-common-A**2*e2-2*s*c**2/3;etaF=w-common-d**2*e2;etaP=w-common-Fp**2*e2-g**2*w*(l-1)/l-2*s*c**2/(3*l**2)
 leafpair=-1-common-A*d*e2;mu=(2*leafpair+etaF)/3;alpha=2*(2*etaL-leafpair-etaF);beta=etaF-mu;Cmean=3*mu/l;nu=(l*etaP-3*Cmean)/(l-1)
 D=N-7;H=N-1;A0=N-q-2;J=A0*(N-4)-3*(q-1)
 def I0(a,b):
  return ((q-1)*(N-4)*a[0]*b[0]+3*(q-1)*(a[0]*b[1]+a[1]*b[0])+3*A0*a[1]*b[1])/J+3*((q-1)*a[2]*b[2]-l*(a[2]*b[3]+a[3]*b[2])+l*(q-l)*a[3]*b[3])/D+2*l*s*a[4]*b[4]/(3*H)
 hx=[0,F(1,3),F(1,3),0,0];vb=[0,F(1,3),0,1/(3*l),1/l];K=[1,l/3,1,F(1,3),1];E=vadd(hx,vscale(-rho,vb));C=[hx,vb,K];diag=[F(1,3),1/l,ell]
 S3=[[(diag[i]if i==j else 0)-I0(C[i],C[j])for j in range(3)]for i in range(3)];b=[I0(x,E)for x in C];Tb=m/(3*l)
 aug=[S3[i]+[b[i]]for i in range(3)]+[b+[Tb-I0(E,E)]]
 # Column congruence, first add hx-rho*vb to the last coordinate.
 T=[[1,0,0,1],[0,1,0,-rho],[0,0,1,0],[0,0,0,1]]
 columns=[list(x)for x in zip(*T)];shifted=[[pair(x,aug,y)for y in columns]for x in columns]
 Hcols=[[1,-1,0,0],[3,l,0,0],[-3,-l,1,0],[0,0,0,1]]
 transformed=[[pair(x,shifted,y)for y in Hcols]for x in Hcols]
 aa=(m-q*(l+1)/D-2*s/H)/(3*l);zz=2*(2*l-1)/(D*H);bb=m-m**2*A0/(3*J)-((l+9)*q-m**2)/(3*D)-2*l*s/(3*H);cc=-m*(1-(2*l+5)/J);dd=2*m+1-((q-1)*(N-10)+3*A0)/J
 last=[F(1,3)+rho/l,1-rho,rho-1];arrow=[[aa,zz,0,last[0]],[zz,bb,cc,last[1]],[0,cc,dd,last[2]],last+[Tb+F(1,3)+rho**2/l]]
 anti=[[(N-1)/(2*s)-(1+c**2)/2,c/2],[c/2,(N-1)/alpha-F(1,2)]]
 B=q/(6*D)+s/(3*H);standard=[[F(1,2)-B,-g*B],[-g*B,F(1,2)-g**2*B-nu/(2*H)]]
 a=-l*Fp/3;di=A-d;ts=6*s/(N-1-s)
 ZZ=a*a*Tb+c*c*ts/81+mu/H;DD=di*di*Tb+c*c*ts/36+F(9,4)*beta/H;ZD=a*di*Tb+c*c*ts/54
 final=[[l/(3*m)-ZZ,-ZD],[-ZD,F(3,2)-DD]]
 return locals()
