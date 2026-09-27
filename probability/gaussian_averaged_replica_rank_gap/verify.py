"""Exact normalization controls, not a computation of the compactness gap."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import math

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def norm2(x):
    return sum((a*a for a in x), F(0))


def sub(x, y):
    return tuple(a-b for a,b in zip(x,y))


def scatter(points):
    n=len(points)
    return sum((norm2(sub(points[i],points[j]))
                for i in range(n) for j in range(i+1,n)),F(0))/n


def centered_scatter(points):
    n=len(points)
    b=tuple(sum(row[j] for row in points)/n for j in range(len(points[0])))
    return sum((norm2(sub(row,b)) for row in points), F(0))


def diamond(points):
    d=lambda i,j:norm2(sub(points[i],points[j]))
    return d(0,1)/6+(d(0,2)+d(0,3)+d(1,2)+d(1,3))/3


def gaussian_moment(k):
    if k%2:
        return F(0)
    return F(math.prod(range(1,k,2)))


def calculate():
    # Integrate the two Gaussian kernels divided by the standard Gaussian.
    rho=F(1,3)
    variance=1-rho
    precision=2/variance-1
    squared_prefactor=1/(variance*variance*precision)
    cross=rho/(variance*variance*precision)
    self_coefficient=-rho/(2*variance)+cross/2
    require(squared_prefactor==F(9,8), 'Gaussian prefactor')
    require(cross==F(3,8) and self_coefficient==F(-1,16), 'Gaussian completion')
    constant=F(8,9)**3
    require(constant*(F(9,8)**3)==1, 'six dimensional factor')
    point_defect=F(9,8)**3-1
    require(constant*(1+point_defect)==1, 'point law control')

    # Direct Gaussian moments, followed by the OU second-moment scaling.
    normal_second=gaussian_moment(2)
    normal_fourth=gaussian_moment(4)
    centered_squared_norm=3*(normal_fourth-normal_second**2)
    require(centered_squared_norm==6, 'three dimensional Gaussian norm')
    moment_constant=centered_squared_norm/(rho*rho)
    require(moment_constant==54, 'moment bound')
    for w in [F(-3),F(-1,2),F(0),F(2,3),F(4)]:
        ou_second=rho*w*w+variance
        require(ou_second-1==rho*(w*w-1), 'OU polynomial')
    e_cut=F(1,216)
    require(moment_constant*e_cut==F(1,4), 'half unit moment threshold')
    require(F(4,5)/(1-F(4,5))==4, 'graph Lipschitz square')
    good_loss=F(5,2)-F(1,4)*F(7,2)
    require(good_loss==F(13,8), 'good-event remaining loss')
    good_probability=1/good_loss
    bad_probability=1-good_probability
    require(bad_probability==F(5,13), 'averaged positive fraction')
    eta_cap=bad_probability*e_cut
    require(eta_cap==F(5,2808), 'stated eta cap')
    require((1+eta_cap)**2<F(9,8), 'full Hankel sign is not obtained')

    sites=[(F(0),F(0),F(0))]
    for j in range(3):
        for sign in [-1,1]:
            sites.append(tuple(F(sign if j==k else 0) for k in range(3)))
    images=[tuple(abs(a) for a in row) for row in sites]
    priors=[F(i+1,28) for i in range(7)]
    require(sum(priors)==1, 'prior normalization')
    strict_pairs=0
    for i in range(7):
        for j in range(i+1,7):
            loss=norm2(sub(sites[i],sites[j]))-norm2(sub(images[i],images[j]))
            require(loss>=0, 'fold contraction')
            strict_pairs+=int(loss>0)
    require(strict_pairs==3, 'positive marks and zero-loss pairs')

    rows=0
    clock_controls=0
    for labels in product(range(7),repeat=4):
        x=[sites[i] for i in labels]
        y=[images[i] for i in labels]
        for points in [x,y]:
            b=tuple((points[0][j]+points[1][j])/2 for j in range(3))
            u,v=sub(points[2],b),sub(points[3],b)
            pair=scatter(points[:2])
            q4=pair+F(3,4)*(norm2(u)+norm2(v))-sum(a*c for a,c in zip(u,v))/2
            qd=pair+F(2,3)*(norm2(u)+norm2(v))
            require(q4==centered_scatter(points)==scatter(points), 'clique centering')
            require(qd==diamond(points), 'diamond centering')
        delta=norm2(sub(x[0],x[1]))-norm2(sub(y[0],y[1]))
        loss=diamond(x)-diamond(y)
        require(loss>=0, 'graph loss')
        bx=tuple((x[0][j]+x[1][j])/2 for j in range(3))
        by=tuple((y[0][j]+y[1][j])/2 for j in range(3))
        xsum=sum(norm2(sub(x[i],bx)) for i in [2,3])
        ysum=sum(norm2(sub(y[i],by)) for i in [2,3])
        require(loss==delta/2+F(2,3)*(xsum-ysum), 'loss centering')
        # The two-replica average becomes one conditional expectation in (22).
        for t in [F(1,5),F(1,2),F(9,10)]:
            z=1-t
            a_mean=F(2,3)*z*xsum/2
            b_mean=F(2,3)*t*ysum/2
            require(z*loss/2 == z*delta/4+a_mean-z*b_mean/t, 'clock moment scaling')
            clock_controls+=1
        rows+=1

    histogram_sizes={}
    for m in [2,3,4]:
        marked=defaultdict(F)
        symmetric=defaultdict(F)
        for labels in product(range(7),repeat=m):
            x=[sites[i] for i in labels];y=[images[i] for i in labels]
            mass=math.prod(priors[i] for i in labels)
            qx,qy=scatter(x),scatter(y)
            delta=norm2(sub(x[0],x[1]))-norm2(sub(y[0],y[1]))
            marked[qx,qy]+=mass*delta
            symmetric[qx,qy]+=mass*(qx-qy)*F(2,m-1)
        require(dict(marked)==dict(symmetric), 'replica mark normalization')
        histogram_sizes[str(m)]=len(marked)

    # Primitive for the truncated exponential moments, with no quadrature.
    for k in range(8):
        p=[F(math.factorial(k),math.factorial(j)) for j in range(k+1)]
        require(all(p[j]-(j+1)*p[j+1]==0 for j in range(k)), 'clock primitive')
        require(p[-1]==1, 'clock primitive leading term')

    return {'status':'AVERAGED_REPLICA_RANK_GAP_CONTROLS_PASS',
            'unrestricted_hankel_sign_proved':False,
            'compactness_constant_computed':False,
            'gaussian_completion':{'rho':str(rho),'cross':str(cross),
                'self':str(self_coefficient),'six_dimensional_constant':str(constant)},
            'moment_constant':str(moment_constant),'moment_cut':str(e_cut),
            'good_loss':str(good_loss),'bad_probability':str(bad_probability),
            'eta_cap':str(eta_cap),'strict_fold_pairs':strict_pairs,
            'ordered_quadruples':rows,'clock_controls':clock_controls,
            'histogram_sizes':histogram_sizes,'clock_primitives':8}


def compare(actual, expected):
    require(actual==expected, 'EXPECTED.json mismatch')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    result=calculate()
    changed=dict(result)
    changed['moment_constant']='53'
    try:
        compare(result,changed)
    except RuntimeError:
        pass
    else:
        raise RuntimeError('Corrupted record was not rejected')
    if args.write_expected:
        (ROOT/'EXPECTED.json').write_text(json.dumps(result,indent=2)+'\n')
    else:
        compare(result,json.loads((ROOT/'EXPECTED.json').read_text()))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
