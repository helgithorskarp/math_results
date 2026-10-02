"""Transcription of written rational definitions, not new target implementation."""
from fractions import Fraction as F
from linear import need

def model(r,l,q,harmonic=True):
 s=q+3;w=q+2;m=3*r+l;ell=m+1;t=r+l-1;N=2*q+2*m;H=N-1;rho=(q-1)/(q+1)
 d=3*(q-ell-1)/(ell*q);g=(q-ell+1)/(ell*w);Fp=-g/rho;A=(-d-l*Fp/r)/2;a=-d/3;ast=(-r*d/3-A)/(r-1);c=(a-d)*q/s;common=(ell*q+2-6*r)/ell**2;e2=q/(3*r)+rho**2*w/l;di2=q*(r-1)/(3*r)
 etaL=w-common-A*A*e2-ast*ast*di2-2*s*c*c/3
 etaF=w-common-d*d*(e2+di2)-2*s*c*c*(r-1)/(3*t*t)
 etaP=w-common-Fp*Fp*e2-g*g*w*(l-1)/l-2*s*c*c*r/(3*t*t)
 pair=-1-common-A*d*e2-ast*d*di2;mu=(2*pair+etaF)/3;alpha=2*(2*etaL-pair-etaF);beta=etaF-mu
 C=1/(2*(l/(3*r*mu)+3*r/(l*etaP)+m/q)) if harmonic else None
 nuT=(r*mu-l*C/3)/(r-1) if harmonic else None;nuL=(l*etaP-3*r*C)/(l-1) if harmonic else None
 return locals()
def arrow(r,l,q):
 m=3*r+l;N=2*q+2*m;s=q+3;D=N-7;H=N-1;A0=N-q-2;J=A0*(N-4)-3*(q-1);rho=(q-1)/(q+1)
 aa=(m-q*(l+r)/D-2*r*s/H)/(3*r*l);zz=2*(2*m-7)/(D*H)
 bb=m-m*m*A0/(3*J)-((l+9*r)*q-m*m)/(3*D)-2*l*s/(3*H)
 cc=-m*(1-(2*m-1)/J);dd=2*m+1-((q-1)*(N-10)+3*A0)/J
 c1=1/(3*r)+rho/l;c2=1-rho;e=m/(3*r*l)+1/(3*r)+rho*rho/l
 return [[aa,zz,0,c1],[zz,bb,cc,c2],[0,cc,dd,-c2],[c1,c2,-c2,e]]
def tests(r,l,q,boundary=False):
 z=model(r,l,q,not boundary);s=z['s'];H=z['H'];d=z['d'];g=z['g'];c=z['c'];ast=z['ast'];beta=z['beta'];mu=z['mu'];etaP=z['etaP'];m=z['m'];ell=z['ell'];t=z['t'];rho=z['rho'];Fp=z['Fp'];A=z['A']
 nuL=l*etaP/(l-1);nuT=2*mu-2*q/F(87) if boundary else z['nuT'];Chat=q/(2*m)
 anti=[[H/(2*s)-(1+c*c)/2,c/2],[c/2,H/z['alpha']-F(1,2)]]
 B=q/(6*(H-6))+s/(3*H);pend=[[F(1,2)-B,-g*B],[-g*B,F(1,2)-g*g*B-nuL/(2*H)]]
 Tq=H-q-6;Ts=H-q-3
 LL=ast*ast*q/(6*Tq)+c*c*s/(12*Ts)+nuT/(2*H)+beta/(8*H)
 FF=d*d*q/(6*Tq)+c*c*s/(3*t*t*Ts)+nuT/(2*H)+beta/(2*H)
 LF=ast*d*q/(6*Tq)+c*c*s/(6*t*Ts)+nuT/(2*H)-beta/(4*H)
 tri=[[F(1,4)-LL,-LF],[-LF,F(1,2)-FF]]
 Tb=m/(3*r*l);aZ=-l*Fp/(3*r);bZ=c*l/(9*r*t);dE=A-d;bD=c*(t+2*(r-1))/(6*r*t);T=6*r*s/(H-s)
 fin=[[l/(3*r*m)-aZ*aZ*Tb-bZ*bZ*T-l*Chat/(3*r*H),-aZ*dE*Tb-bZ*bD*T],[-aZ*dE*Tb-bZ*bD*T,F(3,2)/r-dE*dE*Tb-bD*bD*T-F(9,4)*beta/(r*H)]]
 return {'anti':anti,'pendant':pend,'triangle':tri,'fixed_inverse':arrow(r,l,q),'final':fin}
