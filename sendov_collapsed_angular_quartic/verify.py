#!/usr/bin/env python3
"""Exact all-degree algebra for PROOF.md; Python standard library.

No floating point, root solve, interpolation, solver or external corpus.
Matrices are free ordered block words A,b,c, with b a column and c its
transpose. Coefficients belong to Q(m,r)[i,h]/(i^2+1,h^2-m-1).
Balanced diagonal compression uses mu1=0; trace moment symbols are formal.
Analytic, spectral continuity and uniform-remainder bridges are written
mathematics, not formalized here. Agent six-sendov-2, role researcher.
"""
from pathlib import Path
import importlib.util
from fractions import Fraction as F
from itertools import product
from math import comb
import json

spec=importlib.util.spec_from_file_location('angular_algebra',Path(__file__).with_name('algebra.py'))
algebra=importlib.util.module_from_spec(spec)
spec.loader.exec_module(algebra)
RF,Poly,m,r=algebra.RF,algebra.Poly,algebra.m,algebra.r
D,M=algebra.D,algebra.M
n=m+1
invm=RF(1,(1,0,0)); v=RF(2*m,(0,1,0))
iv=RF(F(1,2)*D,(1,0,0)); iG=RF(F(1,2)*D,(2,0,0))
c2=F(1,2)*v*v-v**3
c3=F(1,6)*v*v-v**3+v**4
c4=-F(1,24)*v*v+F(7,12)*v**3-F(3,2)*v**4+v**5


def trace_cycle(word):
    """Only cyclicity and adjacent P,Q projection identities."""
    word=list(word)
    while len(word)>1:
        removed=False
        for i in range(len(word)):
            j=(i+1)%len(word)
            if word[i] in 'PQ' and word[j] in 'PQ':
                if word[i]!=word[j]: return None
                word.pop(j); removed=True; break
        if not removed:break
    word=tuple(word)
    return min(word[k:]+word[:k] for k in range(len(word))) if word else ()


def moment_words(ell,k):
    out={}
    for ps in product('PQ',repeat=k+1):
        degree=ps.count('P')-ell-1; nq=ps.count('Q')
        if degree<0:continue
        if nq:
            coefficient=F((-1)**nq*comb(nq+degree-1,degree)); gp=-nq-degree
        else:
            coefficient=F(degree==0); gp=0
        word=[]
        for j,p in enumerate(ps):
            word.append(p)
            if j<k:word.append('V')
        cycle=trace_cycle(word)
        if coefficient and cycle is not None:
            key=cycle,gp;out[key]=out.get(key,F(0))+coefficient
    return {k:c for k,c in out.items() if c}


def nc_add(*polys):
    out={}
    for p in polys:
        for key,c in p.items():out[key]=out.get(key,RF(0))+c
    return {k:c for k,c in out.items() if c!=0}


