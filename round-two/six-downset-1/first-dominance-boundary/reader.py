"""Whole original FIRST-boundary reader with source-before-arithmetic binding.

six-downset-1/researcher. Ordinary infinite/real bridges remain in PROOF.md;
these same-author finite controls are neither formalization nor review.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
from hashlib import sha256
import importlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

HERE = Path(__file__).resolve().parent
EARLY = ('geometry.py','common.py','counts.py','original.py','compact.py',
         'count_reader.py','reader.py','adverse.py','reproduce.py',
         'PROOF.md','README.md','DEPENDENCIES.json','PROVENANCE.json')
CASES = ((4,3,2),(5,2,2),(3,2,2,2))
MAX_BYTES = 32*1024*1024
sys.dont_write_bytecode = True


def require(ok, message):
    if not ok:
        raise ValueError(message)


def barrier():
    state = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state)/n).exists() for n in
                ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')), 'operational barrier')


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()+b'\n'


def binding(raw):
    return dict(bytes=len(raw),sha256=sha256(raw).hexdigest())


def verify_sources():
    barrier()
    require(sys.version_info >= (3,11), 'CPython3.11 or newer')
    path = HERE/'SOURCE.json'
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MAX_BYTES,
            'bounded source manifest')
    pins = json.loads(path.read_bytes())
    require(type(pins['early']) is dict and set(pins['early'])==set(EARLY),
            'whole early source census')
    for name in EARLY:
        path = HERE/name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MAX_BYTES,
                'bounded source census '+name)
        require(binding(path.read_bytes())==pins['early'][name], 'source pin mismatch '+name)
    return pins


def modules():
    sys.path.insert(0,str(HERE))
    result = {name:importlib.import_module(name) for name in
              ('geometry','common','counts','original','compact','count_reader')}
    require(all(Path(module.__file__).resolve().parent==HERE for module in result.values()),
            'bound local arithmetic module origins')
    return result


def calculate():
    m = modules()
    scalar = m['counts'].calculate()
    for record, counts in zip(scalar['controls'],CASES):
        m['count_reader'].validate(record,11,list(counts))
    originals = []
    for counts in CASES:
        barrier()
        originals.append(m['original'].read(4,list(counts)))
    full = m['counts'].stringify(dict(agent='six-downset-1',role='researcher',
            status='COMPLETE PRIVATE NEW MATHEMATICAL RECORD',
            count_controls=scalar,original_controls=originals))
    return full,m['compact'].summary(full)


def fresh_output(path):
    require(not path.exists() and path.resolve()!=HERE
            and HERE not in path.resolve().parents, 'fresh output outside defining source')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--whole-out',type=Path)
    args = parser.parse_args()
    fresh_output(args.out)
    if args.whole_out:
        fresh_output(args.whole_out)
        require(args.whole_out.resolve()!=args.out.resolve(), 'distinct whole and compact outputs')
    def expire(_signal,_frame):
        raise TimeoutError('unchanged60s; incomplete is not mathematical absence')
    signal.signal(signal.SIGALRM,expire); signal.alarm(60)
    started = time.monotonic()
    pins = verify_sources()
    full,compact = calculate()
    whole,raw = encoded(full),encoded(compact)
    require(len(whole)<=MAX_BYTES and len(raw)<=MAX_BYTES, 'whole output32MiB')
    require(binding(whole)==pins['whole'], 'whole regenerated private mathematics binding')
    # EXPECTED is first read and decoded AFTER EVERY mathematical guard above.
    path = HERE/'EXPECTED.json'
    require(path.is_file() and not path.is_symlink() and path.stat().st_size<=MAX_BYTES,
            'expected boundary AFTER whole mathematics')
    expected = path.read_bytes()
    require(binding(expected)==pins['expected'], 'whole expected source binding')
    require(compact==json.loads(expected) and raw==expected,
            'ENTIRE compact mathematical fields and canonical bytes')
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_bytes(raw)
    if args.whole_out:
        args.whole_out.parent.mkdir(parents=True,exist_ok=True); args.whole_out.write_bytes(whole)
    barrier(); signal.alarm(0)
    print(json.dumps(dict(status='COMPLETE SOURCE-ONLY FIRST-DOMINANCE READER',
        compact=binding(raw),whole=binding(whole),
        source_before_arithmetic_import=True,expected_after_whole_mathematics=True,
        seconds=time.monotonic()-started,
        peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__=='__main__':
    main()
