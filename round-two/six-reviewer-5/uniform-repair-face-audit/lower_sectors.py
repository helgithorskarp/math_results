"""Independent full-S_q original lower sectors and singular right derivative.

Physical constant indicators and f=(1,-1,0,...) on outside labels.
Uses only the original affine table, not target generators/certificates.
"""
import json
from pathlib import Path
from sympy import QQ, symbols
import original_field as O

qs=symbols('q'); FF=QQ.frac_field(qs); q=FF.convert(qs); Z=FF.zero; I=FF.one

def conv(x):
    return FF.convert(x.as_expr()) if hasattr(x,'as_expr') else FF.convert(x)

TAB={key:tuple(conv(y) for y in vals) for key,vals in O.table().items()}

def c(x,n):
    if n==0:return I
    if n==1:return x
    if n==2:return x*(x-1)/2
    raise ValueError('invalid literal outside count')

def sector(standard):
    groups=[(0,),(0,),(1,),(2,4),(3,5),(6,)] if standard else [(0,),(0,),(1,),(2,4),(6,),(7,),(3,5),(6,)]
    sizes=[1,2,1,1,1,1] if standard else [1,2,1,1,0,0,1,1]
    out0=[];out1=[];norm=[]
    for g,r in zip(groups,sizes):
        norm.append(len(g)*(2*(q-2) if r==2 else 2) if standard else len(g)*c(q,r))
    for i,(g,r) in enumerate(zip(groups,sizes)):
        row0=[];row1=[]
        for j,(h,t) in enumerate(zip(groups,sizes)):
            dis=sum(not(a&b) for a in g for b in h)
            v0=(3*q+4)*norm[i] if i==j else Z
            if not standard:v0-=norm[i]*norm[j]
            if dis:
                typ=tuple(sorted(((g[0].bit_count(),r),(h[0].bit_count(),t))))
                b0,b1=TAB[typ]
                factor=(-2*(q-2)*(q-3) if r==t==2 else -2 if r==t==1 else -2*(q-2)) if standard else c(q,r)*c(q-r,t)
                v0+=dis*factor*b0; v1=dis*factor*b1
            else:v1=Z
            row0.append(v0);row1.append(v1)
        out0.append(row0);out1.append(row1)
    O.require(all(A[i][j]==A[j][i] for A in (out0,out1) for i in range(len(groups)) for j in range(len(groups))), 'whole original sector symmetry')
    return out0,out1,norm

def deriv(standard):
    A,D,norm=sector(standard)
    target=len(A)-1;excluded=[] if standard else [0]
    S,V=O.short(A,[target],excluded,norm)
    normtarget=2 if standard else q
    value=S[0][0]/normtarget
    E=O.energy(D,V)[0][0]
    record=dict(standard=standard,zero=value,zero_minimizer=[row[0] for row in V],Gram0=A,Delta=D)
    if not standard:
        z=[I,I,Z,Z,Z,-I,Z,Z]
        O.require(all(sum((A[i][j]*z[j] for j in range(8)),Z)==0 for i in range(8)), 'all singular-kernel rows')
        alpha=sum((z[i]*D[i][j]*z[j] for i in range(8) for j in range(8)),Z)
        cross=sum((z[i]*D[i][j]*V[j][0] for i in range(8) for j in range(8)),Z)
        O.require(alpha==q*(q+1)/2+3*(q+1)/(3*q+5),'original kernel normalization')
        E-=cross*cross/alpha
        record.update(alpha=alpha,shift=-cross/alpha)
    record['right_derivative']=E/normtarget
    return record

def encode(x):
    if isinstance(x,dict):return {a:encode(b) for a,b in x.items()}
    if isinstance(x,list):return [encode(y) for y in x]
    return str(x.as_expr()) if hasattr(x,'as_expr') else x

if __name__=='__main__':
    nu=deriv(True); print('full original standard derivative complete',flush=True)
    tau=deriv(False); print('full original singular trivial derivative complete',flush=True)
    F=2*nu['right_derivative']/nu['zero']**2+tau['right_derivative']/tau['zero']**2
    rec=dict(nu=nu,tau=tau,F=F)
    P=Path(__file__).resolve().parent/'lower-sectors.json';P.write_text(json.dumps(encode(rec),indent=2)+'\n')
    print('degrees F',F.numer.degree(),F.denom.degree(),flush=True)
