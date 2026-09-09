"""Fresh deterministic reproduction from the pinned h4149 run directory."""
import argparse
import json
from pathlib import Path
import time

import audit_queue
import bridge
import controls
import independent_check
import run_queue


def main(directory, output):
    start=time.monotonic();out=Path(output);out.mkdir(exist_ok=False)
    bridge.check_parent()
    cert=bridge.produce(directory)
    raw=json.dumps(cert,separators=(',',':'))+'\n'
    (out/'branch-certificate.json').write_text(raw)
    published=bridge.HERE/'branch-certificate.json'
    if published.exists() and published.read_text()!=raw:
        raise ValueError('Fresh normalization proof differs')
    results=dict(theorem=bridge.verify(directory,cert),
                 independent_proof=independent_check.check(directory,cert),
                 controls=controls.run(directory,cert))
    results['queue']=run_queue.execute(directory,cert,out/'run')
    results['independent_queue']=audit_queue.audit(directory,out/'run')
    results['original_requests']=[bridge.request(directory,cert,out/'run/q8r8-dispatch.records',
        f'bo1-q8-r8-c{c:06d}') for c in (0,273178,546355)]
    results['overall_original_task_gate']='UNKNOWN: no original task excluded and no target solve invoked'
    results['seconds']=time.monotonic()-start
    (out/'REPLAY.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k!='original_requests'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('output')
    a=p.parse_args();main(a.directory,a.output)
