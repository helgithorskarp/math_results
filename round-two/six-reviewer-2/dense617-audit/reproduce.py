"""Cold source-only replay. Generated whole transcripts remain in a fresh workdir."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from partitions import split_stream

ROOT=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def replay(output):
    need(not output.exists(),"fresh nonexistent work directory required")
    output.mkdir(parents=True)
    expected=json.loads((ROOT/"EXPECTED.json").read_text())
    env=os.environ.copy()
    for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS",
              "NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS","BLIS_NUM_THREADS"):
        env[k]="1"
    runs=[];whole_pairs=0
    def run(script,args,opt):
        start=time.monotonic()
        p=subprocess.run([sys.executable]+(["-O"] if opt else [])+[str(ROOT/script)]+args,
                         env=env,timeout=20,capture_output=True)
        need(p.returncode==0,(script,args,p.returncode,p.stderr.decode()))
        runs.append(dict(script=script,optimized=opt,seconds=time.monotonic()-start,
                         peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
        return p.stdout,json.loads(p.stdout)
    for mode in ("model","cores"):
        pairs=[run("primary.py",[mode],opt) for opt in (False,True)]
        need(pairs[0][0]==pairs[1][0] and pairs[0][1]==expected[mode],"whole "+mode)
        whole_pairs+=1
    for which in ("balanced",):
        for result in expected[which]:
            first,last=result["range"];name=f"{which}-{first:04d}";pairs=[];streams=[]
            for opt in (False,True):
                stream=output/(name+("-O" if opt else "")+".jsonl")
                args=["extension","--which",which,"--start",str(first),"--stop",str(last),
                      "--stream",str(stream)]
                pairs.append(run("primary.py",args,opt));streams.append(stream)
            need(pairs[0][0]==pairs[1][0] and pairs[0][1]==result,"whole primary batch")
            need(streams[0].read_bytes()==streams[1].read_bytes(),"whole primary transcript")
            whole_pairs+=1
            aggregate=Counter();count=0
            for lo,hi,part in split_stream(which,first,last,streams[0],output):
                pairs=[]
                for opt in (False,True):
                    args=["--which",which,"--start",str(lo),"--stop",str(hi),"--stream",str(part)]
                    pairs.append(run("verify_records.py",args,opt))
                    need(pairs[-1][1]["stream_sha256"]==hashlib.sha256(part.read_bytes()).hexdigest(),"entire independent substream")
                need(pairs[0][0]==pairs[1][0],"whole independent checker")
                for key,value in pairs[0][1]["histogram"]:aggregate[key]+=value
                count+=pairs[0][1]["count"];whole_pairs+=1
            need(count==result["count"] and sorted(aggregate.items())==[tuple(x) for x in result["histogram"]],"whole32-core reconstruction")
    pairs=[run("controls.py",["--stream",str(output/"balanced-0000-check.jsonl")],opt) for opt in (False,True)]
    need(pairs[0][0]==pairs[1][0],"whole controls")
    whole_pairs+=1
    seal=json.loads((ROOT/"INDEPENDENCE.json").read_text())
    for name in seal["retained_unchanged_pre_native_kernels"]:
        pin=seal["original_seal"]["files"][name];raw=(ROOT/name).read_bytes()
        need(len(raw)==pin["bytes"] and hashlib.sha256(raw).hexdigest()==pin["sha256"],"original independent kernel seal "+name)
    summary=dict(status="COMPLETE_DENSE617_INDEPENDENT_AUDIT",children=len(runs),
                 whole_pairs=whole_pairs,all_primary_entries_checked=True,
                 controls=pairs[0][1],max_child_seconds=max(x["seconds"] for x in runs),
                 peak_child_rss_kib=max(x["peak_child_rss_kib"] for x in runs),
                 guards_seconds=20,threads=1,expected_sha256=hashlib.sha256((ROOT/"EXPECTED.json").read_bytes()).hexdigest())
    (output/"VALIDATION.json").write_text(json.dumps(dict(summary=summary,runs=runs),indent=2)+"\n")
    return summary

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path,required=True)
    x=ap.parse_args();print(json.dumps(replay(x.output),sort_keys=True))
