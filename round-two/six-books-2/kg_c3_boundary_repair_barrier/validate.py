"""Whole sanitizer replay and meaningful damaged-input checks."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,os,subprocess,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import reproduce

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();work=args.work.resolve();replay=args.replay.resolve()
    if work==HERE or HERE in work.parents or work.exists() and any(work.iterdir()):
        raise ValueError('use a new work directory outside public source')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    environment=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:environment[key]='1'
    flags=['-O1','-g','-fno-omit-frame-pointer','-fno-pie','-no-pie','-fsanitize=address,undefined']
    result=subprocess.run(['g++','-std=c++17']+flags+['-Wall','-Wextra','-Wpedantic',str(HERE/'direct.cpp'),'-o',str(work/'sanitized')],env=environment,capture_output=True,text=True,timeout=30)
    result.check_returncode()
    if result.stderr:raise ValueError('sanitizer compiler warnings')
    result=subprocess.run([str(work/'sanitized'),str(replay/'parents.txt'),str(work/'optimal.txt'),str(work/'pools.txt')],env=environment,capture_output=True,text=True,timeout=30)
    (work/'sanitizer.stdout').write_text(result.stdout);(work/'sanitizer.stderr').write_text(result.stderr)
    result.check_returncode()
    original=reproduce.strict_json(replay/'direct-summary.json');checked=json.loads(result.stdout)
    if {k:v for k,v in original.items() if k!='seconds'}!={k:v for k,v in checked.items() if k!='seconds'}:
        raise ValueError('whole release vs sanitizer mathematical outputs differ')
    for name in ['optimal.txt','pools.txt']:
        if (replay/name).read_bytes()!=(work/name).read_bytes():raise ValueError('whole release vs sanitizer stream differs')
    native_damages=[];lines=(replay/'parents.txt').read_text().splitlines()
    changes={
        'missing-parent':lines[:-1],
        'duplicate-parent':lines[:1]+lines[:1]+lines[2:],
        'extra-field':[lines[0]+' 99']+lines[1:],
        'truncated-row':[' '.join(lines[0].split()[:-1])]+lines[1:],
        'noninteger':['false '+' '.join(lines[0].split()[1:])]+lines[1:],
    }
    # A semantically false minimum-five certificate for an actual minimum-four
    # parent must fail the direct below-bound enumeration, despite a red-valid upper.
    for i,line in enumerate(lines):
        values=list(map(int,line.split()))
        if values[18]!=4:continue
        taken=set(values[9:18]+values[19:]);extra=next(v for v in range(35) if v not in taken)
        values[18]=5;values.append(extra)
        bad=lines[:];bad[i]=' '.join(map(str,values));changes['forged-minimum']=bad;break
    for name,bad in changes.items():
        path=work/(name+'.txt');path.write_text('\n'.join(bad)+'\n')
        result=subprocess.run([str(replay/'direct'),str(path),str(work/(name+'-optimal.txt')),str(work/(name+'-pools.txt'))],env=environment,capture_output=True,text=True,timeout=30)
        if result.returncode==0:raise ValueError('damaged native input accepted: '+name)
        native_damages.append(dict(name=name,reason=result.stderr.strip()))
    parent_damages=[];parents=reproduce.strict_json(HERE/'PARENTS.json')
    for name in ['omission','duplicate','Boolean-weight','Boolean-orbit','unknown-field']:
        bad=deepcopy(parents)
        if name=='omission':bad.pop()
        elif name=='duplicate':bad[1]=deepcopy(bad[0])
        elif name=='Boolean-weight':bad[0]['weight']=True
        elif name=='Boolean-orbit':bad[0]['J'][0]=True
        else:bad[0]['unknown']=0
        try:reproduce.validate_parents(bad)
        except ValueError:parent_damages.append(name)
        else:raise ValueError('damaged complete parent fixture accepted: '+name)
    duplicate=work/'duplicate-key.json';duplicate.write_text('{"a":1,"a":2}')
    try:reproduce.strict_json(duplicate)
    except ValueError:parent_damages.append('duplicate-JSON-key')
    else:raise ValueError('duplicate JSON key accepted')
    report=dict(status='WHOLE_SANITIZER_STREAMS_AND_DAMAGED_INPUTS_PASS',
                direct_deletion_subsets=checked['total_deletion_subsets'],
                residual_promotion_subsets=checked['promotion_subset_tests'],
                every_release_sanitizer_field_equal=True,both_complete_streams_byte_equal=True,
                flags=flags,native_damages=native_damages,parent_damages=parent_damages,
                seconds=time.monotonic()-start,sanitizer_program_seconds=checked['seconds'],
                scope='Whole finite direct graph census, not merely selected sanitizer intervals; same author, no external review.')
    (work/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
