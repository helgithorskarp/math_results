"""Portable seven-phase source-only replay; generated evidence stays in work/."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import os
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()


def compact(records, rows, stream):
    uniform = records["uniform"]
    return dict(
        agent="six-downset-1", role="researcher",
        scope="Complete exact balanced old-edge h>=2 sign/identity verification and original h2/h3 controls; ordinary geometric/completeness/rank proof in PROOF.md is unformalized and independent review is pending",
        phases=7,
        complete_mathematical_bytes=len(stream),
        whole_mathematical_stream_sha256=sha256(stream).hexdigest(),
        phase_records=rows,
        uniform=dict(
            domain=uniform["domain"],
            fixed_sector_dimensions=uniform["fixed_sector_dimensions"],
            signs=[{k: r[k] for k in ("group", "order", "positive", "degree", "original_terms", "shifted_terms")} for r in uniform["rows"]],
            guards=uniform["guards"],
        ),
        independent=records["independent"]["result"],
        original_controls=[records["original-h" + str(h)] for h in (2, 3)],
        complete_sector_controls=[records["sectors-h" + str(h)] for h in (2, 3)],
        damages=records["damages"]["cases"],
    )


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check")
    parser.add_argument("--output")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    work = root / "work"
    work.mkdir(exist_ok=True)
    mode = sys.flags.optimize
    require(mode in (0, 1), "Use normal Python or optimization level one")
    env = dict(os.environ)
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    phases = [
        ("uniform", "uniform.py", [], "uniform-O{mode}.json"),
        ("independent", "check_uniform.py", ["work/uniform-O{mode}.json"], "checked-O{mode}.json"),
    ]
    phases += [("original-h" + str(h), "model.py", ["--h", str(h)], "original-h" + str(h) + "-O{mode}.json") for h in (2, 3)]
    phases += [("sectors-h" + str(h), "sector_control.py", ["--h", str(h)], "sectors-h" + str(h) + "-O{mode}.json") for h in (2, 3)]
    phases += [("damages", "damages.py", ["work/uniform-O{mode}.json"], "damages-O{mode}.json")]
    records, rows, runtime = {}, [], []
    stream = bytearray()
    start = time.monotonic()
    for phase, script, arguments, file in phases:
        command = [sys.executable, "-I", "-B"] + (["-O"] if mode else []) + [script] + [a.format(mode=mode) for a in arguments]
        then = time.monotonic()
        child = subprocess.run(command, cwd=root, env=env, capture_output=True, timeout=60)
        (work / (phase + f"-O{mode}.stdout")).write_bytes(child.stdout)
        (work / (phase + f"-O{mode}.stderr")).write_bytes(child.stderr)
        require(child.returncode == 0, "Complete phase " + phase + " failed: " + child.stderr.decode()[-1600:])
        data = json.loads((work / file.format(mode=mode)).read_text())
        require(data["optimized"] == mode, "Actual child optimization flag")
        mathematical = {k: v for k, v in data.items() if k not in ("seconds", "peak_KiB", "optimized")}
        if phase == "uniform":
            require(len(mathematical["rows"]) == 17 and all(row["positive"] for row in mathematical["rows"]), "All seventeen original sign obligations")
        if "certificate_sha256" in mathematical:
            raw = (work / f"uniform-O{mode}.json").read_bytes()
            require(sha256(raw).hexdigest() == mathematical["certificate_sha256"], "Entire actual raw certificate input binding")
            mathematical["certificate_sha256"] = sha256(canonical(records["uniform"])).hexdigest()
        records[phase] = mathematical
        encoded = canonical(dict(phase=phase, record=mathematical))
        stream += encoded + b"\n"
        rows.append(dict(phase=phase, mathematical_bytes=len(encoded), mathematical_sha256=sha256(encoded).hexdigest()))
        runtime.append(dict(phase=phase, seconds=time.monotonic() - then, peak_KiB=data["peak_KiB"]))
        print(json.dumps(dict(phase=phase, complete=True, optimized=mode)), flush=True)
    result = compact(records, rows, bytes(stream))
    if args.check:
        expected = json.loads(Path(args.check).read_text())
        require(result == expected, "Entire compact record and full seven-phase mathematical stream")
    output = Path(args.output) if args.output else work / f"replay-O{mode}.json"
    output.write_bytes(canonical(result) + b"\n")
    (work / f"whole-mathematical-O{mode}.jsonl").write_bytes(stream)
    measured = dict(agent="six-downset-1", role="researcher", optimized=mode,
                    complete=True, source_only=True, phases=runtime,
                    seconds=time.monotonic() - start,
                    whole_mathematical_stream_sha256=result["whole_mathematical_stream_sha256"],
                    compact_result_sha256=sha256(canonical(result) + b"\n").hexdigest())
    (work / f"execution-O{mode}.json").write_text(json.dumps(measured, indent=2) + "\n")
    print(json.dumps({k: v for k, v in measured.items() if k != "phases"}))


if __name__ == "__main__":
    run()
