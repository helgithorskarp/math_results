#!/usr/bin/env python3
"""Run the complete independent certificate audit into fresh external scratch."""
import argparse,json,time,resource,sys
from pathlib import Path
from hashlib import sha256
from audit import audit,compare_author
from controls import controls
from exact import require,canonical

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();source=Path(__file__).resolve().parent;work=args.work.resolve()
    require(work!=source and source not in work.parents,'scratch must be outside source')
    require(not work.exists(),'fresh scratch required');work.mkdir(parents=True)
    c=json.loads((source/'INPUT.json').read_text())
    require(c['agent']=='six-reviewer-5' and c['role']=='independent mathematical reviewer','review provenance')
    for item in c['data_pins']:
        path=source/item['file'];blob=path.read_bytes()
        require(len(blob)==item['bytes'] and sha256(blob).hexdigest()==item['sha256'],'mandatory data pin: '+item['file'])
    start=time.monotonic()
    dual=json.loads((source/'DUAL.json').read_text());original=json.loads((source/'AUTHOR_EXPECTED.json').read_text())
    result=audit(dual)
    result['author_data_comparison']=compare_author(result,original)
    result['controls']=controls(dual)
    blob=canonical(result)
    require((source/'expected.json').read_bytes()==blob,'mandatory complete expected result')
    (work/'result.json').write_bytes(blob)
    record={'agent':'six-reviewer-5','role':'independent mathematical reviewer','status':'COMPLETE','python':sys.version.split()[0],'python_optimized':bool(sys.flags.optimize),'author_executable_imported':False,'dense_full_slack_eliminations':0,'elapsed_seconds':time.monotonic()-start,'peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'result_bytes':len(blob),'result_sha256':sha256(blob).hexdigest()}
    (work/'run.json').write_bytes(canonical(record));print(json.dumps(record))

if __name__=='__main__':main()
