"""Damaged-scope/coverage/arithmetic controls, separate from generation."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as Q
import hashlib,json,signal
from polynomials import P,dot
from model import make
from algebra import require,LO,HI
from schema import validate
from signs import rational_bernstein,taylor_positive
from check import HERE,pins,obligations

def reject(call):
    try:call()
    except (ValueError,TypeError,KeyError):return
    raise ValueError('damaged control was accepted')

def run():
    pins();original=json.loads((HERE/'CERTIFICATE.json').read_text());validate(original);damages=[]
    def damaged(name,edit):
        c=deepcopy(original);edit(c);reject(lambda:validate(c));damages.append(name)
    damaged('missing-required5-12',lambda c:c['system']['literal_contacts'].remove([5,12]))
    damaged('wrong-older-G24-edge',lambda c:c['system']['literal_contacts'].__setitem__(-1,[8,13]))
    damaged('discard-critical-strip',lambda c:c['system'].__setitem__('closed_parameter_interval',['14/25','592/1000']))
    damaged('widen-unproved-band',lambda c:c['system'].__setitem__('closed_parameter_interval',['1/2','3/5']))
    damaged('wrong-cut-normal',lambda c:c['system']['caps'][0].__setitem__('normal',[5,14,-20]))
    damaged('wrong-cut-bound',lambda c:c['system']['caps'][0].__setitem__('cut',16))
    damaged('floating-proof-input',lambda c:c['system']['caps'][1].__setitem__('cut',9.0))
    damaged('unit-short-bound',lambda c:c['system'].__setitem__('short_norm_squared_bound','1'))
    damaged('fixed-added-points',lambda c:c['system'].__setitem__('all_additional_points','two prescribed incumbent labels'))
    damaged('added-face-premise',lambda c:c['system'].__setitem__('extra_contact_or_face_or_degree_premise_for_capacity',True))
    damaged('require-actual-extra-core13',lambda c:c['system'].__setitem__('actual_extra_core_point_required',True))
    damaged('missing-second-cap',lambda c:c['system']['caps'].pop())
    damaged('wrong-second-normal',lambda c:c['system']['caps'][1].__setitem__('normal',[-8,12,5]))
    damaged('wrong-second-cut',lambda c:c['system']['caps'][1].__setitem__('cut',10))
    damaged('claim-global-bound',lambda c:c['system'].__setitem__('global_Tammes_bound_claimed',True))
    damaged('assume-optimizer-occurrence',lambda c:c['system'].__setitem__('optimizer_motif_occurrence_claimed',True))
    damaged('missing-triple',lambda c:c['records'].pop())
    damaged('duplicate-triple',lambda c:c['records'].__setitem__(1,deepcopy(c['records'][0])))
    damaged('unknown-completeness-claim',lambda c:c['records'][0].__setitem__('type','UNKNOWN'))
    split=next(i for i,r in enumerate(original['records']) if len(r.get('leaves',[]))>1)
    damaged('missing-closed-cell',lambda c:c['records'][split]['leaves'].pop())
    damaged('duplicate-cell',lambda c:c['records'][split]['leaves'].append(deepcopy(c['records'][split]['leaves'][0])))
    i2=next(i for i,r in enumerate(original['records']) if any(l['type']=='I2' for l in r.get('leaves',[])))
    leaf=next(j for j,l in enumerate(original['records'][i2]['leaves']) if l['type']=='I2')
    damaged('same-opposite-residual',lambda c:c['records'][i2]['leaves'][leaf].__setitem__('negative_residual',c['records'][i2]['leaves'][leaf]['positive_residual']))
    damaged('boolean-plane-label',lambda c:c['records'][i2]['leaves'][leaf].__setitem__('positive_residual',True))
    damaged('unknown-leaf-field',lambda c:c['records'][i2]['leaves'][leaf].__setitem__('sample_only',True))
    c=deepcopy(original);target=c['records'][i2]['leaves'][leaf]
    target['positive_residual'],target['negative_residual']=target['negative_residual'],target['positive_residual'];validate(c)
    prefix='-'.join(map(str,c['records'][i2]['triple']))+':'+''.join(map(str,target['path']))+':positive_residual:'
    for name,p,a,b in obligations(c):
        if name.startswith(prefix):reject(lambda:require(min(rational_bernstein(p,a,b))>0,'swapped residual orientation'));break
    else:raise ValueError('corrupted arithmetic obligation was not located')
    t=P.var(0);Y,O,_=make(t);bad=list(Y[7]);bad[0]+=O
    require(bool((dot(bad,bad,t)-O*O).c),'damaged core coordinate detected')
    # The polynomial library accepts integers only; clear the rational lo.
    zero_endpoint=25*t-14
    reject(lambda:require(min(rational_bernstein(zero_endpoint,LO,HI))>0,'closed endpoint zero'))
    reject(lambda:taylor_positive(zero_endpoint,LO,HI,max_depth=3))
    good=deepcopy(original);good['records'].reverse();validate(good)
    good=deepcopy(original)
    for r in good['records']:
        if 'leaves'in r:r['leaves'].reverse()
    validate(good)
    for p in (P.cv(1),1+t):
        require(min(rational_bernstein(p,LO,HI))>0,'valid positivity control');taylor_positive(p,LO,HI)
    return {'format':'g21-two-cap-controls-v1','actual_agent':'six-tammes-2','role':'researcher',
            'damaged_scope_and_cover_rejections':len(damages),'damage_names':damages,
            'swapped_arithmetic_orientation_rejected':True,'corrupted_core_coordinate_detected':True,
            'closed_endpoint_zero_rejected_by_both_sign_methods':True,
            'valid_schema_representations':3,'valid_positive_polynomial_controls':2,
            'new_independent_review_claimed':False}

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second controls guard')));signal.alarm(50)
    print(json.dumps(run(),sort_keys=True,indent=2))
if __name__=='__main__':main()
