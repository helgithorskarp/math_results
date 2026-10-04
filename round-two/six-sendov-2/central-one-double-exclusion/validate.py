"""Four complete serial replays and six mathematical damage controls.

Each child has a fixed 45-second guard and native threads one. No resource
limit is altered. Source copies, outputs and full records stay in --scratch.
An interrupted/failed child makes the suite incomplete, not nonexistence.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time


def need(ok, label):
    if not ok: raise ValueError(label)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--sympy-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    args.scratch = args.scratch.resolve()
    args.scratch.mkdir(parents=True, exist_ok=True)
    need(not args.scratch.resolve().is_relative_to(source), "scratch must be outside source")
    files = ["verify.py", "compare_cas.py", "record_io.py", "EXPECTED.json"]
    before = {name: sha256((source/name).read_bytes()).hexdigest() for name in files}
    environment = os.environ.copy()
    for name in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"]:
        environment[name] = "1"
    expected = json.loads((source/"EXPECTED.json").read_text())
    completed = []
    with tempfile.TemporaryDirectory(prefix="central-proof-", dir=args.scratch) as temp:
        tmp = Path(temp)
        cold = tmp/"cold"
        cold.mkdir()
        for name in files: shutil.copyfile(source/name, cold/name)

        def run(label, script, optimized=False, reject=None, whole=None):
            command = [sys.executable, "-I", "-B"]
            if optimized: command.append("-O")
            if script.name == "compare_cas.py" and args.sympy_root:
                command += ["-c", "import runpy,sys;root=sys.argv.pop(1);sys.path.insert(0,root);"
                            "script=sys.argv.pop(1);sys.argv[0]=script;"
                            "runpy.run_path(script,run_name='__main__')",
                            str(args.sympy_root.resolve()), str(script)]
            else: command.append(str(script))
            command += ["--expected", str(script.parent/"EXPECTED.json")]
            if whole: command += ["--whole", str(whole)]
            start = time.monotonic()
            p = subprocess.run(command, capture_output=True, text=True,
                               env=environment, timeout=45, cwd=tmp)
            seconds = time.monotonic()-start
            if reject:
                need(p.returncode != 0 and reject in p.stderr, "intended mathematical rejection: "+label)
            else:
                need(p.returncode == 0, label+" failed: "+p.stderr)
                need(json.loads(p.stdout) == expected, "entire compact record: "+label)
            completed.append({"label": label, "optimized": optimized,
                              "intended_rejection": reject, "returncode": p.returncode,
                              "seconds": seconds})
            print(json.dumps(completed[-1]), flush=True)

        generated = []
        for label, script, optimized in [
            ("native-local-normal", source/"verify.py", False),
            ("native-cold-optimized", cold/"verify.py", True),
            ("cas-local-normal", source/"compare_cas.py", False),
            ("cas-cold-optimized", cold/"compare_cas.py", True)]:
            whole = tmp/(label+".json")
            run(label, script, optimized, whole=whole)
            generated.append(whole.read_bytes())
        need(all(b == generated[0] for b in generated), "EVERY coefficient agrees across all engines/replays")
        need(sha256(generated[0]).hexdigest() == expected["whole_math_sha256"], "whole record commitment")

        # Damage source only in isolated disposable copies. These target actual
        # polynomial/mass/cap/basis/coverage obligations, not a summary label.
        changes = [
            ("original-single-root-factor", "Q = add(mul(power(add(z, a), 2), q), scale(u, 4))",
             "Q = add(mul(power(add(z, a), 2), q), scale(u, 2))", "entire original factorization"),
            ("original-second-moment", "const(F(-1, 2))", "const(F(-49, 100))",
             "entire original derivative factorization"),
            ("full-mass-factor-eight", "r = add(scale(mul(z, H), 8),",
             "r = add(scale(mul(z, H), 7),", "entire degree-five residue numerator"),
            ("root-gap-square", "scale(mul(w, g), -4)", "scale(mul(w, g), -3)",
             "entire root-gap square identity"),
            ("whole-reverse-tensor", "c = comb(n, k) * sum(", "c = (comb(n, k)+1) * sum(",
             "entire parent tensor reverse identity"),
            ("missing-positive-right-box",
             '            ("positive-right", mid, qhi, affine(box, 0, F(1, 2), F(1)), bisect_q(ctrl, deg)[1])',
             "", "three-box coverage")]
        original = (source/"verify.py").read_text()
        for label, old, new, rejection in changes:
            need(original.count(old) == 1, "unique semantic damage site: "+label)
            fault = tmp/label
            fault.mkdir()
            for name in ["record_io.py", "EXPECTED.json"]: shutil.copyfile(source/name, fault/name)
            damaged = fault/"verify.py"
            damaged.write_text(original.replace(old, new))
            run(label, damaged, reject=rejection)
    need(before == {name: sha256((source/name).read_bytes()).hexdigest() for name in files},
         "production mathematical source unchanged by suite")
    result = {"actual_agent": "six-sendov-2", "role": "researcher", "complete": True,
              "python": sys.version.split()[0], "sympy": "1.14.0", "native_threads": 1,
              "serial_cpu_children": 1, "fixed_child_guard_seconds": 45,
              "resource_limits_changed": False, "no_timeout_or_resource_hit": True,
              "full_positive_replays": 4, "mathematical_rejections": 6,
              "all_four_entire_records_identical": True,
              "whole_math_sha256": expected["whole_math_sha256"],
              "mathematical_source_sha256": before, "runs": completed,
              "peak_child_rss_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "not_independent_peer_review": True, "ordinary_bridges_unformalized": True}
    if args.output: args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    print(json.dumps({"complete": True, "full_positive_replays": 4, "mathematical_rejections": 6,
                      "max_child_seconds": max(x["seconds"] for x in completed),
                      "peak_child_rss_KiB": result["peak_child_rss_KiB"]}))


if __name__ == "__main__":
    main()
