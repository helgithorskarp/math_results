"""Sanitized boundary cases and independent positive/negative mapping checks."""
import json
import os
import resource
import subprocess
import time
from paths import BASE, WORK
from reference import literal_python


def run():
    started=time.monotonic()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name]='1'
    os.environ['ASAN_OPTIONS']='detect_leaks=1'
    os.environ['UBSAN_OPTIONS']='halt_on_error=1'
    sanitized=WORK/'pair_fibers_sanitized.exe'
    subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wpedantic',
                    '-fsanitize=address,undefined','-fno-omit-frame-pointer','-fno-pie','-no-pie',
                    str(BASE/'pair_fibers.cpp'),'-o',str(sanitized)],check=True)
    matrix=(WORK/'mapping_fibers.txt').read_bytes()
    entries=[json.loads(line) for line in (WORK/'all_prune.jsonl').read_text().splitlines()]
    checked=0
    for index in (0,111,4005):
        for mode in ('prune','literal'):
            result=subprocess.run([str(sanitized),mode,str(index),str(index+1),'200000','10'],
                                  input=matrix,capture_output=True,timeout=30)
            if result.returncode or result.stderr: raise RuntimeError(result.stderr[:2000])
            actual=json.loads(result.stdout)
            if actual['status']!='COMPLETE' or actual['accepted']!=entries[index]['accepted']:
                raise RuntimeError('sanitized actual fiber differs')
            checked+=1
    carrier=json.loads((WORK/'tail_carrier.json').read_text())
    specs=json.loads((WORK/'mapping_specs.json').read_text())['fibers']
    for index in list(range(14))+[111,4005]:
        spec=specs[index]
        actual=literal_python(spec,carrier['stars'][spec['first']],carrier['stars'][spec['second']])
        if actual['accepted']!=entries[index]['accepted']:
            raise RuntimeError('complete Python literal mapping fiber differs')
    row=matrix.decode().splitlines()[112].split();row[0]='0'
    valid='PAIR2111_V1 1\n'+' '.join(row)+'\n'
    malformed=[]
    a=row[:];a[1]='0';malformed.append('PAIR2111_V1 1\n'+' '.join(a)+'\n')
    a=row[:];a[2]=a[1];malformed.append('PAIR2111_V1 1\n'+' '.join(a)+'\n')
    a=row[:];fixed=[i for i in range(35,51) if a[i]!='-1'];a[fixed[1]]=a[fixed[0]]
    malformed.append('PAIR2111_V1 1\n'+' '.join(a)+'\n')
    malformed.extend([valid+'trailing\n',valid.replace('PAIR2111_V1','WRONG'),valid[:40]])
    binary=WORK/'pair_fibers.exe'
    for text in malformed:
        result=subprocess.run([str(binary),'prune','0','1','200000','10'],input=text,
                              text=True,capture_output=True,timeout=10)
        if not result.returncode: raise RuntimeError('malformed matrix accepted')
    for nodes,seconds in [('0','10'),('200001','10'),('200000','0'),('200000','11'),('200000','nan')]:
        result=subprocess.run([str(binary),'prune','0','1',nodes,seconds],input=valid,
                              text=True,capture_output=True,timeout=10)
        if not result.returncode: raise RuntimeError('invalid guard accepted')
    for mode in ('prune','literal'):
        result=subprocess.run([str(binary),mode,'0','1','1','10'],input=valid,
                              text=True,capture_output=True,timeout=10)
        if not result.returncode or 'INCOMPLETE' not in result.stdout or 'INCOMPLETE' not in result.stderr:
            raise RuntimeError('small guard not visibly incomplete')
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE',sanitized_actual_fibers=checked,
                sanitizer_diagnostics=0,python_full_mapping_fibers=16,malformed_matrices_rejected=6,
                invalid_guards_rejected=5,visible_incomplete_guards=2,
                seconds=round(time.monotonic()-started,6),
                parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (WORK/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)
    return result


if __name__=='__main__':
    run()
