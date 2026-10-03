"""Arithmetic, singularity, critical-map and once-verified projection controls.

Damaged-record projection checks are not presented as full geometric reruns.
Only the damaged first-anchor case additionally reruns the independent audit.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import argparse,json
import check as C
import audit as A


def run():
    ref=C.build();given=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text());C.verify(given,ref);A.audit(given)
    arithmetic=[]
    for i,(matrix,target) in enumerate((([[1,2],[3,4]],-2),([[0,1],[1,0]],-1),([[0,0],[1,1]],0),([[2,4],[1,2]],0))):
        dense=[[[F(x)] if x else [] for x in row] for row in matrix]
        sparse=[[A.P(x) for x in row] for row in matrix]
        C.need(C.bareiss(dense)==([F(target)] if target else []) and A.interpolate_det(sparse)==A.P(target),'both whole determinant fixture values');arithmetic.append('determinant-'+str(i))
    C.need(C.sign([])==0 and C.strip([])==[] and A.centered_sign({})==0 and A.reduced({},A.P(1))=={},'zero polynomial never gives an exclusion');arithmetic.append('zero')
    h=[F(-1),F(1),F(1)];hh=A.P(-1,1,1)
    C.need(C.direct_sign(h)==1 and A.centered_sign(hh)==1,'positive whole closed-band fixture');arithmetic.append('positive-closed')
    C.need(C.direct_sign([F(-7,10),F(1)])==0 and A.centered_sign(A.P(F(-7,10),1))==0,'endpoint zero retained');arithmetic.append('closed-endpoint')
    root=F(29,40)
    for inconsistent in (False,True):
        mat=[[([F(-root),F(1)] if i==5 else [F(1)]) if i==j else [] for j in range(6)] for i in range(6)]
        rhs=[[F(i+1)] if inconsistent else C.mul(mat[i][i],[F(i+1)]) for i in range(6)]
        delta=C.bareiss(mat);nums=[C.bareiss([[rhs[i] if j==k else x for k,x in enumerate(ar)] for i,ar in enumerate(mat)]) for j in range(6)]
        am=[[A.P(*p) for p in ar] for ar in mat];ab=[A.P(*p) for p in rhs]
        C.need(A.encode(A.interpolate_det(am))==C.enc(delta),'whole singular determinant polynomial agrees')
        for j in range(6):
            ad=A.interpolate_det([[ab[i] if j==k else x for k,x in enumerate(ar)] for i,ar in enumerate(am)])
            C.need(A.encode(ad)==C.enc(nums[j]),'entire singular Cramer numerator agrees')
        C.need(sum(v*root**i for i,v in enumerate(delta))==0,'interior determinant root present')
        values=[sum(v*root**i for i,v in enumerate(p)) for p in nums]
        C.need((any(values) if inconsistent else not any(values)),'singular consistent and inconsistent cases distinguished without division')
        arithmetic.append('singular-inconsistent' if inconsistent else 'singular-consistent')
    p=C.parent();row=p['geometric_maps'][8];cs,md=C.coeffs();control,eqs=C.linear_case(8,row,p['all_shapes'][row['shape']],C.predictions(row)[0],cs,md)
    C.need(control['closed_gcd_sign']==0 and C.direct_sign(C.G)==0 and A.centered_sign(A.P(*C.G))==0,'known critical map not excluded')
    for eq in eqs:
        _,rem=C.divide(eq,C.G);_,ar=A.divrem(A.P(*eq),A.P(*C.G));C.need(not rem and not ar,'each whole critical-map necessary equation retains G')
    derivative=[F(i)*C.G[i] for i in range(1,len(C.G))]
    C.need(C.direct_sign(derivative)==1 and sum(x*C.LO**i for i,x in enumerate(C.G))<0<sum(x*C.HI**i for i,x in enumerate(C.G)),'unique critical root retained');arithmetic.append('critical-map8')
    mutations=[]
    def damage(label,f):
        bad=deepcopy(given);f(bad);mutations.append((label,bad))
    damage('missing-row',lambda x:x['rows'].pop())
    damage('duplicate-row',lambda x:x['rows'].__setitem__(1,deepcopy(x['rows'][0])))
    damage('reordered-cover',lambda x:x['rows'].reverse())
    damage('critical-map-in-cover',lambda x:x['rows'][0].__setitem__('map',8))
    damage('cross-contact',lambda x:x['rows'][0]['cross'][0].__setitem__(1,10))
    damage('B-triangle',lambda x:x['rows'][0]['B_triangles'][0].__setitem__(0,99))
    damage('quad',lambda x:x['rows'][0]['quad'].__setitem__(0,9))
    damage('anchor',lambda x:x['rows'][0].__setitem__('anchor',6))
    damage('anchor-coordinate',lambda x:x['rows'][0]['anchor_n'][0].__setitem__(0,'-3'))
    damage('anchor-denominator',lambda x:x['rows'][0]['anchor_L'].__setitem__(0,'5'))
    damage('row-divisor-zero',lambda x:x['rows'][0]['row_divisors'].__setitem__(0,[]))
    for field in ('linear_system_digest','Cramer_digest','norm_equations_digest','reduced_equations_digest'):
        damage(field,lambda x,key=field:x['rows'][0].__setitem__(key,'0'*64))
    damage('wrong-GCD',lambda x:x['rows'][0].__setitem__('common_gcd',['-1','1']))
    damage('wrong-sign',lambda x:x['rows'][0].__setitem__('closed_gcd_sign',-1))
    damage('float-index',lambda x:x['rows'][0].__setitem__('map',2.0))
    damage('boolean-index',lambda x:x['rows'][0].__setitem__('map',True))
    damage('float-coefficient',lambda x:x['rows'][0]['anchor_n'][0].__setitem__(0,-4.0))
    damage('band',lambda x:x['r_closed_band'].__setitem__(0,'0'))
    damage('parent-pin',lambda x:x.__setitem__('parent_sha256','0'*64))
    damage('retained-map-missing',lambda x:x['remaining_strict_maps'].pop())
    damage('format',lambda x:x.__setitem__('format','wrong'))
    rejected=[]
    for label,bad in mutations:
        try:C.verify(bad,ref)
        except ValueError:pass
        else:raise ValueError('producer accepted '+label)
        try:A.require(A.canon(bad)==A.canon(given),'projection of once independently validated certificate')
        except ValueError:pass
        else:raise ValueError('auditor projection accepted '+label)
        rejected.append(label)
    bad=next(x for label,x in mutations if label=='anchor-coordinate')
    try:A.audit(bad)
    except ValueError:pass
    else:raise ValueError('full independent audit accepted changed anchor ratio')
    valid=[json.loads(json.dumps(given,indent=3)),dict(reversed(list(given.items())))]
    for x in valid:C.verify(x,ref);A.require(A.canon(x)==A.canon(given),'valid JSON presentation')
    return {'status':'complete','arithmetic_and_singularity_controls':arithmetic,'critical_map8_root_retained':True,
            'damaged_projection_cases_rejected_by_both':rejected,'projection_reference_freshly_geometrically_verified_by_both':True,
            'full_independent_geometric_negative_reruns':['anchor-coordinate'],'valid_JSON_presentations':len(valid)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args();r=run()
    if args.emit:Path(args.emit).write_text(C.canonical(r))
    print(C.canonical(r).strip())
