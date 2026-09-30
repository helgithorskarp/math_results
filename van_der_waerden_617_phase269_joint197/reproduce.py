"""Complete frozen integer replay; optional four serial bounded fresh solves."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import verify

HERE=Path(__file__).resolve().parent


def run(args):
    optimization = ["-"+"O"*sys.flags.optimize] if sys.flags.optimize else []
    subprocess.run([sys.executable]+optimization+[str(x) for x in args],cwd=HERE,check=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--regenerate",action="store_true")
    p.add_argument("--work",type=Path,default=HERE/"build")
    args=p.parse_args()
    run(["verify.py","--expected","expected.json"])
    run(["low/controls.py"])
    run(["controls.py"])
    if args.regenerate:
        work=args.work.absolute();work.mkdir(parents=True,exist_ok=True)
        documents,hashes=[],{}
        for v in (1004,1327,1650,1973):
            output=work/f"{v}.json"
            run(["generate.py","--root",v,"--output",output,"--summary",work/f"{v}.guidance.json"])
            documents.append(json.loads(output.read_text()))
            hashes[str(v)]={"fresh":hashlib.sha256(output.read_bytes()).hexdigest(),
                            "frozen":hashlib.sha256((HERE/f"roots/{v}.json").read_bytes()).hexdigest()}
        result=verify.check_all(documents=documents)
        (work/"checked.json").write_text(json.dumps(result,indent=2)+"\n")
        (work/"hashes.json").write_text(json.dumps(hashes,indent=2)+"\n")
    print(json.dumps({"status":"VERIFIED_PHASE269_JOINT197_EXCLUSION","agent":"six-vdw-3",
                      "role":"researcher","regenerated":args.regenerate}))


if __name__=="__main__":main()
