#!/usr/bin/env python3
"""Every exact bridge and closed product region, serially and resumably.

Default uses a fresh temporary journal and requires the fixed expected record.
45s per child; timeout or a campaign barrier leaves an incomplete journal.
"""
from pathlib import Path
import argparse,hashlib,json,os,resource,subprocess,sys,tempfile,time
HERE=Path(__file__).resolve().parent;SIZE=256

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def mathematical(x):return {k:v for k,v in x.items() if k!='wall_seconds'}
def barriers():
    root=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    return root is not None and any((Path(root)/x).exists() for x in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json'))
def jobs():
    out=[('local',0,['--local']),('coordinate',0,['--coordinate'])]
    for fan in range(1):
        path=HERE/('certificate'+str(fan)+'.json');cert=json.loads(path.read_text())
        require(cert['fan']==fan and cert['closed_fan_original_triangle_indices']==[[0,1,2]][fan],'one literal whole closed triangle required')
        leaves=sum(n[0] in ('C','G','H') for n in cert['nodes'])
        for name in ('layer','partition','semantics'):
            out.append(('fan'+str(fan)+'-'+name,fan,['--'+name,'--proposal',str(path)]))
        for index in range((leaves+SIZE-1)//SIZE):
            out.append(('fan'+str(fan)+'-chunk'+str(index).zfill(3),fan,['--proposal',str(path),'--chunk',str(index),'--size',str(SIZE)]))
    return out

def fingerprint():
    files=['check.py','forms.py','source_cover.py','run.py','DEPENDENCIES.json']+['certificate'+str(f)+'.json' for f in range(1)]
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in files}
def assemble(records):
    required=jobs();require(set(records)=={name for name,_,_ in required},'every local/universal/source/stress/partition/leaf record required')
    require(records['coordinate']['source_M']=='15/4' and records['coordinate']['body_actions_only']=='H,Mx; no A/B or parent-group right quotient','actual universal source canonicalization')
    fans=[];totalleaves=0;totalcontrols=0;chunks=[]
    for fan in range(1):
        cert=json.loads((HERE/('certificate'+str(fan)+'.json')).read_text());cid=digest(cert)
        part=records['fan'+str(fan)+'-partition'];require(part['inventory']['closed_cover_complete'] and part['inventory']['pending']==0,'entire closed original receiving/source product cover')
        require(part['certificate_canonical_sha256']==cid and part['closed_fan']==fan,'same literal certified whole closed fan')
        layer=records['fan'+str(fan)+'-layer'];semantics=records['fan'+str(fan)+'-semantics']
        require(layer['closed_fan']==semantics['closed_fan']==fan and len(semantics['semantic_damage_rejections'])==11,'all fan-dependent force and semantic checks')
        cursor=0;signs=0;counts={'C':0,'G':0,'H':0};stream=[]
        for name,ff,args in required:
            if ff!=fan or '-chunk' not in name:continue
            r=records[name]
            require(r['certificate_canonical_sha256']==cid and r['closed_fan']==fan and r['inventory']==part['inventory'] and not r['partial_forest'],'same entire actual mathematical certificate')
            require(r['leaf_start']==cursor and r['verified_leaves']==r['leaf_end']-r['leaf_start'],'all leaves exactly once without gaps')
            cursor=r['leaf_end'];signs+=r['strict_exact_controls']
            for k,v in r['leaf_kinds'].items():counts[k]+=v
            stream.append([name,mathematical(r)]);chunks.append([name,mathematical(r)])
        require(cursor==part['inventory']['leaves'] and counts==part['leaf_kinds'],'entire fan covered and all signs checked')
        expected_signs=162*counts['C']+54*counts['G']+sum((27 if int(k)<10 else 162)*v for k,v in part['trace_hole_kinds'].items())
        require(signs==expected_signs,'every required receiver/source coefficient including all closed boundaries')
        fans.append({'fan':fan,'certificate_canonical_sha256':cid,'partition':mathematical(part),'layer':mathematical(layer),'semantics':mathematical(semantics),'verified_leaves':cursor,'strict_exact_product_controls':signs,'leaf_kinds':counts,'complete_chunk_records_sha256':digest(stream)})
        totalleaves+=cursor;totalcontrols+=signs
    return {'agent':'six-rupert-2','role':'researcher','scope':'ALL original proper sources, arbitrary physical translation and lambda>=1 on the ENTIRE CLOSED original phase4 triangle; ordinary proof and conditional local lemma required','local':mathematical(records['local']),'coordinate':mathematical(records['coordinate']),'closed_fans':fans,'required_records':len(required),'required_leaf_chunks':len(chunks),'verified_leaves':totalleaves,'strict_exact_product_controls':totalcontrols,'complete_chunk_records_sha256':digest(chunks),'all_required_mathematical_records_sha256':digest([[name,mathematical(records[name])] for name,_,_ in required]),'global_J74_Rupert_status':'OPEN','formalized':False,'independent_review':False}

def run(journal,emit=False):
    journal.mkdir(parents=True,exist_ok=True);pins=fingerprint();path=journal/'fingerprints.json'
    if path.exists():require(json.loads(path.read_text())==pins,'source changed: old journal cannot certify this source')
    else:path.write_text(json.dumps(pins,indent=2)+'\n')
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    records={};resources=[]
    for name,fan,args in jobs():
        require(not barriers(),'campaign pause/handover: preserve journal and stop')
        path=journal/(name+'.json')
        if path.exists():records[name]=json.loads(path.read_text());print('resumed',name,flush=True);continue
        env['J74_PHASE4_FAN']=str(fan)
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/'check.py'),*args,'--output',str(path)]
        start=time.monotonic()
        try:r=subprocess.run(command,env=env,timeout=45,capture_output=True,text=True)
        except subprocess.TimeoutExpired:
            raise RuntimeError('45s '+name+' child guard: incomplete, no mathematical exclusion; journal preserved')
        resources.append({'job':name,'seconds':time.monotonic()-start,'exit_code':r.returncode})
        (journal/'resource-summary.json').write_text(json.dumps({'measured_fresh_jobs':resources,'cumulative_child_RSS_upper_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'single_cpu_intensive_child':True,'numeric_threads':1,'guard_seconds':45,'unchanged_process_scope':'1CPU2GiB'},indent=2)+'\n')
        require(r.returncode==0,'exact job '+name+' failed: '+r.stderr[-3000:])
        require(path.exists(),'successful exact child omitted its record')
        records[name]=json.loads(path.read_text());print('checked',name,round(resources[-1]['seconds'],4),flush=True)
    result=assemble(records)
    if not emit:require(result==json.loads((HERE/'expected.json').read_text()),'all exact mathematical records match the fixed public expected result')
    (journal/'complete.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--journal');parser.add_argument('--emit',action='store_true');parser.add_argument('--output');args=parser.parse_args()
    if args.journal:result=run(Path(args.journal),args.emit)
    else:
        with tempfile.TemporaryDirectory(prefix='j74-phase4-exact-') as root:result=run(Path(root),args.emit)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('local','coordinate','closed_fans')},indent=2))
