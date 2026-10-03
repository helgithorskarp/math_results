"""PRIVATE bounded coefficient certificate for complete compact solves."""
import os
for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[v] = '1'
from pathlib import Path
import sys, json, signal, time, resource, traceback
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bivariate import P, R, ATOMS, PROBES, DEN_CACHE, atom
from clearing import encode, shift
from energies import energies, require


def coded(z):
    z = R(z)
    return dict(numerator=encode(z.num), denominator_factors=[dict(factor=encode(ATOMS[k]), power=e) for k, e in sorted(z.den.items())])


def main():
    state = Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state / n).exists() for n in ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')), 'operational barrier')
    def alarm(a, b):
        raise TimeoutError('unchanged60s one compact symbolic solve guard')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(60)
    started = time.monotonic()
    ATOMS.clear(); PROBES.clear(); DEN_CACHE.clear()
    result = dict(agent='six-downset-1', role='researcher', status='INCOMPLETE', phase='initialize')
    recorded = []
    try:
        h = R(P({(1, 0): 1})); q = R(P({(0, 1): 1}))
        for z in (h, h - 1, 6 * h + 1, q + 3 * h, 2 * h - 1, q, q - 1, q - 2):
            atom(z.num)
        def register(z):
            z = R(z)
            require(shift(z.num).positive(), 'new compact pivot numerator sign')
            require(all(shift(ATOMS[k]).positive() for k in z.den), 'new compact pivot denominator signs')
            atom(z.num)
            recorded.append(coded(z))
            result['phase'] = 'compact pivot ' + str(len(recorded))
            print(json.dumps(dict(pivot=len(recorded), degree=z.num.degree(), terms=len(z.num.a))), flush=True)
        e = energies(q, h, register)
        result['phase'] = 'serialize complete inverse energies'
        result['certificate'] = dict(
            domain='q>=4,h>=2 auxiliary; physical integerh>=2,q=2^(n-1),integern>=3',
            standard_solution=[[coded(z) for z in row] for row in e['standard_solution']],
            trace_solution=[[coded(z) for z in row] for row in e['trace_solution']],
            pivots=recorded,
            scalars={name:coded(e[name]) for name in ('Eu', 'Ev', 'Et', 'mean', 'A', 'B', 'D', 'kappa')})
        require(len(recorded) == 6, 'all four standard and two trace pivots')
        result['status'] = 'ALL compact solve coefficients and eight energies exact; independent reconstruction outstanding'
        result['phase'] = 'complete compact energies; uniform endpoint ordering not attempted'
    except (ValueError, TimeoutError) as exc:
        result['status'] = 'STOPPED: ' + str(exc)
        result['traceback'] = traceback.format_exc()
        result['completed_pivots'] = recorded
    finally:
        signal.alarm(0)
        result.update(seconds=time.monotonic()-started, peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      optimized=sys.flags.optimize, guards=dict(child_seconds=60, polynomial_terms=512,
                      packing_bytes=33554432, native_threads=1, serial_math_child=1))
        (Path(__file__).resolve().parent / 'work' / f'symbolic-O{sys.flags.optimize}.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('certificate', 'completed_pivots')}), flush=True)


if __name__ == '__main__':
    main()
