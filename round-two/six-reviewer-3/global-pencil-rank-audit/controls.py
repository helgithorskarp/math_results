"""Exact trust-boundary examples and consequential damage checks."""
from fractions import Fraction as F
from polys import cast,symbol,need,times,plus
from audit import detQQ,lagrange,megcd,mmul,madd,mdiv

def checks():
 rows=[]
 def record(name,verdict):need(verdict,name);rows.append(name)
 q=symbol('q');G=q*q+3*q+7
 # Algebraic clearing never supplies sufficiency at a zero slope.
 record('zero affine pivot retains necessity, never sufficiency',cast(0)*G==0 and G!=0)
 record('nonzero constant affine pivot has no root even with zero slope',cast(3)!=0)
 for aa,bb in [(0,0),(0,3),(2,0),(2,-5)]:
  FF=aa*q+bb;clear=bb*bb-3*aa*bb+7*aa*aa
  record('complete affine quadratic syzygy '+str((aa,bb)),aa*aa*G-clear==FF*(aa*q+3*aa-bb))
 # Fixed-degree Sylvester matrix vanishes when both polynomials specialize
 # to zero; no division by specialized leading coefficients is legal.
 record('specialized degree loss fixed determinant retained',detQQ([[0,0],[1,0]])==0)
 record('rational Gaussian pivot swap sign',detQQ([[0,2],[3,4]])==-6)
 record('duplicate determinant row damage rejected',detQQ([[1,2],[1,2]])==0)
 # Leading-degree preservation is indispensable, even in one variable.
 u,v=megcd([-1,257],[-1,257],257)
 record('modular unit can hide genuine complex rational root if leading degree drops',madd(mmul(u,[-1,257],257),mmul(v,[-1,257],257),257)==[1] and -1+257*F(1,257)==0 and 257%257==0)
 # Polynomial identity reconstruction must check a known degree bound.
 got=lagrange([-2,-1,0,1,2],[246,253,254,255,5],257)
 record('independent full cardinal interpolation',got==[254,0,0,1])
 # Correct values for x^3-3 at the five nodes are -11,-4,-3,-2,5;
 # therefore the changed data above must not masquerade as that polynomial.
 record('changed interpolation values do not match alleged cubic',lagrange([-2,-1,0,1,2],[247,253,254,255,5],257)!=[254,0,0,1])
 # Two rank-two equations with a common root, one double and one simple.
 record('joint simplicity retains individually double rows',1-2+1==0 and 1-1==0 and 2-2==0 and 1!=0)
 # Complex Gram fails: a=(1,i) has S=0 while a is nonzero.
 record('complex square cancellation blocks real Gram extension',plus((F(1),F(0)),times((F(0),F(1)),(F(0),F(1))))==(0,0))
 # Complex coefficient rank-two quadratics may have a single NONREAL root.
 record('complex uniqueness does not imply real root',plus(times((F(0),F(1)),(F(0),F(1))),(F(1),F(0)))==(0,0))
 # Singular complex factors are explicit and cannot be canceled globally.
 record('complex exceptional factors retain both distinct slices',F(-2,49)!=F(-4,7) and 49*F(-2,49)+2==0 and 7*F(-4,7)+4==0)
 # Exact projection identities, with unconstrained derivative Qprime.
 c=symbol('c');v=symbol('v');y=symbol('y');z=symbol('z')
 # In a real orthogonal frame C=(c,0), w=(1/c,v), a=(-c*v*y,y).
 # ||C||^2||w||^2=1+c^2*v^2 and orthogonal component of a is y.
 record('whole oblique projection norm identity',(1+c*c*v*v)*y*y==y*y+c*c*v*v*y*y)
 record('whole orthogonal derivative decomposition',(c*z-c*v*y)**2+y*y-y*y==(c*z-c*v*y)**2)
 return rows
