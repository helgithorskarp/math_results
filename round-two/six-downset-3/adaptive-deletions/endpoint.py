"""Exact unbounded zero-parameter endpoint; ordinary bridge in PROOF.md."""
from pathlib import Path
import sys,json
from fractions import Fraction as F
import bootstrap
from weights import formula,model
from poly import R,mul,exact_divide
from signs import determinant,lower_sign
from exact import require,digest

def endpoint():
    q=R((4,1));data=model(q,formula(q,F(0)))
    clear=2*q*(q-1)*(q-2)*(q-3);clear.coefficients_positive()
    lower=[];upper=[]
    for item in data:
        degree=item['degree'];levels=item['levels'];norms=item['norms'];g=item['lower'];ks=item['kernel'];size=len(norms)
        ks=ks+[[1]*size] if degree==(0,0) else ks
        require(all(sum(g[i][j]*v[j] for j in range(size))==0 for i in range(size) for v in ks),'zero-endpoint kernel action')
        anchors=[(0,1),(1,0),(2,0)] if degree==(0,0) else [(1,0)] if degree==(1,0) else []
        if ks:require(determinant([[(R(v[levels.index(a)])).n for a in anchors] for v in ks])!=(F(0),),'zero-endpoint anchor independence')
        keep=[i for i in range(size) if levels[i] not in anchors]
        scaled=[[exact_divide(mul(clear.n,g[i][j].n),mul(clear.d,g[i][j].d)) for j in keep] for i in keep]
        for order in range(1,len(keep)+1):
            coeff=determinant([row[:order] for row in scaled[:order]]);lower_sign(coeff)
            lower.append({'degree':degree,'order':order,'polynomial_degree':len(coeff)-1,'coefficients':[str(x) for x in coeff]})
        if degree==(0,0):v=[F(4,3)/q if a==0 else 2+1/q if a==3 else R(1) for a,b in levels]
        elif degree==(0,1):v=[R(1) if a==0 else R(F(9,10)) for a,b in levels]
        else:v=[R(1)]*size
        for x in v:x.coefficients_positive()
        for i in range(size):
            absolute=R(0)
            for j in range(size):
                entry=g[i][j]/norms[i]
                try:entry.coefficients_positive(strict=False)
                except ValueError:entry=-entry;entry.coefficients_positive(strict=False)
                absolute+=entry*v[j]/v[i]
            margin=2*(3*q+4)-absolute;margin.coefficients_positive(strict=False)
            upper.append({'degree':degree,'row':i,**margin.record()})
    require(len(lower)==14 and len(upper)==18,'zero-endpoint sign coverage')
    require(formula(q,F(1,16))=={key:(value+formula(q,F(1,8))[key])/2 for key,value in formula(q,F(0)).items()},'affine midpoint table identity')
    return {'q':'4+u,u>=0','kappa':'0','kernel':'span(Sa,Sb,Sc,F,1)','lower_leading_determinants':lower,'weighted_upper_margins':upper,'affine_midpoint_identity':True}

if __name__=='__main__':
    record=endpoint()
    print(json.dumps({'agent':'six-downset-3','role':'researcher','status':'author exact coefficient certificate; unformalized ordinary bridge in PROOF.md','record':record,'record_sha256':digest(record)},sort_keys=True,indent=2))
