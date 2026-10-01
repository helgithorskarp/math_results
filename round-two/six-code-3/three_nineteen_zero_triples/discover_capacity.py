"""Optional floating discovery; the resulting integer certificate is exact."""
import argparse
import hashlib
from itertools import combinations
import json
import math
import os
from pathlib import Path
import time

for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[name]='1'
import highspy
import numpy as np

HERE=Path(__file__).resolve().parent


def encode(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()


def certificate(core):
    fixed=core['blocks']
    forbidden=set()
    for w in fixed:
        old=[i for i in range(15) if w & (1 << i)]
        forbidden.update(combinations(old,3))
    candidates=[q for q in combinations(range(15),5)
                if all(t not in forbidden for t in combinations(q,3))]
    rows=[t for t in combinations(range(15),3) if t not in forbidden]
    index={t:i for i,t in enumerate(rows)}
    columns=[[index[t] for t in combinations(q,3)] for q in candidates]
    h=highspy.Highs()
    for key,value in [('threads',1),('parallel','off'),('time_limit',20.0),
                       ('output_flag',False),('solver','simplex')]:
        if h.setOptionValue(key,value)!=highspy.HighsStatus.kOk:
            raise ValueError('solver rejected fixed option '+key)
    lp=highspy.HighsLp();lp.num_col_=len(columns);lp.num_row_=len(rows)
    lp.col_cost_=np.ones(len(columns));lp.col_lower_=np.zeros(len(columns))
    lp.col_upper_=np.full(len(columns),highspy.kHighsInf)
    lp.row_lower_=np.full(len(rows),-highspy.kHighsInf);lp.row_upper_=np.ones(len(rows))
    lp.sense_=highspy.ObjSense.kMaximize;lp.a_matrix_.format_=highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_=np.array([10*i for i in range(len(columns)+1)])
    lp.a_matrix_.index_=np.array([i for c in columns for i in c])
    lp.a_matrix_.value_=np.ones(10*len(columns))
    if h.passModel(lp)!=highspy.HighsStatus.kOk:
        raise ValueError('solver rejected model')
    h.run();solution=h.getSolution()
    if h.getModelStatus()!=highspy.HighsModelStatus.kOptimal or not solution.dual_valid:
        raise RuntimeError('INCOMPLETE numerical discovery, no mathematical conclusion')
    scale=1000
    dual=[math.ceil(max(0,v)*scale) for v in solution.row_dual]
    # This exact check, rather than the numerical status, proves the inequality.
    if any(sum(dual[i] for i in c)<scale for c in columns):
        raise ValueError('rounded integer weights do not cover every candidate')
    total=sum(dual)
    if total//scale>28:
        raise RuntimeError('NO_EXCLUSION: exact capacity is not below twenty-nine')
    return {'core_sha256':core['core_sha256'],'candidate_count':len(candidates),
            'candidate_sha256':hashlib.sha256(encode(candidates)).hexdigest(),
            'denominator':scale,'numerator':total,
            'weights':[[*t,d] for t,d in zip(rows,dual) if d]}


def run(work,output):
    start=time.monotonic()
    cores=[j for k in range(6) for j in json.loads((work/f'joints-{k}.json').read_text())]
    result={'format':1,'highs_version':highspy.Highs().version(),
            'trust':'INTEGER_WEIGHT_COVER; floating solver not needed for verification',
            'certificates':[]}
    for i,core in enumerate(cores):
        result['certificates'].append(certificate(core))
        if (i+1)%25==0:
            temporary=output.with_suffix('.partial.json')
            temporary.write_bytes(encode(dict(result,status='PARTIAL')))
            print(json.dumps({'through':i+1,'seconds':time.monotonic()-start}),flush=True)
    result['status']='COMPLETE'
    output.write_bytes(encode(result))
    output.with_suffix('.partial.json').unlink(missing_ok=True)
    print(json.dumps({'status':'COMPLETE','cores':len(cores),'seconds':time.monotonic()-start,
                      'maximum_additional_bound':max(c['numerator']//c['denominator'] for c in result['certificates']),
                      'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=HERE/'capacity.json')
    args=parser.parse_args()
    run(args.work,args.output)
