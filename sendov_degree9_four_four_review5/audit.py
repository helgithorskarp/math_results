"""Independent complete exact audit by six-reviewer-5, mathematical reviewer.

Python 3.10+ standard library; no author imports, floats, solver or network.
Copied author manifests are untrusted comparisons, never polynomial inputs.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from math import comb
import hashlib, json
import kernel as K
import tensors as B

ROOT = Path(__file__).resolve().parent
require = K.require
BASE = (F(0), F(1))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',',':')).encode()).hexdigest()


def stage(s):
    print(s, file=sys.stderr, flush=True)


def compare(record, expected, keys):
    require(all(record[k] == expected[k] for k in keys), 'Author comparison differs: '+str(keys))


def cell(p, degrees, box):
    values, denominator = B.convert(p, degrees, box)
    return B.inventory(values, denominator, degrees)


def gaussian_add(a,b):
    return a[0]+b[0], a[1]+b[1]


def gaussian_mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def gaussian_scale(a,v):
    return a[0]*v, a[1]*v


def convolve(a,b):
    result = [(F(0),F(0))]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            result[i+j] = gaussian_add(result[i+j], gaussian_mul(x,y))
    return result


def norm(z):
    return z[0]**2+z[1]**2


def controls(E,J,P,T):
    # Different control inventory from the researcher: 64 signed tests,
    # including zero cosines, full imbalance, skew sign and equality faces.
    units = [(F(0),F(1)),(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(1),F(0))]
    records = []
    for c,d in units:
        for x,yabs in units:
            for eta in [F(0),F(1,2)]:
                for sign in [-1,1]:
                    y = sign*yabs
                    u = gaussian_scale(gaussian_mul((x,y),(c,d)),1+eta)
                    v = gaussian_scale(gaussian_mul((x,y),(c,-d)),1-eta)
                    lam = -eta*d*y
                    mu = c*x+lam
                    b = c*x if lam<0 else mu/2
                    coeff = [(F(1),F(0))]
                    for z in [u]*4+[v]*4:
                        coeff = convolve(coeff,[(F(1),F(0)), gaussian_scale(z,-b)])
                    integral = (F(0),F(0))
                    for j,z in enumerate(coeff):
                        integral = gaussian_add(integral,gaussian_scale(z,F(9,j+1)))
                    actual = norm(integral)
                    require(actual == K.evaluate(E,[b,c,x,eta**2])+lam*K.evaluate(J,[b,c,x,eta**2]), 'Signed Gaussian norm')
                    if lam>=0:
                        predicted = K.evaluate(P,[F(1,2),c,x,eta**2])+lam*K.evaluate(T,[F(1,2),c,x,eta**2])
                        require(actual-(1-eta**2)**8 == predicted, 'Weighted signed Gaussian control')
                    records.append([str(b),str(c),str(x),str(eta),str(lam),str(actual)])
    require(len(records)==64, 'Gaussian control count')
    return {'count':len(records),'sha256':digest(records)}


def mean_certificate():
    # Independently clear the POLAR integral's denominators before raising
    # the quadratic to its fourth power. This proves exactly the weak mean
    # used by the target; no review of 7518's stronger mean is claimed.
    one={(0,0,0,0):1};a=K.variable(0);tau=K.variable(1)
    a2=K.multiply(a,a);ap2=K.power(K.add(one,a),2)
    delta=K.add(one,K.scale(a2,-1))
    quadratic=K.add(K.multiply(a2,ap2),
      K.scale(K.multiply(K.multiply(K.multiply(a2,delta),ap2),tau),2),
      K.multiply(K.multiply(K.multiply(delta,delta),K.add(ap2,a2)),K.multiply(tau,tau)))
    fourth=K.power(quadratic,4)
    integrated={}
    for (i,j,k,l),v in fourth.items():
        require(k==l==0, 'Unexpected polar variable')
        integrated[i]=integrated.get(i,F(0))+F(v,j+1)
    numerator={i:F(comb(8,i))-integrated.get(i,0) for i in range(max(integrated)+1)}
    numerator={i:v for i,v in numerator.items() if v}
    remainder=dict(numerator);quotient={}
    while remainder and max(remainder)>=2:
        j=max(remainder)-2;v=remainder[j+2];quotient[j]=v
        for offset,coefficient in [(0,1),(1,-2),(2,1)]:
            i=j+offset;remainder[i]=remainder.get(i,F(0))-v*coefficient
            if not remainder[i]:del remainder[i]
    require(not remainder and max(quotient)==22, 'Polar clearing/division')
    weights,den=B.matrix(22,F(0),F(1))
    coefficients=[sum(F(w,den)*quotient.get(k,0) for k,w in row) for row in weights]
    require(min(coefficients)==F(8,9), 'Weak polar mean sign')
    return {'degree':22,'coefficients':[str(v) for v in coefficients],
            'minimum':'8/9','quotient_sha256':digest([[i,str(v)] for i,v in sorted(quotient.items())])}


def polynomial_control():
    # Expand the critical polynomial with binomial factors, then integrate.
    points=[(F(0),F(1,20)),(F(1,40),F(1,40))]
    factors=[]
    for z in points:
        factor=[]
        for i in range(5):
            w=(F(1),F(0))
            for _ in range(4-i):w=gaussian_mul(w,gaussian_scale(z,-1))
            factor.append(gaussian_scale(w,comb(4,i)))
        factors.append(factor)
    derivative=[gaussian_scale(z,9) for z in convolve(*factors)]
    primitive=[(F(0),F(0))]+[gaussian_scale(z,F(1,i+1)) for i,z in enumerate(derivative)]
    a=F(3,4);value=(F(0),F(0))
    for z in reversed(primitive):value=gaussian_add(gaussian_scale(value,a),z)
    primitive[0]=gaussian_scale(value,-1)
    check=(F(0),F(0))
    for z in reversed(primitive):check=gaussian_add(gaussian_scale(check,a),z)
    require(check==(F(0),F(0)) and primitive[-1]==(F(1),F(0)), 'Actual marked root')
    require([gaussian_scale(z,i) for i,z in enumerate(primitive) if i]==derivative, 'Actual derivative')
    bound=sum(abs(z[0])+abs(z[1]) for z in primitive[:-1])
    require(bound<1, 'Actual Rouche bound')
    vectors=[(a-z[0],-z[1]) for z in points];radii2=[norm(z) for z in vectors]
    require(radii2[1]<radii2[0]<1 and all(z[0]>0 for z in vectors), 'Actual reciprocal order')
    require(vectors[1][0]**2/radii2[1]>vectors[0][0]**2/radii2[0], 'Actual positive covariance')
    return {'rouche_l1_bound':str(bound),'coefficient_sha256':digest([[str(v) for v in z] for z in primitive])}


def audit():
    full=json.loads((ROOT/'full_expected.json').read_text())
    individual=json.loads((ROOT/'individual_expected.json').read_text())
    E,J=K.origin_kernel(stage)
    normrecord={'E':[[[e[0],0,e[1],e[2],e[3]],str(v)] for e,v in sorted(E.items())],
                'J':[[[e[0],0,e[1],e[2],e[3]],str(v)] for e,v in sorted(J.items())]}
    require(digest(normrecord)==individual['norm_sha256'], 'All independent origin coefficients')
    R={(0,0,0,j):F((-1)**j*comb(8,j)) for j in range(9)}
    D=K.add(E,K.scale(R,-1));P,T=K.weighted(D,J)
    require((len(P),len(T))==(7415,5474), 'Weighted inventory')
    require(digest([K.canonical(P),K.canonical(T)])==full['weighted_sha256'], 'Weighted polynomial hash')
    one={(0,0,0,0):1};c,x=K.variable(1),K.variable(2)
    s=K.add(one,K.scale(K.multiply(c,x),-1))
    g=K.multiply(K.add(one,K.scale(K.power(c,2),-1)),K.add(one,K.scale(K.power(x,2),-1)))
    s2=K.multiply(s,s)
    require(K.add(s2,K.scale(g,-1))==K.power(K.add(c,K.scale(x,-1)),2), 'Circle geometry identity')
    den=K.scale(K.multiply(s,K.add(s2,g)),4)
    num=K.add(K.multiply(s2,s2),K.scale(K.multiply(s2,g),6),K.multiply(g,g))
    H=K.add(K.multiply(den,K.parameters(P,eta=True)),K.multiply(num,K.parameters(T,eta=True,signed=True)))
    require(len(H)==35890 and digest(K.canonical(H))==full['envelope_sha256'], 'Weighted envelope identity')
    stage('independent norm, weighted reduction and Newton envelope match')
    records=[]
    pboxes=[(BASE,BASE,(F(0),F(1,2)),BASE),
            (BASE,(F(0),F(1,2)),(F(1,2),F(1)),BASE),
            (BASE,(F(1,2),F(1)),(F(1,2),F(1)),BASE)]
    B.cover(pboxes,lambda c,x:True)
    for i,box in enumerate(pboxes):
        rec,zeros=cell(K.parameters(P),(16,16,16,16),box)
        require(zeros==([(16,16,16,0)] if i==2 else []), 'Even equality support')
        require(F(rec['zeroth_c_minimum'])>0 and F(rec['zeroth_x_minimum'])>0, 'Even strict slices')
        compare(rec,full['even_cells'][i],rec.keys());records.append({'type':'weighted-even','box':[[str(a),str(b)] for a,b in box],**rec})
        stage('weighted even cell '+str(i+1)+' confirmed')
    hboxes=[(BASE,BASE,(F(1,2),F(1)),BASE),
            (BASE,BASE,(F(0),F(1,2)),(F(0),F(1,2))),
            (BASE,BASE,(F(0),F(1,2)),(F(1,2),F(3,4)))]
    B.cover(hboxes,lambda x,z:x>=F(1,2) or z<=F(3,4),axes=(2,3))
    for i,box in enumerate(hboxes):
        rec,zeros=cell(H,(16,19,19,32),box)
        require((len(zeros)==3374 and all(e[1]>=16 and e[2]>=16 for e in zeros)) if i==0 else not zeros, 'Envelope zero support')
        require(F(rec['zeroth_c_minimum'])>0 and F(rec['zeroth_x_minimum'])>0, 'Envelope strict slices')
        compare(rec,full['envelope_cells'][i],rec.keys())
        require(digest(zeros)==full['envelope_cells'][i]['zero_indices_sha256'], 'Full envelope zero inventory')
        records.append({'type':'weighted-envelope','box':[[str(a),str(b)] for a,b in box],**rec});stage('weighted envelope cell '+str(i+1)+' confirmed')
    # Quantitative refinement. These slice minima and all low-x minima imply
    # H >= A*max((1-c)^19,(1-x)^19) >= A*s^19/2^19.
    A=F(376414451433,10522669875200);kappa=A/2**22
    require(A<F(1,16) and 0<kappa<F(1,16), 'Quantitative constants')
    require(all(F(rec['minimum'])>=A for rec in records[4:6]), 'Low-x quantitative support')
    require(F(records[3]['zeroth_c_minimum'])>=A and F(records[3]['zeroth_x_minimum'])>=A, 'High-x quantitative support')
    require(all(F(rec['minimum_positive'])>=F(1,16) for rec in records[:3]), 'Even quantitative support')
    # Audit the prerequisite individual minima rather than assume them.
    even=K.scale(K.multiply(s,D),2)
    odd=K.multiply(K.add(s2,g),J)
    targets=[K.add(K.parameters(K.unweighted(even),eta=True),K.scale(K.parameters(K.unweighted(odd),eta=True,signed=True),sign)) for sign in [1,-1]]
    boxes=[[(BASE,BASE,(F(0),F(1,2)),BASE),(BASE,BASE,(F(1,2),F(1)),BASE)],
           [(BASE,BASE,(F(0),F(1,2)),BASE),
            (BASE,(F(0),F(1,2)),(F(1,2),F(1)),BASE),
            (BASE,(F(1,2),F(1)),(F(1,2),F(3,4)),BASE),
            (BASE,(F(1,2),F(1)),(F(3,4),F(1)),BASE)]]
    cornerzeros={(t,17,17,z) for t in range(17) for z in range(17)}
    cornerzeros.update((16,c,x,z) for c,x in [(16,17),(17,16)] for z in [0,1])
    for margin,(target,cells) in enumerate(zip(targets,boxes)):
        require(len(target)==2044 and digest(K.canonical(target))==individual['envelopes'][margin]['power_sha256'], 'Independent individual margin')
        B.cover(cells,lambda c,x:True)
        for i,box in enumerate(cells):
            rec,zeros=cell(target,(16,17,17,16),box)
            corner=box[1][1]==box[2][1]==1
            require(set(zeros)==(cornerzeros if corner else set()), 'Individual strict boundary support')
            require(not any(e[1]==0 or e[2]==0 for e in zeros), 'Individual strict zeroth slices')
            expected=individual['envelopes'][margin]['cells'][i]
            compare(rec,expected,['coefficients','minimum','minimum_positive','sha256'])
            require(len(zeros)==expected['zero_count'], 'Individual zero count')
            records.append({'type':'individual-plus' if margin==0 else 'individual-minus','box':[[str(a),str(b)] for a,b in box],**rec})
            stage('individual margin '+str(margin+1)+' cell '+str(i+1)+' confirmed')
    endpoint={}
    for (b,c,x,q),v in D.items():endpoint[(b,0,0,q)]=endpoint.get((b,0,0,q),F(0))+v
    endpoint=K.add(endpoint)
    require(len(endpoint)==89, 'Endpoint inventory')
    rec,zeros=cell(K.parameters(endpoint),(16,0,0,8),(BASE,)*4)
    require(zeros==[(16,0,0,0)] and F(rec['minimum_positive'])==F(1,8), 'Endpoint equality corner')
    compare(rec,individual['corner'],['coefficients','minimum','minimum_positive','sha256'])
    records.append({'type':'equality-corner',**rec})
    mean=mean_certificate();compare(mean,individual['weak_polar_mean'],mean.keys())
    # The sharper necessary cutoff is the unique zero rho in (0,1/2) of f.
    f=lambda z:-1+2*z+6*z**3-3*z**4
    require(f(F(3,8))==F(29,4096), 'Physical separation')
    require(f(F(373,1000))<0<f(F(374,1000)), 'Unique cutoff rational bracket')
    eta=K.variable(0);eta2=K.power(eta,2);one_minus=K.add(one,K.scale(eta,-1))
    require(K.add(eta2,K.scale(K.multiply(eta2,K.power(one_minus,2)),-1))
            ==K.multiply(K.power(eta,3),K.add(K.scale(one,2),K.scale(eta,-1))), 'Curved feasibility numerator')
    require(K.multiply(K.power(one_minus,2),K.add(one,K.scale(eta2,-1)))
            ==K.multiply(K.power(one_minus,3),K.add(one,eta)), 'Curved feasibility denominator')
    gaussian=controls(E,J,P,T);actual=polynomial_control()
    compare(actual,full['polynomial_control'],actual.keys())
    count=sum(r['coefficients'] for r in records)
    require(count==1485732, 'Complete coefficient census')
    # Bounded independent negative controls on actual basis output and inputs.
    rejected=0
    for values,degrees in [([-1],(0,0,0,0)),([1,1],(0,0,0,0))]:
        try:B.inventory(values,1,degrees)
        except ArithmeticError:rejected+=1
    try:compare({'sha256':'corrupt'},individual['corner'],['sha256'])
    except ArithmeticError:rejected+=1
    try:B.cover([(BASE,BASE,(F(0),F(1,2)),BASE)]*2,lambda c,x:True)
    except ArithmeticError:rejected+=1
    try:B.cover([(BASE,BASE,(F(0),F(1,2)),BASE)],lambda c,x:True)
    except ArithmeticError:rejected+=1
    require(rejected==5, 'Corruption controls')
    return {'result':'PASS','agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'method':'eight-linear-factor circle-ring norm; fused affine/Bernstein matrices, reverse axis order',
            'norm_sha256':digest(normrecord),'weighted_sha256':full['weighted_sha256'],
            'envelope_sha256':full['envelope_sha256'],'sign_coefficients':count,
            'weighted_sign_coefficients':923763,'prerequisite_sign_coefficients':561969,
            'cells':records,'weak_polar_mean':mean,'gaussian_controls':gaussian,
            'actual_polynomial':actual,'rejected_corruptions':rejected,
            'quantitative_refinement':{'exponent':16,'kappa':str(kappa),'H_slice_constant':str(A)},
            'necessary_low_phase_cutoff':{'polynomial_coefficients':[-1,2,0,6,-3],'root_bracket':['373/1000','374/1000'],
              'curved_bound':'x^2 > eta^3*(2-eta)/((1-eta)^3*(1+eta))'}}


if __name__=='__main__':
    require(len(sys.argv)==1, 'No arguments or mutable manifest mode')
    print(json.dumps(audit(),sort_keys=True,indent=2))
