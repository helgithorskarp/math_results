"""Separate exact rational-function audit; no target executable or data input."""
import json
from fractions import Fraction
from itertools import combinations
import sympy as S
from frame import base,plus,scale,dot,cross,inverse_metric,CONTACTS,AA,BB,TESTS,LABELS

field,t=S.polys.fields.field('t',S.QQ); r,b=base(t)
def eq(a,b,label):
    if a-b!=0: raise ValueError('identity failed: '+label)
    checked.append(label)
checked=[]
D=(1-t)**2*(1+2*t)
k=t*(9*t*t-2*t-3)/(1+t)**2
h=4*t*t/(1+t)-1
ell=r*(h+k)-t
for i in BB: eq(dot(b[i],b[i],t),1,'B unit '+str(i))
for i,j in combinations(BB,2):
    if (i,j) in CONTACTS: rhs=t
    elif (i,j) in ((1,8),(2,12),(4,10)):rhs=h
    elif (i,j) in ((4,12),(8,10)):rhs=k
    elif (i,j)==(8,12):rhs=ell
    else:raise ValueError('B pair completeness')
    eq(dot(b[i],b[j],t),rhs,'B pair '+str((i,j)))
u,w,v=[1,0,0],[0,1,0],[0,0,1]
def kdot(x,y):return (1-k)*sum(a*b for a,b in zip(x,y))+k*sum(x)*sum(y)
den=(2*r-1)*(r+1)
a={6:u,7:w,9:v,
 0:scale(1/den,plus(plus(scale(r,u),scale(r,w)),scale(1-r,v))),
 5:scale(1/den,plus(plus(scale(1-r,u),scale(r,w)),scale(r,v))),
 11:scale(1/den,plus(plus(scale(r,u),scale(1-r,w)),scale(r,v)))}
for i in AA:eq(kdot(a[i],a[i]),1,'A unit '+str(i))
noncontacts=[]
for i,j in combinations(AA,2):
    value=kdot(a[i],a[j])
    if (i,j) in CONTACTS:rhs=t
    elif value-k==0:rhs=k
    elif value-h==0:rhs=h
    else:raise ValueError('A unknown noncontact')
    eq(value,rhs,'A pair '+str((i,j)))
    if rhs!=t:noncontacts.append([i,j,str(rhs)])
eq(k.diff(t),(9*t*t-1)*(t+3)/(1+t)**3,'monotone k')
eq(k-t,4*t*(2*t+1)*(t-1)/(1+t)**2,'k<t factor')
eq(h-t,(3*t+1)*(t-1)/(1+t),'h<t factor')
mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
eq(mu*mu,D*(1+2*k)/(1+k)**2,'mu square')
eq(1+2*k,(3*t-1)**2*(2*t+1)/(1+t)**2,'k Gram positivity')
eq(9*t**3-t*t-t+1,(1+t)**2*(1+k),'U denominator')
d=inverse_metric(cross(b[12],b[1]),t); bb=b[12]; e=b[1];f=plus(e,scale(-t,bb))
eq(dot(d,d,t),(1-t*t)/D,'circle normal length')
eq(dot(f,d,t),0,'circle transverse orthogonality')
eq(dot(f,f,t),1-t*t,'circle radial length')
eq(dot(bb,d,t),0,'normal contact orthogonality')
# Polynomial fraction fields avoid general-expression expansion overhead.
field2,t,z=S.polys.fields.field('t,z',S.QQ)
r,b=base(t); D=(1-t)**2*(1+2*t);bb=b[12];e=b[1]
d=inverse_metric(cross(bb,e),t);f=plus(e,scale(-t,bb));C=1+D*z*z
W=plus(scale(t,bb),plus(scale((D*z*z-1)/C,f),scale(2*D*z/C,d)))
eq(dot(W,W,t),1,'W circle unit')
eq(dot(W,bb,t),t,'W circle contact')
eq(dot(W,e,t)-t,(1-t)*(1+2*t)*((1-t)**2*z*z-1)/C,'chart packing gap')
sv=dot(W,b[10],t)
eq(sv,(D*(t*z*z-2*z)+t*(2*t-1))/C,'homogeneous s')
field3,sv,kv,tv=S.polys.fields.field('s,k,T',S.QQ)
gv=1-sv*sv-kv*kv-tv*tv+2*sv*kv*tv
av=(kv-sv*tv)/(1-sv*sv);bv=(tv-sv*kv)/(1-sv*sv)
eq(av+bv*sv,kv,'V projection first contact')
eq(av*sv+bv,tv,'V projection second contact')
eq(av*av+bv*bv+2*sv*av*bv+gv/(1-sv*sv),1,'both V roots unit')
eq(2*kv*kv/(1+kv)+(1+2*kv)*(1-kv*kv)/(1+kv)**2,1,'both U roots unit')
eq(gv,(1-sv*sv)*(1-tv*tv)-(kv-sv*tv)**2,'strong denominator identity')
def gram(s,k,t):return 1-s*s-k*k-t*t+2*s*k*t
subneg=gram(Fraction(-24,25),Fraction(-3,10),Fraction(14,25))
subpos=gram(Fraction(7,10),Fraction(-1,5),Fraction(14,25))
eq(subneg,-Fraction(33,12500),'negative s endpoint')
eq(subpos,-Fraction(1,2500),'positive s endpoint')
field,t=S.polys.fields.field('t',S.QQ)
k=t*(9*t*t-2*t-3)/(1+t)**2
def kval(x):return x*(9*x*x-2*x-3)/(1+x)**2
ends={str(x):str(kval(x)) for x in (Fraction(14,25),Fraction(593,1000))}
if not all(Fraction(-3,10)<kval(x)<Fraction(-1,5) for x in (Fraction(14,25),Fraction(593,1000))):raise ValueError('k endpoints')
if len(CONTACTS)!=20 or len(TESTS)!=33 or len(set(LABELS))!=12:raise ValueError('scope completeness')
report=dict(identities=len(checked),checks=checked,k_endpoints=ends,A_noncontacts=noncontacts,
 labels=list(LABELS),contacts=[list(e) for e in CONTACTS],tests=[list(e) for e in TESTS],
 strengthened_denominator='g>1/2 implies 1-s^2>625/858, and |s|<sqrt(233/858)<523/1000')
print(json.dumps(report,sort_keys=True,indent=2))
