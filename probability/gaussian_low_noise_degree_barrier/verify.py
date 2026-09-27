"""Exact finite controls for the written low-noise degree-barrier theorem.

No floating point, transcendental evaluation, Gaussian integration or solver.
The theorem is the written proof; this program validates its finite algebra
and a compact rational input. A rejected input is not a counterexample.
"""
import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def squared(p,q):
    return sum((a-b)**2 for a,b in zip(p,q))


def constants(degree,bits):
    require(type(degree) is int and degree>=1,'positive integer degree required')
    require(type(bits) is int and bits>=1,'positive integer mass exponent required')
    m=2*degree+2;k=8*degree*(degree+1)*(2*degree+1)
    ceiling=(2*degree-1).bit_length()
    return m,k,m*bits+ceiling


def certify(x,y,w,variance,degree,bits):
    require(len(x)==len(y)==len(w)>=2,'at least two matched atoms required')
    x=[[F(v) for v in p] for p in x];y=[[F(v) for v in p] for p in y]
    w=list(map(F,w));s=F(variance)
    require(all(len(p)==3 for p in x+y),'R3 coordinates required')
    require(s>0 and min(w)>0 and sum(w)==1,'positive variance/probability required')
    m,k,l=constants(degree,bits)
    require(min(w)>=F(1,2**bits),'mass lower bound failed')
    pairs=[(i,j,squared(y[i],y[j]),squared(x[i],x[j])-squared(y[i],y[j]))
           for i,j in combinations(range(len(w)),2)]
    require(all(loss>=0 for _,_,_,loss in pairs),'not a contraction')
    delta=min(d for _,_,d,_ in pairs)
    require(delta>0,'distinct targets required')
    nearest=[(i,j,loss) for i,j,d,loss in pairs if d==delta]
    chosen=max(nearest,key=lambda p:p[2]);eta=chosen[2]
    require(eta>0,'every nearest target pair is tight')
    require(eta/s>=4,'nearest-pair loss/noise condition failed')
    require(delta/s>=k*l,'separation/noise condition failed')
    return {'status':'EXACT_HYPOTHESES_PASS','curvature_square_degree':degree,
            'energy_degree':m,'mass_exponent':bits,'K_D':k,'L_D_b':l,
            'variance':str(s),'delta':str(delta),'eta':str(eta),
            'chosen_nearest_pair':list(chosen[:2]),
            'minimum_pair_loss':str(min(v[3] for v in pairs)),
            'variance_upper_bound':str(min(eta/4,delta/(k*l))),
            'normalized_matrix_lower_bound':'1/2'}


def fixture():
    x=[['0','0','0'],['2','0','0'],['1','2','0'],['1/2','1/3','3'],
       ['19/6','16/9','17/9'],['-5/2','41/18','4/3'],['5/6','-35/9','13/9']]
    y=[['0','0','0'],['3/2','0','0'],['3/4','3/2','0'],['3/8','1/4','9/4'],
       ['-5/8','-1/6','1/12'],['21/8','-13/24','1/2'],['5/8','37/12','5/12']]
    w=['1/8','1/8','1/8','1/8','1/4','1/8','1/8']
    return [[F(v) for v in p] for p in x],[[F(v) for v in p] for p in y],list(map(F,w))


def determinant(a):
    a=[list(map(F,row)) for row in a];n=len(a);result=F(1)
    require(all(len(row)==n for row in a),'square matrix required')
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];result=-result
        q=a[j][j];result*=q
        for i in range(j+1,n):
            ratio=a[i][j]/q
            for k in range(j+1,n):a[i][k]-=ratio*a[j][k]
            a[i][j]=0
    return result


def compositions(total,n):
    if n==1:
        yield (total,)
    else:
        for a in range(total+1):
            for tail in compositions(total-a,n-1):yield (a,)+tail


