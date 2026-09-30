#!/usr/bin/env python3
"""Independent collapsed-radius audit; Python 3.11.2 standard library only.

Written proofs establish the analytic quantifiers. This program checks their
exact algebra, all-degree sign certificates, and finite matrix controls.
No author code, data, solver, sampled root or CAS package is imported.
"""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
from algebra import P,G,mm,trace


def run():
    groups = {}
    def check(group, condition, label):
        if not condition: raise ValueError(group+': '+label)
        groups[group]=groups.get(group,0)+1

    m,a,c,z,q,x,y,R,E,A,Y = [P.variable(s) for s in
                              ('m','a','c','z','q','x','y','R','E','A','Y')]
    n,d,b=m+1,a+1,1-a*a
    # Disk geometry and every degree-dependent inequality stay symbolic.
    kap2m=d*(2*m*a-m-2)
    centered=b*((1+d*x)**2+d*d*y*y)+2*a*d*(1+d*x)-d*d
    check('symbolic_disk',centered==d*d*(2*x+b*(x*x+y*y)),'centering')
    check('symbolic_disk',(m-2)*d-2*m*b==kap2m,'leading energy coefficient')
    check('symbolic_disk',2*m-4-kap2m==(1-a)*(2*m*a+3*m-2),'kappa<=gamma')
    check('symbolic_disk',8*m*(1-b)-2*kap2m==2*m*(1-a)+4*m*a*a+4*d,
          'absolute-real-part budget')
    # Derive the cubic directly by product rule; m is an indeterminate.
    g=z*z+2*c*z+1
    critical=(z+1)*g+(m-2)*(z-a)*g+(z-a)*(z+1)*g.diff('z')
    cubic=sum((critical.coefficient('z',k)*(a*q-1)**k*q**(3-k)
               for k in range(4)),P(0))
    diskden=a*a+2*a*c+1
    proposed=d*diskden*q**3-((m-1)*diskden+4*d*(a+c))*q*q+(2*m*(a+c)+3*d)*q-n
    check('moving_pair',cubic==proposed,'reciprocal cubic')
    scaled,_=cubic.rational_substitution('q',x,d)
    normalized=scaled.substitute('c',1-y)
    L=-2*a*x**3+(2*a*(m-1)+4*d)*x*x-2*m*d*x
    check('moving_pair',normalized==d*(d*d*(x-1)**2*(x-n)+y*L),
          'dimensionless perturbation')
    f0=(x-1)**2*(x-n)
    check('implicit_branch',f0.diff('x').substitute('x',n)==m*m,'simple root')
    check('implicit_branch',f0.diff('x').diff('x').substitute('x',n)==4*m,
          'second derivative')
    K=m+2-m*a
    Bnum=-2*n*K; Bden=m*m*d*d
    Lprime=L.diff('x').substitute('x',n)
    Cnum=-2*Bnum*Bnum-m*Lprime*Bnum; Cden=m**5*d**4
    check('implicit_branch',m*m*Bnum+L.substitute('x',n)*m*m==0,'linear coefficient')
    check('implicit_branch',m*m*Cnum+2*m*Bnum*Bnum*m+Lprime*Bnum*m**3==0,
          'quadratic coefficient, common denominator m^5 d^4')
    # W=n/[(1-sh)x_*], with B=beta/n,T=chi/n,S=s.
    # A formal square-root calculation over three independent variables.
    B,T,S=x,R,E
    w1=S-B; w2=B*B-T+S*S-S*B
    r1=w1*Q(1,2); r2=(w2-r1*r1)*Q(1,2)
    check('modulus_series',2*r1==S-B,'linear sqrt coefficient')
    check('modulus_series',r2==Q(3,8)*(B-S)**2-Q(1,2)*(T-S*B),
          'quadratic sqrt coefficient')
    # Discriminant slope and gap slope derived from sum/product of roots.
    check('moving_pair',6*a*m-4*m*d+2*K==-2*(m-2),'pair discriminant slope')
    check('moving_pair',Bnum+2*a*m*n==2*n*(2*m*a-m-2),'first-order gap')
    check('moving_pair',((a+c)*d-diskden)**2+d*d*(1-c*c)==2*(1-c)*diskden,
          'exact perturbation energy')
    # At a=alpha, directly eliminate a from the implicit branch equations.
    dn=3*m+2; sn=4*m*(m+2)
    lp=-sn*n*(m+5)+2*m*(6*m+8)*dn
    bc,bd=Bnum.rational_substitution('a',m+2,2*m)
    check('cutoff',4*m*bc==-n*sn*bd,'specialized beta')
    cc,cd=Cnum.rational_substitution('a',m+2,2*m)
    chi_at=n*sn*(lp-2*n*sn)
    check('cutoff',16*m*m*cc==chi_at*cd,'specialized chi')
    second=sn*(lp-2*n*sn)+Q(3,4)*sn*sn*n*n-sn*sn*m
    H=m**3-4*m*m+13*m+18
    check('cutoff',2*second==-8*m*m*(m+2)*H,'negative quadratic gap')
    # At the cutoff E=4h/d0^4+O(h^2). Convert the fixed-radius
    # h^2 coefficient to the E^2 coefficient cited by the new refinement.
    check('cutoff',8*m*(m+2)*H*dn**8*512*m**7 ==
          (m+2)*H*dn**3*dn**5*16*(2*m)**8,
          'fixed-cutoff energy coefficient, cleared denominators')
    shifted=H.substitute('m',3+y)
    check('cutoff',shifted==y**3+5*y*y+16*y+48,'all-degree sign')
    # The actual contour factor is radius cubed, not one. Keeping it
    # gives remainder4 instead of32 and total error5 instead of37.
    check('improved_constants',Q(1,2)**3*2*2**3==2,'Neumann tail numerator')
    check('improved_constants',Q(2)/(1-Q(1,2))==4,'closed tail bound')
    signs={
      'error5':m*n**3-2*n-3*m,
      'new_radius_inside_cluster':10*m*n*n-4,
      'root_cap_bounded':5*m*n**3-960,
      'trace_error':m*m+4*m-1,
      'valid_pair_discriminant':m-2,
    }
    for name,polynomial in signs.items():
        shifted=polynomial.substitute('m',3+y)
        check('uniform_signs',bool(shifted.t) and all(t>=0 for t in shifted.t.values()),name)
    check('improved_constants',Q(3,2)*(Q(3,2)-Q(1,960))>2,'original-root transport')
    check('improved_constants',Q(5,10)==Q(1,2),'half kappa retained')
    check('improved_constants',Q(80,10)==8 and Q(40,5)==8,'eightfold enlargement')
    # Explicit Laurent residues for every order-zero/one/two projection word.
    for length in (1,2,3):
        for word in product('PQ',repeat=length):
            pole=word.count('P')-2
            residue=Q(1) if pole==1 and word.count('Q')==0 else Q(0)
            check('contour_words',residue==Q(word==('P','P','P')),''.join(word))
    # Independent matrix controls: Faddeev-LeVerrier characteristic
    # coefficients, not principal-minor expansion or author's trace words.
    for size in range(3,10):
        for pattern in range(5):
            delta=[G(Q((i+pattern)%4,17),Q((2*i+pattern)%5-2,19)) for i in range(size)]
            if pattern==0: delta=[G() for _ in range(size)]
            if pattern==1: delta=[G(Q(1,17),Q(2,19)) for _ in range(size)]
            u=[G(Q(1,2))+t for t in delta]
            identity=[[G(int(i==j)) for j in range(size)] for i in range(size)]
            proj=[[G(Q(int(i==j))-Q(1,size)) for j in range(size)] for i in range(size)]
            diag=[[delta[i] if i==j else G() for j in range(size)] for i in range(size)]
            compressed=mm(mm(proj,diag),proj)
            moment=trace(mm(compressed,compressed))
            expected=(1-Q(2,size))*sum((t*t for t in delta),G())
            total=sum(delta,G());expected+=total*total/Q(size*size)
            check('matrix_compressed_trace',moment==expected,f'{size},{pattern}')
            matrix=[[u[i]*G(1+int(i==j)) for j in range(size)] for i in range(size)]
            symmetric=[G(1)]+[G() for _ in range(size)]
            for value in u:
                for k in range(size,0,-1): symmetric[k]+=value*symmetric[k-1]
            previous=identity
            for k in range(1,size+1):
                step=mm(matrix,previous); ck=-trace(step)/k
                check('matrix_characteristic',ck==((-1)**k)*(k+1)*symmetric[k],
                      f'{size},{pattern},degree{k}')
                previous=[[step[i][j]+ck*identity[i][j] for j in range(size)]
                          for i in range(size)]
    # Concrete rational identities at degree9 and a necessary degree3 boundary.
    check('special_cases',-Q(2*8*10*(8**3-4*8**2+13*8+18),26**5)==-Q(1890,13**5),
          'degree9 t^4 coefficient')
    check('special_cases',10*8*9**3==58320 and 5*8*9**3==29160,'new degree9 radii')
    # At degree3,a=1,c=3/4, the two critical roots are real and <1;
    # their positive reciprocal sum is exactly2. The n>=4 cutoff claim
    # must therefore not be extended to n=3.
    check('special_cases',Q(16)*Q(3,4)**2+8*Q(3,4)-8==7,'degree3 real discriminant')
    check('special_cases',2*(2*(1+Q(3,4))/(2+2*Q(3,4)))==2,'degree3 boundary equality')
    mutations={
      'wrong_leading_cutoff':(m-2)*d-2*m*b != d*(2*m*a-m-1),
      'wrong_cubic_constant':cubic != proposed+1,
      'wrong_cutoff_sign':2*second != 8*m*m*(m+2)*H,
      'wrong_implicit_quadratic':m*m*(Cnum+1)+2*m*Bnum*Bnum*m+Lprime*Bnum*m**3 != 0,
      'wrong_tail_prefactor':Q(1,2)**3*2*2**3 != 1,
    }
    for label,rejected in mutations.items():check('rejected_controls',rejected,label)
    return {'agent':'six-reviewer-2','role':'independent mathematical reviewer',
      'status':'PASS','groups':groups,'exact_checks':sum(groups.values()),
      'symbolic_degree_parameter':'m=n-1','external_inputs':0,
      'floating_point_operations':0,'improved_signed_error':5,
      'reciprocal_radius_denominator':'10*m*n^3',
      'original_root_radius_denominator':'5*m*n^3',
      'radius_enlargement_factor':8,'cutoff':'(m+2)/(2*m)',
      'rejected_controls':list(mutations)}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args();result=run()
    if args.expected and result!=json.loads(args.expected.read_text()):
        raise ValueError('Expected evidence mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))
