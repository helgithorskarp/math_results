"""Factored integral numerators for the original twelve-point frame."""
from polynomials import cross,dot,scale,add
from itertools import combinations
CORE=(0,1,2,4,5,6,7,8,9,10,11,12)
A=(0,5,6,7,9,11);B=(1,2,4,8,10,12)
CONTACTS=((0,5),(0,6),(0,7),(0,11),(1,2),(1,4),(1,10),(1,12),(2,4),(2,8),(2,10),(4,8),(5,7),(5,9),(5,11),(6,11),(7,12),(9,10),(9,11),(10,12))
PAIRS=tuple((i,j) for i in A for j in B if (i,j) not in ((7,12),(9,10),(7,1)))
def make(t,z,w):
 zero=t*0;one=zero+1;a=1+t;b=1-t;c=1+2*t;D=b*b*c;C=1+D*z*z;K=t*(9*t*t-2*t-3);J=a*a+K;h=(3*t-1)*(3*t+1)
 N={1:[a*a,zero,zero],2:[zero,a*a,zero],4:[zero,zero,a*a],8:[-a*a,2*t*a,2*t*a],10:[2*t*a,2*t*a,-a*a],12:[2*t*(1+3*t),3*t*t-2*t-1,-2*t*a]}
 def tilde(v):return [c*x-t*sum(v,zero) for x in v]
 W=add(add(scale([one,zero,zero],(D*z*z-1)*a*a),scale(N[12],2*t)),scale(tilde(cross(N[12],[one,zero,zero])),2*b*z))
 S=D*(t*z*z-2*z)+t*(2*t-1);E=C*C-S*S
 G=a**4*((1-t*t)*C*C-S*S)-K*K*C*C+2*S*K*t*a*a*C
 wd=a*a*C;vd=b*c*(a**6)*E
 V=add(scale(add(scale(W,K*C-S*t*a*a),scale(N[10],C*(t*a*a*C-S*K))),b*c*a*a),scale(tilde(cross(W,N[10])),-w))
 U=add(scale(add(scale(W,vd),scale(V,wd)),K),scale(tilde(cross(W,V)),-a*(3*t-1)))
 Wlift=scale(W,J*vd);Vlift=scale(V,J*wd);L=J*wd*vd;Omega=h*L
 Y={i:scale(v,h*J*C*vd) for i,v in N.items()}
 Y[6]=scale(U,h);Y[7]=scale(Wlift,h);Y[9]=scale(Vlift,h)
 for label,co in ((0,(2*t,2*t,b)),(5,(b,2*t,2*t)),(11,(2*t,b,2*t))):
  Y[label]=[a*sum((x*v[j] for x,v in zip(co,(U,Wlift,Vlift))),zero) for j in range(3)]
 return {'points':Y,'Omega':Omega,'D':D,'C':C,'S':S,'E':E,'G':G,'root_squared':D*G,'a':a,'b':b,'c':c,'J':J,'h':h,'W_num':W,'B_num':N,'W_den':wd,'V_den':vd,'U_num':U,'V_num':V}

def stereographic(t,u,v):
 R=(1-t)*((1+t)*(u*u+v*v)+2*t*u*v)
 return [R-1-2*t*(u+v),2*u,2*v],1+R,R

def incumbent_quintic(t):return 13*t**5-t**4+6*t**3+2*t*t-3*t-1

def constraints(t,z,w,addition_coordinates,strict_improvement=False):
 """Generate every defining polynomial using ring operations only.

 Three distinct coordinate pairs are supplied by the caller. Equality
 values are zero, strict values positive, weak and packing values >=0.
 All coefficients are integral; rational box bounds are cleared by
 positive integers. No sample test, symmetry quotient or local gate.
 """
 if len(addition_coordinates)!=3 or any(len(uv)!=2 for uv in addition_coordinates):raise ValueError('three arbitrary coordinate pairs')
 if type(strict_improvement)is not bool:raise TypeError('explicit strict-improvement switch')
 m=make(t,z,w);Y=m['points'];O=m['Omega'];added=[stereographic(t,*uv) for uv in addition_coordinates]
 weak=[('t-lower',25*t-14),('t-upper',593-1000*t),('z-lower',2*z+5),('z-upper',5-2*z),('w-lower',w),('w-upper',6-w),('core-chart',1-m['b']**2*z*z)]
 for j,uv in enumerate(addition_coordinates):
  for k,x in enumerate(uv):weak.extend(((str(j)+'-'+str(k)+'-lower',5*x+16),(str(j)+'-'+str(k)+'-upper',16-5*x)))
 packing=[('core-'+str(i)+'-'+str(k),t*O*O-dot(Y[i],Y[k],t)) for i,k in PAIRS]
 for j,(T,A,R) in enumerate(added):packing.extend(('added-'+str(j)+'-core-'+str(i),t*A*O-dot(T,Y[i],t)) for i in CORE)
 for j,k in combinations(range(3),2):
  T,A,_=added[j];U,Bden,_=added[k];packing.append(('added-'+str(j)+'-'+str(k),t*A*Bden-dot(T,U,t)))
 strict=[('positive-radical-sign',w),('strict-core-regularity',2*m['G']-m['a']**4*m['C']**2)]
 if strict_improvement:strict.append(('strict-improvement',-incumbent_quintic(t)))
 return {'equalities':[('positive-radical-square',w*w-m['root_squared'])],
         'strict':strict,
         'weak_domain':weak,'packing':packing}
