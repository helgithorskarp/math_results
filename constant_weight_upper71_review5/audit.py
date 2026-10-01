"""Cold independent audit; writes generated state only to an explicit work directory."""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import platform
import resource
import subprocess
import time
import urllib.request
from clique_audit import audit as clique_audit
from ordinary import bridges
from common import require,canonical,unique_object

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--repo-root',type=Path)
    parser.add_argument('--offline',action='store_true')
    parser.add_argument('--sanitize',action='store_true')
    args=parser.parse_args()
    source=Path(__file__).resolve().parent
    work=args.work.resolve()
    require(work!=source and source not in work.parents,'work must be outside the source directory')
    work.mkdir(parents=True,exist_ok=False)
    began=time.monotonic()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        os.environ[name]='1'
    pins=json.loads((source/'INPUT.json').read_text(),object_pairs_hook=unique_object)
    inputs={}
    for item in pins['inputs']:
        path=Path(item['path'])
        require(not path.is_absolute() and '..' not in path.parts,'invalid input path')
        local=(args.repo_root/path) if args.repo_root else source.parent/path
        if local.is_file(): blob=local.read_bytes()
        else:
            require(not args.offline,'missing offline input: '+str(path))
            url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+item['source_commit']+'/'+str(path)
            with urllib.request.urlopen(url,timeout=25) as response:
                require(response.status==200,'input HTTP status')
                blob=response.read()
        require(len(blob)==item['bytes'] and sha256(blob).hexdigest()==item['sha256'],'input pin mismatch: '+str(path))
        cached=work/'inputs'/path
        cached.parent.mkdir(parents=True,exist_ok=True);cached.write_bytes(blob)
        inputs[path.name]=cached
    binary=work/'clique'
    flags=['-std=c++17','-Wall','-Wextra','-Werror']
    flags+=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'] if args.sanitize else ['-O2']
    command=['g++',*flags,str(source/'clique.cpp'),'-o',str(binary)]
    built=subprocess.run(command,capture_output=True,text=True,timeout=45)
    require(built.returncode==0 and not built.stderr,'native compilation failed: '+built.stderr)
    result={'clique':clique_audit(binary,inputs['certificate.json']),
            'ordinary':bridges(inputs['baseline69.txt'])}
    stable=canonical(result)
    expected=json.loads((source/'expected.json').read_text(),object_pairs_hook=unique_object)
    require(stable==canonical(expected),'complete result differs from frozen expected record')
    (work/'result.json').write_bytes(stable)
    compiler=subprocess.run(['g++','--version'],capture_output=True,text=True,check=True,timeout=5).stdout.splitlines()[0]
    provenance={'agent':'six-reviewer-5','role':'independent mathematical reviewer',
                'python':platform.python_version(),'compiler':compiler,'compile_flags':flags,
                'optimized_python':not __debug__,'sanitized_native':args.sanitize,
                'elapsed_seconds':time.monotonic()-began,
                'parent_peak_RSS_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                'child_peak_RSS_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                'result_bytes':len(stable),'result_sha256':sha256(stable).hexdigest(),
                'native_threads':1,'native_guard_nodes':200000,'native_guard_seconds':10,
                'native_outer_timeout_seconds':30,'diagnostics_on_success':0,
                'author_executable_imports':0,'old_graph_theorems_needed_for_main_proof':0}
    (work/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(json.dumps(provenance,indent=2))

if __name__=='__main__':main()
