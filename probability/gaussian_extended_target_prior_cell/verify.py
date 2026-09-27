#!/usr/bin/env python3
"""Exact full-prior/diffuse certificate on the extended-target cell.
Standard-library CPython >=3.11. Float roots are proposals only.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb,factorial
import argparse,json,time,resource
from common import HERE,PINS,r,geometry_module,exp_neg
import middle_certificate as mid
import radial_certificate as rad


def need(c,msg):
    if not c:raise ValueError(msg)


def small_grid_controls():
    sites=0
    for M,h in [(1,F(1,2)),(2,F(1,3)),(3,F(1,4))]:
        bits=32;Q=1<<bits;den=256*Q*Q
        hist,peaks,ns,*_=mid.histogram(h,M,bits)
        direct=[Counter(),Counter()];dp=[0,0]
        for point in product(range(-M,M+1),repeat=3):
            xyz=tuple(h*j for j in point);xx=[];yl=[];yu=[]
            for P in [r.X,r.Y]:
                vals=[]
                for atom in P:
                    factors=[exp_neg((z-a)**2/2,bits) for z,a in zip(xyz,atom)]
                    vals.append((factors[0][0]*factors[1][0]*factors[2][0],
                                 factors[0][1]*factors[1][1]*factors[2][1]))
                if P is r.X:xx=[v[1] for v in vals]
                else:yl=[v[0] for v in vals];yu=[v[1] for v in vals]
            gl=sum(yl)//(16*Q*Q)
            for typ,label in enumerate([0,4]):
                f=(15*sum(xx)+16*xx[label]+den-1)//den
                g=(17*sum(yu)-16*yu[label]+den-1)//den
                for val,coeff in [(f,1),(g,1),(gl,-2)]:
                    if val>Q//512:direct[typ][val]+=coeff
                dp[typ]=max(dp[typ],f)
        for typ in range(2):
            a={k:v for k,v in hist[typ].items() if v}
            b={k:ns[typ]*v for k,v in direct[typ].items() if v}
            need(a==b,'averaged orbit histogram disagrees with fixed-label full grid')
            need(peaks[typ]==dp[typ],'source peak orbit disagreement')
        sites+=(2*M+1)**3
    return sites


def convex_controls():
    count=0;u=[F(1,3)]*3;v=[[F(3,4)*u[j]+F(i==j,4) for j in range(3)] for i in range(3)]
    q=[[2*u[j]-p[j] for j in range(3)] for p in v]
    need(all(min(p)>=0 and sum(p)==1 for p in v+q),'backward priors')
    def mix(p,rows):return [sum(w*row[j] for w,row in zip(p,rows)) for j in range(4)]
    def hinge(d,a):return sum(max(x-a,0) for x in d)
    for seed in range(12):
        arrays=[]
        for modulus,offset in [(17,3),(23,5)]:
            rows=[]
            for i in range(3):
                z=[((seed+7*i+offset*j)**2%modulus)+1 for j in range(4)]
                rows.append([F(x,sum(z)) for x in z])
            arrays.append(rows)
        sx,ty=arrays
        for a in [F(i,16) for i in range(17)]:
            base=hinge(mix(u,ty),a)
            lower=[2*base-hinge(mix(p,ty),a) for p in q]
            gaps=[hinge(mix(p,sx),a)-ll for p,ll in zip(v,lower)]
            for i in range(5):
                for j in range(5-i):
                    lam=[F(i,4),F(j,4),F(4-i-j,4)]
                    p=[sum(t*w[k] for t,w in zip(lam,v)) for k in range(3)]
                    bound=sum(t*z for t,z in zip(lam,gaps))
                    need(hinge(mix(p,sx),a)-hinge(mix(p,ty),a)<=bound<=max(gaps),'supporting-plane certificate')
                    count+=1
    # Negative control: the difference of two hinges need not be convex.
    source=[[F(7,10),F(3,10),F(0)],[F(7,10),F(0),F(3,10)]]
    target=[[F(1),F(0),F(0)],[F(0),F(1),F(0)]];a=F(3,5)
    vertex=[hinge(x,a)-hinge(y,a) for x,y in zip(source,target)]
    center=hinge([(x+y)/2 for x,y in zip(*source)],a)-hinge([(x+y)/2 for x,y in zip(*target)],a)
    need(max(vertex)<0<center,'false vertex-only route was not rejected')
    return {'supporting_plane_controls':count,'false_difference_convexity_rejected':True}


def sweep_controls():
    count=0
    for seed in range(16):
        hist={i:((seed+3*i)**2%11)-5 for i in range(10)}
        for left,right in [(F(0),F(9)),(F(1,2),F(13,2)),(F(3),F(9,2))]:
            value,*_=mid.sweep(hist,left,right)
            nodes={left,right}|{F(v) for v in hist if left<v<right}
            expected=max(sum(c*max(v-t,0) for v,c in hist.items()) for t in nodes)
            need(value==expected,'signed-histogram sweep')
            count+=1
    return count


def endpoint_controls():
    geometry=geometry_module.geometry();tail=geometry_module.tail_analytic()
    inner=F(tail['inner_ball_exponent_upper'])+F(1,15)
    need(inner<F(49,8),'all-prior interior sublevel')
    need(sum(F(3)**j/factorial(j) for j in range(6))>F(256,15),'log minimum weight bound')
    need(F(2)*exp_neg(F(3,2),50)[1]<(1<<50),'Gaussian Hessian operator bound')
    p=rad.r.patches(2)[0];S=F(7,2);rejected=0
    for record,lower in [(p['x'],True),(p['y'],False)]:
        root=rad.proposal(S,record,lower);rad.checked(S,record,root,lower)
        wrong=root+(rad.r.RQ//2 if lower else -rad.r.RQ//2)
        try:rad.checked(S,record,wrong,lower)
        except ValueError:rejected+=1
        else:raise ValueError('corrupted radial bracket accepted')
    need(rejected==2,'radial rejection count')
    need((7104*15+255)//256==417,'rational simplex rounding')
    return {'inherited_geometry':geometry,'tail':tail,'new_inner_exponent_upper':str(inner),
            'minimum_mass':'15/256','log_inverse_minimum_mass_upper':'3',
            'corrupted_radial_brackets_rejected':rejected,
            'frontier':{'k':2,'W':7104,'minimum_mass_units':417,'free_units':432,
                        'labelled_priors':comb(447,15),'anchored_coordinate_and_weight_parameters':105}}


def calculate(progress=False):
    controls={'unquotiented_grid_sites_per_vertex':small_grid_controls(),
              'signed_histogram_sweeps':sweep_controls(),**convex_controls()}
    endpoints=endpoint_controls()
    middle=mid.calculate(progress=progress)
    need(F(exp_neg(F(18),48)[1],1<<48)<min(F(x['peak']) for x in middle['rows']),
         'outside-grid source peak')
    bands=[rad.band(*spec,progress=progress) for spec in
           [(48,F(1,32),F(7,2),F(4)),(32,F(1,16),F(4),F(6)),
            (24,F(1,16),F(6),F(12)),(12,F(1,8),F(12),F(64))]]
    need(sum(b['windows'] for b in bands)==560,'whole threshold cover')
    return {'status':'EXTENDED_TARGET_PRIOR_CELL_PASS','dependency_pins':PINS,
            'controls':controls,'endpoints':endpoints,'middle':middle,'radial_bands':bands,
            'theorem':{'variance':1,'prior_floor':'15/256','prior_vertices':'31/256 at one label; 15/256 elsewhere',
                       'backward_target_priors':'1/256 at one label; 17/256 elsewhere',
                       'coordinate_radius':'1/2048','diffuse_component_laws':True,
                       'middle':['1/512','9/32'],'middle_adverse_upper':'-1/256',
                       'low_adverse_upper':'-C*u/2','all_thresholds':True,
                       'independent_review':'PENDING','unrestricted_status':'OPEN'}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=__import__('pathlib').Path,default=HERE/'EXPECTED.json')
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();start=time.monotonic();record=calculate(args.progress)
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.emit:args.expected.write_bytes(raw)
    else:need(json.loads(args.expected.read_text())==record,'expected record mismatch')
    print(record['status']);print('record_sha256',sha256(raw).hexdigest())
    print('seconds',round(time.monotonic()-start,3));print('peak_rss_kib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

if __name__=='__main__':main()
