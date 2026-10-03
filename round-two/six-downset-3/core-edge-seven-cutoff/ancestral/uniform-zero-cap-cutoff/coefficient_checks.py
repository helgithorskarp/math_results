"""Bounded exact phases; controls and degree-bounded proofs are separated."""
from pathlib import Path
from fractions import Fraction as F
import copy
import json
import coefficient as c
import portable_zero as z
import recovery as v
r,require=c.r,c.require


def coefficients():
    cases = [(q,k,kap) for q,k in ((9,3),(12,4),(21,6),(21,7),(24,8))
             for kap in (F(0),F(1,4096),F(1,8))]
    cases += [(q,k,kap) for q,k in ((4,1),(4,4),(9,1),(9,9),(12,2),(12,12))
              for kap in (F(0),F(1,8))]
    rows=[]
    for q,k,kap in cases:
        a,record=c.separated(q,k,kap)
        require(c.direct(q,k,kap)==a,'whole direct lower shorting equals count separation')
        if kap==0:
            closed,nu,tau=v.zero_coefficients(q,k)
            require(closed==a and nu==record['nu'] and tau==record['tau'],
                    'both independently derived closed zero coefficients')
        rows.append(record)
    monotonic=[]
    for q,kap in ((4,F(0)),(9,F(1,8)),(12,F(1,4096))):
        values=[c.separated(q,k,kap)[0] for k in range(1,q+1)]
        require(all(values[j]<values[j+1] for j in range(q-1)),
                'all deletion counts in each complete monotonic control')
        monotonic.append({'q':q,'kappa':kap,'all_k_values':values})
    return {'actual_agent':'six-downset-3','role':'researcher','complete_control_count':len(cases),
            'controls_not_unbounded_proof':rows,'all_count_monotonic_controls':monotonic,
            'original_boundary_deleted_complement_zero_covered':True,
            'all_general_real_kappa_bridges_ordinary_unformalized':True}


def damages():
    rows=[]
    def reject(name,fn):
        try:
            fn()
        except ValueError as exc:
            rows.append({'name':name,'rejected':True,'stated_reason':str(exc)})
            return
        raise ValueError('Semantic damage accepted: '+name)
    certificate=json.loads(Path(__file__).with_name('CLOSED-ZERO.json').read_text())
    changed=copy.deepcopy(certificate)
    changed['rows'][0]['numerator'][0]=str(F(changed['rows'][0]['numerator'][0])+1)
    reject('changed complete nu0 constant coefficient',lambda:z.verify(changed))
    changed=copy.deepcopy(certificate)
    changed['rows'][1]['denominator'][1]=str(F(changed['rows'][1]['denominator'][1])-1)
    reject('changed complete tau0 denominator coefficient',lambda:z.verify(changed))
    changed=copy.deepcopy(certificate);changed['rows'].pop()
    reject('omitted entire second coefficient target',lambda:z.verify(changed))
    reject('floating-point kappa',lambda:c.separated(9,3,0.125))
    reject('boolean deletion count',lambda:c.separated(9,True,F(0)))
    reject('kappa outside credited interval',lambda:c.separated(9,3,F(1,4)))
    reject('out-of-quadrant positive recovery',lambda:v.canonical(20,7))
    reject('k2 is outside proved uniform untouched regime',lambda:v.canonical(9,2))
    reject('failed canonical q27k7 repair is insufficient',lambda:v.canonical(27,7))
    reject('zero kappa cannot enter positive coupled rank bridge',lambda:r.reduced(28,7,F(0)))
    D,value=v.canonical(28,7)
    C0,U0=r.evaluate(D,F(0),value['t'],value['sigma'])
    reject('false greatest lower rank at zero',lambda:require(r.schur_psd(C0)==22,'extra original zeta kernel'))
    reject('false whole weighted cap floor',lambda:r.schur_psd(
        [[U0[i][j]-D['N']*D['sizes'][i]*int(i==j) for j in range(23)] for i in range(23)]))
    require(v.dyadic_floor(F(3,17))==F(1,8) and v.dyadic_floor(F(1,16))==F(1,16),
            'valid compact exact dyadic boundary controls')
    return {'actual_agent':'six-downset-3','role':'researcher','semantic_rejections':rows,
            'count':len(rows),'valid_exact_boundary_controls':True,
            'canonical_failure_does_not_imply_face_nonexistence':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=('portable','coefficients','recovery28','recovery100','damage'))
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    if args.phase=='portable':value=z.verify()
    elif args.phase=='coefficients':value=coefficients()
    elif args.phase=='damage':value=damages()
    else:value=v.verify_positive(*((28,7) if args.phase=='recovery28' else (100,20)))
    args.out.write_text(json.dumps(r.encode(value),indent=2,sort_keys=True)+'\n')
    print(args.phase+' COMPLETE')
