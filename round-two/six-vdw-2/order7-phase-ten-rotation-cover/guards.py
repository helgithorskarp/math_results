"""Repaired-metadata damages must fail for their mathematical/coverage reason."""
import argparse
import copy
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time
from common import HERE,pins,require,sha

def main(checked,work):
    began=time.monotonic();dependency=pins()
    require(not work.exists(),'fresh damage directory required');work.mkdir(parents=True)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    lines=(checked/'representatives.txt').read_text().splitlines()
    tests=[]
    # Each subprocess imports only the checker, never the DFS proposer.
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        mutations=[]
        mutations.append(('missing-last',lines[:-1],{},'incomplete or wrong-period phase cover'))
        duplicate=list(lines);duplicate[1]=duplicate[0]
        mutations.append(('duplicate',duplicate,{},'duplicate or unordered phase representative'))
        badsum=list(lines);row=list(map(int,badsum[0].split()));row[-1]+=1
        badsum[0]=' '.join(map(str,row))
        mutations.append(('wrong-cycle-sum',badsum,{},'wrong literal selected-position domain'))
        noncanonical=list(lines)
        for index,line in enumerate(lines):
            row=tuple(map(int,line.split()))
            candidates=[row[i:]+row[:i] for i in range(1,10)
                        if row[i]==2 and row[(i+1)%10]==3 and row[i:]+row[:i]!=row]
            if candidates:
                noncanonical[index]=' '.join(map(str,candidates[0]));break
        else:raise ValueError('missing noncanonical valid damage fixture')
        mutations.append(('noncanonical-valid-word',noncanonical,{},'noncanonical actual phase root'))
        mutations.extend([
            ('wrong-background-scope',None,{'backgrounds':[0]},'changed mathematical scope'),
            ('wrong-period-count',None,{'period22_phase_classes':30},'changed exact count expectation'),
            ('wrong-class-count',None,{'phase_rotation_classes':127048},'changed exact count expectation')])
        for name,changed,metadata,phrase in mutations:
            case=work/(mode+'-'+name);case.mkdir()
            path=case/'representatives.txt'
            if changed is None:path.symlink_to((checked/'representatives.txt').absolute())
            else:path.write_text('\n'.join(changed)+'\n')
            repaired=copy.deepcopy(expected);repaired.update(metadata)
            repaired['corpus_sha256']=sha(path);repaired['corpus_bytes']=path.stat().st_size
            (case/'repaired.json').write_text(json.dumps(repaired))
            code='import json; from pathlib import Path; import check; check.audit(Path('+repr(str(case))+'),json.loads(Path('+repr(str(case/'repaired.json'))+').read_text()),False)'
            process=subprocess.run([sys.executable,*flags,'-c',code],cwd=HERE,
                                   capture_output=True,text=True,timeout=55)
            require(process.returncode!=0 and phrase in process.stderr,
                    'damage accepted or wrong failure: '+name+' '+process.stderr[-500:])
            tests.append(mode+'-'+name)
        isolated=work/(mode+'-source');here=isolated/'order7-phase-ten-rotation-cover'
        here.mkdir(parents=True)
        for name in ('check.py','common.py','SOURCE_PINS.json'):
            shutil.copyfile(HERE/name,here/name)
        for name in dependency['relative_files']:
            target=isolated/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE.parent/name,target)
        name=next(iter(dependency['relative_files']))
        with (isolated/name).open('a') as stream:stream.write('\nDAMAGED INPUT\n')
        process=subprocess.run([sys.executable,*flags,'-c','import check; check.pins()'],
                               cwd=here,capture_output=True,text=True,timeout=55)
        require(process.returncode!=0 and 'changed mathematical input:' in process.stderr,
                'changed premise pin accepted')
        tests.append(mode+'-changed-mathematical-input')
    result=dict(agent='six-vdw-2',role='researcher',status='ALL_REPAIRED_COVER_DAMAGES_REJECTED',
                rejected=len(tests),tests=tests,seconds=time.monotonic()-began,
                maxrss_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (work/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--checked-work',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
    main(args.checked_work.absolute(),args.work.absolute())
