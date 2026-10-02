"""Reject source, full-premise and semantic damages BEFORE any native solve."""
import json,os
from pathlib import Path
import shutil,subprocess,sys,time
from common import HERE,pins,require,sha,BASE
from head_audit import head_fixed,rule_clauses
import argparse
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
R=HERE;work=args.work.absolute()/'head';output=args.output.absolute()
require(not output.exists(),'fresh damage directory required');output.mkdir()
began=time.monotonic();tests=[];manifest=pins()
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
kinds=('missing-background','missing-fifth','missing-sixth','wrong-remainder-five','wrong-remainder-four',
       'false-sixth-anchor','false-next-neighbor','removed-density-b0','removed-density-b1',
       'reversed-density-b0','reversed-density-b1','removed-following-b0','removed-following-b1',
       'reversed-following-b0','reversed-following-b1','counter-unit','counter-gate','palette-gauge','removed-field',
       'false-successor','proposed-cut','no-adjacency')
require(len(kinds)==22,"wrong public semantic damage count")

for mode,flags in (('normal',[]),('optimized',['-O'])):
    for kind in kinds:
        target=output/(mode+'-'+kind);target.mkdir()
        data=json.loads((work/'models.json').read_text())
        for p in work.glob('*.cnf'):(target/p.name).symlink_to(p.absolute())
        entry=R/'head_audit.py'
        record=data['records'][16 if kind in ('wrong-remainder-four','false-sixth-anchor') else 1 if kind.endswith('b1') else 0]
        if kind in ('missing-background','missing-fifth','missing-sixth'):
            data['records'].pop({'missing-background':1,'missing-fifth':14,'missing-sixth':16}[kind])
            phrase='incomplete twenty-two-case fifth/sixth-selection cover'
        elif kind in ('wrong-remainder-five','wrong-remainder-four','false-sixth-anchor','false-successor','proposed-cut','no-adjacency'):
            if kind.startswith('wrong-remainder'):record['free_selected_count']+=1
            elif kind=='false-sixth-anchor':record['selected_anchors'].remove(8)
            else:record[{'false-successor':'conditional_successor_cut','proposed-cut':'proposed_third_within_two_cut','no-adjacency':'no_adjacency_cut'}[kind]]=True
            phrase='changed heterogeneous head semantics or false premise'
        else:
            cnf=target/(record['stem']+'.cnf');lines=cnf.read_text().splitlines();cnf.unlink()
            rows=[tuple(sorted(map(int,line.split()[:-1]))) for line in lines[1:]]
            n=len(record['free_phase_indices'])
            fixed=head_fixed(record['fourth_selected_index'],record['fifth_selected_index'],record['sixth_selected_index'],record['background'])
            if kind=='false-next-neighbor':
                var=45+n+record['free_phase_indices'].index(record['next_free_phase'])
                rows.append((var if record['background'] else -var,))
                phrase='full actual-field THREE-and-FOLLOWING_ONE model audit differs'
            elif any(kind.startswith(p) for p in ('removed-density','reversed-density','removed-following','reversed-following')):
                following='following' in kind
                offsets=(-1,0,1,2,4,5) if following else (-1,0,1,2,3)
                rules,_=rule_clauses(fixed,record['free_phase_indices'],record['background'],offsets)
                row=next(row for row in sorted(rules) if len(row)==len(offsets));pos=rows.index(row)
                if kind.startswith('removed'):del rows[pos]
                else:
                    changed=list(row);changed[0]*=-1;rows[pos]=tuple(sorted(changed))
                phrase='full actual-field THREE-and-FOLLOWING_ONE model audit differs'
            elif kind=='removed-field':
                pos=next(i for i,row in enumerate(rows) if len(row)==7 and all(0<v<=44 for v in row));del rows[pos]
                phrase='full actual-field THREE-and-FOLLOWING_ONE model audit differs'
            elif kind=='palette-gauge':
                require(rows[-1]==(-1,),'wrong original gauge position');rows[-1]=(1,)
                phrase='full actual-field THREE-and-FOLLOWING_ONE model audit differs'
            elif kind=='counter-unit':
                pos=next(i for i,row in enumerate(rows) if len(row)==1 and row[0]>44+2*n);rows[pos]=(-rows[pos][0],)
                phrase='wrong heterogeneous exact-count units'
            elif kind=='counter-gate':
                pos=next(i for i,row in enumerate(rows) if len(row)==2 and max(map(abs,row))>44+2*n)
                changed=list(rows[pos]);changed[0]*=-1;rows[pos]=tuple(sorted(changed))
                phrase='wrong heterogeneous gate truth relation'
            else:raise ValueError('unhandled model damage')
            record['clauses']=len(rows)
            cnf.write_text(f"p cnf {record['variables']} {len(rows)}\n"+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
            record['cnf_sha256']=sha(cnf)
        (target/'models.json').write_text(json.dumps(data,indent=2)+'\n')
        proc=subprocess.run([sys.executable,*flags,str(entry),'--work',str(target)],capture_output=True,text=True,env=env,timeout=55)
        (target/'stdout').write_text(proc.stdout);(target/'stderr').write_text(proc.stderr)
        require(proc.returncode!=0 and phrase in proc.stdout+proc.stderr,'damage accepted or rejected for wrong reason: '+mode+'-'+kind)
        tests.append(mode+'-'+kind)
        result=dict(agent='six-vdw-2',role='researcher',status='ALL_44_PUBLIC_SEMANTIC_DAMAGES_REJECTED' if len(tests)==44 else 'PUBLIC_GUARDS_INCOMPLETE',tests=tests,seconds=time.monotonic()-began)
        (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(damage=tests[-1],status='REJECTED',seconds=result['seconds'])),flush=True)
