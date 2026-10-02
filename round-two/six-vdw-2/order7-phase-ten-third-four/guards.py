"""Eight-case coverage, heterogeneous exact counts and both prior rules and proof/source damage controls."""
import argparse
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time
from common import BASE,HERE,pins,require,sha


def main(work,output):
    began=time.monotonic();dependency=pins()
    require(not output.exists(),'fresh corruption directory required')
    output.mkdir(parents=True)
    python=Path(sys.executable).absolute()
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
             MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    tests=[];positive=[]

    def rejected(name,argv,phrase=None,cwd=None):
        result=subprocess.run(list(map(str,argv)),capture_output=True,text=True,
                              timeout=55,env=env,cwd=cwd)
        require(result.returncode!=0 and
                (phrase is None or phrase in result.stdout+result.stderr),
                'corruption accepted or wrong failure: '+name+' '+result.stderr[-600:])
        tests.append(name)

    def link_case(group,name):
        target=output/name;target.mkdir()
        data=json.loads((work/group/'models.json').read_text())
        (target/'models.json').write_text(json.dumps(data))
        for path in (work/group).glob('*.cnf'):
            (target/path.name).symlink_to(path.absolute())
        return target,data

    for label,flags in [('normal',[]),('optimized',['-O'])]:
        for group,stem,phrase in [
                ('head','pair-k5-fifth-7-b-1','incomplete eight-case fifth-selection cover'),
                ('head','pair-k5-fifth-10-b-1','incomplete eight-case fifth-selection cover')]:
            case,data=link_case(group,label+'-missing-'+stem)
            data['records']=[r for r in data['records'] if r['stem']!=stem]
            (case/'models.json').write_text(json.dumps(data))
            (case/(stem+'.cnf')).unlink()
            rejected(label+'-missing-'+stem,
                     [python,*flags,HERE/(group+'_audit.py'),'--work',case],phrase)

        for group,stem,unit,phrase in [
                ('head','pair-k5-fifth-10-b-0',251,'wrong heterogeneous exact-count units')]:
            case,data=link_case(group,label+'-wrong-unit-'+stem)
            cnf=case/(stem+'.cnf');text=cnf.read_text();cnf.unlink()
            old='\n-'+str(unit)+' 0\n';new='\n'+str(unit)+' 0\n'
            require(old in text,'canonical final counter unit absent')
            cnf.write_text(text.replace(old,new,1))
            # Repair the digest so rejection must come from mathematical semantics.
            for record in data['records']:
                if record['stem']==stem:record['cnf_sha256']=sha(cnf)
            (case/'models.json').write_text(json.dumps(data))
            rejected(label+'-wrong-unit-'+stem,
                     [python,*flags,HERE/(group+'_audit.py'),'--work',case],phrase)

        case,data=link_case('head',label+'-removed-semantic-input')
        stem='pair-k5-fifth-10-b-0';cnf=case/(stem+'.cnf')
        lines=cnf.read_text().splitlines();cnf.unlink()
        base=44+2*len(data['records'][0]['free_phase_indices'])
        remove=next(i for i,line in enumerate(lines[1:],1)
                    if len(line.split())>=4 and
                    max(abs(int(v)) for v in line.split()[:-1])<=base)
        del lines[remove]
        header=lines[0].split();header[3]=str(int(header[3])-1)
        lines[0]=' '.join(header);cnf.write_text('\n'.join(lines)+'\n')
        data['records'][0]['cnf_sha256']=sha(cnf)
        data['records'][0]['clauses']-=1
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-removed-semantic-input',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'full actual-field pair-strengthened model audit differs')

        case,data=link_case('head',label+'-wrong-selected-count')
        data['records'][0]['free_selected_count']=7
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-wrong-selected-count',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'changed heterogeneous head semantics')

        case,data=link_case('head',label+'-false-no-adjacency-premise')
        data['records'][0]['no_adjacency_cut']=True
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-false-no-adjacency-premise',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'changed heterogeneous head semantics')

        case,data=link_case('head',label+'-forced-next-background')
        data['records'][0]['free_phase_indices'].remove(12)
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-forced-next-background',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'wrong free phase domain or false next neighbor')

        for kind in ('spacing','conditional-successor'):
            case,data=link_case('head',label+'-imported-'+kind)
            cnf=case/'pair-k5-fifth-10-b-0.cnf'
            lines=cnf.read_text().splitlines();cnf.unlink()
            free=data['records'][0]['free_phase_indices'];n=len(free)
            def fv(i):return 45+n+free.index(i)
            values=([-fv(30),-fv(31)] if kind=='spacing' else
                    [-fv(20),-fv(22),fv(24),fv(25)])
            require(tuple(sorted(values)) not in
                    {tuple(sorted(map(int,line.split()[:-1]))) for line in lines[1:]},
                    'premise-damage row already exists')
            lines[0]='p cnf '+str(data['records'][0]['variables'])+' '+str(len(lines))
            lines.append(' '.join(map(str,values))+' 0')
            cnf.write_text('\n'.join(lines)+'\n')
            data['records'][0]['cnf_sha256']=sha(cnf)
            data['records'][0]['clauses']+=1
            (case/'models.json').write_text(json.dumps(data))
            rejected(label+'-imported-'+kind,
                     [python,*flags,HERE/'head_audit.py','--work',case],
                     'full actual-field pair-strengthened model audit differs')


        for kind in ('removed-density', 'reversed-density-sign', 'false-density-source',
                     'removed-pair-b0', 'removed-pair-b1', 'reversed-pair', 'false-pair-source'):
            case,data=link_case('head',label+'-'+kind)
            record=data['records'][1 if kind=='removed-pair-b1' else 0]
            if kind in ('false-density-source','false-pair-source'):
                record['pair_lemma_source_commit' if kind=='false-pair-source' else 'density_lemma_source_commit']='0'*40
                phrase='changed heterogeneous head semantics'
            else:
                cnf=case/(record['stem']+'.cnf')
                lines=cnf.read_text().splitlines();cnf.unlink()
                n=len(record['free_phase_indices'])
                import head_audit
                free=record['free_phase_indices']
                fixed=head_audit.head_fixed(record['fifth_selected_index'],record['background'])
                density,_=head_audit.rule_clauses(fixed,free,record['background'],(-1,0,1,2,3,4,5))
                pair,_=head_audit.rule_clauses(fixed,free,record['background'],(-1,0,1,2,3,4,6))
                wanted=density-pair if 'density' in kind else pair-density
                row=next(row for row in sorted(wanted) if len(row)==7)
                position=next(i for i,line in enumerate(lines[1:],1)
                              if tuple(sorted(map(int,line.split()[:-1])))==row)
                if kind.startswith('removed'):
                    del lines[position];record['clauses']-=1
                    lines[0]='p cnf '+str(record['variables'])+' '+str(record['clauses'])
                else:
                    values=list(map(int,lines[position].split()[:-1]))
                    j=next(i for i,value in enumerate(values) if value<0)
                    values[j]*=-1
                    lines[position]=' '.join(map(str,values))+' 0'
                cnf.write_text('\n'.join(lines)+'\n')
                record['cnf_sha256']=sha(cnf)
                phrase='full actual-field pair-strengthened model audit differs'
            (case/'models.json').write_text(json.dumps(data))
            rejected(label+'-'+kind,
                     [python,*flags,HERE/'head_audit.py','--work',case],phrase)

        case,data=link_case('head',label+'-false-sixth-anchor')
        data['records'][0]['extra_selected11']=False
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-false-sixth-anchor',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'changed heterogeneous head semantics')

        case,data=link_case('head',label+'-counter-gate')
        record=data['records'][0]
        cnf=case/(record['stem']+'.cnf')
        lines=cnf.read_text().splitlines();cnf.unlink()
        base=44+2*len(record['free_phase_indices'])
        position=next(i for i,line in enumerate(lines[1:],1)
                      if len(line.split())==3 and max(map(abs,map(int,line.split()[:-1])))>base)
        row=list(map(int,lines[position].split()[:-1]));row[0]*=-1
        lines[position]=' '.join(map(str,row))+' 0'
        cnf.write_text('\n'.join(lines)+'\n')
        record['cnf_sha256']=sha(cnf)
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-counter-gate',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'wrong heterogeneous gate truth relation')

        isolated=output/(label+'-changed-helper')
        here=isolated/'order7-phase-ten-third-four';here.mkdir(parents=True)
        for name in ('common.py','SOURCE_PINS.json'):
            shutil.copyfile(HERE/name,here/name)
        for name in dependency['relative_files']:
            destination=isolated/name;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE.parent/name,destination)
        with (isolated/'order7-geometric-cut/encode.py').open('a') as stream:
            stream.write('\nraise RuntimeError("EXECUTED_CHANGED_HELPER")\n')
        rejected(label+'-changed-helper-before-import',
                 [python,*flags,'-c','import common; common.load_encoder()'],
                 'changed pinned source: order7-geometric-cut/encode.py',here)

        cnf=output/(label+'-toy.cnf')
        cnf.write_text('p cnf 1 2\n1 0\n-1 0\n')
        good=output/(label+'-toy-valid.lrat');good.write_text('3 0 1 2 0\n')
        result=subprocess.run([str(python),*flags,str(BASE/'check_rup_lrat.py'),
                               str(cnf),str(good)],capture_output=True,text=True,
                              timeout=30,env=env)
        require(result.returncode==0 and
                json.loads(result.stdout)['status']=='EXACT_RUP_LRAT_VERIFIED',
                'valid proof positive control failed')
        positive.append(label+'-toy-positive-RUP')
        for name,tail in [('empty-without-hints','0 0'),
                          ('missing-live-hint','0 999999999 0')]:
            proof=output/(label+'-'+name+'.lrat');proof.write_text('3 '+tail+'\n')
            rejected(label+'-'+name,
                     [python,*flags,BASE/'check_rup_lrat.py',cnf,proof],'REJECTED')

    result=dict(agent='six-vdw-2',role='researcher',
                status='ALL_CORRUPTION_CONTROLS_REJECTED',tests=tests,
                rejected=len(tests),positive_controls=positive,
                seconds=time.monotonic()-began,
                maxrss_parent_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--checked-work',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();main(args.checked_work.absolute(),args.work.absolute())
