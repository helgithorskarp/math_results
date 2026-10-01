"""Sequential source-only reproduction; generated bitmaps stay in scratch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

SOURCE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--scratch",type=Path,default=SOURCE/"build")
    args=parser.parse_args(); scratch=args.scratch.resolve(); scratch.mkdir(parents=True,exist_ok=True)
    begin=time.monotonic(); env=os.environ.copy()
    for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
        env[name]="1"
    env["PYTHONHASHSEED"]="0"
    def run(command,label,expected_ok=True,deadline=55):
        result=subprocess.run(list(map(str,command)),capture_output=True,text=True,env=env,timeout=deadline)
        (scratch/(label+".stdout")).write_text(result.stdout)
        (scratch/(label+".stderr")).write_text(result.stderr)
        if expected_ok and result.returncode:
            raise RuntimeError(label+" failed: "+result.stderr[:1500])
        if not expected_ok and result.returncode==0:
            raise RuntimeError(label+" accepted damaged input")
        return result
    compiler=os.environ.get("CXX","g++")
    flags=["-std=c++17","-Wall","-Wextra","-Wconversion","-pedantic","-Werror"]
    release=scratch/"census"; sanitized=scratch/"census-sanitized"
    run([compiler,*flags,"-O2",SOURCE/"census.cpp","-o",release],"compile-release",deadline=30)
    cases=[]
    for p,s in [(7,1),(7,6),(11,2),(17,2),(31,4),(37,2),(41,2),(73,6),(617,2)]:
        stem=scratch/f"{p}-{s}"; bitmap=stem.with_suffix(".bitmap"); metadata=stem.with_suffix(".metadata.json")
        generated=run([release,p,s,bitmap],f"census-{p}-{s}")
        metadata.write_text(generated.stdout)
        checked=run([sys.executable,SOURCE/"verify.py",metadata,bitmap],f"verify-{p}-{s}")
        cases.append(json.loads(checked.stdout))
        print("checked",p,s,cases[-1]["classification_entries_checked"],flush=True)
    target=scratch/"617-2"; metadata=target.with_suffix(".metadata.json"); bitmap=target.with_suffix(".bitmap")
    optimized=run([sys.executable,"-O",SOURCE/"verify.py",metadata,bitmap],"verify-617-optimized")
    if json.loads(optimized.stdout)!=cases[-1]:
        raise RuntimeError("normal and optimized Python results differ")
    run([compiler,*flags,"-O1","-g","-fsanitize=address,undefined","-fno-omit-frame-pointer",
         SOURCE/"census.cpp","-o",sanitized],"compile-sanitizers",deadline=30)
    for p,s in [(7,6),(617,2)]:
        sanitizer_bitmap=scratch/f"sanitized-{p}-{s}.bitmap"
        generated=run([sanitized,p,s,sanitizer_bitmap],f"sanitizers-{p}-{s}")
        base=scratch/f"{p}-{s}"
        if generated.stdout!=base.with_suffix(".metadata.json").read_text() or sanitizer_bitmap.read_bytes()!=base.with_suffix(".bitmap").read_bytes():
            raise RuntimeError("release and ASAN/UBSAN entries differ")
    bad_metadata=scratch/"wrong.metadata.json"; data=json.loads(metadata.read_text()); data["realized_triples"]+=1
    bad_metadata.write_text(json.dumps(data))
    run([sys.executable,SOURCE/"verify.py",bad_metadata,bitmap],"reject-wrong-count",False)
    bad_bitmap=scratch/"truncated.bitmap"; bad_bitmap.write_bytes(bitmap.read_bytes()[:-1])
    run([sys.executable,SOURCE/"verify.py",metadata,bad_bitmap],"reject-truncated-bitmap",False)
    original=bitmap.read_bytes(); damaged=bytearray(original)
    selected={}
    for rank in range(cases[-1]["ordinary_triples"]):
        value=(original[rank//8]>>(rank%8))&1
        selected.setdefault(value,rank)
        if len(selected)==2:
            break
    if len(selected)!=2:
        raise RuntimeError("entry-corruption control requires both membership values")
    for rank in selected.values():
        damaged[rank//8]^=1<<(rank%8)
    if sum(x.bit_count() for x in damaged)!=sum(x.bit_count() for x in original):
        raise RuntimeError("entry swap did not preserve aggregate count")
    bad_bitmap=scratch/"swapped.bitmap"; bad_bitmap.write_bytes(damaged)
    run([sys.executable,SOURCE/"verify.py",metadata,bad_bitmap],"reject-count-preserving-swap",False)
    run([release,616,2,scratch/"invalid.bitmap"],"reject-composite-modulus",False)
    run([release,617,0,scratch/"invalid.bitmap"],"reject-invalid-boundary",False)
    canonical={"status":"SOURCE_ONLY_EXACT_SUPPORT_CLASSIFICATION_CHECKED","cases":cases,
               "release_sanitizer_cases":2,"normal_optimized_agree":True,"damaged_inputs_rejected":5}
    expected=json.loads((SOURCE/"expected.json").read_text())
    if canonical!=expected:
        raise RuntimeError("canonical result differs from compact expected result")
    digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    result={"canonical":canonical,"canonical_sha256":digest,
            "resources":{"seconds":round(time.monotonic()-begin,6),
                         "child_peak_KiB":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},
            "versions":{"python":sys.version.split()[0],"compiler":run([compiler,"--version"],"compiler-version").stdout.splitlines()[0]}}
    (scratch/"result.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="canonical"},sort_keys=True,indent=2))


if __name__=="__main__":
    main()