# Pin helpers before import and check positive-only kernel's live clauses/hints/deletions.
positives=[]
for mode,flags in (('normal',[]),('optimized',['-O'])):
    fake=output/(mode+'-changed-helper');fake.mkdir()
    here=fake/R.name;here.mkdir()
    for name in ('common.py','SOURCE_PINS.json'):shutil.copy2(R/name,here/name)
    for name in manifest['relative_files']:
        dest=fake/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R.parent/name,dest)
    altered=fake/'order7-geometric-cut/encode.py'
    altered.write_text(altered.read_text()+'\nraise RuntimeError("EXECUTED_CHANGED_HELPER")\n')
    proc=subprocess.run([sys.executable,*flags,'-c','import common;common.load_encoder()'],cwd=here,env=env,capture_output=True,text=True,timeout=30)
    require(proc.returncode!=0 and 'changed pinned source' in proc.stderr and 'EXECUTED_CHANGED_HELPER' not in proc.stderr,'helper executed before pin validation')
    tests.append(mode+'-changed-helper-before-import')
    cnf=output/(mode+'-toy.cnf');cnf.write_text('p cnf 1 2\n1 0\n-1 0\n')
    for label,trace,valid in [('valid','3 0 1 2 0\n',True),('unknown-hint','3 0 99 0\n',False),('deleted-hint','3 d 2 0\n4 0 1 2 0\n',False),('no-contradiction','3 0 1 0\n',False),('missing-empty','3 1 0 1 0\n',False)]:
        proof=output/(mode+'-'+label+'.lrat');proof.write_text(trace)
        proc=subprocess.run([sys.executable,*flags,str(BASE/'check_rup_lrat.py'),str(cnf),str(proof)],env=env,capture_output=True,text=True,timeout=30)
        if valid:
            require(proc.returncode==0 and json.loads(proc.stdout)['status']=='EXACT_RUP_LRAT_VERIFIED','valid RUP control rejected');positives.append(mode+'-'+label)
        else:
            require(proc.returncode!=0,'malformed RUP accepted: '+label);tests.append(mode+'-'+label)
result=dict(agent='six-vdw-2',role='researcher',status='ALL_54_PUBLIC_DAMAGES_REJECTED_TWO_VALID_RUP_CONTROLS',tests=tests,positive_controls=positives,seconds=time.monotonic()-began)
require(len(tests)==54 and len(positives)==2,'incomplete public damage suite')
(output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
