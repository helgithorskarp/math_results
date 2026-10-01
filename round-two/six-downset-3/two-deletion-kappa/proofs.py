"""Regenerate every unbounded coefficient and exact constant identity."""
import bootstrap
from fractions import Fraction as F
from weights import formula,cap_parameters,credited_formula,model,inverse,KAPPA,FLOOR
from poly import R,mul,exact_divide
from signs import determinant,lower_sign
from exact import require,digest

EPSILON=FLOOR

def cap(q,k,kappa):
    require(type(q) is int and k==2,"two-deletion literal comparison domain")
    _,_,chi,gamma=cap_parameters(F(q),kappa)
    return {"chi":str(chi),"gamma":str(gamma),"positive":chi>0}

def base():
    q=R((4,1));require(formula(q,F(1,2))==credited_formula(q),'symbolic fixed-kappa baseline differs')
    data=model(q,formula(q,KAPPA));clear=16*q*(q-1)*(q-2)*(q-3)*(3*q+5)*(q+1);clear.coefficients_positive()
    lower=[];upper=[]
    for item in data:
        degree=item['degree'];levels=item['levels'];norms=item['norms'];ks=item['kernel'];g=item['lower'];size=len(norms)
        proj=[[R(norms[i]*int(i==j)) for j in range(size)] for i in range(size)]
        if ks:
            kernel_gram=[[sum(norms[h]*v[h]*w[h] for h in range(size)) for w in ks] for v in ks];inv=inverse(kernel_gram)
            for i in range(size):
                for j in range(size):proj[i][j]-=norms[i]*norms[j]*sum(ks[a][i]*inv[a][b]*ks[b][j] for a in range(len(ks)) for b in range(len(ks)))
        shifted=[[g[i][j]-EPSILON*proj[i][j] for j in range(size)] for i in range(size)]
        require(all(sum(shifted[i][j]*v[j] for j in range(size))==0 for i in range(size) for v in ks),'floor prescribed kernel differs')
        anchors=[(1,0),(2,0)] if degree==(0,0) else [(1,0)] if degree==(1,0) else []
        if ks:
            require(determinant([[(R(v[levels.index(a)])).n for a in anchors] for v in ks])!=(F(0),),'kernel anchors are singular')
        keep=[i for i in range(size) if levels[i] not in anchors]
        scaled=[[exact_divide(mul(clear.n,shifted[i][j].n),mul(clear.d,shifted[i][j].d)) for j in keep] for i in keep]
        for order in range(1,len(keep)+1):
            coeff=determinant([row[:order] for row in scaled[:order]]);lower_sign(coeff)
            lower.append({'degree':degree,'order':order,'polynomial_degree':len(coeff)-1,'coefficients':[str(x) for x in coeff]})
        # The same complete action, with exact sign certificates, bounds
        # its largest eigenvalue by 2s via weighted absolute row sums.
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
    trivial=data[0];levels=trivial['levels'];norms=trivial['norms'];ks=trivial['kernel']
    resid=[R(1) if a==0 else 1/(3*q+5) if a<3 else -3*(q+1)/(3*q+5) for a,b in levels]
    require(all(sum(norms[i]*resid[i]*v[i] for i in range(len(levels)))==0 for v in ks),'P1 is not orthogonal to known kernels')
    require(all(sum(trivial['lower'][i])==KAPPA*norms[i]*resid[i] for i in range(len(levels))),'variable-kappa C1 identity fails')
    alpha=q*(q+1)/2+3*(q+1)/(3*q+5)
    require(sum(norms[i]*resid[i]**2 for i in range(len(levels)))==alpha,'projected-constant norm identity differs')
    require(len(lower)==15 and len(upper)==18,'unbounded base sign coverage differs')
    return {'q':'4+u,u>=0','kappa':str(KAPPA),'spectral_floor':str(EPSILON),'lower_floor_determinants':lower,'weighted_upper_margins':upper,'four_exact_kernel_and_constant_action':True,'projected_constant_norm':alpha.record()}

def cap_region():
    q=R((7,1));k=2;N=(q*q+13*q+16)/2-k;s=3*q+4;g=N-2*s
    alpha=q*(q+1)/2+3*(q+1)/(3*q+5);h=1/(3*q+5);c=KAPPA
    chi=k*g*(N-c+c*h)**2-((k-1)*(N-c)+c*alpha)*(N-c)*(N-s-k)
    gamma=g*chi/(N*(N-c)**2*(N-s-k));chi.coefficients_positive();gamma.coefficients_positive()
    literal=[]
    for qq in [7,8,9,10,12,24]:
        info=cap(qq,k,KAPPA);require(chi.at(qq-7)==F(info['chi'])>0 and gamma.at(qq-7)==F(info['gamma'])>0,'symbolic/literal cap scalar differs')
        literal.append({'q':qq,**info})
    return {'q':'7+u,u>=0','deletions':k,'kappa':str(c),'chi':chi.record(),'gamma':gamma.record(),'chi_degrees':[len(chi.n)-1,len(chi.d)-1],'literal_scalar_comparisons':literal}
