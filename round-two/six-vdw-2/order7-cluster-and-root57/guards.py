"""Meaningful coverage, definition, source-integrity and proof corruptions."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from common import BASE,HERE,pins,require


def main(work,output):
    began = time.monotonic();pins()
    require(not output.exists(),'fresh corruption directory required')
    output.mkdir(parents=True)
    python = Path(sys.executable).absolute()
    env = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    tests = []

    def rejected(name,argv,phrase=None,cwd=None):
        result = subprocess.run(list(map(str,argv)),capture_output=True,text=True,
                                timeout=55,env=env,cwd=cwd)
        require(result.returncode!=0 and (phrase is None or phrase in result.stderr),
                'corruption accepted or wrong failure: '+name+' '+result.stderr[-600:])
        tests.append(name)

    def link_case(group,name):
        target = output/name;target.mkdir()
        data = json.loads((work/group/'models.json').read_text())
        (target/'models.json').write_text(json.dumps(data))
        for path in (work/group).glob('*.cnf'):
            (target/path.name).symlink_to(path.absolute())
        return target,data

    for label,flags in [('normal',[]),('optimized',['-O'])]:
        case,data = link_case('packed',label+'-missing-period11')
        data['records'] = [r for r in data['records'] if r['case']!=42]
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-missing-period11-orbit',
            [python,*flags,HERE/'packed_audit.py','--work',case],
            'missing or duplicate eight-minority case')

        case,data = link_case('packed',label+'-wrong-case-index')
        data['records'][0]['case']=2
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-wrong-case-index',
            [python,*flags,HERE/'packed_audit.py','--work',case],
            'case metadata changes the complete cover')

        case,data = link_case('root57',label+'-missing-run8')
        data['records']=data['records'][1:]
        (case/'models.json').write_text(json.dumps(data))
        rejected(label+'-missing-longest-run8',
            [python,*flags,HERE/'root57_audit.py','--work',case],
            'incomplete longest-run cover')

        case,data = link_case('root57',label+'-wrong-root3-stride')
        cnf = case/'run-8.cnf';text=cnf.read_text().splitlines();cnf.unlink()
        # The first imported color row follows52976 field rows. Replace it
        # by a different in-range row, without changing counts or DIMACS syntax.
        require(text[52977]=='1 52 15 66 29 80 43 0','unexpected canonical color row')
        text[52977]='1 2 15 66 29 80 43 0'
        cnf.write_text('\n'.join(text)+'\n')
        rejected(label+'-wrong-geometric-stride',
            [python,*flags,HERE/'root57_audit.py','--work',case],
            'complete literal-field/run clauses differ')

        case,data = link_case('close',label+'-wrong-count-unit')
        cnf = case/'d-4-b-0.cnf';text=cnf.read_text();cnf.unlink()
        require('\n319 0\n' in text,'canonical exact-six unit absent')
        cnf.write_text(text.replace('\n319 0\n','\n-319 0\n',1))
        rejected(label+'-wrong-exact-six-unit',
            [python,*flags,HERE/'close_audit.py','--work',case],'wrong exact-six units')

        isolated = output/(label+'-changed-helper')
        here = isolated/'order7-cluster-and-root57';here.mkdir(parents=True)
        for name in ('common.py','SOURCE_PINS.json'):
            shutil.copyfile(HERE/name,here/name)
        dependency = json.loads((HERE/'SOURCE_PINS.json').read_text())
        for name in dependency['relative_files']:
            destination = isolated/name;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE.parent/name,destination)
        with (isolated/'order7-geometric-cut/encode.py').open('a') as stream:
            stream.write('\nraise RuntimeError("EXECUTED_CHANGED_HELPER")\n')
        rejected(label+'-changed-helper-before-import',
            [python,*flags,'-c','import common; common.load_encoder()'],
            'changed pinned source: order7-geometric-cut/encode.py',here)

        cnf = work/'root57/run-8.cnf'
        initial = int(cnf.read_text().splitlines()[0].split()[3])
        for name,tail in [('empty-without-hints','0 0'),
                          ('missing-live-hint','0 999999999 0')]:
            proof = output/(label+'-'+name+'.lrat')
            proof.write_text(str(initial+1)+' '+tail+'\n')
            rejected(label+'-'+name,[python,*flags,BASE/'check_rup_lrat.py',cnf,proof])
    result = dict(agent='six-vdw-2',role='researcher',
                  status='ALL_CORRUPTION_CONTROLS_REJECTED',tests=tests,
                  rejected=len(tests),seconds=time.monotonic()-began)
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args();main(args.work.absolute(),args.output.absolute())
