"""Complete antipodal H7 phase-weight2/42 covers: 22 signed models each.
Generator uses committed log supports; auditor uses literal group cosets
and all actual field APs, aggregating only identical signed supports.
"""
from pathlib import Path
from collections import Counter
import sys,hashlib,json,itertools,subprocess,os,time,resource,argparse

HERE=Path(__file__).resolve().parent
base=HERE.parent/'order7-geometric-cut'
parser=argparse.ArgumentParser()
parser.add_argument('--kind',choices=['opposed','agreed'],required=True)
parser.add_argument('--work',type=Path,required=True)
parser.add_argument('--resume',action='store_true')
parser.add_argument('--audit-only',action='store_true')
args=parser.parse_args()
kind=args.kind
baseline=int(kind=='agreed')
K=42 if baseline else 2
work=args.work.absolute()
if work.exists() and not args.resume:raise ValueError('fresh work directory or --resume required')
work.mkdir(parents=True,exist_ok=True)
prior=json.loads((work/'progress.json').read_text()) if args.resume and (work/'progress.json').exists() else None
pins=json.loads((HERE/'SOURCE_PINS.json').read_text())
for name,digest in pins['files'].items():
    if hashlib.sha256((base/name).read_bytes()).hexdigest()!=digest:raise ValueError('changed committed source dependency: '+name)
if prior is not None and prior.get('dependency_pins')!=pins['files']:raise ValueError('changed resume dependencies')
started=time.monotonic()
sys.path.insert(0,str(base))
from encode import field_edges
from sign_audit import orientations,read_cnf

def require(ok,text):
    if not ok:raise ValueError(text)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def fold(indices,phase):
    signed={i+1 if i<44 else (-1 if phase[i-44] else 1)*(i-44+1) for i in indices}
    if any(-v in signed for v in signed):return None
    return tuple(sorted(signed))

edges=field_edges()
for d in range(1,23):
    phase=[baseline ^ int(i in (0,d)) for i in range(44)]
    clauses=set()
    for edge in edges:
        c=fold(edge,phase)
        if c is not None:clauses.add(c);clauses.add(tuple(sorted(-v for v in c)))
    ordered=sorted(clauses,key=lambda c:(len(c),c))+[(-1,)]
    path=work/f'd-{d}.cnf'
    content=f'p cnf 44 {len(ordered)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in ordered)
    if args.resume and path.exists() and path.read_text()!=content:raise ValueError('changed resume CNF')
    path.write_text(content)
# Independently construct complete actual AP support signatures.
slots=orientations()
signatures=set();retained=removed=0
for a in range(617):
    for delta in range(1,617):
        terms=[(a+j*delta)%617 for j in range(7)]
        if 0 in terms:removed+=1;continue
        signatures.add(tuple(sorted({slots[x] for x in terms})))
        retained+=1
require((retained,removed,len(signatures))==(375760,4312,26488),'independent signed AP census wrong')
qr_controls=0
control=set()
for sig in signatures:
    c=tuple(sorted({i+1 for i,side in sig}));control.add(c);control.add(tuple(sorted(-v for v in c)))
for flip in [0,1]:
    vals={i+1:(i%2)^flip for i in range(44)}
    require(all(any(vals[abs(v)]==(v>0) for v in c) for c in control),'phase-zero QR positive control failed')
    qr_controls+=1
records=[]
for d in range(1,23):
    expected=set()
    for sig in signatures:
        # Semantic signs: only coset pairs0,d are opposed.
        signed={(i+1)*(-1 if side and ((i in (0,d)) != bool(baseline)) else 1) for i,side in sig}
        if any(-v in signed for v in signed):continue
        expected.add(tuple(sorted(signed)));expected.add(tuple(sorted(-v for v in signed)))
    cnf=work/f'd-{d}.cnf';actual=read_cnf(cnf)
    require(Counter(actual)==Counter(list(expected)+[(-1,)]),'complete signed model mismatch')
    records.append({'d':d,'phase_K':K,'variables':44,'clauses':len(actual),'cnf_sha256':sha(cnf),'status':'EXACTLY_AUDITED_NOT_PROPOSED','mathematical_exclusion':False})
normalizations=0
for half in range(2,7):
    for bits in itertools.product((0,1),repeat=2*half):
        phase=[bits[i]^bits[i+half] for i in range(half)]
        if sum(phase)!=(half-2 if baseline else 2):continue
        u,v=[i for i in range(half) if phase[i]!=(baseline)]
        gap=(v-u)%half
        shift=u if gap<=half-gap else v
        d=min(gap,half-gap)
        normalized=[bits[(i+shift)%(2*half)]^bits[shift] for i in range(2*half)]
        require(normalized[0]==0,'color normalizer failed')
        require([normalized[i]^normalized[i+half] for i in range(half)]==[baseline ^ int(i in (0,d)) for i in range(half)],'two-pair cyclic cover failed')
        normalizations+=1
