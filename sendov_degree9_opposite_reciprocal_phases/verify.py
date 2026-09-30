"""Check every coefficient and reconstruct the norm derivative independently.

Python 3.11 standard library; no floats, solver, external ledger or parent
source.  Exact dual-number integral values and tensor interpolation are
independent of algebra.py's symbolic coefficient construction.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('face_exact_algebra',ROOT/'algebra.py')
A=importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)


def require(condition,message):
    if not condition:
        raise ArithmeticError(message)


def digest(value):
    data=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(data).hexdigest()


def dual_origin(b,c,q):
    """Integral and q derivative by scalar dual arithmetic in i beta.

    Return E,K.  B=beta^2=q(1-c^2) and B'=1-c^2 are differentiated
    inside every multiplication, including at q=0. No square root or
    division by beta is used.
    """
    B=q*(1-c*c)
    Bp=1-c*c

    def multiply(z,w):
        p,t,dp,dt=z
        r,s,dr,ds=w
        return (p*r-B*t*s,
                p*s+t*r,
                dp*r+p*dr-Bp*t*s-B*(dt*s+t*ds),
                dp*s+p*ds+dt*r+t*dr)

    pair=[(F(1),F(0),F(0),F(0)),
          (-2*b*c,-2*b,F(0),F(0)),
          (b*b*(1-q),F(0),-b*b,F(0))]
    coeff=[(F(1),F(0),F(0),F(0))]
    for _ in range(4):
        out=[(F(0),)*4 for _ in range(len(coeff)+2)]
        for j,z in enumerate(coeff):
            for k,w in enumerate(pair):
                v=multiply(z,w)
                out[j+k]=tuple(out[j+k][i]+v[i] for i in range(4))
        coeff=out
    P,T,dP,dT=tuple(sum(z[i]*F(9,k+1) for k,z in enumerate(coeff))
                    for i in range(4))
    E=P*P+B*T*T
    derivative=2*P*dP+Bp*T*T+2*B*T*dT
    return E,(1-q)*derivative+8*E


def inverse(matrix):
    n=len(matrix)
    rows=[list(row)+[F(i==j) for j in range(n)]
          for i,row in enumerate(matrix)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if rows[i][j]),None)
        require(pivot is not None,'Singular interpolation matrix')
        rows[j],rows[pivot]=rows[pivot],rows[j]
        z=rows[j][j]
        rows[j]=[v/z for v in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                z=rows[i][j]
                rows[i]=[v-z*w for v,w in zip(rows[i],rows[j])]
    result=[row[n:] for row in rows]
    for i in range(n):
        for j in range(n):
            require(sum(matrix[i][k]*result[k][j] for k in range(n))==F(i==j),
                    'Interpolation inverse identity failed')
    return result


def interpolated_cells():
    degrees=(16,8,7)
    tensors={}
    for i,j,k in product(*(range(d+1) for d in degrees)):
        b=F(i,16)
        c=b+(1-b)*F(j,8)
        q=F(k,28)
        tensors[(i,j,k)]=dual_origin(b,c,q)[1]
    inverse_checks=0
    for axis,d in enumerate(degrees):
        matrix=[[F(comb(d,j))*F(i,d)**j*(1-F(i,d))**(d-j)
                 for j in range(d+1)] for i in range(d+1)]
        inv=inverse(matrix)
        inverse_checks+=(d+1)**2
        out={}
        for e in tensors:
            value=F(0)
            for j in range(d+1):
                f=list(e)
                f[axis]=j
                value+=inv[e[axis]][j]*tensors[tuple(f)]
            out[e]=value
        tensors=out
    left,right={},{}
    for i,j,k in product(*(range(d+1) for d in degrees)):
        # Independent de Casteljau subdivision, not power substitution.
        left[(i,j,k)]=sum(F(comb(i,s),2**i)*tensors[(s,j,k)]
                          for s in range(i+1))
        right[(i,j,k)]=sum(F(comb(16-i,s-i),2**(16-i))*tensors[(s,j,k)]
                           for s in range(i,17))
    return [left,right],inverse_checks


def gauss_mul(z,w):
    return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])


def direct_gaussian(b,c,d,h):
    U=((1+h)*c,(1+h)*d)
    V=((1-h)*c,-(1-h)*d)
    coeff=[(F(1),F(0))]
    for z in [U]*4+[V]*4:
        out=[(F(0),F(0)) for _ in range(len(coeff)+1)]
        for j,w in enumerate(coeff):
            out[j]=tuple(out[j][i]+w[i] for i in range(2))
            p=gauss_mul(w,z)
            out[j+1]=tuple(out[j+1][i]-b*p[i] for i in range(2))
        coeff=out
    O=tuple(sum(z[i]*F(9,j+1) for j,z in enumerate(coeff)) for i in range(2))
    return O[0]**2+O[1]**2


def gaussian_controls(E,K):
    values=[]
    data=[(F(0),F(1),F(0)),(F(1),F(0),F(0)),
          (F(1),F(0),F(1,2)),(F(1,2),F(1,2),F(1,4))]
    for i in range(16):
        data.append((F(3+i,24),F((i%5)-2,9),F((i%7)-3,10)))
    for b,t,h in data:
        c,d=(1-t*t)/(1+t*t),2*t/(1+t*t)
        direct=direct_gaussian(b,c,d,h)
        unit=A.evaluate(E,(b,c,h*h))
        dual,dk=dual_origin(b,c,h*h)
        require(direct==unit==dual,'Exact Gaussian norm control failed')
        require(dk==A.evaluate(K,(b,c,h*h)),'Exact dual derivative control failed')
        values.append([str(b),str(c),str(d),str(h),str(unit),str(dk)])
    return values


def compute():
    E,K=A.origin_norm()
    require(len(E)==214 and len(K)==204,'Unexpected complete polynomial inventory')
    b,c,Q=[A.variable(i) for i in range(3)]
    balanced=A.substitute(E,2,{})
    aligned=A.substitute(balanced,1,A.ONE)
    # B(b)=sum_{j=0}^8(1-b)^j, including its continuous b=0 value.
    B=A.add(*(A.power(A.add(A.ONE,A.scale(b,-1)),j) for j in range(9)))
    require(aligned==A.mul(B,B),'Balanced aligned integral identity failed')
    reconstructed,inverse_checks=interpolated_cells()
    cells=[]
    coefficient_checks=0
    for index,(left,right,coeff,degrees) in enumerate(A.cells(K)):
        require(coeff==reconstructed[index],'Entrywise interpolation/subdivision mismatch')
        require(len(coeff)==1224,'Incomplete tensor certificate')
        require(all(v>7 for v in coeff.values()),'Uniform K>7 certificate failed')
        coefficient_checks+=len(coeff)
        cells.append({'b_interval':[str(left),str(right)],'degrees':list(degrees),
                      'coefficients':len(coeff),'minimum':str(min(coeff.values())),
                      'sha256':digest(A.canonical(coeff))})
    quotient,weak_coeff,weak_degrees=A.weak_mean_certificate()
    require(weak_degrees==(22,0,0) and len(weak_coeff)==23,'Incomplete weak-mean certificate')
    require(all(v>=F(8,9) for v in weak_coeff.values()),'Credited weak mean filter failed')
    controls=gaussian_controls(E,K)
    return {'status':'exact finite steps verified; surrounding argument is an ordinary written proof',
            'ring':'Q[b,c,Q], characteristic zero',
            'norm_terms':len(E),'derivative_terms':len(K),
            'norm_sha256':digest(A.canonical(E)),
            'derivative_sha256':digest(A.canonical(K)),
            'origin_cells':cells,'complete_coefficient_comparisons':coefficient_checks,
            'direct_dual_grid_values':1224,'interpolation_inverse_checks':inverse_checks,
            'weak_mean_coefficients':[str(v) for _,v in sorted(weak_coeff.items())],
            'weak_mean_quotient_sha256':digest(A.canonical(quotient)),
            'gaussian_controls':len(controls),'gaussian_controls_sha256':digest(controls),
            'balanced_reference_identities':1}


def validate(manifest,expected):
    require(manifest==expected,'Complete expected manifest mismatch')


def corrupt_controls(manifest):
    changes=[('norm_terms',0),('norm_sha256','0'*64),
             ('complete_coefficient_comparisons',2447),('direct_dual_grid_values',0),
             ('gaussian_controls_sha256','0'*64)]
    rejected=0
    for key,value in changes:
        bad=deepcopy(manifest)
        bad[key]=value
        try:
            validate(manifest,bad)
        except ArithmeticError:
            rejected+=1
    for selector in ['minimum','sha256','coefficients']:
        bad=deepcopy(manifest)
        bad['origin_cells'][0][selector]='invalid'
        try:
            validate(manifest,bad)
        except ArithmeticError:
            rejected+=1
    require(rejected==8,'Corrupted manifest was accepted')
    return rejected


if __name__=='__main__':
    require(len(sys.argv)==1,'No mutable output modes are supported')
    manifest=compute()
    expected=json.loads((ROOT/'expected.json').read_text())
    validate(manifest,expected)
    rejected=corrupt_controls(manifest)
    print(json.dumps({'verified':manifest,'corrupt_manifest_rejections':rejected},indent=2))
