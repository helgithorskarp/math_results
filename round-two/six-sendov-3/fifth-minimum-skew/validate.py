"""Serial author controls, fixed 45s per child; no solver or peer imports."""
from pathlib import Path
from hashlib import sha256
import copy, importlib.util, json, os, resource, shutil, subprocess, sys, time

D = Path(__file__).resolve().parent
NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
         "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    output = Path(sys.argv[1]).resolve()
    require(output != D and D not in output.parents, "use an external output directory")
    output.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, **{n: "1" for n in NAMES}}
    env.pop("PYTHONOPTIMIZE", None)
    records = []
    manifest = json.loads((D / "SOURCE.json").read_text())
    initial = {p.relative_to(D).as_posix(): p.read_bytes()
               for p in D.rglob("*") if p.is_file()
               and "__pycache__" not in p.parts and p.name != "record.json"}

    def fresh(name):
        target = output / name
        require(not target.exists(), "fresh resumable case required: " + name)
        target.mkdir()
        for path, b in initial.items():
            q = target / path
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_bytes(b)
        return target

    def child(name, directory, optimized, expected_error=None):
        command = [sys.executable, "-B"] + (["-O"] if optimized else [])
        command += [str(directory / "verify.py"), "--output", str(output / (name + ".json"))]
        start = time.monotonic()
        try:
            p = subprocess.run(command, env=env, capture_output=True, timeout=45)
        except subprocess.TimeoutExpired:
            raise RuntimeError("operational timeout; no mathematical conclusion: " + name)
        (output / (name + ".stdout")).write_bytes(p.stdout)
        (output / (name + ".stderr")).write_bytes(p.stderr)
        if expected_error is None:
            require(p.returncode == 0, "positive child failed: " + name + "\n" + p.stderr.decode())
            b = (output / (name + ".json")).read_bytes()
            require(b == (D / "EXPECTED.json").read_bytes(), "whole replay bytes: " + name)
        else:
            require(p.returncode != 0 and expected_error.encode() in p.stderr,
                    "specific rejection missing: " + name + "\n" + p.stderr.decode())
            require(b"UNTRUSTED_IMPORT_REACHED" not in p.stderr, "pre-import boundary escaped")
        row = {"case": name, "optimized": optimized, "exit": p.returncode,
               "seconds": time.monotonic() - start,
               "peak_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "expected_rejection": expected_error, "passed": True}
        if expected_error is None:
            row.update({"whole_bytes": len(b), "sha256": sha256(b).hexdigest()})
        records.append(row)
        print(json.dumps(row), flush=True)

    for name, optimized, cold in (
        ("local", False, False), ("local-O", True, False),
        ("cold", False, True), ("cold-O", True, True)):
        child(name, fresh(name) if cold else D, optimized)

    # Math probes deliberately rebind only the changed producer source pin.
    # Thus they pass the source gate and must fail an algebraic invariant;
    # these are NOT merely hash-refusal controls.
    defects = [
        ("wrong-anchor", "base_p = s.actual_polynomial(*base, order, 2)",
         'base_p = s.actual_polynomial(*base, order, 2, "wrong_anchor")',
         "BASELINE all4 active half-normals below10"),
        ("omitted-beta", "s.pa(K, {(8, 0): (s.N0, beta)})",
         "s.pa(K, {(8, 0): (s.N0, s.N0)})", "ALL4 repaired half-normals through10"),
        ("outward-tau", "s.gf(tau)", "s.gf(s.ns(tau, -1))",
         "ALL4 repaired half-normals through10"),
        ("wrong-J0", "F(-8304485822364161, 181398528)",
         "F(-8304485822364160, 181398528)", "ENTIRE fresh zero-skew fifth scalar"),
        ("wrong-first-jet", "s.ns(j.m.MUstar, F(-1, 3))",
         "s.ns(j.m.MUstar, F(1, 3))", "WHOLE selected small real first jet"),
        ("missing-h-axis", "field_scale(sqh, ar.nm(aT, ar.ni(b2)))",
         "field_scale(squares(hs[:-1]), ar.nm(aT, ar.ni(b2)))",
         "WHOLE12 sharp rank-one quadratic identity"),
        ("missing-real-cross", "ar.ps(ar.pm(sumu, sumu), F(1, 4))",
         "ar.ps(ar.pm(sumu, sumu), F(0))", "WHOLE12 sharp rank-one quadratic identity"),
        ("doubled-gamma", "gamma = ar.nm(s.fkappa, ar.ni(H))",
         "gamma = ar.ns(ar.nm(s.fkappa, ar.ni(H)), 2)",
         "WHOLE12 sharp rank-one quadratic identity"),
        ("wrong-cubic-sign", "ar.pm(sumh, sumh), sumh), F(1, 2))",
         "ar.pm(sumh, sumh), sumh), F(-1, 2))",
         "WHOLE12 exact cubic pair elimination"),
        ("missing-eighth-moment", "for power in powers[1:]",
         "for power in powers[1:-1]", "RECORD: all eight Newton slots"),
    ]
    for i, (name, before, after, error) in enumerate(defects):
        target = fresh("math-" + name)
        f = target / "derive.py"
        text = f.read_text()
        require(before in text, "specific producer mutation absent: " + name)
        f.write_text(text.replace(before, after, 1))
        m = copy.deepcopy(manifest)
        b = f.read_bytes()
        m["preimport_mathematical_source_pins"]["derive.py"] = {
            "bytes": len(b), "sha256": sha256(b).hexdigest()}
        (target / "SOURCE.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")
        child("math-" + name, target, bool(i % 2), error)

    target = fresh("math-dropped-critical-mass")
    f = target / "kernel/series.py"
    text = f.read_text()
    require("pp(la,6,order)" in text, "actual sixfold critical mass mutation")
    f.write_text(text.replace("pp(la,6,order)", "pp(la,5,order)", 1))
    m = copy.deepcopy(manifest)
    b = f.read_bytes()
    m["preimport_mathematical_source_pins"]["kernel/series.py"] = {
        "bytes": len(b), "sha256": sha256(b).hexdigest()}
    (target / "SOURCE.json").write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")
    child("math-dropped-critical-mass", target, True, "ALL9 full original equation")

    # No further mathematical import is needed for record/scope mutations.
    spec = importlib.util.spec_from_file_location("finite_gate", D / "verify.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    expected = (D / "EXPECTED.json").read_bytes()
    good = json.loads(expected)
    fixtures = [
        ("missing-ninth-root", lambda r: r["whole_all9_originals"].pop()),
        ("missing-eighth-moment", lambda r: r["whole_all8_moments"].pop()),
        ("short-half-normal", lambda r: r["whole_all9_originals"][3]["all_half_normals"].pop()),
        ("false-review", lambda r: r.update(independent_review=True)),
        ("formalized-bridge", lambda r: r.update(ordinary_analytic_bridges_outside_exact_kernel=False)),
        ("missing-real-map", lambda r: r["whole_residual"].pop()),
        ("false-differential", lambda r: r.update(all12_cubic_differential_coordinates_equal=False)),
        ("nonzero-residual", lambda r: r["whole_identities"][0].update(nonzero_residual_coefficients=1)),
        ("wrong-fifth", lambda r: r.update(J0=[])),
        ("omitted-sign", lambda r: r["strict_signs"].pop()),
    ]
    for name, mutate in fixtures:
        row = copy.deepcopy(good)
        mutate(row)
        data = json.dumps(row, sort_keys=True, separators=(",", ":")).encode() + b"\n"
        try:
            gate.check_record(data, expected)
        except ValueError as e:
            require(str(e).startswith("RECORD:"), "wrong fixture rejection")
            records.append({"case": "fixture-" + name, "expected_rejection": str(e), "passed": True})
        else:
            raise ValueError("record defect accepted: " + name)
    for key in gate.SCOPE:
        scope = copy.deepcopy(gate.SCOPE)
        v = scope[key]
        scope[key] = not v if type(v) is bool else v + 1 if type(v) is int else "weakened/overclaimed"
        try:
            gate.check_scope(scope)
        except ValueError as e:
            require(str(e).startswith("SCOPE:"), "wrong scope rejection")
            records.append({"case": "scope-" + key, "expected_rejection": str(e), "passed": True})
        else:
            raise ValueError("scope defect accepted: " + key)
    for name, mode in (("missing-kernel", False), ("mutated-kernel", True),
                       ("malformed-seal", False), ("mutated-fixture", True)):
        target = fresh("source-" + name)
        if name == "missing-kernel":
            (target / "kernel/calculation.py").unlink()
        elif name == "mutated-kernel":
            (target / "kernel/calculation.py").write_text('raise RuntimeError("UNTRUSTED_IMPORT_REACHED")\n')
        elif name == "malformed-seal":
            (target / "SOURCE.json").write_text("{not json\n")
        else:
            (target / "EXPECTED.json").write_bytes(expected + b" ")
        child("source-" + name, target, mode, "SOURCE_SEAL:")

    for path, b in initial.items():
        require((D / path).read_bytes() == b, "author source changed during controls: " + path)
    summary = {
        "agent": "six-sendov-3", "role": "researcher", "independent_review": False,
        "full_byte_replays": 4, "mathematical_producer_rejections": len(defects) + 1,
        "complete_record_mutation_rejections": len(fixtures),
        "scope_declaration_rejections": len(gate.SCOPE), "preimport_source_rejections": 4,
        "all_cases_passed": True, "cases": records,
        "expected_record": manifest["expected_record"],
        "maximum_child_seconds": max(r["seconds"] for r in records if "seconds" in r),
        "peak_child_kib": max(r["peak_kib"] for r in records if "peak_kib" in r),
        "mathematical_children_serial": True, "native_threads": {n: "1" for n in NAMES},
        "timeout_seconds_per_child": 45, "resource_limit_hit": False,
        "scope_checks_and_source_digests_are_not_proofs": True,
        "ordinary_analytic_bridges_outside_exact_kernel": True,
    }
    (output / "VALIDATION.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("cases", "native_threads")}),
          flush=True)

if __name__ == "__main__":
    main()
