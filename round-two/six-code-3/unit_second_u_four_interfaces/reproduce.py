"""Cold serial complete carrier and color replay against frozen records."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

def need(test, message):
    if not test:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    here = Path(__file__).absolute().parent
    work = Path(args.work).absolute(); work.mkdir(parents=True, exist_ok=True)
    need(not any(work.iterdir()), 'cold work directory must be empty')
    need(all((here/name).is_file() for name in ('expected.json', 'BRIDGE.json', 'certificates.json')),
         'pre-existing frozen evidence required')
    expected = json.loads((here/'expected.json').read_text())
    bridge_raw = (here/'BRIDGE.json').read_bytes()
    certificate_raw = (here/'certificates.json').read_bytes()
    need(hashlib.sha256(bridge_raw).hexdigest() == expected['bridge_sha256'], 'frozen bridge differs')
    need(hashlib.sha256(certificate_raw).hexdigest() == expected['certificate_sha256'], 'frozen colors differ')
    bridge = json.loads(bridge_raw)
    environment = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        environment[name] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    python = [sys.executable]+(['-O'] if sys.flags.optimize else [])
    receipts = []; start = time.monotonic()
    source_hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in here.iterdir() if p.is_file()}
    def run(label, arguments):
        for flag in ('PAUSED', 'PAUSED.json'):
            need(not Path('/scratch/research-team-sol61-six-20260929/state', flag).exists(),
                 'INCOMPLETE standing campaign pause barrier')
        command = python+[str(here/arguments[0])]+[str(a) for a in arguments[1:]]
        began = time.monotonic()
        result = subprocess.run(command, env=environment, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, timeout=60)
        (work/(label+'.stdout')).write_text(result.stdout)
        (work/(label+'.stderr')).write_text(result.stderr)
        receipt = dict(label=label, command=command, exit_code=result.returncode,
                       seconds=time.monotonic()-began)
        receipts.append(receipt)
        (work/'receipts.json').write_text(json.dumps(receipts, indent=2, sort_keys=True)+'\n')
        need(result.returncode == 0, 'INCOMPLETE failed stage '+label)
        print(json.dumps(dict(stage=label, seconds=receipt['seconds'])), flush=True)
        return result.stdout
    total = expected['products']
    chunks = []
    for first in range(0, total, 30):
        finish = min(first+30, total)
        run(f'primary-{first:03d}', ['produce.py', '--fixtures', here/'fixtures.json', '--work', work/'primary',
                                    '--first', first, '--finish', finish])
        output = work/f'point-dfs-{first:03d}.json'
        run(f'point-dfs-{first:03d}', ['verify.py', '--fixtures', here/'fixtures.json', '--primary-work', work/'primary',
            '--output', output, '--first', first, '--finish', finish])
        chunk = json.loads(output.read_text())
        need(chunk['status'] == 'COMPLETE_SELECTED_PRODUCTS_ONLY' and
             chunk['first'] == first and chunk['finish'] == finish and chunk['total_products'] == total and
             len(chunk['records']) == finish-first, 'independent chunk incomplete')
        chunks.append(chunk)
    need({p.name for p in (work/'primary').glob('product-*.json')} ==
         {f'product-{i:03d}.json' for i in range(total)}, 'whole primary product population gap')
    records = [r for chunk in chunks for r in chunk['records']]
    need([r['product_index'] for r in records] == list(range(total)), 'independent whole-domain coverage gap')
    need({c['domain_sha256'] for c in chunks} == {expected['domain_sha256']}, 'independent chunk domains differ')
    records_sha = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    checked = dict(status='COMPLETE_INDEPENDENT_POINT_DFS_BATCHED', first=0, finish=total,
        total_products=total, domain_sha256=expected['domain_sha256'], records_sha256=records_sha, records=records)
    (work/'point-dfs.json').write_text(json.dumps(checked, sort_keys=True, indent=2)+'\n')
    need(checked['records_sha256'] == expected['checker_records_sha256'] and
         checked['domain_sha256'] == expected['domain_sha256'], 'complete frozen carrier differs')
    actual = [dict(product_index=row['product_index'], first=row['first'], second=row['second'], **p)
              for row in checked['records'] for p in row['positives']]
    need(actual == bridge['raw_positive_maps'], 'actual full positive arrays differ')
    counts = dict(products=len(checked['records']), positive_maps=len(actual),
                  positive_products=sum(bool(r['positives']) for r in checked['records']),
                  distinct_word_unions=len({tuple(p['word_masks']) for p in actual}),
                  represented_full_maps=sum(r['represented_full_maps'] for r in checked['records']),
                  explicit_full_maps=sum(r['full_maps_tested'] for r in checked['records']),
                  dfs_states=sum(r['dfs_states'] for r in checked['records']),
                  maximum_states=max(r['dfs_states'] for r in checked['records']),
                  positive_source_uv_uncovered=sum(sum(
                      (w & sum(1 << q for q in p['first'][1][:2])) == sum(1 << q for q in p['first'][1][:2])
                      for w in p['word_masks']) == 1 for p in actual))
    need(all(value == expected[key] for key, value in counts.items()), 'complete carrier counts differ')
    run('generate-colors', ['generate_colors.py', '--bridge', here/'BRIDGE.json',
                           '--output', work/'regenerated-certificates.json'])
    need((work/'regenerated-certificates.json').read_bytes() == certificate_raw,
         'whole regenerated color bytes differ')
    colors = json.loads(run('check-colors', ['check_colors.py', '--fixtures', here/'fixtures.json',
                                            '--bridge', here/'BRIDGE.json', '--certificate', here/'certificates.json']))
    need(colors == expected['color_check'], 'every literal color record differs')
    controls = json.loads(run('controls', ['controls.py', '--primary-work', work/'primary', '--work', work/'controls']))
    need(controls == expected['controls'], 'semantic/transport control records differ')
    stable = dict(status='COMPLETE_UNIT_SECOND_U_FOUR_LOCAL_UPPER62',
                  expected_frozen_before_replay=True, bridge_sha256=expected['bridge_sha256'],
                  certificate_sha256=expected['certificate_sha256'],
                  domain_sha256=checked['domain_sha256'], checker_records_sha256=checked['records_sha256'],
                  carrier=counts, color_check=colors, controls=controls,
                  scope='Isolated deficient first u and unit second y row with yu4/yv4 or5. Full356-product carrier retains all source u-v leave cases. No global profile, forced selector or code symmetry.')
    (work/'RESULT.json').write_text(json.dumps(stable, indent=2, sort_keys=True)+'\n')
    metadata = dict(agent='six-code-3', role='researcher', python=sys.version,
                    optimized=bool(sys.flags.optimize), finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    seconds=time.monotonic()-start, peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                    threads=1, scope='Unchanged1CPU2GiB;one CPU-intensive job at a time',
                    guards='10s/product;200000 point-DFS states/product;5s/color product;64 priority trials;60s/subprocess',
                    source_sha256=source_hashes, receipts=receipts)
    (work/'METADATA.json').write_text(json.dumps(metadata, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status=stable['status'], products=counts['products'],
                         interfaces=counts['positive_maps'], upper_bound=colors['maximum_upper_bound'],
                         seconds=metadata['seconds'], peak_child_rss_kib=metadata['peak_child_rss_kib'])), flush=True)

if __name__ == '__main__':
    main()
