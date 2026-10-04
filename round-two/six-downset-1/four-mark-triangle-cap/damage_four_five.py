"""Semantic defects of fresh FOUR-mark all-q data must be rejected.

Six defect algorithms credited to public source4dd74e66/damage_three_five.
The declared complete four-mark polynomial data and reader are different.
"""
from pathlib import Path
import copy, json, signal, time, resource
from check_four_five import check

def damages(data):
    out = []
    def case(name, mutate):
        x = copy.deepcopy(data); mutate(x)
        try: check(x)
        except ValueError as error:
            out.append(dict(name=name,rejected=True,reason=str(error))); return
        raise ValueError('mathematical damaged certificate accepted: '+name)
    case('omit retained light-mean direction', lambda x:
         x['forms'].__setitem__('four-even-five-allq',
             [r[:4] for r in x['forms']['four-even-five-allq'][:4]]))
    def common(x):
        i = x['forms']['four-even-five-allq'][4][4]
        p = x['polynomials'][x['fields'][i]['numerator']]
        p['terms'][0][1] = str(int(p['terms'][0][1])+1)
    case('change actual aggregate/common pairing', common)
    case('use a different first pivot', lambda x:
         x['rows'][0].__setitem__('pivot',x['rows'][1]['pivot']))
    case('omit final local Schur identity', lambda x:x['updates'].pop())
    case('change an actual Schur left field', lambda x:
         x['updates'][0].__setitem__('left',x['updates'][0]['right']))
    case('replace final Schur result by old value', lambda x:
         x['updates'][-1].__setitem__('after',x['updates'][-1]['before']))
    return out

if __name__ == '__main__':
    def alarm(a,b): raise TimeoutError('unchanged60s damage-control guard')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(60)
    start = time.monotonic(); folder = Path(__file__).resolve().parent
    results = damages(json.loads((folder/'FOUR-EVEN-FIVE-ALLQ-CERTIFICATE.json').read_text()))
    output = dict(agent='six-downset-1',role='researcher',private=True,
                  all_rejected=True,cases=results)
    (folder/'FOUR-FIVE-DAMAGES.json').write_text(json.dumps(output,indent=2)+'\n')
    output['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    signal.alarm(0); print(json.dumps(output),flush=True)
