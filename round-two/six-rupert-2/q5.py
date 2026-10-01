"""Exact arithmetic in the ordered field Q(sqrt(5)).

Reused with attribution from the published J77 diameter source:
https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_projection_diameter/q5.py
This arithmetic implementation is prior work, not a new result.
"""
from fractions import Fraction as F


class Q:
    __slots__ = ('a','b')

    def __init__(self,a=0,b=0):
        if isinstance(a,Q): self.a,self.b = a.a,a.b
        else: self.a,self.b = F(a),F(b)

    def __add__(self,o):
        o=Q(o);return Q(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q(-self.a,-self.b)
    def __sub__(self,o): return self+-Q(o)
    def __rsub__(self,o): return Q(o)+-self
    def __mul__(self,o):
        o=Q(o);return Q(self.a*o.a+5*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=Q(o);den=o.a*o.a-5*o.b*o.b
        if not den: raise ZeroDivisionError
        return self*Q(o.a/den,-o.b/den)
    def __rtruediv__(self,o): return Q(o)/self
    def __eq__(self,o):
        o=Q(o);return self.a==o.a and self.b==o.b
    def __hash__(self): return hash((self.a,self.b))
    def sign(self):
        a,b=self.a,self.b
        if a==0: return (b>0)-(b<0)
        if b==0: return (a>0)-(a<0)
        if a>0 and b>0: return 1
        if a<0 and b<0: return -1
        c=a*a-5*b*b
        return ((c>0)-(c<0))*((a>0)-(a<0))
    def __lt__(self,o): return (self-Q(o)).sign()<0
    def __le__(self,o): return (self-Q(o)).sign()<=0
    def __gt__(self,o): return (self-Q(o)).sign()>0
    def __ge__(self,o): return (self-Q(o)).sign()>=0
    def __float__(self): return float(self.a)+float(self.b)*5**0.5
    def __repr__(self): return f'({self.a})+({self.b})sqrt5'


def dot(u,v): return sum((x*y for x,y in zip(u,v)),Q())
def sub(u,v): return tuple(x-y for x,y in zip(u,v))
def add(u,v): return tuple(x+y for x,y in zip(u,v))
def scale(a,u): return tuple(a*x for x in u)
def cross(u,v):
    return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
