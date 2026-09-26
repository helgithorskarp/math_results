"""Public replay controls: real traces, malformed evidence, SAT and UNKNOWN."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

from audit import audit
from evidence import atomic_json, audit_record, case_files, cnf_bytes, load_domain
from point_model import generate

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    domain = load_domain(args.domain)
    indices = [0, 251, 252, 9807, 9808, 20807, 20808, 27418,
               27419, 54837, 54838, 82256, 82257, 109675]
    base = [sys.executable, str(HERE / "replay.py"), "--domain", str(args.domain.resolve()),
            "--drat-trim", str(args.drat_trim.resolve())]
    proofs = out / "valid"
    for index in indices:
        subprocess.run(base + ["--out", str(proofs), "--start", str(index),
                               "--stop", str(index + 1)], check=True, stdout=subprocess.PIPE)
    # Reuse actually checks saved bytes and remains explicit about partial scope.
    subprocess.run(base + ["--out", str(proofs), "--start", "0", "--stop", "1"],
                   check=True, stdout=subprocess.PIPE)
    partial = json.loads((proofs / "replay_0_1.json").read_text())
    if partial["complete_family"] or partial["reused_records"] != 1:
        raise ValueError("partial or resumed replay is mislabeled")
    audited = audit(domain, proofs, 0, 1)
    if audited["complete_family"] or audited["verified_records"] != 1:
        raise ValueError("partial audit is mislabeled")
    try:
        audit(domain, proofs, 0, 2)
    except FileNotFoundError:
        pass
    else:
        raise ValueError("missing case accepted by corpus audit")

    unknown = subprocess.run(base + ["--out", str(out / "budget1"), "--start", "0",
                                    "--stop", "1", "--conflicts", "1"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if unknown.returncode == 0 or not (out / "budget1/UNKNOWN_0.json").exists():
        raise ValueError("budget-one UNKNOWN was not explicitly rejected")
    cnf, proof, log, record_path = case_files(proofs, 0)
    original_record = json.loads(record_path.read_text())
    for field, bad in [("cnf_sha256", "0" * 64), ("status", "UNKNOWN"), ("gauge", [0, 1, 2])]:
        broken = deepcopy(original_record)
        broken[field] = bad
        atomic_json(record_path, broken)
        try:
            audit_record(proofs, 0, domain[0])
        except ValueError:
            pass
        else:
            raise ValueError(f"damaged field {field} was accepted")
        finally:
            atomic_json(record_path, original_record)

    empty, false_empty = out / "empty.drat", out / "false-empty.drat"
    empty.write_bytes(b"")
    false_empty.write_bytes(b"0\n")
    points = json.loads((HERE.parent / "known70.json").read_text())["points"]
    word = "".join(str(sum(p // 5 == i for p in points)) for i in range(25))
    formula, _ = generate(word)
    sat = out / "known70.cnf"
    sat.write_bytes(cnf_bytes(formula))
    for number, (instance, trace) in enumerate([(cnf, empty), (cnf, false_empty), (sat, proof)]):
        result = subprocess.run([str(args.drat_trim.resolve()), str(instance), str(trace)],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (out / f"rejected_{number}.log").write_text(result.stdout)
        if result.returncode == 0 and "s VERIFIED" in result.stdout:
            raise ValueError("invalid proof accepted by checker")
    result = {"status": "REPLAY_PIPELINE_CONTROLS_PASSED", "fresh_checked_indices": indices,
              "damaged_records_rejected": 3, "invalid_proofs_rejected": 3,
              "unknown_rejected": True, "missing_case_rejected": True,
              "partial_scope_checked": True, "resume_checked": True}
    atomic_json(out / "validation.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