def algebra_controls():
    count=equal=0
    digest=sha256()
    for n in range(2,8):
        for m in range(2,13):
            for c in compositions(m,n):
                if max(c)==m:continue
                cross=sum(c[i]*c[j] for i,j in combinations(range(n),2))
                require(cross>=m-1,'nonconstant replica scatter bound failed')
                if cross==m-1:equal+=1
                count+=1;digest.update(f'{n},{m},{c},{cross}\n'.encode())
    curvature=0
    for degree in range(1,65):
        _,k,_=constants(degree,3)
        for i,j in combinations(range(degree+1),2):
            a,b=2*i+2,2*j+2;m=i+j+2
            alpha=lambda n:F(n-1,2*n)
            gap=alpha(m)-(alpha(a)+alpha(b))/2
            exact=F((i-j)**2,8*(i+1)*(j+1)*(i+j+2))
            require(gap==exact and gap>=F(1,k),'curvature identity/minimum failed')
            # After squaring, c_m <= sqrt(c_a*c_b) is wholly rational.
            ratio_squared=F((a*b)**5*(a-1)**2*(b-1)**2,m**10*(m-1)**4)
            require(ratio_squared<=1,'prefactor log-convexity failed')
            curvature+=1;digest.update(f'{degree},{i},{j},{gap},{ratio_squared}\n'.encode())
    cutoffs=[]
    for degree in [1,2,5,10,20,50,100,1000]:
        m,k,l=constants(degree,3)
        require(2**(l-m*3)>=2*degree,'integer exponential budget failed')
        cutoffs.append({'curvature_degree':degree,'energy_degree':m,'K_D':k,'L_D_b':l,
                        'uniform_variance_cutoff':str(min(F(1,4),F(1,4*k*l)))})
    return {'nonconstant_compositions':count,'sharp_composition_cases':equal,
            'curvature_and_prefactor_checks':curvature,'algebra_sha256':digest.hexdigest(),
            'uniform_class':{'minimum_weight':'1/8','minimum_target_separation_squared':'1/4',
                             'minimum_loss_at_some_nearest_target_pair':'1'},
            'uniform_cutoffs':cutoffs}


def rejected_controls(x,y,w,bound):
    tests=[]
    tests.append(lambda:certify(x,y,w,bound*F(1000001,1000000),5,3))
    tests.append(lambda:certify(x,y,w,F(1,422400),5,2))
    bad=deepcopy(y);bad[1][0]=100
    tests.append(lambda:certify(x,bad,w,F(1,422400),5,3))
    collision=deepcopy(y);collision[1]=collision[0][:]
    tests.append(lambda:certify(x,collision,w,F(1,422400),5,3))
    line=[[F(0),F(0),F(0)],[F(1),F(0),F(0)],[F(10),F(0),F(0)]]
    fixed_nearest=[line[0],line[1],[F(5),F(0),F(0)]]
    tests.append(lambda:certify(line,fixed_nearest,[F(1,3)]*3,F(1,10**9),5,2))
    tests.append(lambda:certify(x,x,w,F(1,10**9),5,3))
    tests.append(lambda:constants(0,3));tests.append(lambda:constants(5,0))
    tests.append(lambda:certify(x,y,w,0,5,3))
    for test in tests:
        try:test()
        except ValueError:continue
        raise RuntimeError('A damaged hypothesis passed')
    return len(tests)


def reproduce():
    x,y,w=fixture();joint=[a+b for a,b in zip(x,y)]
    paired_det=determinant([[a-b for a,b in zip(p,joint[0])] for p in joint[1:]])
    require(paired_det!=0,'fixture lost paired rank six')
    certificate=certify(x,y,w,F(1,422400),5,3)
    require(certificate['delta']=='245/576' and certificate['eta']=='84659/5184',
            'nearest pair changed')
    bound=F(certificate['variance_upper_bound'])
    boundary=certify(x,y,w,bound,5,3)
    algebra=algebra_controls()
    return {'status':'LOW_NOISE_DEGREE_BARRIER_EXACT_PASS',
            'conjecture_status':'OPEN: finite polynomial degree exclusion only',
            'fixture':{'source':[[str(v) for v in p] for p in x],
                       'target':[[str(v) for v in p] for p in y],
                       'weights':list(map(str,w)),'paired_determinant':str(paired_det),
                       'certificate':certificate,'exact_boundary_certificate':boundary},
            'algebra_controls':algebra,'damaged_controls_rejected':rejected_controls(x,y,w,bound),
            'trust_boundary':'Exact finite controls. Universal theorem is the written replica and diagonal-dominance proof; no full Gaussian sign.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true')
    ap.add_argument('--write-expected',action='store_true');args=ap.parse_args()
    text=json.dumps(reproduce(),indent=2)+'\n'
    if args.write_expected:(ROOT/'EXPECTED.json').write_text(text)
    if args.check:require(text==(ROOT/'EXPECTED.json').read_text(),'expected output mismatch')
    print(text,end='')


if __name__=='__main__':main()
