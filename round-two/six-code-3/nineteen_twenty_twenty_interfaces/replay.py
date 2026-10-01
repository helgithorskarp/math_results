"""Sequential resumable independent census, with exact interval coverage.

Cold execution is the default. --resume accepts only this runner's sealed
local records with identical source, executable and primary fingerprints.
These are local execution checkpoints, not independent mathematical proof
certificates; the default reruns every query.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
CHUNK_SIZE=15000


def check(ok,message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def fingerprint(executable):
    paths=[HERE/'verify.py',HERE/'native.py',HERE/'pivot_server.cpp',
           HERE.parent/'three_nineteen_zero_triples'/'verify.py',
           HERE.parent/'nineteen_star_classification'/'expected.json',executable]
    return {str(path.resolve()):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def record_check(record,expected,start,finish):
    check(record['status']=='COMPLETE_ENTRYWISE_CHUNK' and record['case']==expected['case'],
          'independent completion status')
    check(record['start']==start and record['finish']==finish and
          record['total_covers']==expected['covers'],'independent interval domain')
    check(record['counts']['covers']==finish-start,'independent interval cardinality')
    for key in ('header_sha256','carrier_sha256','joints_sha256'):
        check(record[key]==expected[key],'independent primary binding')
    check(type(record['max_query_nodes']) is int and 0<record['max_query_nodes']<=2000000,
          'independent query node guard')


def run(work,executable,resume=False):
    begun=time.monotonic()
    primary=json.loads((work/'summary.json').read_text())
    expected=json.loads((HERE/'expected.json').read_text())
    check(encode(primary)==encode(expected) and len(primary['cases'])==46,'complete primary manifest')
    check([c['case'] for c in primary['cases']]==list(range(46)),'independent case coverage domain')
    fp=fingerprint(executable)
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
    case_records=[]
    native_nodes=0;max_query_nodes=0
    for case in primary['cases']:
        k=case['case'];chunks=[]
        for start in range(0,case['covers'],CHUNK_SIZE):
            finish=min(start+CHUNK_SIZE,case['covers'])
            output=work/f'verified-{k}-{start}-{finish}.json'
            seal=work/f'replay-seal-{k}-{start}-{finish}.json'
            reused=False
            if resume and output.exists() and seal.exists():
                marker=json.loads(seal.read_text())
                check(marker['fingerprint']==fp and marker['primary_sha256']==sha(primary),
                      'changed dependency in resumed independent replay')
                check(marker['record_sha256']==hashlib.sha256(output.read_bytes()).hexdigest(),
                      'changed resumed independent record')
                record=json.loads(output.read_text())
                record_check(record,case,start,finish);reused=True
            else:
                command=[sys.executable,str(HERE/'verify.py'),'--work',str(work),
                         '--executable',str(executable),'--case',str(k),
                         '--start',str(start),'--size',str(CHUNK_SIZE)]
                result=subprocess.run(command,capture_output=True,text=True,env=env,timeout=70)
                (work/f'replay-{k}-{start}-{finish}.log').write_text(result.stdout+result.stderr)
                check(result.returncode==0,'INCOMPLETE independent child; no exclusion: '+result.stderr[-1200:])
                record=json.loads(output.read_text())
                record_check(record,case,start,finish)
                marker={'status':'COMPLETE_LOCAL_EXECUTION_CHECKPOINT','fingerprint':fp,
                        'primary_sha256':sha(primary),
                        'record_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
                seal.write_bytes(encode(marker))
            chunks.append(record)
            native_nodes+=record['native_nodes'];max_query_nodes=max(max_query_nodes,record['max_query_nodes'])
            progress={'status':'INDEPENDENT_REPLAY_IN_PROGRESS','complete_cases':len(case_records),
                      'current_case':k,'verified_through':finish,'current_case_covers':case['covers'],
                      'primary_sha256':sha(primary),'fingerprint':fp,'native_nodes':native_nodes,
                      'maximum_query_nodes':max_query_nodes,'seconds':time.monotonic()-begun,
                      'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
            (work/'independent-progress.json').write_bytes(encode(progress))
            print(json.dumps({'case':k,'start':start,'finish':finish,'cores':record['joint_count'],
                              'seconds':record['seconds'],'reused':reused}),flush=True)
        check(chunks[0]['start']==0 and chunks[-1]['finish']==case['covers'] and
              all(a['finish']==b['start'] for a,b in zip(chunks,chunks[1:])),
              'missing or overlapping independent interval')
        counts=sum((Counter(c['counts']) for c in chunks),Counter())
        for key in ('covers','y_eleven','z_eleven'):
            check(counts[key]==case['counts'].get(key,0),'full independent count mismatch')
        check(sum(c['joint_count'] for c in chunks)==case['joint_count'],'full independent core count')
        profiles=sum((Counter(c['y_profiles']) for c in chunks),Counter())
        case_record={'case':k,'counts':dict(counts),'cores':case['joint_count'],
                     'native_nodes':sum(c['native_nodes'] for c in chunks),
                     'max_query_nodes':max(c['max_query_nodes'] for c in chunks),
                     'y_profiles':dict(sorted(profiles.items())),
                     'intervals':[[c['start'],c['finish']] for c in chunks],
                     'chunk_record_sha256':[sha(c) for c in chunks],
                     'header_sha256':case['header_sha256'],'carrier_sha256':case['carrier_sha256'],
                     'joints_sha256':case['joints_sha256']}
        case_records.append(case_record)
        (work/f'independent-case-{k}.json').write_bytes(encode(case_record))
        print(json.dumps({'status':'COMPLETE_INDEPENDENT_CASE','case':k,'cores':case['joint_count'],
                          'counts':dict(counts)}),flush=True)
    check(len(case_records)==46,'incomplete independent case domain')
    result={'status':'COMPLETE_ENTRYWISE_ALL_CASES','cases':case_records,
            'primary_sha256':sha(primary),'fingerprint':fp,'native_nodes':native_nodes,
            'maximum_query_nodes':max_query_nodes,'seconds':time.monotonic()-begun,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'total_counts':dict(sum((Counter(c['counts']) for c in case_records),Counter())),
            'cores':sum(c['cores'] for c in case_records)}
    (work/'independent-complete.json').write_bytes(encode(result))
    print(json.dumps({k:value for k,value in result.items() if k not in ('cases','fingerprint')}),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--executable',type=Path,required=True)
    ap.add_argument('--resume',action='store_true')
    args=ap.parse_args()
    run(args.work.resolve(),args.executable.resolve(),args.resume)