meta={'agent':'six-vdw-2','role':'researcher','status':'EXACT_TWO_PHASE_MODELS_AUDITED','exception_kind':kind,'phase_K':K,'canonical_distances':list(range(1,23)),'complete_labeled_words':946*2**44,'phase_patterns':946,'cyclic_pattern_orbits':22,'orbit_sizes':[44]*21+[22],'retained_APs':retained,'zero_APs_removed':removed,'actual_signed_supports':len(signatures),'QR_controls':qr_controls,'small_normalizations_checked':normalizations,'records':records,'seconds_audit':time.monotonic()-started,'family_exclusion':False}
meta['dependency_pins']=pins['files']
progress=work/'progress.json';progress.write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'stage':'ALL_22_TWO_PHASE_MODELS_EXACTLY_AUDITED','seconds':meta['seconds_audit'],'normalizations':normalizations,'whole_class_words':meta['complete_labeled_words']}),flush=True)
if args.audit_only:
    print(json.dumps({'status':'EXACT_TWO_PHASE_MODELS_AUDITED','phase_K':K,'cases':len(records)}));raise SystemExit(0)
require(sha(base/'check_rup_lrat.py')=='55543f905d42aaf0955906f97a8484ec8522a182512b1d2e8fe132bb45cb545c','checker changed')
from urllib.request import urlopen
converter_source=work/'drat-trim.c'
if not converter_source.exists():converter_source.write_bytes(urlopen(pins['converter']['url'],timeout=20).read())
require(sha(converter_source)==pins['converter']['sha256'],'converter source changed')
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
def run(cmd):
    p=subprocess.run([str(v) for v in cmd],capture_output=True,text=True,env=env,timeout=30)
    require(p.returncode==0,p.stderr[:1600] or p.stdout[-1600:])
    return p.stdout
compiled=subprocess.run(['gcc','-O2','-std=gnu99',str(converter_source),'-o',str(work/'drat-trim')],capture_output=True,text=True,timeout=30,env=env)
require(compiled.returncode==0,compiled.stderr[-1400:])
expected=json.loads((HERE/'expected.json').read_text())['cases'][kind]
for rec in records:
    d=rec['d'];cnf=work/f'd-{d}.cnf';drat=cnf.with_suffix('.drat');lrat=cnf.with_suffix('.lrat')
    try:
        if args.resume and cnf.with_suffix('.solve.json').exists():
            prop=json.loads(cnf.with_suffix('.solve.json').read_text())
            require(prop['cnf_sha256']==sha(cnf),'changed proposal input')
            require(prop['status']=='UNSAT_PENDING_CHECK' and drat.exists() and prop['drat_sha256']==sha(drat),'incomplete resume proposal')
        else:
            require(not drat.exists() and not cnf.with_suffix('.solve.json').exists(),'unmarked solver output')
            prop=json.loads(run([sys.executable,base/'solve.py',cnf,'--conflicts',50000]))
        rec['proposal']=prop;rec['status']=prop['status']
        if prop['status']=='UNSAT_PENDING_CHECK':
            completion=cnf.with_suffix('.conversion.complete.json')
            if args.resume and completion.exists():
                marker=json.loads(completion.read_text())
                require(lrat.exists() and marker=={'drat_sha256':sha(drat),'lrat_sha256':sha(lrat)},'changed conversion checkpoint')
            else:
                require(not lrat.exists(),'unmarked converted output')
                output=run([work/'drat-trim',cnf,drat,'-t',25,'-L',lrat])
                require('s VERIFIED' in output,'incomplete signed conversion')
                completion.write_text(json.dumps({'drat_sha256':sha(drat),'lrat_sha256':sha(lrat)},indent=2)+'\n')
            checked=[json.loads(run([sys.executable]+flags+[base/'check_rup_lrat.py',cnf,lrat])) for flags in [[],['-O']]]
            require({k:v for k,v in checked[0].items() if k!='seconds'}=={k:v for k,v in checked[1].items() if k!='seconds'},'signed checker modes differ')
            require(checked[0]['status']=='EXACT_RUP_LRAT_VERIFIED','signed proof not verified')
            fixture=next(r for r in expected if r['d']==d)
            require(fixture['cnf_sha256']==sha(cnf) and fixture['clauses']==rec['clauses'],'reference exact instance differs')
            rec['reference_proof_byte_match']=fixture['proof_sha256']==checked[0]['proof_sha256']
            rec['RUP']=checked[0];rec['RUP_optimized']=checked[1]
            rec['mathematical_exclusion']=True;rec['status']='EXACT_TWO_PHASE_DISTANCE_REFUTATION'
    except subprocess.TimeoutExpired:
        rec['status']='BOUNDED_STAGE_TIMEOUT_NO_EXCLUSION';rec['mathematical_exclusion']=False
    meta['seconds']=time.monotonic()-started
    progress.write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({'d':d,'status':rec['status'],'conflicts':rec.get('proposal',{}).get('stats',{}).get('conflicts'),'seconds':meta['seconds']}),flush=True)
    if rec['status']=='SAT_PENDING_INDEPENDENT_CHECK':break
meta['status']='EXACT_TWO_PHASE_CLASS_EXCLUDED' if all(r['mathematical_exclusion'] for r in records) else 'INCOMPLETE_NO_CLASS_EXCLUSION'
meta['whole_phase_class_exclusion']=all(r['mathematical_exclusion'] for r in records)
meta['counts']=dict(Counter(r['status'] for r in records))
meta['maxrss_parent_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
meta['maxrss_child_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
meta['reference_all_proof_bytes_match']=all(r.get('reference_proof_byte_match',False) for r in records)
progress.write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({k:meta[k] for k in ['status','whole_phase_class_exclusion','counts','seconds','maxrss_parent_kib','maxrss_child_kib']}),flush=True)

if not meta['whole_phase_class_exclusion']:raise SystemExit(2)
