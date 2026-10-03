"""PRIVATE semantic rejection controls for the complete Newton checker."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json,time,signal
from newton_check import check,require

def main():
    def alarm(signum,frame):raise TimeoutError('unchanged60s Newton damage guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    base=json.loads(Path('work/newton-coefficients.json').read_text());out=[]
    for name in ['wrong_anchor','false_continuous_h_domain','missing_final_minor','wrong_positive_Newton_coefficient','false_degree','float_coefficient','negative_coefficient','missing_tail']:
        d=deepcopy(base)
        if name=='wrong_anchor':d['raw_anchor_sha256']='0'*64
        elif name=='false_continuous_h_domain':d['domain']='real h>=3, real q>=4'
        elif name=='missing_final_minor':d['rows'].pop()
        elif name=='wrong_positive_Newton_coefficient':
            d['rows'][0]['Newton_coefficients_by_q_power'][0][0]=str(F(d['rows'][0]['Newton_coefficients_by_q_power'][0][0])+1)
            d['rows'][0]['strict_constant']=d['rows'][0]['Newton_coefficients_by_q_power'][0][0]
        elif name=='false_degree':d['rows'][0]['h_degree_bound']-=1
        elif name=='float_coefficient':d['rows'][0]['Newton_coefficients_by_q_power'][0][0]='1.0'
        elif name=='negative_coefficient':d['rows'][0]['Newton_coefficients_by_q_power'][0][0]='-1'
        elif name=='missing_tail':d['rows'][0]['Newton_coefficients_by_q_power'][0].pop()
        path=Path('work/newton-damage-input.json');path.write_text(json.dumps(d,separators=(',',':'))+'\n')
        rejected=False;reason=None
        try:check(str(path))
        except (ValueError,TypeError,KeyError) as e:rejected=True;reason=str(e)
        require(rejected,'Newton semantic corruption accepted '+name);out.append(dict(name=name,rejected=True,reason=reason))
    signal.alarm(0);record=dict(agent='six-downset-1',role='researcher',status='PASS: all eight semantic Newton corruptions reject',optimized=not __debug__,controls=out)
    suffix='optimized' if not __debug__ else 'normal';Path(f'work/newton-damages-{suffix}.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='controls'}|{'rejected':len(out)}))
if __name__=='__main__':main()
