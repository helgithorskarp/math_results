#!/usr/bin/env python3
"""Full author certificate. Exact checks, untrusted floating root proposals.

Run python3 -B verify.py or python3 -B -O verify.py. --emit recomputes all
mathematical checks before printing a replacement expected record.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product, combinations
import argparse,json,time
import radial as r
import middle
from direct_hinge import matrix_rank

HERE=r.HERE
need=r.need

def cell():
    return {'variance':1,'source_centers':[[str(a) for a in v] for v in r.X],
      'target_centers':[[str(a) for a in v] for v in r.Y],
      'weights':['1/16']*16,'coordinate_radius':'1/2048',
      'euclidean_radius_upper':'1/1024','coordinate_parameters':96,
      'anchored_coordinate_parameters':90,'frontier_level':2,
      'label_order':'four cores, then (i,j) in lexicographic order with i!=j',
      'reference_vertices':[list(v) for v in r.V],'depth':2,'spatial_scale':'1/2',
      'target_homothety':'63/64'}

def determinant(rows):
    a=[list(map(F,row)) for row in rows];out=F(1)
    for i in range(len(a)):
        p=next((j for j in range(i,len(a)) if a[j][i]),None)
        if p is None:return F(0)
        if p!=i:a[i],a[p]=a[p],a[i];out=-out
        pivot=a[i][i];out*=pivot
        for j in range(i+1,len(a)):
            factor=a[j][i]/pivot
            for k in range(i,len(a)):a[j][k]-=factor*a[i][k]
    return out

def geometry():
    X,Y=r.X,r.Y;e=r.EPS
    need(len(set(X))==len(set(Y))==16,'distinct sites')
    need(all(sum(v[k] for v in P)==0 for P in (X,Y) for k in range(3)), 'reference centering')
    losses=[];xd=[];yd=[]
    for i,j in combinations(range(16),2):
        a=sum((u-v)**2 for u,v in zip(X[i],X[j]))
        b=sum((u-v)**2 for u,v in zip(Y[i],Y[j]))
        xd.append(a);yd.append(b);losses.append(a-b)
    need(min(losses)==F(127,2048),'reference pair loss')
    floor=min(losses)-4*e*F(63,8)
    need(floor==F(1,32)>F(1,4096),'cell contraction floor')
    need(min(xd)>4*e*e and min(yd)>4*e*e,'collision control')
    normals=[r.sqrt_bounds(sum(a*a for a in v),48)[1] for v in X+Y]
    need(max(normals[:16])+e<F(9,4) and max(normals[16:])+e<F(27,16),'radial support bounds')
    need(2*F(9,4)<6 and 2*F(27,16)<6,'anchored radius')
    need(all((a*2048).denominator==1 for P in (X,Y) for v in P for a in v),'coordinate lattice')
    A2=8*(2*56-1);W=8*A2
    need(A2==888 and W==7104 and W%16==0 and 16<=A2,'R3 rational budget')
    rows=[tuple(a-b for a,b in zip(X[i]+Y[i],X[0]+Y[0])) for i in range(1,16)]
    need(matrix_rank(rows)==6,'paired rank')
    labels=next(ids for ids in combinations(range(1,16),6) if determinant([rows[i-1] for i in ids]))
    det=determinant([rows[i-1] for i in labels])
    midpoint=[]
    for q in Y:
        original=tuple(a*64/63 for a in q)
        pair=next(((i,j) for i in range(16) for j in range(i,16)
              if tuple((a+b)/2 for a,b in zip(X[i],X[j]))==original),None)
        need(pair is not None,'target convex hull');midpoint.append(list(pair))
    cross=[]
    for k in range(3):
        for sign in (-1,1):
            ids=[i for i,x in enumerate(X) if x[k]==sign*F(3,2)]
            mean=tuple(sum(X[i][j] for i in ids)/len(ids) for j in range(3))
            need(mean==tuple(sign*F(3,2) if j==k else F(0) for j in range(3)),'source crosspolytope')
            cross.append(ids)
    sym=0
    for perm in permutations(range(3)):
        for signs in product((-1,1),repeat=3):
            if signs[0]*signs[1]*signs[2]!=1:continue
            for P in (X,Y):
                need(Counter(tuple(signs[k]*v[perm[k]] for k in range(3)) for v in P)==Counter(P),'reference symmetry')
            sym+=1
    need(sym==24,'group coverage')
    return {'reference_minimum_pair_loss':str(min(losses)),'cell_pair_loss_floor':str(floor),
       'minimum_source_squared_separation':str(min(xd)),'minimum_target_squared_separation':str(min(yd)),
       'paired_rank':6,'minor_labels':[0]+list(labels),'minor_determinant':str(det),
       'source_crosspolytope_witnesses':cross,'target_midpoint_witnesses':midpoint,
       'reference_symmetries':sym,'frontier':{'k':2,'A':A2,'L':2048,'W':W,'mass_units':W//16}}

def tail_analytic():
    e=r.EPS;RX=F(9,4);RY=F(27,16);A=F(269,25);B=F(277,200)
    inner=F(141,32)+F(9,2)*e+e*e/2
    need(inner<F(49,8),'inner ball covered by low superlevels')
    need(r.exp_neg(F(49,8),50)[0]>F(1,512)*(1<<50),'endpoint overlap')
    need(r.exp_neg(F(1,2),50)[1]<F(61,100)*(1<<50),'Gaussian gradient')
    need(sum(F(3)**k/__import__('math').factorial(k) for k in range(5))>16,'log16<3')
    need(F(3,224)-2*e>0,'strict support inclusion under perturbation')
    need(F(63,64)*F(2,7)-e>0,'target origin inside convex hull')
    need(F(19,4)+2*RX*e+e*e+6<A,'source far-tail constant')
    need(F(11,4)*F(63,64)**2+2*RY*e+e*e<2*B,'target far-tail constant')
    total=F(0);ps=r.patches(12)
    for p in ps:
        gap=max(F(0),F(max(p['x'][0])-max(p['y'][0]),r.Q))
        total+=p['area']*p['jl']*gap
    delta=F(21,11)*total
    need(delta>F(1,4),'mean support gap')
    S=F(64)
    error=A/S*(1+RX/S)**2+B/S*(1+RY/S+B/S**2)**2
    need(error<F(21,100),'uniform far-tail volume sign')
    need(12*S*S/25>F(1,2),'far-tail half-volume margin')
    return {'inner_ball_exponent_upper':str(inner),'mean_support_lower':str(delta),
       'far_tail_A':str(A),'far_tail_B':str(B),'far_error_at_64':str(error),
       'far_volume_margin':'1/2','S_cutoff':'7/2','threshold_overlap':'exp(-49/8)>1/512'}

def controls():
    result=r.controls()
    # Probe dyadics with the large denominators used by the actual roots.
    for i in range(1,129):
        num=int.from_bytes(sha256(str(i).encode()).digest()[:9],'big')>>3
        lo,hi=r.exp_neg_dyadic(num,61)
        a,b=r.exp_neg(F(num,1<<61),70)
        need(F(lo,1<<50)<=F(a,1<<70)<=F(b,1<<70)<=F(hi,1<<50),'root-scale exponential cross-check')
    result['root_scale_exponential_controls']=128
    # Intentionally invalid root endpoints must be rejected by exact arithmetic.
    p=r.patches(12)[0];bad=0
    for s,data,lower,delta in [(F(6),p['x'],True,1),(F(6),p['y'],False,-1)]:
        root=r.root_proposal(s,data,lower)+delta*r.RQ//4
        try:r.check_root(s,data,root,lower)
        except ValueError:bad+=1
        else:raise ValueError('false root bracket accepted')
    result['rejected_root_corruptions']=bad
    # Verify the all-knots sweep directly on small discrete distributions.
    count=0
    for xs in product(range(4),repeat=2):
        for ys in product(range(4),repeat=2):
            for a,b in [(0,3),(1,2),(1,3)]:
                best,arg,_=middle.window_max(Counter(xs),Counter(ys),a,b)
                vals={u:sum(max(x-u,0) for x in xs)-sum(max(y-u,0) for y in ys)
                      for u in {a,b}|{v for v in xs+ys if a<=v<=b}}
                need(best==max(vals.values()) and vals[arg]==best,'sweep definition control')
                count+=1
    result['definition_level_window_sweeps']=count
    return result

def calculate(progress):
    need(json.loads((HERE/'CELL.json').read_text())==cell(),'cell input mismatch')
    result={'status':'GAP_FREE_DEEP_FLAP_CELL_PASS','cell_sha256':sha256((HERE/'CELL.json').read_bytes()).hexdigest(),
      'dependency_pins':r.PINS,'geometry':geometry(),'analytic_tail':tail_analytic(),'controls':controls()}
    result['radial_bands']=[r.run_band(24,F(1,16),F(7,2),F(6),progress),
                           r.run_band(12,F(1,8),F(6),F(64),progress)]
    result['middle']=middle.calculate()
    result['theorem']={'variance':1,'all_thresholds':True,'low_adverse_upper':'-C*u/2 for 0<u<=1/512',
       'middle_adverse_upper':'-1/128 for 1/512<=u<=9/32','high':'source hinge vanishes for u>=9/32',
       'independent_review':'PENDING'}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();result=calculate(args.progress)
    if not args.emit:need(result==json.loads((HERE/'EXPECTED.json').read_text()),'expected record mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
