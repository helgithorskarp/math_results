"""PRIVATE eight semantic inverse-certificate rejection controls."""
import os
for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[v] = '1'
from pathlib import Path
import sys, json, signal, time, resource, copy, tempfile, subprocess
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact import require


def add_polynomial(record, additions):
    denominator = record['denominator']
    terms = {tuple(k):int(z) for k,z in record['terms']}
    for k,z in additions.items():
        terms[k] = terms.get(k,0) + denominator*z
        if not terms[k]:
            del terms[k]
    record['terms'] = [[list(k),str(z)] for k,z in sorted(terms.items())]


def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')), 'operational barrier')
    def alarm(a,b):
        raise TimeoutError('unchanged60s eight semantic rejection controls guard')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(60); started=time.monotonic()
    directory=Path(__file__).resolve().parent
    original=json.loads((directory/'INVERSE.json').read_text())
    cases=[]
    def mutate(name, action):
        data=copy.deepcopy(original); action(data); cases.append((name,data))
    mutate('wrong physical domain',lambda d:d.update(domain='q>=2,h>=2'))
    mutate('missing original inverse-energy B',lambda d:d['scalars'].pop('B'))
    mutate('missing standard coefficient row',lambda d:d['standard_solution'].pop())
    mutate('missing trace coefficient',lambda d:d['trace_solution'].pop())
    mutate('wrong inverse coefficient',lambda d:add_polynomial(d['standard_solution'][0][0]['numerator'],{(0,0):1}))
    # This vanishes on every h=2 node AND every q=4 node; complete Cartesian
    # identity coverage must reach an interior point to reject it.
    mutate('wrong energy agreeing on both boundary lines',lambda d:add_polynomial(d['scalars']['A']['numerator'],{(1,1):1,(1,0):-4,(0,1):-2,(0,0):8}))
    mutate('wrong positive denominator power',lambda d:d['trace_solution'][1][0]['denominator_factors'][0].update(power=d['trace_solution'][1][0]['denominator_factors'][0]['power']+1))
    def negate_factor(d):
        factor=d['standard_solution'][0][0]['denominator_factors'][0]['factor']
        factor['terms']=[[k,str(-int(z))] for k,z in factor['terms']]
    mutate('negative denominator on full domain',negate_factor)
    results=[]
    with tempfile.TemporaryDirectory(prefix='inverse-damages-',dir=directory/'work') as temporary:
        temp=Path(temporary)
        for i,(name,data) in enumerate(cases):
            target=temp/f'damage{i}.json'; target.write_text(json.dumps(data,sort_keys=True)+'\n')
            command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(directory/'check_inverse.py'),str(target),'--output',str(temp/f'out{i}.json')]
            p=subprocess.run(command,text=True,capture_output=True,timeout=65)
            require(p.returncode==1 and 'ValueError:' in p.stderr and 'TimeoutError' not in p.stderr and 'MemoryError' not in p.stderr,
                    'semantic ValueError rejection required; timeout/kill/incomplete is not rejection: '+name)
            results.append(dict(name=name,rejected=True,exception='ValueError'))
    signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',complete=True,semantic_cases=results,
             timeouts_are_not_rejections=True,seconds=time.monotonic()-started,
             peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (directory/'work'/f'damages-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':
    main()
