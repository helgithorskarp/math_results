"""Check exact pairwise contraction certificates with ordered-pair moments.

The supplied-record checker imports no producer. The controls call the
producer only to obtain records, then check them independently.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parent


def need(test, why):
    if not test:
        raise ValueError(why)


def dist(a, b):
    return sum((u-v)**2 for u, v in zip(a, b))


def inputs(data):
    raw = [v for row in data['sources']+data['targets'] for v in row]+data['weights']
    raw += [data.get('variance',1)]+([data['factor']] if 'factor' in data else [])
    need(all(type(v) in (int,str) for v in raw), 'exact input')
    x,y = [[[F(v) for v in row] for row in data[k]] for k in ['sources','targets']]
    p = list(map(F,data['weights']));s = F(data.get('variance',1))
    need(len(x)==len(y)==len(p)>0 and all(len(z)==3 for z in x+y), 'dimensions')
    need(s>0 and min(p)>=0 and sum(p)==1, 'probability or variance')
    if 'factor' in data:need(0<F(data['factor'])<1, 'factor range')
    keep=[i for i,w in enumerate(p) if w]
    x,y,p=[[v[i] for i in keep] for v in (x,y,p)]
    n=len(p);scatter=F(0);loss=F(0);beta=F(0)
    for i,j in product(range(n),repeat=2):
        a,b=dist(x[i],x[j]),dist(y[i],y[j])
        need(b<=a, 'original pair expands')
        if a:beta=max(beta,b/a)
        scatter+=p[i]*p[j]*a/2
        loss+=p[i]*p[j]*(a-b)
    radius=max(sum(p[j]*dist(z,x[j]) for j in range(n))-scatter for z in x)
    return x,y,p,s,beta,scatter,radius,loss


def check_record(data, record):
    x,y,p,s,beta,V,B,D=inputs(data);n=len(p)
    need(record['schema']=='uniform-lipschitz-v1' and record['active_sites']==n,'schema')
    for key,value in [('variance',s),('squared_lipschitz',beta),('source_scatter',V),
                      ('source_radius_squared',B)]:
        need(F(record[key])==value,'record '+key)
    status=record['status']
    if status=='ISOMETRIC_ZERO':
        need(D==0,'isometric equality');return {'status':'ISOMETRIC_ZERO_CHECK_PASS'}
    if status=='POINT_TARGET_ALL_VARIANCES':
        need(beta==0,'point target');return {'status':'POINT_TARGET_CHECK_PASS'}
    if status=='UNRESOLVED':return {'status':'NO_SIGN_ASSERTED'}
    need(status in ['SIGNED_ALL_THRESHOLDS','UNRESOLVED_AT_REQUESTED_VARIANCE'],'status')
    q=F(record['factor']);need(0<q<1 and 0<V<=B,'positive parameters')
    slack=None
    for i,j in product(range(n),repeat=2):
        v=q*q*dist(x[i],x[j])-27*dist(y[i],y[j])
        need(v>=0,'spherical pair bound')
        if i!=j:slack=v if slack is None else min(slack,v)
    eta=(1-q)*V/(96*B);cutoff=4224*B*B/((1-q)*V)
    floor=2*(1-beta)*V
    for key,value in [('spherical_gap',eta),('variance_cutoff',cutoff),('pair_loss_floor',floor)]:
        need(F(record[key])==value,'record '+key)
    need(D>=floor and cutoff*eta==44*B and cutoff>8*B,'endpoint budget')
    need((status=='SIGNED_ALL_THRESHOLDS')==(s>=cutoff),'requested variance')
    need(record['certified_variances']=='[variance_cutoff,infinity)' and
         record['certified_thresholds']=='[0,infinity)','certified intervals')
    return {'status':'UNIFORM_LIPSCHITZ_RECORD_PASS','ordered_pairs':n*n,
            'pair_loss':str(D),'minimum_pair_slack':str(slack)}


def determinant(rows):
    a=[[F(v) for v in row] for row in rows];value=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[k],a[j]=a[j],a[k];value=-value
        pivot=a[j][j];value*=pivot
        for i in range(j+1,len(a)):
            c=a[i][j]/pivot
            for l in range(j,len(a)):a[i][l]-=c*a[j][l]
    return value


def covariance_pairs(z,p):
    return [[sum(p[i]*p[j]*(z[i][k]-z[j][k])*(z[i][l]-z[j][l])
                 for i,j in product(range(len(p)),repeat=2))/2 for l in range(3)] for k in range(3)]


def encode(x,y,p,s=51000,q=None):
    d={'sources':[list(map(str,z)) for z in x], 'targets':[list(map(str,z)) for z in y],
       'weights':list(map(str,p)), 'variance':str(s)}
    if q is not None:d['factor']=str(q)
    return d


def thin(epsilon=F(1,100)):
    x=list(product([-1,0,1],[-1,0,1],[-epsilon,epsilon]))
    y=[[F(abs(u),12),F(abs(v),12),F(abs(u+v),12)] for u,v,z in x]
    return encode(x,y,[F(1,18)]*18,q=F(3,4))


def checks():
    from certificate import produce
    pins=json.loads((ROOT/'INPUTS.json').read_text())
    for p in pins:need(sha256((ROOT/p['relative_path']).read_bytes()).hexdigest()==p['sha256'],'source pin')
    # Exact universal endpoint and automatic-factor algebra controls.
    schedules=0
    for q,B,rho in product([F(1,8),F(1,2),F(3,4),F(7,8),1-F(1,2**50)],
                           [F(1,100),F(1),F(3),F(10000)],
                           [F(1),F(1,3),F(1,2**100)]):
        V=rho*B;eta=(1-q)*V/(96*B);cut=4224*B*B/((1-q)*V)
        need(cut*eta==44*B and cut>8*B,'universal budget');schedules+=1
        need((1-q*q/27)/(1-q)>1,'separation from fixed-covariance tiny-loss slab')
    for z in [F(0),F(1,10),F(27,48),1-F(1,2**100)]:
        q=(1+z)/2
        need(q*q-z==(1-z)**2/4 and q<1,'automatic factor')
    need(F(27,36)<=F(7,8)**2 and 4224/(1-F(7,8))==33792,'one-sixth family')
    need(F(9,64)-F(1,8)==F(1,64),'threshold overlap')
    # Cleared A_j>=1 product inequality for d=3, as a polynomial in u_j=A_j-1.
    coefficients={mask:F(3) for mask in product([0,1],repeat=3)}
    coefficients[(0,0,0)]-=3
    for j in range(3):
        mask=tuple(int(i==j) for i in range(3));coefficients[mask]-=1
    need(coefficients[(0,0,0)]==0 and all(v>=0 for v in coefficients.values()),'product polynomial')
    base=thin();cases={'thin':base,'thinner':thin(F(1,2**70))}
    automatic=deepcopy(base);automatic.pop('factor');automatic['variance']='100000';cases['automatic']=automatic
    badfactor=deepcopy(base);badfactor['factor']='7/10';cases['small_factor']=badfactor
    r=produce(base);below=deepcopy(base);below['variance']=str(F(r['variance_cutoff'])-1);cases['below_variance']=below
    equal=deepcopy(base);equal['targets']=equal['sources'];cases['isometry']=equal
    point=deepcopy(base);point['targets']=[['0']*3 for _ in point['sources']];point['variance']='1/1000000';cases['point_target']=point
    boundary=encode([[-1,0,0],[1,0,0]],[[-F(1,9)]*3,[F(1,9)]*3],[F(1,2)]*2);cases['factor_boundary']=boundary
    singular=thin(F(0));cases['singular_source']=singular
    rare=deepcopy(base);rare['weights']=[str(F(1,2**100))]+[str((1-F(1,2**100))/17)]*17
    rare['variance']='1000000';cases['rare_mass']=rare
    records={k:produce(v) for k,v in cases.items()}
    checked={k:check_record(cases[k],v) for k,v in records.items()}
    for k in ['thin','thinner','automatic','singular_source','rare_mass']:
        need(records[k]['status']=='SIGNED_ALL_THRESHOLDS','signed control '+k)
    need(records['below_variance']['status']=='UNRESOLVED_AT_REQUESTED_VARIANCE','below cutoff')
    need(records['small_factor']['status']==records['factor_boundary']['status']=='UNRESOLVED','factor boundary')
    need(records['isometry']['status']=='ISOMETRIC_ZERO','isometry')
    need(records['point_target']['status']=='POINT_TARGET_ALL_VARIANCES','point target')
    # Whole epsilon family: exact covariance and minor coefficients.
    target=[[F(1,648),F(0),F(1,1944)],[F(0),F(1,648),F(1,1944)],
            [F(1,1944),F(1,1944),F(11,2916)]]
    need(all(target[i][i]-F(1,972)>=sum(abs(target[i][j]) for j in range(3) if j!=i)
             for i in range(3)),'target covariance lower bound')
    need(F(1,10000)<F(1,972),'covariance separation for the whole interval')
    minor_coefficient=None
    for eps in [F(1),F(1,100),F(1,2**70)]:
        x,y,p,s,beta,V,B,D=inputs(thin(eps))
        need(beta==F(1,48) and V==F(4,3)+eps*eps and B==2+eps*eps,'family geometry')
        need(covariance_pairs(y,p)==target,'target covariance')
        need(covariance_pairs(x,p)==[[F(2,3) if i==j and i<2 else eps*eps if i==j else F(0)
                                    for j in range(3)] for i in range(3)],'source covariance')
        rows=[[1]+x[i]+y[i] for i in [0,1,2,4,6,12,16]]
        value=determinant(rows)/eps
        if minor_coefficient is None:minor_coefficient=value
        need(value==minor_coefficient and value!=0,'minor linear in epsilon')
    need(16896*(2+F(1,10000))**2/F(4,3)<51000,'uniform epsilon-family variance')
    # Scaling, independent target rotation, and inactive labels.
    moved=deepcopy(base)
    for k in ['sources','targets']:
        moved[k]=[[str(3*F(v)+(7 if k=='sources' else -5)) for v in z] for z in moved[k]]
    moved['variance']=str(9*F(moved['variance']));mr=produce(moved);check_record(moved,mr)
    need(F(mr['variance_cutoff'])==9*F(records['thin']['variance_cutoff']),'scale')
    rot=deepcopy(base)
    rot['targets']=[[str(F(3,5)*F(a)-F(4,5)*F(b)),str(F(4,5)*F(a)+F(3,5)*F(b)),c]
                    for a,b,c in rot['targets']]
    rr=produce(rot);check_record(rot,rr);need(rr==records['thin'],'independent rotation')
    zero=deepcopy(base);zero['sources'].append(['0']*3);zero['targets'].append(['100']*3);zero['weights'].append('0')
    need(produce(zero)==records['thin'],'zero mass')
    rejected=0
    for key,value in [('factor','1/2'),('spherical_gap','1'),('variance_cutoff','1'),
                      ('squared_lipschitz','0'),('source_scatter','0'),('pair_loss_floor','0'),
                      ('certified_variances','[0,infinity)')]:
        damaged=deepcopy(records['thin']);damaged[key]=value
        try:check_record(base,damaged)
        except ValueError:rejected+=1
        else:raise RuntimeError('damaged record accepted')
    damaged=deepcopy(records['below_variance']);damaged['status']='SIGNED_ALL_THRESHOLDS'
    try:check_record(below,damaged)
    except ValueError:rejected+=1
    else:raise RuntimeError('below-cutoff sign accepted')
    for key,value in [('variance',0),('variance',1.0),('factor',1),('factor',0),
                      ('weights',['-1']+['2/17']*17)]:
        bad=deepcopy(base);bad[key]=value
        try:produce(bad)
        except ValueError:rejected+=1
        else:raise RuntimeError('malformed input accepted')
    bad=encode([[0,0,0],[0,0,0]],[[0,0,0],[1,0,0]],[F(1,2)]*2)
    try:produce(bad)
    except ValueError:rejected+=1
    else:raise RuntimeError('duplicate-source expansion accepted')
    return {'status':'UNIFORM_LIPSCHITZ_ALL_THRESHOLD_PASS','pinned_sources':len(pins),
            'parameter_schedules':schedules,'records':records,'separate_checks':checked,
            'thin_family':{'epsilon_range':'(0,1/100]','variance':51000,'squared_lipschitz':'1/48',
                           'target_covariance_floor':'1/972','paired_minor_over_epsilon':str(minor_coefficient)},
            'rejected_inputs':rejected}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true');parser.add_argument('--input');parser.add_argument('--certificate')
    args=parser.parse_args()
    if args.input or args.certificate:
        if not(args.input and args.certificate) or args.emit:parser.error('supply both input and certificate')
        out=check_record(json.loads(Path(args.input).read_text()),json.loads(Path(args.certificate).read_text()))
    else:
        out=checks()
        if not args.emit:need(out==json.loads((ROOT/'EXPECTED.json').read_text()),'expected record')
    print(json.dumps(out,sort_keys=True,indent=2))
    if not args.emit:print('record_sha256',sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest())
