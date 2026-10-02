"""Serial reproducibility runner; no solver or private input."""
import hashlib,json,os
from pathlib import Path
import subprocess,sys,time

import deps

HERE=Path(__file__).absolute().parent

def require(v,m):
    if not v:raise ValueError(m)

def main():
    started=time.monotonic();expected=json.loads((HERE/'expected.json').read_text())
    for path,digest in expected['source_hashes'].items():
        require(hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest,'Changed owned source '+path)
    for path,digest in expected['dependency_hashes'].items():
        require(hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest,'Changed published dependency '+path)
    env=os.environ.copy()
    for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
    jobs=[]
    for optimized in [False,True]:
        for script in ['strip_contact_rectangles.py','strip_notch_intervals.py','strip_local_pair_certificate.py','strip_contact_reader.py']:
            if deps.paused():raise RuntimeError('Operational pause barrier; verification unfinished')
            command=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/script)]
            r=subprocess.run(command,cwd=HERE,env=env,text=True,capture_output=True,timeout=47)
            require(r.returncode==0,'Child incomplete or failed: '+script+'\n'+r.stderr)
            result=json.loads(r.stdout);jobs.append({'script':script,'optimized':optimized,'complete':r.returncode==0})
            if script=='strip_contact_reader.py':require(result['complete'],'Reader incomplete')
    data=HERE/'strip-contact-domain'
    checks={
       'produced':['partition','classes','samples'],
       'notch-intervals':['notch_partition','notch_classes','side_partition','side_classes','samples'],
       'local-angle':['fixed','points','supplier_records','atlas','partition','samples','universal','proof','individual','complete'],
       'verified':['complete','evidence','evidence_sha256']}
    for prefix,keys in checks.items():
        a=json.loads((data/f'{prefix}-normal.json').read_text());b=json.loads((data/f'{prefix}-optimized.json').read_text())
        require({k:a[k] for k in keys}=={k:b[k] for k in keys},'Normal/optimized mathematics differs: '+prefix)
    reader=json.loads((data/'verified-normal.json').read_text())
    require(reader['evidence_sha256']==expected['evidence_sha256'] and reader['evidence']==expected['evidence'],
            'Expected evidence differs')
    print(json.dumps({'agent':'six-heesch-2','role':'researcher','complete':True,'serial_jobs':len(jobs),
                     'normal_optimized_agree':True,'evidence_sha256':reader['evidence_sha256'],
                     'damaged_controls_per_mode':reader['evidence']['damaged_controls'],
                     'raw_cardinality':'96k+184 for every integer k>=6',
                     'notch_suppliers':9,'angle_rejection_DAG_nodes':16,
                     'scope':'Registered contact lemmas and a forced E2 neighbor; no full E2 inclusion or Heesch record',
                     'python':sys.version.split()[0],'seconds':round(time.monotonic()-started,3)},sort_keys=True))

if __name__=='__main__':main()
