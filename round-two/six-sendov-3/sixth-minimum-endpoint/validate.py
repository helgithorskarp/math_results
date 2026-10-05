"""Author publication gates; one serial mathematical child at a time."""
from pathlib import Path
from hashlib import sha256
import copy, importlib.util, json, os, resource, shutil, subprocess, sys, time

D = Path(__file__).resolve().parent
NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
         "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    output = Path(sys.argv[1]).resolve()
    need(output != D and D not in output.parents, "external scratch output required")
    output.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, **{n:"1" for n in NAMES}}
    env.pop("PYTHONOPTIMIZE", None)
    initial = {p.relative_to(D).as_posix():p.read_bytes() for p in D.rglob("*")
               if p.is_file() and "__pycache__" not in p.parts}
    records = []
    def fresh(name):
        target = output / name
        need(not target.exists(), "fresh case path " + name)
        target.mkdir()
        for n, b in initial.items():
            q=target/n; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(b)
        return target
    def child(name, directory, optimized, error=None):
        cmd = [sys.executable, "-B"] + (["-O"] if optimized else [])
        cmd += [str(directory/"verify.py"), "--output", str(output/(name+".json"))]
        start=time.monotonic()
        try:
            p=subprocess.run(cmd,env=env,capture_output=True,timeout=45)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("OPERATIONAL_TIMEOUT: no mathematical conclusion") from exc
        (output/(name+".stdout")).write_bytes(p.stdout)
        (output/(name+".stderr")).write_bytes(p.stderr)
        if error is None:
            need(p.returncode==0, "positive publication gate "+name+"\n"+p.stderr.decode())
            data=(output/(name+".json")).read_bytes()
            need(data==(D/"EXPECTED.json").read_bytes(), "ENTIRE byte fixture "+name)
        else:
            need(p.returncode!=0 and error.encode() in p.stderr, "specific gate missing "+name)
            need(b"UNTRUSTED_IMPORT_REACHED" not in p.stderr, "preimport boundary escaped")
        records.append({"case":name,"optimized":optimized,"exit":p.returncode,
                        "seconds":time.monotonic()-start,
                        "peak_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                        "passed":True,"expected_rejection":error})
        print(name,"PASS",flush=True)
    # Packaging interface is new. Both mathematics and the fixture are
    # unchanged from the separately documented four-replay private run.
    child("local-normal",D,False)
    child("cold-optimized",fresh("cold-source"),True)
    spec=importlib.util.spec_from_file_location("publication_gate",D/"verify.py")
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    baseline=(output/"local-normal.json").read_bytes()
    expected=(D/"EXPECTED.json").read_bytes()
    mutations=[
        ("scalar",lambda x:x["global_sixth_scalar"][0][1].__setitem__(0,"0")),
        ("ninth-original",lambda x:x["sixth"]["whole_all9_originals"].pop()),
        ("eighth-moment",lambda x:x["sixth"]["whole_all8_moments"].pop()),
        ("mean-derivative",lambda x:x["fifth"]["Kprime_at_mu_star"][0][1].__setitem__(1,"0")),
        ("identity-census",lambda x:x["identities"].pop()),
        ("stationary-jet",lambda x:x["small_minimizer_second_jet"][0][1].__setitem__(2,"0")),
    ]
    for name, mutate in mutations:
        row=json.loads(baseline);mutate(row)
        raw=(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n").encode()
        try:gate.check_record(raw,expected)
        except ValueError as error:
            need(str(error).startswith("RECORD:"), "specific whole-record gate")
            records.append({"case":"record-"+name,"passed":True,"expected_rejection":str(error)})
        else:raise ValueError("whole record corruption accepted "+name)
    for key,value in gate.SCOPE.items():
        scope=copy.deepcopy(gate.SCOPE)
        scope[key]=(not value if type(value) is bool else value-1 if type(value) is int else value+" [mutated]")
        try:gate.check_scope(scope)
        except ValueError as error:
            need(str(error).startswith("SCOPE:"),"specific scope gate")
            records.append({"case":"scope-"+key,"passed":True,"expected_rejection":str(error)})
        else:raise ValueError("scope corruption accepted "+key)
    for name in ("missing-kernel","changed-kernel","malformed-seal","changed-fixture"):
        target=fresh("preimport-"+name)
        if name=="missing-kernel":(target/"kernel/series.py").unlink()
        if name=="changed-kernel":
            with (target/"kernel/series.py").open("a") as f:f.write('\nraise RuntimeError("UNTRUSTED_IMPORT_REACHED")\n')
        if name=="malformed-seal":(target/"SOURCE.json").write_text("{")
        if name=="changed-fixture":
            row=json.loads((target/"EXPECTED.json").read_text())
            row["global_sixth_scalar"][0][1][0]="0"
            (target/"EXPECTED.json").write_text(json.dumps(row)+"\n")
        child("preimport-"+name,target,True,"SOURCE_SEAL:")
    need(all((D/n).read_bytes()==b for n,b in initial.items()),"source changed during publication gates")
    result={"agent":"six-sendov-3","role":"researcher","all_cases_passed":True,
            "ordinary_analytic_bridges_outside_kernel":True,"independent_review":False,
            "serial_children":True,"native_threads":{n:"1" for n in NAMES},
            "guard_seconds":45,"resource_limit_hit":False,"publication_full_replays":2,
            "complete_record_rejections":len(mutations),"scope_rejections":len(gate.SCOPE),
            "preimport_source_rejections":4,"cases":records,
            "whole_record_bytes":len(baseline),"whole_record_sha256":sha256(baseline).hexdigest(),
            "maximum_child_seconds":max(r.get("seconds",0) for r in records),
            "peak_child_kib":max(r.get("peak_kib",0) for r in records)}
    (output/"VALIDATION-publication.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("ALL publication gates PASS",len(records),flush=True)

if __name__=="__main__":
    main()
