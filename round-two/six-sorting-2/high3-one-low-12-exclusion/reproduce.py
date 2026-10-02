"""Cold serial regeneration and every original head/tail certificate replay.

No private census or generated negative vector is read. The existing public
preparation source regenerates its full function graph. All selected actual
original domains are replayed by a distinct scalar algorithm. Child55s/native1.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

SOURCE = Path(__file__).resolve().parent
PARENT = SOURCE.parent / 'high3-one-low-preparation-cover'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def barrier():
    selected = os.environ.get('RESEARCH_OPERATIONS_STATE')
    if not selected:
        return
    root = Path(selected)
    for name in ('PAUSED', 'PAUSED.json', 'monitor/PAUSED', 'monitor/PAUSED.json'):
        need(not (root/name).exists(), 'operations pause; incomplete replay, not exclusion')
    handover = root/'monitor/HANDOVER.json'
    if handover.exists():
        need(json.loads(handover.read_text()).get('phase') == 'completed',
             'incomplete handover; stop without mathematical inference')


def run_child(args, env, log):
    barrier()
    with log.open('w') as stream:
        try:
            done = subprocess.run(args, env=env, stdout=stream,
                                  stderr=subprocess.STDOUT, timeout=55)
        except subprocess.TimeoutExpired:
            raise SystemExit('OPERATIONAL_TIMEOUT: incomplete replay, not exclusion: '+str(log))
    need(done.returncode == 0, 'child failed; incomplete replay: '+str(log))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=SOURCE/'generated')
    parser.add_argument('--record-only', action='store_true',
                        help='Author bootstrap: still run every mathematical check, then save a record before freezing checks.json')
    args = parser.parse_args()
    started = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE/'source-manifest.json').read_text())
    for name, expected in manifest['owned_sha256'].items():
        need(hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() == expected,
             'owned whole-byte pin differs: '+name)
    for name, expected in manifest['parent_sha256'].items():
        need(hashlib.sha256((PARENT/name).read_bytes()).hexdigest() == expected,
             'published preparation source pin differs: '+name)
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
               VECLIB_MAXIMUM_THREADS='1', BLIS_NUM_THREADS='1')
    python = [sys.executable, '-B']+(['-O'] if sys.flags.optimize else [])
    full_graph = args.output/'preparation.json'
    run_child(python+[str(PARENT/'generate.py'),'--output',str(full_graph)],
              env,args.output/'preparation-generate.log')
    parent_verify = args.output/'preparation-verify.json'
    run_child(python+[str(PARENT/'verify.py'),'--input',str(full_graph)],
              env,parent_verify)
    parent_record = json.loads(parent_verify.read_text())
    need(parent_record['status'] == 'WHOLE_ORIGINAL_CUBES_FULL64_FUNCTIONS_ALL_EDGES_EXITS_AND_ACTUAL_LENGTH_VERIFIED',
         'published preparation reconstruction is incomplete')
    regenerated = args.output/'regenerated-certificate.json'
    run_child(python+[str(SOURCE/'generate.py'),'--full-graph',str(full_graph),
                     '--output',str(regenerated)], env,args.output/'generate.log')
    raw = (SOURCE/'certificate.json').read_bytes()
    need(regenerated.read_bytes() == raw, 'entire regenerated negative certificate differs')
    certificate = json.loads(raw)
    whole_ids, hashes, telemetry = [], [], []
    kinds, assignments = Counter(), Counter()
    units = 0
    for offset in range(0,1129,40):
        count = min(40,1129-offset)
        output = args.output/f'verify-{offset}-{offset+count}.json'
        run_child(python+[str(SOURCE/'verify.py'),'--certificate',str(regenerated),
                         '--full-graph',str(full_graph),'--offset',str(offset),
                         '--functions',str(count),'--output',str(output)],
                  env,output.with_suffix('.log'))
        data = json.loads(output.read_text())
        result = data['mathematical_result']
        need(data['status'] == 'COMPLETE_SELECTED_INDEPENDENT_SCALAR_CHECK'
             and data['certificate_sha256'] == hashlib.sha256(raw).hexdigest(),
             'scalar slice completion/input binding differs')
        expected = certificate['state_heads'][offset:offset+count]
        ids = [s for s,heads in expected]
        bindings = [[s,h,-1 if type(refs) is int else t,
                     refs if type(refs) is int else ref]
                    for s,heads in expected for h,refs in enumerate(heads)
                    for t,ref in ([(None,refs)] if type(refs) is int else enumerate(refs))]
        need(result['completed_function_ids'] == ids
             and result['checked_bindings_sha256'] == digest(bindings)
             and result['checked_units'] == len(bindings),
             'complete entry-level scalar slice differs')
        whole_ids.extend(ids)
        hashes.append(digest(bindings))
        kinds.update(result['kind_counts'])
        assignments.update(result['original_cube_assignments'])
        units += result['checked_units']
        telemetry.append({'range':[offset,offset+count],
                          'seconds':data['seconds'],
                          'maximum_rss_kib':data['maximum_rss_kib']})
        checkpoint = {'completed_function_ids':whole_ids,'negative_units':units,
                      'complete':False,'telemetry':telemetry,
                      'scope':'Incomplete slices do not prove the whole exclusion.'}
        (args.output/'partial-check.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
        print('COMPLETE_FUNCTION_RANGE',offset,offset+count,flush=True)
    need(whole_ids == [s for s,heads in certificate['state_heads']]
         and len(whole_ids) == 1129 and units == 20322,
         'entire mathematical domain incomplete')
    controls_path = args.output/'controls.json'
    run_child(python+[str(SOURCE/'controls.py'),'--full-graph',str(full_graph)],
              env,controls_path)
    controls = json.loads(controls_path.read_text())['mathematical_result']
    need(controls['status'] == 'POSITIVE_AND_INTENDED_DAMAGE_CONTROLS_PASS',
         'controls incomplete')
    parent_math = {k:v for k,v in parent_record.items()
                   if k not in ('seconds','maximum_rss_kib')}
    math = {'all_function_ids':whole_ids,'negative_units':units,
            'kind_counts':dict(kinds),'cube_assignments':dict(assignments),
            'batch_binding_hashes':hashes,'controls':controls,
            'parent_reconstruction':parent_math}
    if not args.record_only:
        expected = json.loads((SOURCE/'checks.json').read_text())
        need(digest(math) == expected['mathematical_result_sha256'],
             'entire frozen mathematical record differs')
    record = {'agent':'six-sorting-2','role':'researcher',
              'status':'COMPLETE_ONE_PRIOR_LOW_12_HEAD_TAIL_CERTIFICATES_VERIFIED',
              'certificate_sha256':hashlib.sha256(raw).hexdigest(),
              'mathematical_result':math,'mathematical_result_sha256':digest(math),
              'telemetry':telemetry,'seconds':time.monotonic()-started,
              'python':sys.version.split()[0],'optimized':bool(sys.flags.optimize),
              'author_record_bootstrap':bool(args.record_only)}
    (args.output/'full-check.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items()
                     if k not in ('mathematical_result','telemetry')}),flush=True)


if __name__ == '__main__':
    main()
