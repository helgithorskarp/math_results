"""Closed-form rational/algebraic controls for arithmetic and unconstrained AD."""
from fractions import Fraction as F
from algebra import A,T,solve
from enclosure import Box,SCALE
from jets import Jet

def audit():
    checks=0
    def contains(b,x):
        if not F(b.lo,SCALE)<=x<=F(b.hi,SCALE):raise ValueError('rational interval primitive containment')
    for a in (F(-7,3),F(0),F(2,7),F(17,5)):
        for b in (F(-11,4),F(1,3),F(13,6)):
            x,y=Box(a),Box(b)
            for z,v in ((x+y,a+b),(x-y,a-b),(x*y,a*b),(x/y,a/b)):
                contains(z,v);checks+=1
        contains(Box(a).square(),a*a);checks+=1
    for a,b in ((F(-2),F(3)),(F(-7),F(-1)),(F(1,3),F(11,4))):
        sq=Box(a,b).square()
        for x in (a,b,(a+b)/2):contains(sq,x*x);checks+=1
    for a in (F(1,3),F(2),F(17,5)):
        sq=Box(a).sqrt()
        if not F(sq.lo,SCALE)**2<=a<=F(sq.hi,SCALE)**2:raise ValueError('integer-square-root enclosure')
        checks+=1
    t,z=Jet(T,1,0),Jet(A(2),0,1)
    forms=[(t*t,T*T,2*T,A()),(t/z,T/2,A(F(1,2)),-T/4),((t+z)/(t-z),(T+2)/(T-2),-4/(T-2)**2,2*T/(T-2)**2),((t+z).square(),(T+2)**2,2*(T+2),2*(T+2)),((t.square()).sqrt(T),T,A(1),A())]
    for out,value,dt,dz in forms:
        if (out.v,out.d)!=(value,(dt,dz)):raise ValueError('closed-form independent derivative rule')
        checks+=3
    x=A([F(2,3),-1,4,F(7,5),F(-2,9)])
    if x/x!=1 or 13*T**5-T**4+6*T**3+2*T**2-3*T-1:raise ValueError('complete quotient primitive')
    for bad in (lambda:Box(-1,1).__rtruediv__(1),lambda:Box(-1).sqrt(),lambda:A().__rtruediv__(1)):
        try:bad()
        except (ArithmeticError,ValueError,ZeroDivisionError):checks+=1
        else:raise ValueError('invalid arithmetic domain accepted')
    return dict(closed_form_and_domain_checks=checks,unconstrained_derivatives_before_quotient_reduction=True)
if __name__=='__main__':
    import json
    print(json.dumps(audit(),sort_keys=True))
