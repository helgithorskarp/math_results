"""Serial complete offline review check; freeze only a first completed record."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import audit
import controls
import ordinary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    work = Path(args.work).resolve()
    audit.require(work != audit.HERE and audit.HERE not in work.parents, 'outputs must stay outside source')
    work.mkdir(parents=True, exist_ok=True)
    for row in json.loads((audit.HERE/'INPUTS.json').read_text()):
        audit.require(hashlib.sha256((audit.HERE/row['path']).read_bytes()).hexdigest() == row['sha256'], 'changed input '+row['path'])
    start = time.monotonic()
    record = audit.audit(work)
    record.update(ordinary=ordinary.check(), controls=controls.check())
    record = json.loads(json.dumps(record, sort_keys=True))
    audit.require(record == json.loads((audit.HERE/'EXPECTED.json').read_text()), 'whole frozen mathematical record differs')
    (work/'result.json').write_text(json.dumps(record, sort_keys=True)+'\n')
    receipt = {'status': 'PASS_COLD_THREE_HUB_REVIEW', 'expected_sha256': audit.digest(record),
               'main_survivors': record['main_survivors'], 'coarse_rows': len(record['coarse_rows']),
               'refined_rows': len(record['refined_rows']), 'author_budget_valid': 164,
               'seconds': time.monotonic()-start,
               'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (work/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
