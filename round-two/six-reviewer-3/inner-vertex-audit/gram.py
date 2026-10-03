"""Universal symmetric3-by3 adjugate/norm bridges in nine indeterminates.

Small literal coefficient convolution, separate from the digit engine.
"""
import hashlib,json

ZERO=(0,)*9
class P:
    def __init__(self,rows):self.rows={k:v for k,v in rows.items() if v}
    def __add__(self,other):
        other=poly(other);rows=dict(self.rows)
        for k,v in other.rows.items():rows[k]=rows.get(k,0)+v
        return P(rows)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.rows.items()})
    def __sub__(self,other):return self+-poly(other)
    def __rsub__(self,other):return poly(other)+-self
    def __mul__(self,other):
        other=poly(other);rows={}
        for k,v in self.rows.items():
            for l,w in other.rows.items():
                s=tuple(a+b for a,b in zip(k,l));rows[s]=rows.get(s,0)+v*w
        if len(rows)>5000:raise RuntimeError('fixed universal coefficient limit; incomplete')
        return P(rows)
    __rmul__=__mul__

def poly(x):
    if isinstance(x,P):return x
    if type(x) is not int:raise TypeError('integer polynomial coefficients')
    return P({ZERO:x})

def det(A):
    return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])

def adj(A):
    out=[]
    for i in range(3):
        row=[]
        for j in range(3):
            rs=[k for k in range(3) if k!=j];cs=[k for k in range(3) if k!=i]
            row.append(((-1)**(i+j))*(A[rs[0]][cs[0]]*A[rs[1]][cs[1]]-A[rs[0]][cs[1]]*A[rs[1]][cs[0]]))
        out.append(row)
    return out

def verify():
    vars=[P({tuple(int(k==j) for k in range(9)):1}) for j in range(9)]
    a,d,f,b,c,e,*rhs=vars;A=[[a,b,c],[b,d,e],[c,e,f]];D=det(A);Q=adj(A)
    lam=[sum(Q[i][j]*rhs[j] for j in range(3)) for i in range(3)]
    pairs={}
    for i in range(3):
        for j in range(3):pairs['adjugate_'+str(i)+str(j)]=(sum(A[i][k]*Q[k][j] for k in range(3)),D if i==j else poly(0))
    pairs['norm']=(sum(lam[i]*A[i][j]*lam[j] for i in range(3) for j in range(3)),D*sum(rhs[i]*lam[i] for i in range(3)))
    out={}
    for name,(left,right) in pairs.items():
        if left.rows!=right.rows:raise ValueError('whole universal coefficient identity failed')
        rows=[[list(k),v] for k,v in sorted(left.rows.items())]
        out[name]={'whole_common_coefficient_rows':rows,'whole_zero_residual':True}
    # These false bridges must fail as entire coefficient dictionaries.
    if (pairs['norm'][0]+1).rows==pairs['norm'][1].rows:raise ValueError('false norm accepted')
    bad=adj(A);bad[0][1]=-bad[0][1]
    if all((sum(A[i][k]*bad[k][j] for k in range(3))-(D if i==j else 0)).rows=={} for i in range(3) for j in range(3)):raise ValueError('cofactor-sign corruption accepted')
    return {'variable_order':['m00','m11','m22','m01','m02','m12','rhs0','rhs1','rhs2'],
            'whole_universal_identities':out,'damaged_norm_and_cofactor_rejected':True}

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True,separators=(',',':')))