def nc_scale(p,factor=1,phase=0,hpower=0):
    out={}
    for (word,h,i),c in p.items():
        totalh=h+hpower;totalphase=i+phase
        coefficient=c*factor*n**(totalh//2)*((-1)**(totalphase//2))
        key=word,totalh%2,totalphase%2
        out[key]=out.get(key,RF(0))+coefficient
    return {k:c for k,c in out.items() if c!=0}


def nc_mul(p,q):
    out={}
    for (w,h,i),c in p.items():
        for (z,g,j),d in q.items():
            hp=h+g; ip=i+j
            key=w+z,hp%2,ip%2
            out[key]=out.get(key,RF(0))+c*d*n**(hp//2)*((-1)**(ip//2))
    return {k:c for k,c in out.items() if c!=0}


def atom(letter):return {((letter,),0,0):RF(1)}
ONE={((),0,0):RF(1)}
ZERO={}


def matrix_mul(a,b):
    return [[nc_add(*(nc_mul(a[i][k],b[k][j]) for k in range(2)))
             for j in range(2)] for i in range(2)]


def compositions(total,length):
    if length==0:
        if total==0:yield ()
    else:
        for j in range(1,total-length+2):
            for rest in compositions(total-j,length-1):yield (j,)+rest


def moment_coefficient(words,Vs):
    """Substitute every ordered Taylor composition into each trace cycle."""
    out={}
    for (word,gpower),coefficient in words.items():
        ps=word[::2]
        if any(letter!='V' for letter in word[1::2]):raise AssertionError('interlaced word')
        k=len(ps)
        for orders in compositions(4,k):
            term=ONE
            for j,p in enumerate(ps):
                left=int(p=='Q');right=int(ps[(j+1)%k]=='Q')
                term=nc_mul(term,Vs[orders[j]][left][right])
            out=nc_add(out,nc_scale(term,coefficient*iG**(-gpower)))
    return out


def contract_trace(p):
    """Exact basis at order four: tr A^4, c A^2 b, (c b)^2."""
    names={tuple('AAAA'):'T4',tuple('AAbc'):'U',tuple('bcbc'):'R2'}
    names={min(w[k:]+w[:k] for k in range(len(w))):name for w,name in names.items()}
    out={}
    for (word,h,i),c in p.items():
        if h or i:raise AssertionError('fourth coefficient must be real, h-free')
        cycle=min(word[k:]+word[:k] for k in range(len(word)))
        if cycle not in names:raise AssertionError(('unexpected trace monomial',word))
        key=names[cycle];out[key]=out.get(key,RF(0))+c
    return {k:c for k,c in out.items() if c!=0}


def compressed_trace(exponents):
    """Expand every P=I-J/m; cyclic index contraction, formal mu1=0."""
    out={}
    k=len(exponents)
    for choice in product((0,1),repeat=k):
        marks=[j for j in range(k) if choice[j]]
        if not marks:
            moment=(sum(exponents),);coefficient=RF(1)
        else:
            degrees=[]
            for j,start in enumerate(marks):
                stop=marks[(j+1)%len(marks)]
                cursor=(start+1)%k;total=0
                while True:
                    total+=exponents[cursor]
                    if cursor==stop:break
                    cursor=(cursor+1)%k
                degrees.append(total)
            moment=tuple(sorted(degrees));coefficient=(-invm)**len(marks)
        if 1 in moment:continue
        out[moment]=out.get(moment,RF(0))+coefficient
    return {k:c for k,c in out.items() if c!=0}


def run(mutation=None):
    groups={}
    def check(group,condition,label):
        if not condition:raise AssertionError(group+': '+label)
        groups[group]=groups.get(group,0)+1
    check('reciprocal_coefficients',v*iv==1,'positive reciprocal base')
    # Multiply (a+exp(i theta t)) by the displayed reciprocal series.
    # theta is one formal scalar; homogeneity removes its powers.
    a=RF(F(1,2)*M,(1,0,0))
    u=[(v,RF(0)),(RF(0),-v*v),(c2,RF(0)),(RF(0),c3),(c4,RF(0))]
    denominator=[(a+1,RF(0)),(RF(0),RF(1)),(RF(-F(1,2)),RF(0)),
                 (RF(0),RF(-F(1,6))),(RF(F(1,24)),RF(0))]
    def cmul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
    for degree in range(5):
        products=[cmul(u[j],denominator[degree-j]) for j in range(degree+1)]
        value=(sum((x[0] for x in products),RF(0)),sum((x[1] for x in products),RF(0)))
        check('reciprocal_coefficients',value==(RF(int(degree==0)),RF(0)),str(degree))
    cycle=lambda s:trace_cycle(tuple(s))
    expected={
      (2,2):{(cycle('PVPV'),0):F(1)},
      (2,3):{(cycle('PVPVQV'),-1):F(-2)},
      (2,4):{(cycle('PVPVPVQV'),-2):F(-2),(cycle('PVPVQVQV'),-2):F(2),(cycle('PVQVPVQV'),-2):F(1)},
      (3,3):{(cycle('PVPVPV'),0):F(1)},
      (3,4):{(cycle('PVPVPVQV'),-1):F(-3)},
      (4,4):{(cycle('PVPVPVPV'),0):F(1)}}
    all_words={}
    for ell in (2,3,4):
        for k in range(5):
            actual=moment_words(ell,k)
            if mutation=='missing_contour_cycle' and (ell,k)==(2,4):
                actual.pop((cycle('PVQVPVQV'),-2),None)
            check('contour_words',actual==expected.get((ell,k),{}),f'{ell}:{k}')
            all_words[ell,k]=actual
    check('compression_moments',compressed_trace((1,1))=={(2,):1-2*invm},'tr A2')
    check('compression_moments',compressed_trace((1,1,1,1))=={
        (4,):1-4*invm,(2,2):2*invm**2},'tr A4')
    check('compression_moments',compressed_trace((2,2))=={
        (4,):1-2*invm,(2,2):invm**2},'tr (P D2 P)^2')
    # Free 2x2 block algebra starts from D_theta=[[A,b],[c,0]].
    DD=[[atom('A'),atom('b')],[atom('c'),ZERO]]
    power=[[ONE,ZERO],[ZERO,ONE]];powers={}
    for j in range(1,5):
        power=matrix_mul(power,DD);powers[j]=power
    check('block_algebra',powers[2][0][0]==nc_add(nc_mul(atom('A'),atom('A')),nc_mul(atom('b'),atom('c'))),'A2=A^2+W')
    check('block_algebra',powers[3][0][0]==nc_add(
        nc_mul(atom('A'),nc_mul(atom('A'),atom('A'))),
        nc_mul(atom('A'),nc_mul(atom('b'),atom('c'))),
        nc_mul(atom('b'),nc_mul(atom('c'),atom('A')))),'A3=A^3+AW+WA')
    scalars={1:(v*v,3),2:(c2,0),3:(c3,1),4:(c4,0)}
    Vs={}
    for j in range(1,5):
        factor,phase=scalars[j]
        Vs[j]=[[nc_scale(powers[j][x][y],factor,phase,x+y) for y in range(2)] for x in range(2)]
    if mutation=='wrong_coupling_sign':Vs[1][0][1]=nc_scale(Vs[1][0][1],-1)
    computed={}
    for ell in (2,3,4):
        total=nc_add(*(moment_coefficient(all_words[ell,k],Vs) for k in range(1,5)))
        computed[ell]=contract_trace(total)
    target2={
      'T4':c2*c2+2*v*v*c3,
      'U':2*c2*c2+4*v*v*c3+6*n*c2*v**4*iG-2*n*v**8*iG**2,
      'R2':c2*c2+2*n*c2*v**4*iG+n*n*v**8*iG**2}
    target3={'T4':-3*c2*v**4,'U':-3*c2*v**4-3*n*v**8*iG}
    target4={'T4':v**8}
    for ell,target in ((2,target2),(3,target3),(4,target4)):
        check('fourth_trace_coefficients',computed[ell]==target,str(ell))
    cr=c2+n*v**4*iG
    check('effective_block',cr==RF(F(3,4)*(m+2),(1,0,0))*v**3,'rank-one second correction')
    h=RF(F(1,4)*(m-2),(1,0,0))
    check('effective_block',c2==-h*v**3,'quadratic second correction')
    real_square={'T4':c2*c2,'U':2*c2*cr,'Psi':cr*cr}
    if mutation=='omit_pinching':real_square['Psi']=RF(0)
    # The scalar modulus identity is derived in PROOF.md. Substitute here
    # all independently expanded contour coefficients.
    raw={'mu4':2*c4}
    for key in ('T4','U','R2','Psi'):
        raw[key]=(-F(1,2)*iv*computed[2].get(key,RF(0))
                  +F(1,2)*iv*real_square.get(key,RF(0))
                  +F(1,6)*iv**2*computed[3].get(key,RF(0))
                  -F(1,8)*iv**3*computed[4].get(key,RF(0)))
    # T4=(1-4/m)mu4+2mu2^2/m^2, U=mu4/m-mu2^2/m^2.
    closed={
      'mu4':raw['mu4']+(1-4*invm)*raw['T4']+invm*raw['U'],
      'mu2square':invm**2*(2*raw['T4']-raw['U']+raw['R2']),
      'Psi':raw['Psi']}
    L=m*m-4*m-4
    wanted={'mu4':RF(-m*m*M*L,(0,5,0)),
            'mu2square':RF(-m*M*(13*m+18),(0,5,0)),
            'Psi':RF(9*m**3*M*M,(0,5,0))}
    for key in wanted:check('closed_functional',closed[key]==wanted[key],key)
    pref=RF(F(1,256)*M*D**3,(7,0,0))
    check('energy_normalization',pref*v**8==RF(m*M,(0,5,0)),'K=-F4/(v8 mu2^2)')
    if mutation=='bad_energy_normalization':pref*=2
    # Clear the unsupported denominator r(m-r); r remains an indeterminate.
    s=m-r;mu2=m*r*s;mu4=r*s*(s**3+r**3)
    F4two=closed['mu4']*mu4+closed['mu2square']*mu2**2+closed['Psi']*(invm*mu2)**2
    Kclear=pref*(m*m*L-(m-6)*D*r*s)
    check('all_degree_profiles',-F4two==Kclear*v**8*m*m*r*s,'all two-block profiles')
    psi_pair=2*invm**2
    if mutation=='moment_only':psi_pair=4*invm**2
    F4pair=2*closed['mu4']+4*closed['mu2square']+closed['Psi']*psi_pair
    H=m**3-4*m*m+13*m+18
    Cpair=RF(F(1,512)*M*H*D**3,(7,0,0))
    check('all_degree_profiles',-F4pair==4*v**8*Cpair,'all moving-pair profiles')
    # Independent degree-nine cleared polynomial bound; x is r here.
    x=r;den=32*x+2;q=64*x*x-48*x-1
    numer=(224*x+122)*den-90*(8*x-1)**2
    check('degree_nine_bound',numer-(224*x+32)*den==-90*q,'value at feasibility endpoint')
    # Exact derivative by coefficients, without floating-point evaluation.
    def dr(p):return Poly({(a,b-1):b*c for (a,b),c in p.t.items() if b})
    check('degree_nine_bound',dr(numer)*den-numer*dr(den)==44*den*den+6480,'strict monotonicity')
    # Evaluate the quadratic in Q[s]/(s^2-10), x=(3+s)/8.
    xx=F(3,8);yy=F(1,8)
    check('degree_nine_bound',64*(xx*xx+10*yy*yy)-48*xx-1==0 and 128*xx*yy-48*yy==0,'root (3+sqrt10)/8')
    check('degree_nine_bound',224*xx+32==116 and 224*yy==28,'radical upper numerator')
    check('degree_nine_bound',224*F(1,8)+122-90==60,'uniform positive lower numerator')
    check('degree_nine_bound',224*F(43,56)+122-90==204,'singleton versus seven numerator')
    pref9=F(10985,33554432)
    check('degree_nine_bound',pref9==F(10*26**3,256*8**7),'degree-nine prefactor')
    check('degree_nine_bound',pref9*204==F(560235,8388608),'published lower bound')
    upper_ratio=(116+28*F(31623,10000))/204
    check('degree_nine_bound',F(31623,10000)**2>10 and upper_ratio<F(100267,100000),'relative interval below 0.267 percent')
    # k distinct angular values give k-1 nonzero spectral weights; this
    # bridge is written, with exact two-value and moving-pair controls.
    return {'agent':'six-sendov-2','role':'researcher','status':'author exact algebra; written spectral bridge unformalized',
            'groups':groups,'checks':sum(groups.values()),
            'F4_coefficients':{k:c.data() for k,c in closed.items()},
            'degree9':{'prefactor':str(pref9),'K_all_directions_lower':str(60*pref9),
                       'K_max_lower':str(204*pref9),
                       'K_max_upper':'10985/33554432 * (116 + 28*sqrt(10))',
                       'relative_width_percent_less_than':'0.267'},
            'profiles':'all symbolic m>=3, all two-block r+s=m; all moving-pair m>=3'}


def main():
    result=run()
    rejected=[]
    for mutation in ('missing_contour_cycle','wrong_coupling_sign','omit_pinching','bad_energy_normalization','moment_only'):
        try:run(mutation)
        except AssertionError as e:rejected.append({'mutation':mutation,'detected':str(e)})
        else:raise AssertionError('undetected mutation: '+mutation)
    result['rejected_mutations']=rejected
    expected=Path(__file__).with_name('expected.json')
    if expected.exists() and json.loads(expected.read_text())!=result:
        raise AssertionError('fixed compact manifest differs')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
