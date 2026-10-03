"""Generic real/jet formula for the original twelve-point G20 frame.

Basis(1,2,4), sole branch epsilon=-1, eta=+1. Original twenty contacts,
no label13, contact support, clipping or extra packing hypothesis.
The credited original frame9774 supplies its ordinary complete geometry.
"""
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def him(a,t):return [x/(1-t)-t*sum(a,t*0)/((1-t)*(1+2*t)) for x in a]
def points(t,z):
 D=(1-t)**2*(1+2*t);r=2*t/(1+t);k=t*(9*t*t-2*t-3)/(1+t)**2;gamma=k/(1+k)
 mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/((1+t)**2*(1+k));den=(2*r-1)*(r+1)
 B={i:[t*0+(1 if j==s else 0) for j in range(3)] for s,i in enumerate((1,2,4))}
 for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2)):B[n]=[r*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
 C=1+D*z**2;d=him(cross(B[12],B[1]),t)
 W=[t*a+(D*z**2-1)/C*(b-t*a)+2*D*z/C*x for a,b,x in zip(B[12],B[1],d)]
 s=(D*(t*z**2-2*z)+t*(2*t-1))/C;g=1-s**2-k**2-t**2+2*s*k*t;de=1-s**2
 q=(D*g).sqrt();n=him(cross(W,B[10]),t)
 V=[((k-s*t)*a+(t-s*k)*b-q*x)/de for a,b,x in zip(W,B[10],n)]
 U=[gamma*(a+b)+mu*x for a,b,x in zip(W,V,him(cross(W,V),t))]
 P=dict(B)|{6:U,7:W,9:V}
 for label,co in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):P[label]=[sum((a*v[j] for a,v in zip(co,(U,W,V))),t*0)/den for j in range(3)]
 return P,{'g':g.v,'de':de.v,'q':q.v,'chart':(1-(1-t)**2*z**2).v}
