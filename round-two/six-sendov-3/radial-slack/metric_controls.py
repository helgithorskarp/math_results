"""Literal positive-eta factor, root-norm, conjugate and pair-dual controls.

Finite controls check exact formulas. Universal identities and the IFT/coverage
bridge are proved separately in PROOF.md; finite records are not coverage.
"""
from fractions import Fraction as F
from radial import K,require
from sector import anchored
from controls import gaussian_ring,factor_primitive
from series import series_ring


def determinant(a):
    a=[list(row) for row in a];out=F(1)
    for j in range(len(a)):
        pivot=next((k for k in range(j,len(a)) if a[k][j]!=0),None)
        require(pivot is not None,'nonsingular exact control matrix')
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];out=-out
        value=a[j][j];out*=value
        for k in range(j+1,len(a)):
            ratio=a[k][j]/value
            a[k]=[v-ratio*w for v,w in zip(a[k],a[j])]
    return out


def audit(damage=None):
    D=series_ring(1,K);GS=gaussian_ring(D);G=gaussian_ring(K)
    delta=D([0,1]);count=0;records=[]
    def check(ok,label):
        nonlocal count
        require(ok,label);count+=1
    def conjugate(z):return G(z.re,-z.im)
    def divide(z,w):
        denominator=w.re*w.re+w.im*w.im
        require(denominator!=0,'exact Gaussian denominator nonzero')
        return G((z.re*w.re+z.im*w.im)/denominator,(z.im*w.re-z.re*w.im)/denominator)
    for epsilon in (F(1,16),F(1,12),F(1,8)):
        eta=epsilon*epsilon;a=1-eta;x,y,q0=F(-2,3),F(1,2),F(5,4)
        T=q0*q0;r,s=eta*x,eta*y;A=a-r;Delta=r-s
        partials=[anchored([(8,K(-F(9,4))),(7,K(-F(18,7)*Delta))],K(r),K(a)),
                  anchored([(7,K(F(9,7)))],K(r),K(a)),
                  anchored([(8,K(-F(9,8))),(7,K(-F(9,7)*(r-2*s)))],K(r),K(a)),
                  anchored([(7,K(-F(9,7)))],K(r),K(a))]
        if damage=='even-primitive':partials[0][8]*=2
        if damage=='marked-anchor':partials[1][0]+=1
        if damage=='odd-primitive':partials[2][7]=-partials[2][7]
        primitive_records=[]
        for index,label in enumerate(('y','T','V','M')):
            dy,dt,dv,dm=[int(j==index) for j in range(4)]
            mh=delta*(eta*dv/2);nn=delta*((dm-eta*dv*y)/2)
            opening=D(q0)+delta*(F(dt,1)/(2*q0))
            asymmetry=nn/opening
            uh=[D(y)+delta*dy+asymmetry,D(y)+delta*dy-asymmetry]
            hh=[mh+opening,mh-opening]
            heavy=[GS(D(eta)*u,D(epsilon)*h) for u,h in zip(uh,hh)]
            p=factor_primitive([GS(r)]*6+heavy,D(a))
            wanted=partials[index]
            check(all((v.re.a[1]==eta*w and v.im.a[1]==0) if index<2 else
                      (v.re.a[1]==0 and v.im.a[1]==epsilon**3*w)
                      for v,w in zip(p,wanted)), 'all ten anchored partial coefficients '+label)
            check(sum((v*D(a)**j for j,v in enumerate(p)),GS(0))==0,'whole marked-root anchor '+label)
            squared=[(D(a)-z.re)**2+z.im**2 for z in heavy]
            expected=(2*eta*(a-s),-eta,0,0)[index]
            scaled_objective=-sum((v.a[1] for v in squared),K(0))/2
            if damage=='heavy-objective-pair':scaled_objective*=2
            check(scaled_objective==expected,'both heavy objective derivatives times W cubed '+label)
            primitive_records.append({'partial':label,'real_coefficients':[v.re.a[1].record() for v in p],
                                      'imaginary_coefficients':[v.im.a[1].record() for v in p],
                                      'objective_derivative_times_W3':scaled_objective.record()})
        # Universal first-root identity at a rational unit point, for an exact
        # linear polynomial with nonzero p_z. The norm is evaluated literally.
        z0=G(F(3,5),F(4,5));pz=G(F(7,3),-F(2,5));q=G(F(2,7),-F(3,11))
        upper=[];lower=[]
        for odd in (False,True):
            qp=(G(0,epsilon**3)*q) if odd else eta*q
            qlower=(G(0,epsilon**3)*conjugate(q)) if odd else conjugate(qp)
            if damage=='odd-conjugation-sign' and odd:qlower=conjugate(qp)
            dz=-divide(qp,pz);dzlower=-divide(qlower,conjugate(pz))
            location=GS(D(z0.re)+delta*dz.re,D(z0.im)+delta*dz.im)
            locationlower=GS(D(z0.re)+delta*dzlower.re,-D(z0.im)+delta*dzlower.im)
            divisor=1 if damage=='half-squared-modulus' else 2
            norm=(location.re*location.re+location.im*location.im-1)/divisor
            normlower=(locationlower.re*locationlower.re+locationlower.im*locationlower.im-1)/divisor
            ratio=divide(q,z0*pz)
            wanted=epsilon**3*ratio.im if odd else -eta*ratio.re
            check(norm.a[1]==wanted,'literal half-squared original-root metric '+str(odd))
            check(normlower.a[1]==(-wanted if odd else wanted),'both actual conjugate radial signs '+str(odd))
            check(pz*dz+qp==0 and conjugate(pz)*dzlower+qlower==0,'literal first-root equation '+str(odd))
            upper.append(norm.a[1]);lower.append(normlower.a[1])
        # Raw four-root determinant is checked before the half-sum/half-
        # difference row transformation. These rational blocks are arbitrary.
        E=[[F(-3,8),F(3,14)],[F(-7,16),F(1,14)]]
        O=[[F(1,8),F(-1,7)],[F(1,8),F(-5,21)]];sines=(F(4,5),F(3,5))
        raw=[[eta*v for v in E[k]]+[epsilon**3*sines[k]*v for v in O[k]] for k in range(2)]
        raw += [[eta*v for v in E[k]]+[-epsilon**3*sines[k]*v for v in O[k]] for k in range(2)]
        factor=1 if damage=='full-radial-factor-four' else 4
        full=determinant(raw)
        check(full==factor*eta**5*sines[0]*sines[1]*determinant(E)*determinant(O),'complete four actual radial determinant')
        # Literal individual roots have equal conjugate objective derivatives.
        # Pair factor2 is necessary even though alpha already contains 1/2.
        rhs=[-(a-s),F(1,2)];de=determinant(E)
        weights=[(rhs[0]*E[1][1]-E[1][0]*rhs[1])/de,
                 (E[0][0]*rhs[1]-rhs[0]*E[0][1])/de]
        factor=1 if damage=='individual-dual-factor-two' else 2
        gradient=[-factor*eta*sum(weights[k]*E[k][j] for k in range(2)) for j in range(2)]
        check(gradient==[2*eta*(a-s),-eta],'individual root dual equation at positive eta')
        records.append({'eta':str(eta),'anchored_partial_records':primitive_records,
                        'literal_radial_upper':[v.record() for v in upper],'literal_radial_lower':[v.record() for v in lower],
                        'raw_radial_determinant':str(full),'individual_dual_times_W3':[str(v) for v in weights],
                        'literal_gradient_times_W3':[str(v) for v in gradient]})
    return {'exact_identity_controls':count,'positive_eta_whole_records':records,
            'finite_control_status':'exact formula and metric checks, not a replacement for universal proof or interval coverage'}
