#!/usr/bin/env python3
"""Every exact leaf and bridge, serially; timeout never means nonexistence.

Default execution uses a fresh temporary journal. --journal gives an explicit
resumable location. Ordinary/optimized Python produce the same math records.
"""
from pathlib import Path
import argparse, hashlib, json, os, resource, subprocess, sys, tempfile, time

HERE=Path(__file__).resolve().parent
CHECK=HERE/'check.py'; CERT=HERE/'certificate.json'; SIZE=128
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
def mathematical(x):
    return {k:v for k,v in x.items() if k!='wall_seconds'}
def barriers():
    # Optional campaign safety guard; never changes operational state.
    root=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    return root is not None and any((Path(root)/x).exists() for x in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json'))
def jobs():
    # A complete binary prefix tree has one more leaf than split nodes.
    cert=json.loads(CERT.read_text());leaves=sum(n[0] in ('C','G','H') for n in cert['nodes'])
    out=[(name,['--'+name]) for name in ('local','coordinate','layer','partition','semantics')]
    for index in range((leaves+SIZE-1)//SIZE):out.append(('chunk'+str(index).zfill(3),['--chunk',str(index),'--size',str(SIZE)]))
    return out
def fingerprint():
    files=('check.py','forms.py','source_cover.py','run.py','certificate.json','DEPENDENCIES.json')
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files}
def assemble(records):
    required=jobs();require(set(records)=={k for k,_ in required},'every exact bridge and leaf chunk required')
    part=records['partition'];require(part['inventory']['closed_cover_complete'],'exact closed product cover')
    cert=json.loads(CERT.read_text());cid=digest(cert);cursor=0;signs=0;counts={'C':0,'G':0,'H':0};stream=[];minimum={}
    for name,args in required[5:]:
        r=records[name]
        require(r['certificate_canonical_sha256']==cid and r['inventory']==part['inventory'] and not r['partial_forest'],'same complete original mathematical certificate')
        require(r['leaf_start']==cursor and r['verified_leaves']==r['leaf_end']-r['leaf_start'],'every leaf exactly once without gaps')
        cursor=r['leaf_end'];signs+=r['strict_exact_controls']
        for k,v in r['leaf_kinds'].items():counts[k]+=v
        stream.append([name,mathematical(r)])
    require(cursor==part['inventory']['leaves'] and counts==part['leaf_kinds'],'full leaf count and kinds')
    expected_signs=162*counts['C']+54*counts['G']+162*(part['trace_hole_kinds']['0']+part['trace_hole_kinds']['2'])+27*part['trace_hole_kinds']['1']
    require(signs==expected_signs,'all required actual triangular/cube controls')
    return {'agent':'six-rupert-2','role':'researcher','scope':'all original proper sources, arbitrary physical translation and lambda>=1 on ENTIRE CLOSED phase56 triangle; ordinary proof bridge in PROOF.md required','certificate_canonical_sha256':cid,'partition':mathematical(part),'local':mathematical(records['local']),'coordinate':mathematical(records['coordinate']),'layer':mathematical(records['layer']),'semantics':mathematical(records['semantics']),'required_leaf_chunks':len(required)-5,'verified_leaves':cursor,'strict_exact_product_controls':signs,'leaf_kinds':counts,'complete_chunk_records_sha256':digest(stream),'all_required_mathematical_records_sha256':digest([[name,mathematical(records[name])] for name,args in required]),'global_J74_Rupert_status':'OPEN','formalized':False,'independent_review':False}
def run(journal,emit=False):
    journal.mkdir(parents=True,exist_ok=True); pin=fingerprint();pinpath=journal/'fingerprints.json'
    if pinpath.exists():require(json.loads(pinpath.read_text())==pin,'source changed; old journal cannot certify current code')
    else:pinpath.write_text(json.dumps(pin,indent=2)+'\n')
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    records={};resources=[]
    for name,args in jobs():
        require(not barriers(),'campaign pause/handover: preserve journal and stop')
        path=journal/(name+'.json');command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(CHECK),'--proposal',str(CERT),*args,'--output',str(path)]
        if path.exists():
            records[name]=json.loads(path.read_text());print('resumed',name,flush=True);continue
        start=time.monotonic()
        try:r=subprocess.run(command,env=env,timeout=45,text=True,capture_output=True)
        except subprocess.TimeoutExpired:
            raise RuntimeError('45-second '+name+' guard: incomplete, no mathematical exclusion; journal preserved')
        resources.append({'job':name,'seconds':time.monotonic()-start,'exit_code':r.returncode})
        (journal/'resources.json').write_text(json.dumps(resources,indent=2)+'\n')
        require(r.returncode==0,'exact job '+name+' failed: '+r.stderr[-2500:])
        require(path.exists(),'successful job omitted its exact record')
        records[name]=json.loads(path.read_text());print('checked',name,resources[-1]['seconds'],flush=True)
    result=assemble(records);expected=HERE/'expected.json'
    if not emit:
        require(expected.exists(),'complete fixed expected result required; --emit bypasses only expected-record comparison')
        require(json.loads(expected.read_text())==result,'complete expected result differs')
    (journal/'complete.json').write_text(json.dumps(result,indent=2)+'\n')
    (journal/'resource-summary.json').write_text(json.dumps({'guard_seconds_per_child':45,'numeric_threads':1,'serial_mathematical_children':True,'cumulative_child_RSS_upper_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'measured_fresh_jobs':resources},indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--journal');parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    if args.journal:run(Path(args.journal),args.emit)
    else:
        with tempfile.TemporaryDirectory(prefix='j74-joint-phase56-') as tmp:run(Path(tmp),args.emit)
