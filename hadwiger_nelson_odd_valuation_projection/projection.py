"""Explicit four-colouring of E(sqrt(D)) when v_2(D) is odd at one R-place."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from hashlib import sha256
from math import lcm
import sys
P=Path(__file__).resolve().parent;ROOT=P.parent
path=ROOT/'hadwiger_nelson_nonmono_field_obstruction/coloring.py'
if sha256(path.read_bytes()).hexdigest()!='a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e':raise ValueError('field dependency hash')
sys.path.insert(0,str(path.parent));import coloring as K

def need(ok,msg):
 if not ok:raise ValueError(msg)

@lru_cache(maxsize=None)
def valuation_real(d,sign=1):
 need(len(d)==2 and any(d) and sign in [-1,1],'nonzero real element and embedding required')
 a,b=map(F,d);den=lcm(a.denominator,b.denominator);aa=int(a*den);bb=int(b*den);vd=(den&-den).bit_length()-1;bits=16
 while True:
  z=(aa+bb*sign*K.root33_mod_power2(bits))%(1<<bits)
  if z:return (z&-z).bit_length()-1-vd
  bits*=2

def real_sign(d):
 a,b=map(F,d)
 if not b:return (a>0)-(a<0)
 if not a:return (b>0)-(b<0)
 if (a>0)==(b>0):return (a>0)-(a<0)
 q=a*a-33*b*b;return ((a>0)-(a<0))*((q>0)-(q<0))

@lru_cache(maxsize=None)
def certify_radicand(d,sign=1):
 need(len(d)==2 and real_sign(d)>0,'positive physical radicand required');v=valuation_real(d,sign);need(v%2==1,'odd valuation hypothesis fails');return v

def conjugate_place(x,sign):
 need(sign in [-1,1],'embedding sign');a,b,c,d=x;return a,sign*b,c,sign*d

def color(z,d,sign=1):
 """z=(x,y) represents x+y sqrt(d), with x,y in E; either real root is valid."""
 certify_radicand(d,sign);need(len(z)==2 and all(len(x)==4 for x in z),'point basis')
 return K.color(tuple(map(F,conjugate_place(z[0],sign))))

def add(x,y):return K.add(x[0],y[0]),K.add(x[1],y[1])
def neg(x):return K.negate(x[0]),K.negate(x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y,D):
 return K.add(K.multiply(x[0],y[0]),K.multiply(D,K.multiply(x[1],y[1]))),K.add(K.multiply(x[0],y[1]),K.multiply(x[1],y[0]))
def conj(x):return K.conjugate(x[0]),K.conjugate(x[1])
def inverse(x,D):
 den=K.add(K.multiply(x[0],x[0]),K.negate(K.multiply(D,K.multiply(x[1],x[1]))));q=K.inverse(den)
 return K.multiply(x[0],q),K.negate(K.multiply(x[1],q))
ZERO=(K.ZERO,K.ZERO);ONE=(K.ONE,K.ZERO)
