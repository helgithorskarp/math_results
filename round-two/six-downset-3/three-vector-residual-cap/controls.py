"""semantic certificate damages; no hash-only rejections."""
from copy import deepcopy
from pathlib import Path
import json
import time
import residual
import check_coefficients as cc
from algebra import add,constant,scale


def run():
    slack=json.loads(Path(__file__).with_name('POLYNOMIAL-SLACK.json').read_text())
    pell=json.loads(Path(__file__).with_name('PELL-NORM.json').read_text())
    raw=json.loads(Path(__file__).with_name('RESIDUAL-NUMERATORS.json').read_text())
    forms={name:cc.decode(x) for name,x in slack['forms'].items()}
    rn={name:cc.decode(x) for name,x in raw.items() if name!='record_sha256'}
    accepted=[]
    def reject(name,call):
        try:call()
        except ValueError:accepted.append(name)
        else:raise ValueError('semantic damage accepted: '+name)
    bad=deepcopy(rn);bad['00']=add(bad['00'],constant(1))
    reject('changed original residual second moment',lambda:cc.physical_residual(bad,forms['d0']))
    bad=deepcopy(forms);bad['numerator']=add(bad['numerator'],constant(1))
    reject('changed cleared sufficient slack',lambda:cc.cleared_slack(bad,rn))
    bad=deepcopy(forms);bad['Q_denominator']=scale(bad['Q_denominator'],2)
    reject('changed necessary scalar normalization',lambda:cc.cleared_slack(bad,rn))
    bad=deepcopy(pell);bad['mean_numerator'][0][1]=str(-residual.F(bad['mean_numerator'][0][1]))
    reject('changed old-mean comparison sign',lambda:cc.old_mean(bad))
    original=add(forms['Q_numerator'],scale(forms['Q_denominator'],-1))
    bad=deepcopy(pell['Q_minus_one']);bad['quotient_coefficients'][0][1]=str(residual.F(bad['quotient_coefficients'][0][1])+1)
    reject('changed quotient on the Pell norm relation',lambda:cc.norm_check(original,bad))
    bad=deepcopy(pell['Q_minus_one']);bad['coefficient_sandwich'][0][1]=str(residual.F(bad['coefficient_sandwich'][0][1])+1)
    reject('changed positive sandwich coefficient',lambda:cc.norm_check(original,bad))
    result={'agent':'six-downset-3','role':'researcher','semantic_damages_rejected':accepted,
            'hash_only_rejections':0,'status':'exact controls; same author, not peer review'}
    result['record_sha256']=residual.digest(result)
    Path(__file__).with_name('CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result


if __name__=='__main__':
    start=time.perf_counter();r=run();print(json.dumps({'digest':r['record_sha256'],'seconds':time.perf_counter()-start,'semantic_damages':len(r['semantic_damages_rejected'])}))
