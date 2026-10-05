"""Self-contained exact original upper/FIRST reader, before expected data.

six-downset-1 / researcher. Source binding is an integrity boundary;
this same-author calculation is not independent review or formal proof.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
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
EARLY = ('geometry.py','upper_reader.py','shift_reader.py','symbolic.py',
         'reader.py','adverse.py','reproduce.py','PROOF.md','README.md',
         'DEPENDENCIES.json','PROVENANCE.json')
CASES = (('asymmetric',[4,3,2]),('minimum-light',[5,2,2]),('four-baseline',[3,2,2,2]))
MAX_BYTES = 32 * 1024 * 1024
sys.dont_write_bytecode = True


def require(ok, message):
    if not ok:
        raise ValueError(message)


def barrier():
    state = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state) / name).exists() for name in
                ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')), 'operational barrier')


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode() + b'\n'


def bind(raw):
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest())


def verify_sources():
    barrier()
    path = HERE / 'SOURCE.json'
    require(path.is_file() and path.stat().st_size <= MAX_BYTES, 'source pin manifest')
    pins = json.loads(path.read_bytes())
    require(set(pins['early']) == set(EARLY), 'whole early source census')
    for name in EARLY:
        path = HERE / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size <= MAX_BYTES,
                'source file census ' + name)
        require(bind(path.read_bytes()) == pins['early'][name], 'source pin mismatch ' + name)
    return pins


def modules():
    # All arithmetic source bytes have been checked before this function.
    sys.path.insert(0, str(HERE))
    result = [importlib.import_module(name) for name in
              ('geometry','upper_reader','shift_reader','symbolic')]
    require(all(Path(module.__file__).resolve().parent == HERE for module in result),
            'bound source-only module origins')
    return result


def calculate():
    geometry, upper, shift, symbolic = modules()
    records = []
    for name, counts in CASES:
        barrier()
        data = geometry.build(4, counts)  # Both readers also preflight before arrays.
        raw_input = json.dumps(data, separators=(',', ':')).encode() + b'\n'
        require(len(raw_input) <= MAX_BYTES, 'whole regenerated original input size')
        upper_result = upper.read(data)
        shift_result = shift.read(data)
        records.append(dict(name=name, n=4, counts=counts, input_binding=bind(raw_input),
                            upper=upper_result, shift=shift_result))
    return dict(agent='six-downset-1', role='researcher',
                status='COMPLETE SOURCE-ONLY ORIGINAL UPPER/FIRST MATHEMATICS',
                controls=records, generic_symbolic_mathematics=symbolic.calculate())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'unique reader output')
    def expire(_signal, _frame):
        raise TimeoutError('unchanged60s; incomplete work is not mathematical absence')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    started = time.monotonic()
    pins = verify_sources()
    mathematics = calculate()
    raw = encoded(mathematics)
    require(len(raw) <= MAX_BYTES, 'whole mathematical output32MiB')
    # EXPECTED is first read/decoded only after every original identity and
    # generic symbolic calculation has completed.
    expected_path = HERE / 'EXPECTED.json'
    require(expected_path.is_file() and expected_path.stat().st_size <= MAX_BYTES,
            'expected file boundary AFTER complete mathematics')
    expected = expected_path.read_bytes()
    require(bind(expected) == pins['expected'], 'whole expected source binding')
    require(mathematics == json.loads(expected) and raw == expected,
            'ENTIRE mathematical fields and bytes, before overall digest')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(raw)
    barrier()
    signal.alarm(0)
    print(json.dumps(dict(status='SOURCE-ONLY ORIGINAL/FIRST READER COMPLETE',
                         mathematical_bytes=len(raw), mathematical_sha256=sha256(raw).hexdigest(),
                         source_before_arithmetic_import=True,expected_read_after_complete_mathematics=True,
                         seconds=time.monotonic()-started,
                         peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == '__main__':
    main()
