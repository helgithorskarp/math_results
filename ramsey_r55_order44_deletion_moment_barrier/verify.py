"""Exact primal verification; no floating solver is imported."""
from pathlib import Path
import hashlib,json
import numpy as np

def require(condition,message):
    if not condition:
        raise ValueError(message)

def positive_definite(matrix):
    a=[[int(x) for x in row] for row in matrix]
    n=len(a)
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)), 'asymmetric matrix')
    previous=1; leading=[]
    for k in range(n):
        pivot=a[k][k]
        require(pivot>0,f'nonpositive leading principal minor {k}')
        leading.append(pivot)
        for i in range(k+1,n):
            for j in range(i,n):
                value,rem=divmod(pivot*a[i][j]-a[i][k]*a[k][j],previous)
                require(rem==0,'inexact Bareiss division')
                a[i][j]=value; a[j][i]=value
        previous=pivot
    return {'dimension':n,'positive_leading_principal_minors':len(leading),
            'determinant_decimal_digits':len(str(leading[-1])),
            'leading_minors_sha256':hashlib.sha256(json.dumps(leading,separators=(',',':')).encode()).hexdigest()}

def check(work, certificate):
    work=Path(work)
    control=json.loads(Path(certificate).read_text())
    nums=control['numerators'];denominator=control['denominator']
    require(len(nums)==464 and all(type(x) is int and x>0 for x in nums),'invalid numerators')
    require(type(denominator) is int and denominator==sum(nums),'invalid denominator')
    nv=np.array(nums,dtype=object)
    identity=json.loads((work/'degree_identity.json').read_text())
    require(identity['graphs']==control['graphs'],'identity graph order differs')
    residual=sum(a*b for a,b in zip(identity['row'],nums))
    require(residual==0,'degree-support equality failed')
    orders=[]
    for n in (43,44):
        z=np.load(work/f'model_{n}.npz')
        require(z['graphs'].tolist()==control['graphs'],'graph order differs')
        A=z['A'];slacks=A.astype(object)@nv
        require(all(x>0 for x in slacks),f'nonpositive scalar at order {n}')
        matrices=[]
        keys=sorted((k for k in z.files if k.startswith('Q')),key=lambda k:int(k[1:]))
        for key in keys:
            q=z[key]
            value=np.tensordot(nv,q.astype(object),axes=(0,0))
            matrices.append(positive_definite(value))
        orders.append({'n':n,'strict_scalar_inequalities':len(slacks),
                       'minimum_integer_scalar_slack':int(min(slacks)),
                       'positive_definite_matrices':len(matrices),
                       'positive_leading_principal_minors':sum(q['dimension'] for q in matrices),
                       'matrices':matrices})
    return {'status':'EXACT_COMMON_DENSITY_FEASIBLE','denominator':denominator,
            'positive_densities':len(nums),'degree_identity_residual':residual,'orders':orders,
            'terminal_order44_classes_closed':0,'verified_good44_graphs':0,
            'claim':'The specified averaged deletion-moment cone cannot prove nonexistence. No physical realization is asserted.'}
