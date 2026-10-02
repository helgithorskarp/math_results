"""Fourteen-case coverage, exact-six and proof/source damage controls."""
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
                ('head','gap-2-3-next-7-b-1','incomplete fourteen-case cover'),
                ('head','gap-2-3-next-13-b-1','incomplete fourteen-case cover')]:
            case,data=link_case(group,label+'-missing-'+stem)
            data['records']=[r for r in data['records'] if r['stem']!=stem]
            (case/'models.json').write_text(json.dumps(data))
            (case/(stem+'.cnf')).unlink()
            rejected(label+'-missing-'+stem,
                     [python,*flags,HERE/(group+'_audit.py'),'--work',case],phrase)

        for group,stem,unit,phrase in [
                ('head','gap-2-3-next-13-b-0',275,'wrong exact-six units')]:
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
        stem='gap-2-3-next-13-b-0';cnf=case/(stem+'.cnf')
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
                 'full actual-field fourteen-case model audit differs')

        case,data=link_case('head',label+'-wrong-selected-count')
        data['records'][0]['free_selected_count']=5
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-wrong-selected-count',
                 [python,*flags,HERE/'head_audit.py','--work',case],
                 'changed branch semantics')

        isolated=output/(label+'-changed-helper')
        here=isolated/'order7-phase-ten-adjacency';here.mkdir(parents=True)
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
