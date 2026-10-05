"""Stdlib source/scope gates and guarded whole-record verification.

The exact producer checks finite identities. Scope declarations and hashes
do not prove the analytic globality, stationary or sharpness bridges.
"""
from pathlib import Path
from hashlib import sha256
import argparse, json, os, subprocess, sys

D = Path(__file__).resolve().parent
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
SCOPE = {
    "degree": 9, "original_roots": 9, "critical_slots": 8,
    "complex_coefficients": True,
    "all_critical_multiplicities_and_collisions": True,
    "original_root_domain": "closed unit disk",
    "marked_root": "actual a=1-eta>0",
    "reciprocal_zero_denominator": "infinity",
    "objective": "FIRST power, sum of eight positive reciprocal distances",
    "normal_convention": "(abs(Z)^2-1)/2, four independent physical half-normals",
    "minimum_domain": "all actual complex degree-nine disk-root polynomials",
    "collar": "existential, common on each fixed finite parameter interval",
    "fifth_excess_coverage": "every fixed finite D>=0, all Delta in [0,D]",
    "sixth_band_coverage": "every compact interval strictly above J6",
    "exact_fifth_endpoint_J0_claimed": True,
    "exact_sixth_endpoint_J6_claimed": False,
    "all12_free_directions_and_all4_actual_slacks": True,
    "global_interior_FIRST_claimed": False,
    "effective_radius_claimed": False,
    "exact_finite_radius_maximizer_claimed": False,
    "ordinary_analytic_bridges_outside_exact_kernel": True,
    "independent_review_of_new_child": False,
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def check_scope(scope):
    need(type(scope) is dict and scope == SCOPE, "SCOPE: exact quantified declaration")
    for key, value in SCOPE.items():
        need(type(scope[key]) is type(value), "SCOPE: exact scalar type " + key)

def source_gate():
    try:
        manifest = json.loads((D / "SOURCE.json").read_text())
        pins = manifest["preimport_mathematical_source_pins"]
        names = {"derive.py", "kernel-pins.json"} | {
            "kernel/" + n for n in
            ("arithmetic.py", "series.py", "constants.py", "family.py", "calculation.py")}
        need(set(pins) == names, "SOURCE_SEAL: exact mathematical source census")
        for name, pin in pins.items():
            b = (D / name).read_bytes()
            need(len(b) == pin["bytes"] and sha256(b).hexdigest() == pin["sha256"],
                 "SOURCE_SEAL: whole mathematical source " + name)
        b = (D / "EXPECTED.json").read_bytes()
        need(len(b) == manifest["expected_record"]["bytes"] and
             sha256(b).hexdigest() == manifest["expected_record"]["sha256"],
             "SOURCE_SEAL: whole expected fixture")
    except (OSError, KeyError, json.JSONDecodeError) as error:
        raise ValueError("SOURCE_SEAL: absent or malformed pinned input") from error
    return manifest

def check_record(data, expected):
    row = json.loads(data)
    need(row["agent"] == "six-sendov-3" and row["role"] == "researcher",
         "RECORD: actual producer attribution")
    need(row["phase"] == "global" and row["independent_review"] is False and
         row["generated_mathematical_inputs_read"] is False and
         row["ordinary_globality_and_stationary_bridges_outside_kernel"] is True,
         "RECORD: finite trust boundary")
    for phase, order in (("fifth", 10), ("sixth", 12)):
        r = row[phase]
        roots = r["whole_all9_originals"]
        need([x["label"] for x in roots] == list(range(9)),
             "RECORD: all nine original slots/" + phase)
        need(all(len(x["all_root_coefficients"]) == order+1 and
                 len(x["all_half_normals"]) == order+1 for x in roots),
             "RECORD: complete root and actual half-normal jets/" + phase)
        need(len(r["whole_all8_moments"]) == 8 and
             all(len(x) == order+1 for x in r["whole_all8_moments"]),
             "RECORD: all eight complete moments/" + phase)
        need(len(r["whole_primitive"]) == order+1 and
             all(len(x) == 10 for x in r["whole_primitive"]) and
             len(r["whole_first"]) == order+1,
             "RECORD: complete primitive and positive FIRST/" + phase)
    need(len(row["identities"]) == 707 and all(
        x["whole_maps_compared_before_hash"] is True and
        x["nonzero_residual_coefficients"] == 0 for x in row["identities"]),
        "RECORD: complete checked identity census")
    need(len(row["strict_signs"]) == 12, "RECORD: complete rational sign census")
    need(row["strict_global_J6_integer_bracket"] == [-65097, -65096],
         "RECORD: strict whole sixth scalar bracket")
    need(row == json.loads(expected), "RECORD: ENTIRE fresh mathematical maps")
    need(data == expected, "RECORD: ENTIRE canonical mathematical bytes")
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    for name in THREADS:
        os.environ[name] = "1"
    source_gate()                      # No mathematical module imported.
    check_scope(json.loads((D / "THEOREM.json").read_text()))
    command = [sys.executable, "-B"]
    if sys.flags.optimize:
        command.append("-O")
    command += [str(D / "derive.py"), "global"]
    try:
        p = subprocess.run(command, capture_output=True, timeout=45)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("OPERATIONAL_TIMEOUT: no mathematical conclusion") from error
    if p.returncode:
        raise RuntimeError("PRODUCER_REJECTION: " + p.stderr.decode())
    row = check_record(p.stdout, (D / "EXPECTED.json").read_bytes())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(p.stdout)
    print(json.dumps({"verified": True, "bytes": len(p.stdout),
                      "sha256": sha256(p.stdout).hexdigest(),
                      "whole_identities": len(row["identities"]),
                      "strict_signs": len(row["strict_signs"]),
                      "preimport_source_seal": True,
                      "scope_consistency_is_not_a_proof": True,
                      "ordinary_analytic_bridges_outside_kernel": True,
                      "independent_review": False}))

if __name__ == "__main__":
    main()
